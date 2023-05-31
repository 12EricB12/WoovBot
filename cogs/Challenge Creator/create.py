import os
from discord.ext import commands
from discord_slash import cog_ext
from cogs.driver.start import Start
from .helper import *

class Embeds:
    initialEmbed = discord.Embed(title="Create a New Challenge List!", description="Would you like to proceed?",
                                 colour=0x808080)
    timeoutEmbed = discord.Embed(title="You ran out of time!", description="Please try again.",
                                 colour=0xFF0000)
    startEmbed = discord.Embed(title="Insert title!", description="Please enter your title.", colour=0x808080)
    pathEmbed = discord.Embed(title="A challenge by this name "
                                    "already exists!.", description="Please choose a different "
                                                                    "name.",
                              colour=0x808080)
    titleEmbed = discord.Embed(title="Input new title", description="What is your new title?",
                               colour=0x808080)
    setEmbed = discord.Embed(title="Input a new set!", description="Please enter as this format: '(Challenge name): "
                                                                   " (Challenge description)'. Type 'Stop' anytime to "
                                                                   "stop adding sets.",
                             colour=0x808080)
    newSetEmbed = discord.Embed(title="Input a new set!",
                                description="Please enter as this format: '(Challenge name): "
                                            " (Challenge description)'. Type 'Stop' anytime to "
                                            "stop adding sets. (NOTE: You have 5 minutes to input"
                                            " a new set before the program cancels.)",
                                colour=0x808080)
    formattingEmbed = discord.Embed(title="Wrong format!", description="Please input the sets in a correct"
                                                                       " format.",
                                    colour=0x808080)


class Driver(AsyncHelpers):
    fileToEdit = None

    def __init__(self, userMsg, botMsg, reaction_lst, client, ctx, approve, timeoutPeriod):
        super().__init__(client, ctx, botMsg, reaction_lst, timeoutPeriod)
        self.userMsg = userMsg
        self.msg = botMsg
        self.reaction_lst = reaction_lst
        self.approve = approve
        self.fileToEdit = None

    deco = AsyncHelpers(AsyncHelpers.client, AsyncHelpers.ctx, AsyncHelpers.client, AsyncHelpers.reaction_lst,
                        AsyncHelpers.timeoutPeriod)

    def getElements(self):
        content = self.userMsg.content
        print(content)

        for i in range(len(content)):
            if content[i] == ':':
                title = content[0:i]
                context = content[i + 1:len(content)]

                return title, context

    @deco.awaitReaction
    async def startFunc(self, rxn, u):
        await self.clearReactions()
        await self.msg.edit(embed=Embeds.startEmbed)

    @deco.awaitMessage
    async def getFileName(self, msg):
        self.userMsg = msg

        embed = discord.Embed(title=f"Your title is {msg.content}.", description="Is this correct?",
                              colour=0x808080)
        await self.msg.edit(embed=embed)
        await self.addReactions()

    @deco.awaitReaction
    async def checkPath(self, rxn, u):
        if str(rxn) == str(self.approve):
            self.fileToEdit = self.userMsg.content.lower()
            pathExist = os.path.exists(
                r"./Bot files/Val Challenges/{name}.txt".format(
                    name=self.fileToEdit))
            return pathExist
        else:
            return None

    @deco.awaitMessage
    async def getMessageContent(self, msg):
        self.userMsg = msg
        return msg.content

    @deco.awaitReaction
    async def addLines(self, rxn, u):
        elems = self.getElements()

        if str(rxn) == self.approve:
            await self.clearReactions()
            f = open(r"./Bot files/Val Challenges/{name}.txt".format(name=self.fileToEdit), "a")
            f.write(f"\n{elems[0]}, {elems[1]}")
            f.close()
        else:
            await self.clearReactions()


class ChallengeInitializer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="create",
                       description="Creates a new challenge list.",
                       guild_ids=Start.guild_ids)
    async def create(self, ctx):
        check_mark = '✔'
        red_cross = '❌'

        reaction_lst = [check_mark, red_cross]
        client = self.client

        msg = await ctx.send(embed=Embeds.initialEmbed)

        driver = Driver(None, msg, reaction_lst, client, ctx, check_mark, 30)
        reactions = ReactionHandler(ctx, msg, reaction_lst)

        await reactions.addReactions()
        await driver.startFunc(ctx, msg)

        while True:
            await driver.getFileName(msg)  # For message object
            message = driver.userMsg
            pathExist = await driver.checkPath(ctx, msg)

            if pathExist is True:
                await msg.edit(embed=Embeds.pathEmbed)
                await message.delete()
                await reactions.clearReactions()
                await asyncio.sleep(3)
                await msg.edit(embed=Embeds.titleEmbed)
                continue
            else:
                if pathExist is None:
                    await reactions.clearReactions()
                    await msg.edit(embed=Embeds.titleEmbed)
                    await message.delete()
                    continue
                else:
                    f = open(r"./Bot files/Val Challenges/{name}.txt".format(name=message.content),
                             'x')
                    await message.delete()
                    break

        await reactions.clearReactions()

        while True:
            await msg.edit(embed=Embeds.newSetEmbed)
            content = await driver.getMessageContent(msg)
            message = driver.userMsg

            if content.lower() == 'stop':
                await message.delete()
                await msg.delete()
                await ctx.send("Stopping command...")
                break
            elif ':' not in content:
                await message.delete()
                await msg.edit(embed=Embeds.formattingEmbed)
                await asyncio.sleep(3)
                continue
            else:
                elems = driver.getElements()
                await message.delete()
                print(message)
                embed = discord.Embed(title="Is this right?",
                                      description=f"Title of challenge: {elems[0]}"
                                                  f"\nContent: {elems[1]}",
                                      colour=0x808080)
                await msg.edit(embed=embed)
                await reactions.addReactions()
                await driver.addLines(ctx, msg)
                continue


def setup(client):
    client.add_cog(ChallengeInitializer(client))
