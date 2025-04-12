import discord
from discord.ext import commands
import json

# トークンをjsonファイルから読み込む関数
def load_token_from_json(path='token.json'):
    with open(path, 'r') as f:
        data = json.load(f)
        return data['discordBitPrivateToken']

# 必要なIntentsを指定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を扱いたい場合はこれが必要

# Botの初期化
bot = commands.Bot(command_prefix="!", intents=intents)

# Botが起動したときの処理
@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

# トークンを読み込んで実行
token = load_token_from_json()
bot.run(token)
