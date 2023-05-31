import os
import random
from discord.ext import commands
from discord_slash import cog_ext
from cogs.driver.start import Start
from .helper import *


class Methods:
    def loadEmbeds(self, fillEmbeds):
        listEmbeds = fillEmbeds.fillEmbeds()

        listEmbed = listEmbeds[0]
        noListEmbed = listEmbeds[1]
        challengeEmbed = listEmbeds[2]
        randomEmbed = listEmbeds[3]

        return listEmbed, noListEmbed, challengeEmbed, randomEmbed

    def seperateChallenge(self):
        path = r'.\Bot files\Val Challenges'
        available = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]
        for i in range(len(available)):
            text = available[i]
            head, sep, tail = text.partition('.txt')
            available[i] = head
        return available

    def getChallengeList(self, challenge):
        path = r'.\Bot files\Val Challenges'
        f = open(path.format(name=challenge))
        content = f.readlines()
        content = content[1:len(content)]
        f.close()
        return content

    def splitChallenge(self, content):
        challenge_name = []
        index = random.randint(0, len(content) - 1)
        challenge_cont = content[index]

        for i in range(len(content[index])):
            if challenge_cont[i] == ",":
                challenge_name.append(challenge_cont[0:i])
                challenge_name.append(challenge_cont[i + 1:len(challenge_cont)])

        return index, challenge_name


class Embeds:
    challenge = None

    def __init__(self, available, challenge):
        self.available = available
        self.challenge = challenge

    def fillEmbeds(self):
        listEmbed = discord.Embed(title="Available challenges",
                                  description='{available}'.format(available='\n'.join(self.available)),
                                  colour=0x808080)
        listEmbed.set_footer(text="Please select a list by typing it's name in chat. The selection IS case sensitive.")
        noListEmbed = discord.Embed(title="This challenge does not exist!",
                                    description='Make sure your selection is in the list and is properly capitalized.'
                                    .format(available='\n'.join(self.available)),
                                    colour=0x808080)
        challengeEmbed = discord.Embed(title="Is this the challenge you want?",
                                       description='{challenge}'.format(challenge=str(self.challenge)),
                                       colour=0x808080)
        randomEmbed = discord.Embed(title=f"{self.challenge}",
                                    description='React with 🎲 to roll a random challenge. If you want to stop, '
                                                'react with '
                                                '⏰. The challenge will automatically shut down after 15 minutes.',
                                    colour=0x808080)
        return listEmbed, noListEmbed, challengeEmbed, randomEmbed

    notFoundEmbed = discord.Embed(title="That challenge does not exist!",
                                  description='Make sure your input is case sensitive and is in the list.',
                                  colour=0x808080)
    warnEmbed = discord.Embed(title="Warning!",
                              description="This challenge has less than 18 options. This means you have a "
                                          "high chance to "
                                          " get duplicate challenges. Are you sure you want to proceed?",
                              colour=0xFFFF00)
    timeoutEmbed = discord.Embed(title="You ran out of time!", description="Please try again.",
                                 colour=0xFF0000)


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

    async def stopCommand(self):
        await self.userMsg.delete()
        await self.msg.delete()
        await self.ctx.send("Stopping command...")

    @deco.awaitReaction
    async def getReaction(self, rxn, u):
        return rxn

    @deco.awaitMessage
    async def getMessageContent(self, msg):
        self.userMsg = msg
        return msg.content


class ChallengeInitializer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="load",
                       description="Select and load a challenge from the list.",
                       guild_ids=Start.guild_ids)
    async def load(self, ctx):
        check_mark = '✔'
        red_cross = '❌'

        reaction_lst = [check_mark, red_cross]
        client = self.client
        methods = Methods()

        availableFiles = methods.seperateChallenge()
        fillEmbeds = Embeds(availableFiles, None)

        listEmbed, noListEmbed, challengeEmbed, randomEmbed = methods.loadEmbeds(fillEmbeds)

        msg = await ctx.send(embed=listEmbed)

        driver = Driver(None, msg, reaction_lst, client, ctx, check_mark, 30)
        reactions = ReactionHandler(ctx, msg, reaction_lst)

        while True:
            await driver.getMessageContent()
            message = driver.userMsg
            fillEmbeds.challenge = message

            if str(message) in availableFiles:
                await message.delete()
                await msg.edit(embed=challengeEmbed)
                await reactions.addReactions()

                rxn = await driver.getReaction()
                await reactions.clearReactions()

                if rxn == check_mark:
                    break
                else:
                    continue
            else:
                await msg.edit(embed=Embeds.notFoundEmbed)
                await asyncio.sleep(3)
                continue

        content = methods.getChallengeList(fillEmbeds.challenge)
        used = []

        if len(content) < 18:
            await reactions.clearReactions()
            await msg.edit(Embeds.warnEmbed)
            await reactions.addReactions()

            rxn = await driver.getReaction()
            await reactions.clearReactions()

            if rxn == check_mark:
                pass
            else:
                await driver.stopCommand()
                return

        dice = '🎲'
        alarm_clock = '⏰'
        reactions.reaction_lst = [dice, alarm_clock]  # Set reactions for next part
        driver.timeoutPeriod = 900

        await msg.edit(embed=randomEmbed)
        await reactions.addReactions()

        while True:
            rxn = await driver.getReaction()
            if rxn == dice:
                indexOfChallenge, fullChallenge = methods.splitChallenge(content)
                elem = content.pop(indexOfChallenge)
                used.append(elem)

                if len(content) == 1:  # Reload the list
                    used.append(content[0])
                    content = used
                    used = []

                embed = discord.Embed(title=fullChallenge[0], description=fullChallenge[1])
                embed.set_footer(text=f"Challenge started by {message.author}. Only they can cycle through the "
                                      f"challenges.")
            else:
                await driver.stopCommand()
                break

def setup(client):
    client.add_cog(ChallengeInitializer(client))
