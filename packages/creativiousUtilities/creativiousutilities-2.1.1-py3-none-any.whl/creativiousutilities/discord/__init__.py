import discord
import os
from os import path
import logging
import datetime
from discord.ext import commands


def loadAllCogs(bot : commands.Bot, cogFolder : str):
    """Loads all cogs when given the bot object and the folder for the cog"""
    cogs = []
    cogFolderExtensionFormat = (f"{cogFolder.replace('/', '.')}." if cogFolder.replace('/', '.')[-1:] != "." else cogFolder.replace('/', '.')) # Quick checks and fixes
    if path.exists(cogFolder):
        items = os.listdir(cogFolder)
        cogs = [bot.load_extension(f"{cogFolderExtensionFormat}{item[:-3]}") for item in items if item[-3:] == ".py"] # Grabbing all the cogs

    else:
        raise "Couldn't find the given path, please enter the correct path and try again!"


class HelpCommand:
    def __init__(self, client : commands.Bot):
        """Generates an automatic help command for a discord bot using py-cord"""
        self.client = client
        self.cogs = [str(cog) for cog in client.cogs]
        self.base_commands = [str(command.name) for command in list(client.commands)]
        self.prefix = str(self.client.command_prefix)
        self.base_commands_list = self.__generateBaseCommandsList()
        self.pages = self.__generatePages()

    def __generateBaseCommandsList(self):
        base_commands_list = []
        for command in self.base_commands:
            commandDetail = f"***{str(self.prefix)}{str(command)}*** - *{str(self.client.command(command))}*"
            base_commands_list.append(commandDetail)
        return base_commands_list

    def __generatePages(self):
        cogsExist = len(self.cogs) > 0
        pages = []
        string = "\n"
        for command in self.base_commands_list:
            string += command + "\n"
        embed = discord.Embed(title=f"{self.client.user.name} Commands", description=f"""**COMMANDS**
        """, color=discord.Color.random())
        pages.append(embed)
        return pages

    def getHelp(self, page: int = 0):
        return self.pages[page]