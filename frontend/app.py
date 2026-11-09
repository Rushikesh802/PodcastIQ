import streamlit as st
import requests

URL = 'http://127.0.0.1:8000'

st.set_page_config(
    page_title='PodcastIQ',
    page_icon='🤖',
    layout='centered'
)

try:
    response = requests.get(URL, timeout=5)
    response.raise_for_status()

except requests.ConnectionError:
    st.error("API not connected. Please check the backend service.")

except requests.Timeout:
    st.error("Backend request timed out. Please try again.")

except requests.HTTPError as exc:
    st.error(f"Backend returned an error: {exc}")

if 'video_id' not in st.session_state:
    st.session_state.video_id = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title('Welcome to PoadcastIQ')


yt_url = st.text_input('Enter Your Youtube link to parse')


## data ingestion
if st.button('Submit'):

    try:
        
        with st.spinner(text='Processing your video. Please wait...'):

            response = requests.post(url=f'{URL}/data_ingestion/', 
                                            params={'url': yt_url},
                                            timeout=(5, 600))
            response.raise_for_status()
            data = response.json()
            st.session_state.video_id = data['video_id']
            st.session_state.chat_history = []

        st.success('video processed successfully!')

    except requests.Timeout:
        st.error(
            'Data ingestion exceeded the 10-minute request limit. '
            'The backend may still be processing; check its logs before retrying.'
        )
    except requests.HTTPError as error:
        try:
            detail = error.response.json().get('detail', error.response.text)
        except ValueError:
            detail = error.response.text
        st.error(f'Data ingestion failed ({error.response.status_code}): {detail}')
    except requests.RequestException as error:
        st.error(f'Data ingestion failed: {error}')



## chat interface
if st.session_state.video_id:

    st.divider()
    st.subheader('💬 Ask Questions')

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

    query = st.chat_input('Start Now Asking Questions')

    if query:

        st.session_state.chat_history.append(('user', query))

        with st.chat_message('user'):
            st.write(query)

        try:
            with st.spinner('Please wait while genrating response'):
                response = requests.post(url=f'{URL}/chat',
                                        params={'video_id': st.session_state.video_id,
                                                'query': query},
                                        timeout=180)

                response.raise_for_status()

                data = response.json()

                ans = data

            st.session_state.chat_history.append(('assistant', ans))


            with st.chat_message(name='assistant'):
                st.write(ans)
        except requests.HTTPError as error:
            try:
                detail = error.response.json().get('detail', error.response.text)
            except ValueError:
                detail = error.response.text
            st.error(f'Chat request failed ({error.response.status_code}): {detail}')
        except requests.RequestException as error:
            st.error(f'Could not reach the chat service: {error}')

        if st.button('New video'):

            try:
                response = requests.delete(url=f'{URL}', params={'video_id': st.session_state.video_id})
                response.raise_for_status()

            except requests.RequestException as exc:
                st.error(f'Please refresh the page!: {exc}')
                st.stop()

            st.session_state.video = None
            st.rerun()
