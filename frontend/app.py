
import logging
import requests
import streamlit as st

URL = "http://127.0.0.1:8000"

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="PodcastIQ",
    page_icon="🤖",
    layout="centered"
)


# ---------------- SESSION STATE ----------------

DEFAULT_STATE = {
    "video_id": None,
    "chat_history": [],
    "video_url": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- API HEALTH CHECK ----------------

@st.cache_data(ttl=10)
def check_backend():

    try:
        response = requests.get(URL, timeout=5)
        response.raise_for_status()
        return True

    except requests.RequestException:
        return False


if not check_backend():
    st.error("🔴 Backend not connected. Start your FastAPI server.")
    st.stop()


# ---------------- API HELPERS ----------------

def response_generator(query: str, video_id: str):

    with requests.post(
        f"{URL}/chat",
        json={
            "query": query,
            "video_id": video_id
        },
        stream=True,
        timeout=(5, 180)
    ) as response:

        response.raise_for_status()

        for chunk in response.iter_content(
            chunk_size=None,
            decode_unicode=True
        ):

            if chunk:
                if isinstance(chunk, bytes):
                    chunk = chunk.decode("utf-8")

                yield chunk


def ingest_video(url: str):

    response = requests.post(
        f"{URL}/data_ingestion",
        json={"url": url},
        timeout=(5, 600)
    )

    response.raise_for_status()

    return response.json()


def delete_video(video_id: str):

    response = requests.delete(
        f"{URL}/delete/",
        params={"video_id": video_id},
        timeout=10
    )

    response.raise_for_status()


# ---------------- HEADER ----------------

st.title("🤖 PodcastIQ")

st.caption(
    "Your AI-powered YouTube podcast assistant"
)

st.divider()


# ---------------- VIDEO INGESTION ----------------

st.subheader("🎥 Process YouTube Video")

yt_url = st.text_input(
    "Enter YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

if st.button("Process Video", use_container_width=True):

    if not yt_url.strip():

        st.warning("Please enter a YouTube URL.")

    else:

        try:

            with st.spinner("Processing your video..."):

                data = ingest_video(yt_url.strip())

                st.session_state.video_id = data["video_id"]
                st.session_state.video_url = yt_url.strip()
                st.session_state.chat_history = []

            st.success("Video processed successfully!")

        except requests.Timeout:

            st.error("Processing timed out. Check backend logs.")

        except requests.HTTPError as exc:

            try:
                detail = exc.response.json().get(
                    "detail",
                    exc.response.text
                )
            except (ValueError, AttributeError):
                detail = str(exc)

            st.error(f"Ingestion failed: {detail}")

        except requests.RequestException as exc:

            st.error(f"API error: {exc}")

        except (KeyError, ValueError) as exc:

            st.error(f"Invalid ingestion response: {exc}")


# ---------------- VIDEO INFORMATION ----------------

if st.session_state.video_id:

    st.divider()

    st.subheader("🎬 Current Video")

    st.video(st.session_state.video_url)

    st.caption(
        f"Video ID: {st.session_state.video_id}"
    )


# ---------------- CHAT INTERFACE ----------------

if st.session_state.video_id:

    st.divider()

    st.subheader("💬 Ask Your Podcast")

    # Display chat history
    for role, message in st.session_state.chat_history:

        with st.chat_message(role):
            st.markdown(message)

    query = st.chat_input(
        "Ask anything about this video..."
    )

    if query:

        st.session_state.chat_history.append(
            ("user", query)
        )

        with st.chat_message("user"):
            st.markdown(query)

        try:

            with st.chat_message("assistant"):

                response_placeholder = st.empty()
                answer = ""

                for chunk in response_generator(
                    query=query,
                    video_id=st.session_state.video_id
                ):

                    answer += chunk
                    response_placeholder.markdown(answer + "▌")

                response_placeholder.markdown(answer)

            st.session_state.chat_history.append(
                ("assistant", answer)
            )

        except requests.RequestException as exc:

            st.error(f"Chat request failed: {exc}")


# ---------------- NEW VIDEO ----------------

if st.session_state.video_id:

    st.divider()

    if st.button(
        "➕ Process Another Video",
        use_container_width=True
    ):

        try:

            with st.spinner("Resetting previous video..."):

                delete_video(st.session_state.video_id)

            st.session_state.video_id = None
            st.session_state.video_url = None
            st.session_state.chat_history = []

            st.rerun()

        except requests.RequestException as exc:

            st.error(f"Could not delete previous video: {exc}")
