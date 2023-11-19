import discord
import os
from discord.ext import commands
from discord_slash import SlashCommand

client = commands.Bot(command_prefix='+', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
bot_token = os.environ['TOKEN']

print(bot_token)

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
