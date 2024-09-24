# Odia Lingua 🐚🤖 
![OdiaLingua2](https://github.com/HimanshuMohanty-Git24/Odia_Lingua/assets/94133298/5ddfab1c-95b7-4560-9e89-ed66bc466f47)

Jay Jagannath 🙏🕉️, Odia Lingua is an end-to-end generative AI chatbot for the Odia language. It utilizes the Groq API for chat generation and features a Text-to-Speech (TTS) functionality for Odia using the Facebook/mms-tts-ory API. The chatbot also incorporates real-time information retrieval using Google Search API.

### Features:
- Chatbot powered by Groq AI for conversational responses in Odia.
- Real-time information retrieval using Google Search API.
- Text-to-Speech (TTS) feature for generating audio in Odia language.
- End-to-end generative AI project.

### Setting Up:
To set up Odia Lingua locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/HimanshuMohanty-Git24/Odia_Lingua.git
   ```
2. Navigate into the project directory:
   ```
   cd Odia_Lingua
   ```
3. Create a .streamlit directory:
   ```
   mkdir .streamlit
   ```
4. Inside the `.streamlit` directory, create a `secrets.toml` file.

5. Add your API keys to the `secrets.toml` file:
   ```
   GROQ_API_KEY = "<Your-groq-api-key>"
   HUGGINGFACE_API_KEY = "<Your-huggingface-api-key>"
   GOOGLE_API_KEY = "<Your-google-api-key>"
   GOOGLE_CSE_ID = "<Your-GOOGLE_CSE_ID>"
   ```
   To get the API keys, go to the respective websites:
   - Groq: [Link to Groq API keys]
   - Huggingface: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Google Search API: [Link to Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Google CSE ID: [CSE ID](https://programmablesearchengine.google.com/controlpanel/create)


6. Create and activate a Conda environment:
    ```
    conda create --name odia_lingua_v2
    conda activate odia_lingua_v2
    ```
### Requirements(requirements.txt):
Ensure you have the following dependencies installed:
- streamlit
- groq
- python-dotenv
- requests
- langchain
- google-search-results

You can install them using:
```
pip install -r requirements.txt
```

## Usage:
To run the application locally, execute the following command:
```
streamlit run Chatbot.py
```

## Contributing:
Contributions are welcome! Feel free to open issues and pull requests.

## License:
This project is licensed under the [MIT License](LICENSE).