import discord
import requests
import asyncio
import os

from django.core.management.base import BaseCommand
from myapp.models import PostedImage

class Command(BaseCommand):
    help = 'Runs the Discord bot'

    def handle(self, *args, **kwargs):
        DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
        CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

        if not DISCORD_BOT_TOKEN or not CHANNEL_ID:
            raise ValueError("DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID must be set")

        client = discord.Client()

        async def fetch_latest_image():
            response = requests.get('https://danbooru.donmai.us/posts.json?limit=1')
            if response.status_code == 200:
                posts = response.json()
                if posts:
                    return posts[0]['file_url']
            return None

        async def post_latest_image():
            await client.wait_until_ready()
            channel = client.get_channel(CHANNEL_ID)

            while not client.is_closed():
                latest_image_url = await fetch_latest_image()
                if latest_image_url and not PostedImage.objects.filter(image_url=latest_image_url).exists():
                    await channel.send(latest_image_url)
                    PostedImage.objects.create(image_url=latest_image_url)
                await asyncio.sleep(60)

        @client.event
        async def on_ready():
            print(f'Logged in as {client.user}')

        client.loop.create_task(post_latest_image())
        client.run(DISCORD_BOT_TOKEN)
