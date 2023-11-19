import os
import random
from discord.ext import commands
from discord_slash import cog_ext
from cogs.driver.start import Start

class Secret(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="secret",
                       description="admin-test-command-1",
                       guild_ids=Start.guild_ids)
    async def permamute(self, ctx, victim):
        client = self.client

        # def check():
        #     return ctx.author ==

        print(ctx.author)

def setup(client):
    client.add_cog(Secret(client))
