```markdown
# Discord AI Bot

This is a powerful Discord bot that integrates with Google Gemini AI to offer advanced functionalities such as image, video, and audio analysis, PDF summarization, and real-time chat.

## Features

- **Ask AI**: Ask any question and get a thoughtful response.
- **Image Description**: Upload an image, and the bot provides a detailed description.
- **Video Analysis**: Upload a video, and the bot generates a description after processing.
- **PDF Summarization**: Upload a PDF, and the bot summarizes its contents as bullet points.
- **Audio Summarization**: Upload an audio file, and the bot provides a concise summary.
- **Chat Mode**: Engage in a dynamic chat session with the AI.

## Setup

### Prerequisites

- Python 3.9 or higher
- A Discord bot token (create a bot on the [Discord Developer Portal](https://discord.com/developers/applications))
- Google Gemini API key
- Required Python libraries:
  - `discord.py`
  - `python-dotenv`
  - `google-genai`
  - `Pillow`

### Installation

1. Clone the repository or download the code.
2. Create a `.env` file in the root directory and add your keys:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token
   GEMINI_API_KEY=your_google_gemini_api_key
   ```
3. Install the dependencies:
   ```bash
   pip install discord.py python-dotenv google-genai pillow
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

### Bot Commands

| Command            | Description                                      |
|--------------------|--------------------------------------------------|
| **/describe_video** | Upload a video file and have it described by the AI. |
| **/describe**       | Upload an image and have it described by the AI.  |
| **/ask**            | Ask a question to the AI.                        |
| **/help**           | Show this help message.                          |
| **/chat**           | Start a chat session with the AI.                |
| **/summarize**      | Upload a PDF and have it summarized by the AI.   |
| **/summarize_audio**| Upload an audio file and have it summarized by the AI.|

### Help Command
Use `/help` to see all available commands and their descriptions.

## Technical Details

- **Google Gemini Integration**: The bot uses Google Gemini's `genai` library to perform AI tasks.
- **Dynamic Message Handling**: Handles long responses by splitting them into manageable chunks.
- **File Processing**: Supports temporary file storage for processing attachments like PDFs, images, audio, and videos.
- **Extensible**: Easily add more commands and features by leveraging `discord.ext.commands`.

## Troubleshooting

- Ensure your `.env` file is correctly set up with valid API keys.
- Verify all dependencies are installed.
- If the bot doesn't respond, check the logs for errors.

## Contributing

Feel free to fork the repository and submit a pull request with your improvements!
