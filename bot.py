import discord
import asyncio
import os
import re
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents)


async def tasks(setup):
    await bot.wait_until_ready()

    for task in setup:
        if re.search("^send", task):
            r = re.match("^send '(.+?)' '(.+?)' '(.+?)'$", task)
            user_id = r.group(1)
            target_name = r.group(2)
            target_msg = r.group(3)

            last_msg = None
            user = await bot.fetch_user(user_id)
            async for message in user.history(limit=1):
                last_msg = message.content

            if last_msg != target_msg:
                try:
                    await message.delete()
                except discord.errors.Forbidden:
                    pass
                sent_message = await send_message(
                    user_id, f"[{target_name}]({target_msg})")


@bot.event
async def on_ready():
    print("ready")


async def send_message(user_id, message):
    await bot.wait_until_ready()

    user = await bot.fetch_user(user_id)
    return await user.send(content=message)


@bot.command()
async def prune(ctx, num: int = 1):

    count = 0
    async for message in ctx.channel.history(limit=num * 10):
        if message.author == bot.user:
            await message.delete()
            count += 1
        if count >= num:
            break


async def start(setup, token):
    async with bot:
        bot.loop.create_task(tasks(setup))
        await bot.start(token)


def run(setup, token):

    asyncio.run(start(setup, token))
