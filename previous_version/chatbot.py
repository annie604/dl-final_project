import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
import textwrap  # For handling long messages


# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Gemini API URL
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def query_gemini_api(prompt):
    """
    Send a prompt to the Gemini API and retrieve the response.
    """
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": GEMINI_API_KEY}

    response = requests.post(GEMINI_API_URL, headers=headers, json=data, params=params)
    print(f"API Response Code: {response.status_code}")
    print(f"API Raw Response: {response.text}")

    if response.status_code == 200:
        try:
            response_data = response.json()

            # Extract text from response using correct structure
            if "candidates" in response_data:
                candidate = response_data["candidates"][0]  # First candidate response
                if "content" in candidate and "parts" in candidate["content"]:
                    return candidate["content"]["parts"][0]["text"]
                else:
                    return "Error: Unexpected content format in Gemini API response."
            else:
                return "Error: No candidates found in Gemini API response."
        except Exception as e:
            return f"Error: Failed to parse JSON response. {e}"
    else:
        return f"Error: {response.status_code} - {response.text}"


@bot.event
async def on_ready():
    """Print a message when the bot is ready."""
    print(f"Logged in as {bot.user}")


@bot.command()
async def ask(ctx, *, question: str):
    """Handle user queries and respond with Gemini API output."""
    print(f"Command triggered: ask - {question}") # Log the full command for debugging
    await ctx.send("Let me think...")

    # Adding basic prompt engineering
    prompt = f"Answer the following question as helpfully as possible:\n\n{question}"
    gemini_response = query_gemini_api(prompt)
    
    if gemini_response.startswith("Error:"):
         await ctx.send(f"I encountered an error while processing your request: {gemini_response}")
    else:
        # Split the response into multiple messages if necessary to avoid exceeding the Discord character limit
        for chunk in textwrap.wrap(gemini_response, width=2000):
            await ctx.send(chunk)



# Run the bot
bot.run(DISCORD_TOKEN)