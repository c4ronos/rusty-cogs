from typing import Final
from datetime import datetime

import discord
import aiohttp

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import box

embed_icon: Final[str] = 'https://i.pinimg.com/564x/f9/af/85/f9af851ee1dfb82be163fe9f7266b13d.jpg'
footer_text = 'Powered by Waifu.IM API'

class WaifuIM(commands.Cog):
    """
    Get images from Waifu.IM API
    """

    __author__ = ["Shit Show Development"]
    __version__ = "1.0.0"

    def __init__(self, bot):
            self.bot = bot
            self.session = aiohttp.ClientSession()

    async def cog_unload(self):
            await self.session.close()

    @commands.hybrid_group()
    async def waifuim(self, ctx):
            """
            Get waifu images from waifu.im api.

            Will display a SFW response in SFW channel(s) and a NSFW response in NSFW channel(s)
            """
            return

    @waifuim.command()
    async def help(self, ctx):
            """
            Display the waifuim help message
            """
            tags_endpoint = 'https://api.waifu.im/tags'

            async with self.session.get(tags_endpoint) as response:
                data = await response.json()

            versatile = data['versatile']
            nsfw = data['nsfw']

            versatile_array = ', '.join(versatile)
            nsfw_array = ', '.join(nsfw)

            versatile_tags = '{}'.format(versatile_array)
            nsfw_tags = '{}'.format(nsfw_array)

            if ctx.channel.is_nsfw():
                    tags = f'{versatile_tags}, {nsfw_tags}'
            else:
                    tags = f'{versatile_tags}'

            embed = discord.Embed(description=f'Here is a list of available tags from the waifu.im api.\n\n{box(tags)}\n\nTo use them simply type: `[p]waifuim tag <tag>`')
            embed.color = await ctx.embed_color()
            embed.set_image(url='https://cdn.waifu.im/7892.jpg')
            embed.set_footer(text=footer_text, icon_url=embed_icon)
            view = discord.ui.View()
            style = discord.ButtonStyle.grey
            website_button = discord.ui.Button(style=style, label='Waifu.IM', url='https://www.waifu.im/')
            view.add_item(item=website_button)

            await ctx.send(embed=embed, view=view)
            
    
    @waifuim.command()
    async def random(self, ctx):
            """
            Get a random waifu image
            """
            search_endpoint = 'https://api.waifu.im/search'

            if ctx.channel.is_nsfw():
                    params = {'is_nsfw': 'true'}
            else:
                    params = {'is_nsfw': 'false'}

            async with self.session.get(search_endpoint, params=params) as response:
                data = await response.json()

                for image in data['images']:
                        image_url = image['url']
                        image_id = image['image_id']
                        source_url = image['source']
                        uploaded_at = image['uploaded_at']

                raw = datetime.fromisoformat(uploaded_at).date().strftime("%B %d, %Y")

                date = '{}'.format(raw)
                upload_date = date

                embed = discord.Embed()
                embed.add_field(name='Image ID', value=image_id, inline=True)
                embed.add_field(name='Upload Date', value=upload_date, inline=True)
                embed.set_image(url=image_url)
                embed.set_footer(text=footer_text, icon_url=embed_icon)
                embed.color = await ctx.embed_color()
                view = discord.ui.View()
                style = discord.ButtonStyle.grey
                image_button = discord.ui.Button(style=style, label='Open Image', url=image_url)
                source_button = discord.ui.Button(style=style, label='Image Source', url=source_url)
                view.add_item(item=image_button)
                view.add_item(item=source_button)

                await ctx.send(embed=embed, view=view)
            
    @waifuim.command()
    async def tag(self, ctx, tag):
            """
            Get a random waifu image by tag.

            See `[p]waifuim help` for a list of available tags.
            """
            tags_endpoint = 'https://api.waifu.im/tags'
            search_endpoint = 'https://api.waifu.im/search'

            if ctx.channel.is_nsfw():
                    params = {'included_tags': '{}'.format(tag), 'is_nsfw': 'true'}
            else:
                    params = {'included_tags': '{}'.format(tag)}

            async with self.session.get(tags_endpoint) as response:
                data = await response.json()

            versatile_tags = data['versatile']
            nsfw_tags = data['nsfw']

            async def send_image():
                    async with self.session.get(search_endpoint, params=params) as response:
                            data = await response.json()

                    for image in data['images']:
                            image_url = image['url']
                            image_id = image['image_id']
                            source_url = image['source']
                            uploaded_at = image['uploaded_at']

                    raw = datetime.fromisoformat(uploaded_at).date().strftime("%B %d, %Y")
                    date = '{}'.format(raw)
                    upload_date = date

                    embed = discord.Embed()
                    embed.add_field(name='Image ID', value=image_id, inline=True)
                    embed.add_field(name='Upload Date', value=upload_date, inline=True)
                    embed.set_image(url=image_url)
                    embed.set_footer(text=footer_text, icon_url=embed_icon)
                    embed.color = await ctx.embed_color()
                    view = discord.ui.View()
                    style = discord.ButtonStyle.grey
                    image_button = discord.ui.Button(style=style, label='Open Image', url=image_url)
                    source_button = discord.ui.Button(style=style, label='Image Source', url=source_url)
                    view.add_item(item=image_button)
                    view.add_item(item=source_button)

                    await ctx.send(embed=embed, view=view)
            
            if tag in versatile_tags:
                    await send_image()
            elif tag in nsfw_tags:
                    await send_image()
            else:
                    await ctx.send(box('Invalid tag passed. Please pass a valid tag.\n\nUse [p]waifuim help to see a list of available tags.'))

    @waifuim.command()
    async def gif(self, ctx):
            """
            Get a random waifu gif
            """
            search_endpoint = 'https://api.waifu.im/search'

            if ctx.channel.is_nsfw():
                    params = {'gif': 'true', 'is_nsfw': 'true'}
            else:
                    params = {'gif': 'true'}

            async with self.session.get(search_endpoint, params=params) as response:
                data = await response.json()

                for image in data['images']:
                        image_url = image['url']
                        image_id = image['image_id']
                        source_url = image['source']
                        uploaded_at = image['uploaded_at']

                raw = datetime.fromisoformat(uploaded_at).date().strftime("%B %d, %Y")
                date = '{}'.format(raw)
                upload_date = date

                embed = discord.Embed()
                embed.add_field(name='Image ID', value=image_id, inline=True)
                embed.add_field(name='Upload Date', value=upload_date, inline=True)
                embed.set_image(url=image_url)
                embed.set_footer(text=footer_text, icon_url=embed_icon)
                embed.color = await ctx.embed_color()
                view = discord.ui.View()
                style = discord.ButtonStyle.grey
                image_button = discord.ui.Button(style=style, label='Open Image', url=image_url)
                source_button = discord.ui.Button(style=style, label='Image Source', url=source_url)
                view.add_item(item=image_button)
                view.add_item(item=source_button)

                await ctx.send(embed=embed, view=view)
            
