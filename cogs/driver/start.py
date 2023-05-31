import discord
from discord.ext import commands

class Start(commands.Cog):
    guild_ids = [834437459302940722, 954387539060457522, 966802516941635685, 1048680229079634060]

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

def setup(client):
    client.add_cog(Start(client))
