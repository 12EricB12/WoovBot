import asyncio
import discord

timeoutEmbed = discord.Embed(title="You ran out of time!", description="Please try again.",
                                 colour=0xFF0000)
notFoundEmbed = discord.Embed(title="This challenge does not exist!",
                                      description='Make sure your selection is in the list and is properly capitalized.',
                                      colour=0x808080)

class ReactionHandler:
    def __init__(self, ctx, msg, reaction_lst):
        self.ctx = ctx
        self.msg = msg
        self.reaction_lst = reaction_lst

    async def clearReactions(self):
        for i in self.reaction_lst:
            await self.msg.clear_reaction(i)

    async def addReactions(self):
        for i in self.reaction_lst:
            await self.msg.add_reaction(i)

    async def closeFunction(self):
        await self.ctx.message.delete()
        await self.ctx.send("Stopping command...")


class AsyncHelpers(ReactionHandler):
    client = None
    ctx = None
    msg = None
    reaction_lst = None
    user = None
    timeoutPeriod = None

    def __init__(self, client, ctx, msg, reaction_lst, timeoutPeriod):
        super().__init__(ctx, msg, reaction_lst)
        self.client = client
        self.timeoutPeriod = timeoutPeriod

    def awaitReaction(self, f):
        async def wrapper(self, ctx=self.ctx, msg=self.msg):
            try:
                def check(reaction, user):
                    return ctx.author == user

                reaction, user = await self.client.wait_for('reaction_add', timeout=self.timeoutPeriod, check=check)
                self.user = user

            except asyncio.TimeoutError:
                await self.clearReactions()
                await msg.edit(embed=timeoutEmbed)

            else:
                coro = await f(self, reaction, user)
                return coro

        return wrapper

    def awaitMessage(self, f):
        async def wrapper(self, msg):
            try:
                def check(m):
                    return m.author == self.user

                message = await self.client.wait_for('message', timeout=self.timeoutPeriod, check=check)

            except asyncio.TimeoutError:
                await self.clearReactions()
                await msg.edit(embed=timeoutEmbed)

            except FileNotFoundError:
                msg.edit(embed=notFoundEmbed)
                await asyncio.sleep(3)

            else:
                coro = await f(self, message)
                return coro

        return wrapper
