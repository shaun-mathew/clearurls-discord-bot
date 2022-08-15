import os
import re
import discord
from dotenv import load_dotenv
from unalix import clear_url
import cloudscraper
import json


class MyClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="for trackers"
            )
        )

    async def on_message(self, message):
        if message.author == client.user:
            permissions = message.channel.guild.me.permissions_in(message.channel)
            # Suppress embeds for bot messages to avoid visual clutter
            if permissions.manage_messages:
                await message.edit(suppress=True)

                if permissions.add_reactions and permissions.read_message_history:
                    await message.add_reaction("🗑")

        # Extract links and clean

        cleaned = []
        if message.author != client.user:
            urls = re.findall("(?P<url>https?://[^\s]+)", message.content)
            for url in urls:
                cleared_url = clear_url(url)
                amp_request = "https://www.amputatorbot.com/api/v1/convert?gac=true&md=3&q={}".format(
                    url
                )
                de_amp = scraper.get(amp_request)
                js = json.loads(de_amp.text)
                if "error_message" not in js:
                    cleared_url = (
                        js[0]["canonical"]["url"]
                        if (js and "canonical" in js[0])
                        else cleared_url
                    )
                if cleared_url != url:
                    cleaned.append(cleared_url)

        # Send message and add reactions
        if cleaned:
            text = (
                "It appears that you have sent one or more links with tracking parameters or Google AMP links. Below are the same links with those fields removed:\n"
                + "\n".join("||" + clean + "||" for clean in cleaned)
            )
            await message.channel.send(text)


load_dotenv()
client = MyClient()
scraper = cloudscraper.create_scraper()
client.run(os.environ["TOKEN"])
