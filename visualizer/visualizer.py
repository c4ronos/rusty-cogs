import discord
import webcolors
import colorsys
from io import BytesIO
from PIL import Image
from redbot.core import commands, app_commands


class Visualizer(commands.Cog):
    """Visualizes a HEX color as an image and shows its converted values."""


    def closest_color_name(self, rgb):
        try:
            return webcolors.rgb_to_name(rgb, spec='css3')
        except ValueError:
            min_dist = None
            closest_name = None
            for name in webcolors.names('css3'):
                r2, g2, b2 = webcolors.name_to_rgb(name)
                dist = (r2 - rgb[0])**2 + (g2 - rgb[1])**2 + (b2 - rgb[2])**2
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    closest_name = name
            return closest_name

    def rgb_to_hsl(self, rgb):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (round(h * 360), round(s * 100), round(l * 100))

    def rgb_to_cmyk(self, rgb):
        r, g, b = [x / 255.0 for x in rgb]
        k = 1 - max(r, g, b)
        if k == 1:
            return (0, 0, 0, 100)
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        return (round(c * 100), round(m * 100), round(y * 100), round(k * 100))


    @commands.hybrid_command(name="visualize")
    @app_commands.describe(hexcode="The 3 or 6 digit hex value, with or without #.")
    async def visualize(self, ctx: commands.Context, hexcode: str):
        """Visualize a HEX color as an image.
        
        > <hexcode> can be 3 or 6 digit hex color. `#` is optional.
        > Also displays the color's name and its value in other formats.
        """

        raw = hexcode.lstrip('#')
        if len(raw) == 3:
            raw = ''.join(c * 2 for c in raw)

        if len(raw) != 6 or any(c not in '0123456789ABCDEFabcdef' for c in raw):
            return await ctx.send("Invalid HEX code. Provide 3 or 6 digit code.")

        try:
            rgb = tuple(int(raw[i:i+2], 16) for i in (0, 2, 4))
            name = self.closest_color_name(rgb)
            hsl = self.rgb_to_hsl(rgb)
            cmyk = self.rgb_to_cmyk(rgb)

            img = Image.new("RGB", (256, 128), rgb)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            file = discord.File(buffer, filename="color.png")
            embed = discord.Embed(
                title=f"Color Preview: #{raw.upper()}",
                description=(
                    f"**HEX:** `#{raw.upper()}`\n"
                    f"**RGB:** `{rgb}`\n"
                    f"**HSL:** `{hsl}`\n"
                    f"**CMYK:** `{cmyk}`\n"
                    f"**Name:** `{name}`"
                ),
                color=int(raw, 16),
            )
            embed.set_image(url="attachment://color.png")
            await ctx.send(file=file, embed=embed)

        except Exception as e:
            await ctx.send(f"Something went wrong: {e}")
