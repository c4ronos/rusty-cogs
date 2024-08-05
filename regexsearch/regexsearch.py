import discord
import regex as re
from redbot.core import commands, app_commands
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS


class RegexSearch(commands.Cog):
    """A cog to search messages using regex."""
    

    # @app_commands.describe(pattern="the regex pattern to compile", flags="optional flags to enhance and customize search")
    @commands.group(name="regex", invoke_without_command=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.guild_only()
    async def regex(self, ctx, pattern: str, *, flags: str = None):
        """Search messages with a regex pattern
        
        > By default, this will ignore bots, embeds, attachments.
        """


        limit = 500
        user = None
        exclude_user = None
        channel = ctx.channel
        include_bots = False
        only_bots = False
        include_media = False
        only_media = False
        include_embeds = False
        only_embeds = False

        if bool(re.search(r'--', pattern)):
            return await ctx.send("Invalid regex pattern. Double dashes (--) are allowed only for flags.")
                
        try:
            regex = re.compile(pattern)
        except re.error:
            return await ctx.send("Invalid regex pattern.")


        if flags:
            flags = flags.split()
            for i, flag in enumerate(flags):
                if flag == "--limit":
                    limit = min(max(int(flags[i + 1]), 1), 10000)
                elif flag == "--channel":
                    channel = await commands.TextChannelConverter().convert(ctx, flags[i + 1])
                elif flag == "--user":
                    user = await commands.MemberConverter().convert(ctx, flags[i + 1])
                elif flag == "--not-user":
                    exclude_user = await commands.MemberConverter().convert(ctx, flags[i + 1])
                elif flag == "--bots":
                    include_bots = True
                elif flag == "--only-bots":
                    only_bots = True
                elif flag == "--media":
                    include_media = True
                elif flag == "--only-media":
                    only_media = True
                elif flag == "--embeds":
                    include_embeds = True
                elif flag == "--only-embeds":
                    include_bots = True
                    only_embeds = True

                
        if limit > 5000 and not ctx.author.guild_permissions.administrator:
            return await ctx.send("You need administrator permissions for searching more than 5.000 messages.")


        messages = []
        async with ctx.typing():
            async for message in channel.history(limit=limit):
                if exclude_user and message.author == exclude_user:                 # skip messages from excluded user
                    continue
                if user and message.author != user:                                 # prioritize --user over --bots
                    continue
                if not regex.search(message.content):                               # skip message if message does not match the pattern
                    continue
                if not include_bots and message.author.bot and not only_bots:       # check for bot message (unless only-bots is used)
                    continue
                if only_bots and not message.author.bot:                            # only include bot messages
                    continue
                if not include_media and message.attachments and not only_media:    # skip attachments
                    continue
                if only_media and not message.attachments:                          # only include attachments
                    continue
                if not include_embeds and message.embeds and not only_embeds:        # skip embeds
                    continue
                if only_embeds and not message.embeds:                               # only include embeds
                    continue

                messages.append(f"- **content:** {message.content[:60]}\n - [jump url]({message.jump_url})")

        if not messages:
            return await ctx.send("No matches found.")


        pages = [messages[i:i + 10] for i in range(0, len(messages), 10)]
        embed_pages = []

        for i, page in enumerate(pages):
            embed = discord.Embed(title="REGEX SEARCHㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
                                  description="\n".join(page),
                                  color=await ctx.embed_color())
            embed.set_footer(text=f"Page {i + 1}/{len(pages)}")
            embed_pages.append(embed)

        await menu(ctx, embed_pages, DEFAULT_CONTROLS)


    @regex.command(name="help")
    async def help(self, ctx):
        """List of arguments and additional help"""

        embed_list = []

        desc = (
            "- `--limit <int>` - The amount of messages to process. default:`500`, min:`1`, max:`10.000`\n"
            "- `--channel <channel>` - Search messages in a specific channel. Value can be id/mention.\n\n"
            "- `--user <user>` - Search messages only from this user. Value can be username/id/mention.\n"
            "- `--not-user <user>` - Do not search messages from this user. Value can be username/id/mention.\n\n"
        )
        embed_1 = discord.Embed(title="RegexSearch Flags", description=desc, color=await ctx.embed_color())
        embed_1.set_footer(text="Flags. Page 1/3")
        embed_list.append(embed_1)

        desc = (
            "- `--bots` - Search messages also from bots.\n"
            "- `--only-bots` - Search messages only from bots.\n\n"
            "- `--media` - Include messages with attachments in the search results.\n"
            "- `--only-media` - Only search messages with attachments.\n\n"
            "- `--embeds` - Include messages with embeds in the search results.\n"
            "- `--only-embeds` - Only search messages with embeds.\n"
        )
        embed_2 = discord.Embed(title="RegexSearch Flags", description=desc, color=await ctx.embed_color())
        embed_2.set_footer(text="Flags. Page 2/3")
        embed_list.append(embed_2)

        desc = (
            f"- `{ctx.prefix}regex .* --limit 1000 --channel #general --user @egirl`\n"
            "will return all messages sent by @egirl in #general's last 1000 messages.\n"
            f"- `{ctx.prefix}regex (discord\.gg/)[A-Za-z0-9]?.* --channel #general`\n"
            "will return all server invite links in #general's last 500 messages.\n"
            f"- `{ctx.prefix}regex (?i)(help|helpp|helppp) --limit 5000`\n"
            "will return all instances of help, helpp, helppp found in current channel's last 5000 messages. (?i) makes it case-insensitive.\n\n"
            "__**Resources:**__\n"
            "Recommended for trying regex: https://regex101.com/\n"
            "Basic regex cheatsheat: [simple_regex.md](https://github.com/rusty-man/rusty-cogs/blob/main/.archive/simple_regex.md)\n"
        )
        embed_3 = discord.Embed(title="RegexSearch Notes", description=desc, color=await ctx.embed_color())
        embed_3.set_footer(text="Notes. Page 3/3")
        embed_list.append(embed_3)

        await menu(ctx, embed_list, DEFAULT_CONTROLS)
