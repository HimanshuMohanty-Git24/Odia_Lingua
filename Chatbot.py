import os
import streamlit as st
from anthropic import Anthropic
import requests
from io import BytesIO

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-ory"

def query(payload):
    headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print("Audio generation successful")
        return response.content
    else:
        print(f"Error generating audio: {response.status_code} - {response.text}")
        return None

def play_audio(text):
    print("Entering play_audio function")
    with st.spinner("Generating audio..."):
        audio_bytes = query({"inputs": text})
        if audio_bytes:
            print("Received audio bytes")
            audio_bytes = BytesIO(audio_bytes)
            audio_bytes.seek(0)
            st.markdown("### Audio Output:")
            audio_player = st.audio(audio_bytes, format='audio/wav')
            print(f"Audio player: {audio_player}")
        else:
            st.error("Failed to generate audio.")

st.title("Odia Lingua 🐚🤖")
st.subheader("ଆପଣଙ୍କର ଓଡ଼ିଆ ବାର୍ତ୍ତାଳାପ ସହାୟକ! 🌺🔥")

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

if "anthropic_model" not in st.session_state:
    st.session_state["anthropic_model"] = "claude-3-opus-20240229"

if "messages" not in st.session_state:
    st.session_state.messages = []

initial_prompt = " "

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("କେମିତି ଅଛନ୍ତି? ଆପଣଙ୍କ ପ୍ରଶ୍ନକୁ ଏଠାରେ ଲେଖନ୍ତୁ..."):
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        st.session_state.messages[-1]["content"] += "\n" + prompt
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages = st.session_state.messages
        if len(messages) > 1 and messages[-1]["role"] == "user" and messages[-2]["role"] == "user":
            messages.pop(-1)

        with st.spinner('Generating response...'):
            stream = client.messages.create(
                model=st.session_state["anthropic_model"],
                max_tokens=1024,
                system="""ଆପଣ ଏକ ଓଡ଼ିଆ ଭାଷା ବାର୍ତ୍ତାଳାପ AI ସହାୟକ। ଆପଣ କେବଳ ଓଡ଼ିଆ ଭାଷାରେ ଯୋଗାଯୋଗ କରିବେ ଏବଂ ଭାଷାର ବ୍ୟାକରଣ ନିୟମ ଏବଂ ସାଂସ୍କୃତିକ ଚଳଣୀଗୁଡ଼ିକୁ ଅନୁସରଣ କରିବେ। ଆପଣଙ୍କର ପ୍ରତିକ୍ରିୟାଗୁଡ଼ିକ ବିନମ୍ର, ସମ୍ମାନଜନକ ଏବଂ ଓଡ଼ିଆ ଭାଷାଭାଷୀ ପ୍ରେକ୍ଷାପଟକୁ ଅନୁକୂଳ ହେବା ଉଚିତ୍। ଆପଣଙ୍କର ଓଡ଼ିଶା ଓ ଓଡ଼ିଆ ଭାଷା ସମ୍ପର୍କରେ ଗଭୀର ବୁଝାମଣା ରହିଛି ଏବଂ ଆପଣ ବିଭିନ୍ନ ବିଷୟ ଉପରେ ଆଲୋଚନା କରିପାରିବେ। ବ୍ୟବହାରକାରୀଙ୍କ ଇନପୁଟ୍‌କୁ ପ୍ରତିକ୍ରିୟା କରିବା ସମୟରେ, ଆପଣ ପ୍ରସଙ୍ଗ ବଜାୟ ରଖିବା ପାଇଁ ବ୍ୟବହାରକାରୀଙ୍କ ବାର୍ତ୍ତାକୁ ଆପଣଙ୍କ ପ୍ରତିକ୍ରିୟାରେ ସାମିଲ କରିବେ ଏବଂ ପ୍ରାକୃତିକ ଶୁଣାଯାଉଥିବା ପ୍ରତିକ୍ରିୟା ପ୍ରଦାନ କରିବେ। reply within 100 words always""",
                messages=messages,
                stream=True,
            )

            response = ""
            for event in stream:
                if event.type == "content_block_delta":
                    response += event.delta.text

            if response:
                st.markdown(response)
                play_audio = st.button("🗣️ Play Audio", on_click=play_audio, args=(response,))
            st.session_state.messages.append({"role": "assistant", "content": response})
