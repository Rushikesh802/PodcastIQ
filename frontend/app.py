
import streamlit as st
import requests

URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="PodcastIQ",
    page_icon="🤖",
    layout="centered"
)


# ---------------- SESSION STATE ----------------

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


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


# ---------------- HEADER ----------------

st.title("🤖 PodcastIQ")
st.caption("Your AI-powered YouTube podcast assistant")

st.divider()


# ---------------- DATA INGESTION ----------------

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

                response = requests.post(
                    f"{URL}/data_ingestion/",
                    params={"url": yt_url},
                    timeout=(5, 600)
                )

                response.raise_for_status()

                data = response.json()

                st.session_state.video_id = data["video_id"]
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
            except ValueError:
                detail = exc.response.text

            st.error(f"Ingestion failed: {detail}")

        except requests.RequestException as exc:
            st.error(f"API error: {exc}")


# ---------------- CHAT INTERFACE ----------------

if st.session_state.video_id:

    st.divider()
    st.subheader("💬 Ask Your Podcast")

    for role, message in st.session_state.chat_history:

        with st.chat_message(role):
            st.write(message)

    query = st.chat_input("Ask anything about this video...")

    if query:

        st.session_state.chat_history.append(
            ("user", query)
        )

        with st.chat_message("user"):
            st.write(query)

        try:
            with st.chat_message("assistant"):

                with st.spinner("Generating response..."):

                    response = requests.post(
                        f"{URL}/chat",
                        params={
                            "video_id": st.session_state.video_id,
                            "query": query
                        },
                        timeout=180
                    )

                    response.raise_for_status()

                    data = response.json()

                    # Adjust according to your FastAPI response schema
                    ans = (
                        data.get("answer")
                        if isinstance(data, dict)
                        else data
                    )

                    st.write(ans)

            st.session_state.chat_history.append(
                ("assistant", ans)
            )

        except requests.RequestException as exc:
            st.error(f"Chat request failed: {exc}")


    # ---------------- NEW VIDEO ----------------

    if st.button("➕ Process Another Video"):

        try:
            response = requests.delete(
                f"{URL}/delete/",
                params={
                    "video_id": st.session_state.video_id
                },
                timeout=10
            )

            response.raise_for_status()

        except requests.RequestException as exc:
            st.error(f"Could not delete previous video: {exc}")
            st.stop()

        st.session_state.video_id = None
        st.session_state.chat_history = []

        st.rerun()
