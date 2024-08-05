import discord
from typing import Union, Literal
from redbot.core import app_commands, commands


class GetID(commands.Cog):
    """Get ID of a discord model [user/channel/role/emoji/guild]
    
    Examples [-here-](<https://github.com/rusty-man/rusty-cogs/tree/main/getid>)
    """


    @commands.command(name="getid")
    @commands.guild_only()
    async def getid(self, ctx: commands.Context, model: Union[discord.TextChannel, discord.VoiceChannel, discord.Thread, discord.ForumChannel, discord.StageChannel, discord.CategoryChannel, discord.Member, discord.Role, discord.Emoji, discord.GuildSticker, Literal["guild"]]):
        """Get ID of a discord model [user/channel/role/emoji/guild]
        
        - `getid @rusty-man` ~ `getid #general` ~ `getid @members` ~ `getid :bruh_emoji:` ~ `getid guild`
        - `getid username` ~ `getid role_name` ~ `getid emoji_name` ~ `getid channel_name`
        """

        if isinstance(model, discord.Role):
            id = f"&{model.id}"
        elif isinstance(model, discord.Emoji):
            id = f"`<{'a' if model.animated else ''}:{model.name}:{model.id}>`"
        elif model == "guild":
            id = ctx.guild.id
        else:
            id = model.id

        await ctx.send(id)


    @app_commands.command(name="getid-member")
    @app_commands.describe(member="The member whose id is to be retrieved")
    @commands.guild_only()
    async def getid_member(self, interaction: discord.Interaction, member: discord.Member):
        """Get ID of a guild member"""
        
        id = member.id
        await interaction.response.send_message(id)


    @app_commands.command(name="getid-channel")
    @app_commands.describe(channel="The channel whose id is to be retrieved")
    @commands.guild_only()
    async def getid_channel(self, interaction: discord.Interaction, channel: Union[discord.TextChannel, discord.VoiceChannel, discord.Thread, discord.ForumChannel, discord.StageChannel, discord.CategoryChannel]):
        """Get ID of a guild channel"""
        
        id = channel.id
        await interaction.response.send_message(id)


    @app_commands.command(name="getid-role")
    @app_commands.describe(role="The role whose id is to be retrieved")
    @commands.guild_only()
    async def getid_role(self, interaction: discord.Interaction, role: discord.Role):
        """Get ID of a guild role"""
        
        id = f"&{role.id}"
        await interaction.response.send_message(id)
        

    @app_commands.command(name="getid-guild")
    @commands.guild_only()
    async def getid_guild(self, interaction: discord.Interaction):
        """Get ID of the guild"""
        
        id = interaction.guild.id
        await interaction.response.send_message(id)
