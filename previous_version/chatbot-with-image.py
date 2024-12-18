import discord
from google.cloud import vision
import os
from dotenv import load_dotenv

# Load environment variables (make sure GOOGLE_APPLICATION_CREDENTIALS is set in .env)
load_dotenv()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# Google Cloud Vision client
vision_client = vision.ImageAnnotatorClient()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Prevent bot from responding to itself
    if message.author == client.user:
        return
    
    # Check if the message has attachments (images)
    if message.attachments:
        for attachment in message.attachments:
            # Only process image files
            if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg')):
                await message.channel.send("Processing your image...")

                # Download the image to a local file
                image_path = "temp_image.jpg"
                await attachment.save(image_path)

                # Process the image using Google Cloud Vision
                with open(image_path, 'rb') as image_file:
                    content = image_file.read()

                image = vision.Image(content=content)
                response = vision_client.label_detection(image=image)
                labels = response.label_annotations

                # Prepare the response message
                description = "I found the following objects in the image:\n"
                for label in labels:
                    description += f"- {label.description} (Confidence: {label.score*100:.2f}%)\n"

                # Send the description back to Discord
                await message.channel.send(description)

                # Clean up the temporary image file
                os.remove(image_path)

# Run the bot
client.run(os.getenv("DISCORD_TOKEN"))
