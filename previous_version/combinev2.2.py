import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import requests
import pathlib
from PIL import Image
import sys
import time


# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Google Gemini client
client_gemini = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_ID = "gemini-2.0-flash-exp"

# Set up the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


# Remove the default help command before defining our own.
bot.remove_command("help")

async def send_long_message(ctx, prefix, text):
    max_length = 1990 - len(prefix)
    if len(text) == 0:
        await ctx.send("**No response was generated.**")
        return

    for i in range(0, len(text), max_length):
        part = text[i:i + max_length]
        await safe_send(ctx, f"{prefix}{part}")

# 包裝 send 方法，印出訊息內容
async def safe_send(ctx, content):
    try:
        sys.stdout.buffer.write(f"Bot Sending: {content}\n".encode('utf-8', 'replace'))
    except Exception as e:
        print(f"Error printing to console: {e}")
    await ctx.send(content)

# Event: 捕捉每次接收到的訊息
@bot.event
async def on_message(message):
    if message.author == bot.user:  # 避免處理自己的訊息
        return
    print(f"Message Received: {message.content} (from {message.author})")
    await bot.process_commands(message)

# Command: Ask a question
@bot.command(description="Ask a question to the AI.")
async def ask(ctx, *, question):
    await safe_send(ctx, f"\ud83d\udca1 Thinking about your question...")
    response = client_gemini.models.generate_content(
        model=MODEL_ID, contents=question
    )
    full_response = response.candidates[0].content.parts[0].text
    await send_long_message(ctx, "**Answer:** ", full_response)

# Command: Upload an image and describe it
@bot.command(description="Upload an image and have it described by the AI.")
async def describe(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        img_path = pathlib.Path(f"temp_{attachment.filename}")
        await attachment.save(img_path)
        image = Image.open(img_path)
        await safe_send(ctx, "\ud83d\uddbc Processing image...")
        response = client_gemini.models.generate_content(
            model=MODEL_ID,
            contents=[image, "Describe this image."],
        )
        full_response = response.candidates[0].content.parts[0].text
        await send_long_message(ctx, "**Description:** ", full_response)
        img_path.unlink()
    else:
        await safe_send(ctx, "\ud83d\ude14 Please upload an image with this command.")

# Command: Summarize a PDF
@bot.command(description="Upload a PDF and have it summarized by the AI.")
async def summarize(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        pdf_path = pathlib.Path(f"temp_{attachment.filename}")
        await attachment.save(pdf_path)
        await safe_send(ctx, "\ud83d\udcc4 Analyzing PDF...")
        file_upload = client_gemini.files.upload(path=pdf_path)
        response = client_gemini.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_uri(
                            file_uri=file_upload.uri, mime_type=file_upload.mime_type
                        )
                    ],
                ),
                "Summarize this PDF as bullet points.",
            ],
        )
        full_response = response.candidates[0].content.parts[0].text
        await send_long_message(ctx, "**Summary:** ", full_response)
        pdf_path.unlink()
    else:
        await safe_send(ctx, "\ud83d\ude14 Please upload a PDF file with this command.")

# Command: Chat mode
@bot.command(description="Start a chat session with the AI.")
async def chat(ctx, *, message=None):
    if message is None:
        await safe_send(ctx, "Please provide a message to chat with.")
        return
    await safe_send(ctx, f"\ud83d\udca1 Thinking...")
    chat_session = client_gemini.chats.create(
        model=MODEL_ID, config=types.GenerateContentConfig(temperature=0.5)
    )
    response = chat_session.send_message(message)
    full_response = response.candidates[0].content.parts[0].text
    await send_long_message(ctx, "**Response:** ", full_response)

# Command: Summarize an Audio File
@bot.command(description="Upload an audio file and have it summarized by the AI.")
async def summarize_audio(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        audio_path = pathlib.Path(f"temp_{attachment.filename}")
        await attachment.save(audio_path)
        await safe_send(ctx, "\ud83c\udfa7 Analyzing audio...")
        file_upload = client_gemini.files.upload(path=audio_path)
        response = client_gemini.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_uri(
                            file_uri=file_upload.uri, mime_type=file_upload.mime_type
                        )
                    ],
                ),
                 "Listen carefully to the following audio file. Provide a brief summary.",
            ],
        )
        full_response = response.candidates[0].content.parts[0].text
        await send_long_message(ctx, "**Audio Summary:** ", full_response)
        audio_path.unlink()
    else:
        await safe_send(ctx, "\ud83d\ude14 Please upload an audio file with this command.")


# Command: Describe a Video File
@bot.command(description="Upload a video file and have it described by the AI.")
async def describe_video(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        video_path = pathlib.Path(f"temp_{attachment.filename}")
        await attachment.save(video_path)
        await safe_send(ctx, "\ud83c\udfa5 Analyzing video...")
        file_upload = client_gemini.files.upload(path=video_path)

        # Wait for video processing to complete
        await safe_send(ctx, "Waiting for video to be processed...")
        while True:
            time.sleep(10) # Check every 10 seconds
            file_upload = client_gemini.files.get(name=file_upload.name)
            if file_upload.state == "PROCESSING":
                await safe_send(ctx, "Video processing still in progress, please wait...")
                continue
            elif file_upload.state == "FAILED":
                await safe_send(ctx, "Video processing failed.")
                video_path.unlink()
                return
            elif file_upload.state == "ACTIVE":
                break
        await safe_send(ctx, "Video processing complete. Generating Description")
        response = client_gemini.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_uri(
                            file_uri=file_upload.uri,
                            mime_type=file_upload.mime_type),
                    ]),
                "Describe this video.",
            ]
        )
        full_response = response.candidates[0].content.parts[0].text

        # Print to terminal
        print(f"Video Description:\n{full_response}")

        await send_long_message(ctx, "**Video Description:** ", full_response)
        video_path.unlink()
    else:
        await safe_send(ctx, "\ud83d\ude14 Please upload a video file with this command.")


# Overwrite the default help command
@bot.command(name="help", description="Show this help message.")
async def help_command(ctx):
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
    for command in bot.commands:
        embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
    await ctx.send(embed=embed)


# Run the bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

bot.run(TOKEN)