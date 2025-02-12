import discord
import requests
import os
from dotenv import load_dotenv  # 추가

load_dotenv()  # .env 파일 로드

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # .env 파일에서 가져옴
URL = os.getenv("API_URL")  # API URL도 환경 변수에서 가져옴

intents = discord.Intents.default()
intents.message_content = True  

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author.bot:
        return  

    if message.content.startswith("!"):
        rune_name = message.content[1:]
        response = requests.get(f"{URL}?rune={rune_name}")

        if response.status_code == 200:
            data = response.text.split("\n")

            if len(data) < 4:  
                await message.channel.send("❌ Sorry, but we couldn't find the information for the requested rune.")
                return

            embed = discord.Embed(title=data[0], description="\n".join(data[1:-1]), color=0x00ff00)

            # 이미지 URL 가져오기
            image_url = data[-1].strip()
            if image_url.startswith("http"):  # URL이 유효한지 확인
                embed.set_image(url=image_url)
            else:
                print(f"❌ 잘못된 이미지 URL: {image_url}")  # 디버깅 용도

            await message.channel.send(embed=embed)
        else:
            await message.channel.send("❌ Error! Please reach out to the administrator.")

client.run(TOKEN)



