import json
import time
from typing import Optional, Dict, Any
import streamlit as st
from groq import Groq
import requests
from io import BytesIO
from langchain.utilities import GoogleSearchAPIWrapper
from transformers import AutoProcessor, AutoModel

# Page Configuration
st.set_page_config(
    page_title="Odia Lingua 🐚🤖",
    page_icon="🐚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Constants
API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-ory"
MAX_RETRIES = 3
RETRY_DELAY = 1
INITIAL_WARMUP_DELAY = 20  # seconds
BASE_RETRY_DELAY = 2  # seconds
MAX_RETRY_DELAY = 30  # seconds

def parse_error_response(error_text: str) -> Dict[str, Any]:
    try:
        error_data = json.loads(error_text)
        return error_data
    except json.JSONDecodeError:
        return {"error": error_text, "estimated_time": None}

def get_retry_delay(attempt: int, error_response: str) -> float:
    error_data = parse_error_response(error_response)
    estimated_time = error_data.get("estimated_time")
    
    if estimated_time is not None:
        return min(estimated_time, MAX_RETRY_DELAY)
    
    # Exponential backoff if no estimated time provided
    return min(BASE_RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)

@st.cache_resource
def initialize_tts_model() -> bool:
    try:
        headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"}
        # Add initial warm-up delay
        time.sleep(INITIAL_WARMUP_DELAY)
        test_payload = {"inputs": "ନମସ୍କାର"}
        response = requests.post(API_URL, headers=headers, json=test_payload)
        if response.status_code == 200:
            print("TTS model initialized successfully")
            return True
        print(f"TTS model initialization failed: {response.status_code}")
        return False
    except Exception as e:
        print(f"Error initializing TTS model: {e}")
        return False

def query(payload: dict) -> Optional[bytes]:
    headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print("Audio generation successful")
        return response.content
    print(f"Error generating audio: {response.status_code} - {response.text}")
    return None

def generate_and_play_audio(text: str) -> Optional[BytesIO]:
    try:
        if not model_ready:
            st.error("TTS model is not initialized. Please wait...")
            return None
            
        with st.spinner("Generating audio..."):
            for attempt in range(MAX_RETRIES):
                try:
                    audio_bytes = query({"inputs": text})
                    if audio_bytes:
                        audio_buffer = BytesIO(audio_bytes)
                        audio_buffer.seek(0)
                        return audio_buffer
                    
                    response = requests.post(API_URL, 
                                          headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"},
                                          json={"inputs": text})
                    
                    if response.status_code == 503:
                        delay = get_retry_delay(attempt, response.text)
                        print(f"Model loading, waiting {delay} seconds before retry...")
                        time.sleep(delay)
                        continue
                        
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == MAX_RETRIES - 1:
                        raise
            return None
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        print(f"Detailed error: {e}")
        return None

def play_audio(text: str) -> None:
    audio_buffer = generate_and_play_audio(text)
    if audio_buffer:
        st.session_state.audio_key += 1
        st.markdown("### Audio Output:")
        st.audio(audio_buffer, format='audio/wav')
    else:
        st.error("Could not generate audio. Please try again.")

def search_google(query: str) -> str:
    print(f"Searching Google for: {query}")
    search = GoogleSearchAPIWrapper()
    results = search.results(query, num_results=3)
    summary = ""
    for i, result in enumerate(results, 1):
        summary += f"{i}. {result['title']}: {result['snippet']}\n\n"
    print("Search Results:", summary)
    return summary[:500]

# Initialize models and state
model_ready = initialize_tts_model()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize session state
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama-3.2-90b-vision-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0

# UI Components
st.title("Odia Lingua 🐚🤖")
st.subheader("ଆପଣଙ୍କର ଓଡ଼ିଆ ବାର୍ତ୍ତାଳାପ ସହାୟକ! 🌺🔥")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and response handling
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
                ବିନମ୍ର, ସମ୍ମାନଜନକ ଏବଂ ଓଡ଼ିଆ ଭାଷାଭାଷୀ ପ୍େରକ୍ଷାପଟକୁ ଅନୁକୂଳ େହବା ଉଚିତ୍।

                ନିମ୍ନଲିଖିତ ବାସ୍ତବ ସମୟ ସନ୍ଧାନ ସୂଚନାକୁ ଆପଣଙ୍କର ପ୍ରତିକ୍ରିୟାକୁ ବୃଦ୍ଧି କରିବାକୁ ବ୍ୟବହାର କରନ୍ତୁ:
                {search_results}
                don't reapeat the Question asked by the user again in the answer just give answer in the most concise and relevant manner possible.
                Give answers in the most concise and relevant manner possible.
                """

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
                
                if response:
                    st.markdown(response)
                    button_key = f"audio_button_{st.session_state.audio_key}"
                    st.button("🗣 Play Audio", key=button_key, on_click=play_audio, args=(response,))
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("The AI model returned an empty response. Please try again.")
            except Exception as e:
                st.error(f"An error occurred while generating the response: {str(e)}")
                print(f"Error details: {e}")