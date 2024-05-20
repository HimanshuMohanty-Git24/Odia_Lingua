# Odia Lingua 🐚🤖
![OdiaLingua ](https://github.com/HimanshuMohanty-Git24/Odia_Lingua/assets/94133298/c47f3775-f4e7-4b44-8c32-80b68bf792aa)


Jay Jagannath 🙏🕉️, Odia Lingua is an end-to-end generative AI chatbot for the Odia language. It utilizes the Anthropc API for chat generation and features a Text-to-Speech (TTS) functionality for Odia using the Facebook/mms-tts-ory API.

### Features:
- Chatbot powered by Anthropc AI for conversational responses.
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
   ANTHROPIC_API_KEY = "<Your-anthropic-api-key>"
   HUGGINGFACE_API_KEY = "<Your-huggingface-api-key>"
   ```
   To get the api's go to the respective website and get your api key's
### Requirements:
Ensure you have the following dependencies installed:
- streamlit
- anthropic
- python-dotenv

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







