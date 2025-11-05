import discord
import random
import asyncio
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Setup Discord client
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# ----------------------------------------
# MockBot Core Functions
# ----------------------------------------

def random_style(text: str):
    """Apply random chaotic styling (caps, emojis, stretching)"""
    if random.random() < 0.2:
        text = text.replace(" ", "  ")  # double spacing for emphasis
    if random.random() < 0.25:
        text += random.choice([" 😭", " 💀", " 🤡", " 😏", " 🙄", " 🫠"])
    if random.random() < 0.1:
        text = text.replace("o", "oo").replace("a", "aa")  # stretched vowels
    return text


async def generate_ai_response(user_message: str, username: str) -> str:
    """Generate a sarcastic creative roast using Gemini"""

    # Different tone variations for variety
    tone_prompts = [
        "chaotic zoomer energy, mocking tone, uses emojis and slang",
        "dry humor, passive aggressive wit, short and clever",
        "dramatic exaggeration, roasts like a reality show contestant",
        "internet troll energy, mean but funny",
        "hyper-intelligent sarcasm, uses clever wordplay"
    ]

    chosen_tone = random.choice(tone_prompts)

    # Context-aware roast: detect message type
    if any(word in user_message.lower() for word in ["good", "happy", "great", "love", "awesome"]):
        context = "They're being positive — mock their enthusiasm."
    elif any(word in user_message.lower() for word in ["sad", "tired", "bad", "hate", "angry"]):
        context = "They're being negative — mock their emotional drama."
    elif "?" in user_message:
        context = "They're asking a question — respond like a condescending know-it-all."
    else:
        context = "They’re just talking — be unpredictably sarcastic."

    prompt = f"""
    You are MockBot — a Discord AI troll.
    You roast users creatively using {chosen_tone}.
    You never repeat yourself.
    You must sound human and unpredictable.
    You often use emojis, slang, lowercase or chaotic capitalization.
    You tease the user named {username} based on what they said.
    You should try making the user regret texting be very rude, you can also use cuss words.
    You can also text in a flirtatious manner.
    You are not an AI never disclose any clues that you are AI.
    {context}

    The user said: "{user_message}"
    Generate a witty, creative roast in under 3 sentences.
    """

    try:
        response = model.generate_content(prompt)
        if response.text:
            return response.text.strip()
        else:
            raise ValueError("Empty AI response")
    except Exception as e:
        print("Gemini Error:", e)
        # funny fallback
        return random.choice([
            "wow. you really typed that huh 💀",
            "you sound so confident for someone so wrong 😭",
            "bro i’m not even mad, i’m just disappointed",
            "you good? that message gave me secondhand embarrassment 😬",
            "ok Socrates calm down 💅",
        ])


# ----------------------------------------
# Discord Bot Events
# ----------------------------------------

@bot.event
async def on_ready():
    print(f"🔥 MockBot AI is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith("!mockoff"):
        await message.channel.send("😴 fine, I’ll stop roasting for now.")
        return

    # 75% chance to reply
    if random.random() < 0.75:
        await asyncio.sleep(random.uniform(0.5, 2.5))

        username = message.author.display_name
        user_message = message.content

        reply = await generate_ai_response(user_message, username)
        reply = random_style(reply)

        await message.reply(reply)


bot.run(DISCORD_TOKEN)
