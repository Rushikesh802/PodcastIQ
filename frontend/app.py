import streamlit as st
import requests

URL = 'http://127.0.0.1:8000'


if 'video_id' not in st.session_state:
    st.session_state.video_id = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(
    page_title='PodcastIQ',
    page_icon='🤖',
    layout='centered'
)
st.title('Welcome to PoadcastIQ')


yt_url = st.text_input('Enter Your Youtube link to parse')


## data ingestion
if st.button('Submit'):

    try:
        
        with st.spinner(text='Processing your video. Please wait...'):

            response = requests.post(url=f'{URL}/data_ingestion/', 
                                            params={'url': yt_url},
                                            timeout=60)
            response.raise_for_status()
            data = response.json()
            st.session_state.video_id = data['video_id']
            st.session_state.chat_history = []

        st.success('video processed successfully!')

    except requests.RequestException:
        raise st.error('Data ingestion failed!!')



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
