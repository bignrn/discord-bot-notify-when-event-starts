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
    
    # Botが参加している全サーバー（ギルド）を走査
    for guild in bot.guilds:
        print(f"サーバー名: {guild.name}")

        # スケジュールイベントを取得
        events = await guild.fetch_scheduled_events()

        if not events:
            print("  現在スケジュールイベントはありません。")
            continue

        # 各イベントの情報を表示
        for event in events:
            print(f"  イベント名: {event.name}")
            print(f"  開始日時: {event.start_time}")
            print(f"  イベントの終了日時（あれば）: {event.end_time}")
            print(f"  イベントの説明（設定していれば）: {event.description}")
            print(f"  イベントが開催されるチャンネル: {event.channel}")
            print(f"  イベントの種類（ボイス/ステージなど）: {event.entity_type}")


# トークンを読み込んで実行
token = load_token_from_json()
bot.run(token)
