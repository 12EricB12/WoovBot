import discord
import os
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

client = commands.Bot(command_prefix='+', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
bot_token = 'ODM0NDM3OTAyMDA3MDA5Mjgw.YIA42g.Et7eR0tb81WK3cFiLghz_ka3g9Q'


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for name in os.listdir('./cogs'):
    for sub in os.listdir(f'./cogs/{name}'):
        if sub.endswith(".py"):
            try:
                client.load_extension(f'cogs.{name}.{sub[:-3]}')
            except discord.ext.commands.errors.NoEntryPointError:
                # Prevents lots of edge cases without putting the file in the root directory
                pass

client.run(bot_token)
