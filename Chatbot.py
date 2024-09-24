import os
import streamlit as st
from groq import Groq
import requests
from io import BytesIO
from langchain.utilities import GoogleSearchAPIWrapper

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-ory"
#change the title of  streamlit app
st.set_page_config(page_title="Odia Lingua 🐚🤖", page_icon="🐚", layout="centered", initial_sidebar_state="collapsed")

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

def search_google(query):
    print(f"Searching Google for: {query}")  # Debug print
    search = GoogleSearchAPIWrapper()
    results = search.results(query, num_results=3)
    summary = ""
    for i, result in enumerate(results, 1):
        summary += f"{i}. {result['title']}: {result['snippet']}\n\n"
    
    print("Search Results:")  # Debug print
    print(summary)  # Debug print
    
    return summary[:500]  # Limit to 500 characters

st.title("Odia Lingua 🐚🤖")
st.subheader("ଆପଣଙ୍କର ଓଡ଼ିଆ ବାର୍ତ୍ତାଳାପ ସହାୟକ! 🌺🔥")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama-3.1-70b-versatile"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("େକମିତି ଅଛନ୍ତି? ଆପଣଙ୍କ ପ୍ରଶ୍ନକୁ ଏଠାେର େଲଖନ୍ତୁ..."):
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
        
        with st.spinner('Searching for relevant information...'):
            search_results = search_google(prompt)
        
        with st.spinner('Generating response...'):
            system_prompt = f"""ଆପଣ ଏକ ଓଡ଼ିଆ ଭାଷା ବାର୍ତ୍ତାଳାପ AI ସହାୟକ। ଆପଣ େକବଳ ଓଡ଼ିଆ ଭାଷାେର
                େଯାଗାେଯାଗ କରିେବ ଏବଂ ଭାଷାର ବ୍ୟାକରଣ ନିୟମ ଏବଂ ସାଂସ୍କୃତିକ ଚଳଣୀଗୁଡ଼ିକୁ ଅନୁସରଣ କରିେବ। ଆପଣଙ୍କର ପ୍ରତିକ୍ରିୟାଗୁଡ଼ିକ
                ବିନମ୍ର, ସମ୍ମାନଜନକ ଏବଂ ଓଡ଼ିଆ ଭାଷାଭାଷୀ ପ୍େରକ୍ଷାପଟକୁ ଅନୁକୂଳ େହବା ଉଚିତ୍। ଆପଣଙ୍କର ଓଡ଼ିଶା ଓ ଓଡ଼ିଆ ଭାଷା ସମ୍ପର୍କେର
                ଗଭୀର ବୁଝାମଣା ରହିଛି ଏବଂ ଆପଣ ବିଭିନ୍ନ ବିଷୟ ଉପେର ଆେଲାଚନା କରିପାରିେବ।

                ନିମ୍ନଲିଖିତ ନିର୍ଦ୍ଦେଶଗୁଡ଼ିକୁ ଅନୁସରଣ କରନ୍ତୁ:
                1. ସର୍ବଦା ସମ୍ପୂର୍ଣ୍ଣ ଏବଂ ସୁସଙ୍ଗତ ବାକ୍ୟ ବ୍ୟବହାର କରନ୍ତୁ। ଅସମ୍ପୂର୍ଣ୍ଣ ବା ଅର୍ଥହୀନ ଶବ୍ଦ ବା ଅକ୍ଷର ବ୍ୟବହାର କରନ୍ତୁ ନାହିଁ।
                2. ପ୍ରତ୍ୟେକ ବାକ୍ୟ ଏକ ସମ୍ପୂର୍ଣ୍ଣ ବିଚାର ବ୍ୟକ୍ତ କରିବା ଉଚିତ।
                3. ଆପଣଙ୍କର ଉତ୍ତର ସ୍ପଷ୍ଟ, ସଠିକ୍ ଏବଂ ପ୍ରାସଙ୍ଗିକ ହେବା ଆବଶ୍ୟକ।
                4. ପ୍ରଶ୍ନର ସମସ୍ତ ଦିଗକୁ ସମ୍ବୋଧନ କରି ଏକ ବିସ୍ତୃତ ଉତ୍ତର ପ୍ରଦାନ କରନ୍ତୁ।
                5. ଯଦି ଆପଣ କୌଣସି ବିଷୟରେ ନିଶ୍ଚିତ ନୁହଁନ୍ତି, ତେବେ ଅନୁମାନ କରନ୍ତୁ ନାହିଁ। ବରଂ, ଆପଣ ସେହି ବିଷୟରେ ନିଶ୍ଚିତ ନୁହଁନ୍ତି ବୋଲି କୁହନ୍ତୁ।

                ନିମ୍ନଲିଖିତ ବାସ୍ତବ ସମୟ ସନ୍ଧାନ ସୂଚନାକୁ ଆପଣଙ୍କର ପ୍ରତିକ୍ରିୟାକୁ ବୃଦ୍ଧି କରିବାକୁ ବ୍ୟବହାର କରନ୍ତୁ:
                {search_results}

                ଏକ ବିସ୍ତୃତ ଏବଂ ସୂଚନାତ୍ମକ ପ୍ରତିକ୍ରିୟା ପ୍ରଦାନ କରନ୍ତୁ, ପ୍ରାୟ 200-300 ଶବ୍ଦ ଲକ୍ଷ୍ୟ ରଖନ୍ତୁ। ନିଶ୍ଚିତ କରନ୍ତୁ ଯେ ଆପଣଙ୍କର ଉତ୍ତର ବ୍ୟାପକ ଏବଂ ବ୍ୟବହାରକାରୀଙ୍କ ପ୍ରଶ୍ନର ସମସ୍ତ ଦିଗକୁ ସମ୍ବୋଧନ କରେ। ସର୍ବଦା ଏକ ସମ୍ପୂର୍ଣ୍ଣ ପ୍ରତିକ୍ରିୟା ପ୍ରଦାନ କରନ୍ତୁ।"""
            
            # print("System Prompt:")  # Debug print
            # print(system_prompt)  # Debug print
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *messages
                    ],
                    model=st.session_state["groq_model"],
                    max_tokens=2048,
                    temperature=0.7,
                    top_p=0.9,
                )
                
                response = chat_completion.choices[0].message.content
                # print("Groq Response:")  # Debug print
                # print(response)  # Debug print
                
                if response:
                    st.markdown(response)
                    play_audio = st.button("🗣 Play Audio", on_click=play_audio, args=(response,))
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("The AI model returned an empty response. Please try again.")
            except Exception as e:
                st.error(f"An error occurred while generating the response: {str(e)}")
                print(f"Error details: {e}")  # Debug print