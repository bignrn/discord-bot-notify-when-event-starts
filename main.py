import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, timezone, timedelta

# トークンをjsonファイルから読み込む関数
def load_token_from_json(path='token.json'):
    with open(path, 'r') as f:
        data = json.load(f)
        return data['discordBitPrivateToken']

# 必要なIntentsを指定
intents = discord.Intents.default()
intents.message_content = True

# Botの初期化
bot = commands.Bot(command_prefix="!", intents=intents)

# 通知済みイベントIDを記録
notified_event_ids = set()

# 通知するチャンネル名（適宜変更OK）
TARGET_CHANNEL_NAME = "イベント通知"

# Botが起動したときの処理
@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

    for guild in bot.guilds:
        print(f"サーバー名: {guild.name}")

        events = await guild.fetch_scheduled_events()
        if not events:
            print("  現在スケジュールイベントはありません。")
            continue

        for event in events:
            print(f"  イベント名: {event.name}")
            print(f"  開始日時: {event.start_time}")
            print(f"  終了日時: {event.end_time}")
            print(f"  説明: {event.description}")
            print(f"  チャンネル: {event.channel}")
            print(f"  種類: {event.entity_type}")

    check_events.start()  # イベント監視ループを開始

# 定期的にイベントをチェックするタスク
@tasks.loop(seconds=30)
async def check_events():
    now = datetime.now(timezone.utc)

    for guild in bot.guilds:
        events = await guild.fetch_scheduled_events()
        for event in events:
            if event.id in notified_event_ids:
                continue

            # 5分以内に開始されるイベントを通知
            if event.start_time and now <= event.start_time <= now + timedelta(minutes=5):
                target_channel = discord.utils.get(guild.text_channels, name=TARGET_CHANNEL_NAME)
                if target_channel:
                    await target_channel.send(
                        f"📢 イベント『{event.name}』がまもなく開始されます！\n"
                        f"開始時刻: {event.start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC"
                    )
                    notified_event_ids.add(event.id)
                else:
                    print(f"⚠ チャンネル『{TARGET_CHANNEL_NAME}』が見つかりません")

# Bot起動
token = load_token_from_json()
bot.run(token)
