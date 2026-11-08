import streamlit as st
import requests

URL = 'http://127.0.0.1:8000'


if 'video_id' not in st.session_state:
    st.session_state.video_id = None

st.title('Welcome to PoadcastIQ')


yt_url = st.text_input('Enter Your Youtube link to parse')

if st.button('Submit'):

    try:
        
        with st.spinner(text='Processing your video. Please wait...'):

            response = requests.post(url=f'{URL}/data_ingestion/', 
                                            params={'url': yt_url},
                                            timeout=60)
            response.raise_for_status()
            data = response.json()
            st.session_state.video_id = data['video_id']

        st.success('video processed successfully!')

    except requests.RequestException:
        raise st.error('Data ingestion failed!!')


if st.session_state.video_id:

    st.divider()

    st.write('Now You can ask the question base on video')
    query = st.text_input('Start Now Asking Questions')

    try:
        with st.spinner('Please wait while genrating response'):
            response = requests.post(url=f'{URL}/chat',
                                    params={'video_id': st.session_state.video_id,
                                            'query': query},
                                    timeout=180)
    except requests.RequestException:
        st.error('chat failed please try again or check your internet connection')
            