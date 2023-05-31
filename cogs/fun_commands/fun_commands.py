import asyncio

import discord
from time import *
from discord.ext import commands
from discord_slash import cog_ext
from cogs.driver.start import Start


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="ratio",
                       description="Used to settle disputes in a Gen Z way",
                       guild_ids=Start.guild_ids)
    async def ratio(self, ctx):
        channel = ctx.channel
        guild = ctx.message.guild
        r1 = "👍"
        await ctx.message.delete()

        # Finds the user of the message and sets up a very simple "agree" or "disagree" implementation
        try:
            # If the user mentions the bot, scan the message (@everyone does different things than @user)
            if ctx.message.mentions:
                user = ctx.message.mentions[0]

                if user == "":
                    print("a")
                    print(ctx.message)

                await user.send("Get ratioed L+Bozo")
            else:
                msg = ctx.message.content
                if msg[7:len(msg)] == "@everyone":
                    for m in guild.members:
                        await ctx.send(f"{m} just got ratioed. L")
                        await m.send("Get ratioed L+Bozo")

        except AttributeError:
            if self.client.user == self.client:
                await ctx.send("You cannot message the bot")
            else:
                await ctx.send("User does not exist")
        except discord.Forbidden:
            await channel.send("User has messages turned off")
        finally:
            msg = await channel.send("Ratio")
            await msg.add_reaction(r1)

    @commands.command(help="Flood")
    async def flood(self, ctx, times: int):
        await ctx.send("F\nL")
        if times >= 50:
            await ctx.send("Too many times")
        else:
            for i in range(times):
                await ctx.send("O\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\nO\n")
                await asyncio.sleep(1)

        await ctx.send("D!")

def setup(client):
    client.add_cog(Messages(client))
