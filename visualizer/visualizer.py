import discord
import webcolors
from io import BytesIO
from PIL import Image
from redbot.core import app_commands, commands


class Visualizer(commands.Cog):
    """Visualizes a HEX color as an image and shows its converted values."""

    def closest_color_name(self, rgb):
        try:
            return webcolors.rgb_to_name(rgb)
        except ValueError:
            min_colors = {}
            for hex_code, name in webcolors.CSS3_HEX_TO_NAMES.items():
                r_c, g_c, b_c = webcolors.hex_to_rgb(hex_code)
                rd = (r_c - rgb[0]) ** 2
                gd = (g_c - rgb[1]) ** 2
                bd = (b_c - rgb[2]) ** 2
                min_colors[(rd + gd + bd)] = name
            return min_colors[min(min_colors.keys())]

    def rgb_to_hsl(self, rgb):
        r, g, b = [x / 255.0 for x in rgb]
        maxc = max(r, g, b)
        minc = min(r, g, b)
        l = (minc + maxc) / 2.0
        if minc == maxc:
            return (0.0, 0.0, round(l * 100))
        if l <= 0.5:
            s = (maxc - minc) / (maxc + minc)
        else:
            s = (maxc - minc) / (2.0 - maxc - minc)
        rc = (maxc - r) / (maxc - minc)
        gc = (maxc - g) / (maxc - minc)
        bc = (maxc - b) / (maxc - minc)
        if r == maxc:
            h = bc - gc
        elif g == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc
        h = (h / 6.0) % 1.0
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


    @commands.hybrid_command(name="visualize", usage="<hex>")
    @app_commands.describe(hex="The 3 or 6 digit hex value")
    async def visualize(self, ctx: commands.Context, hexcode: str):
        """Visualize a HEX color as an image.
        
        > <hex> can be 3 or 6 digit hex color. `#` is optional.
        > Also displays the color's name and its value in other formats.
        """

        hexcode = hexcode.lstrip('#')
        if len(hexcode) == 3:
            hexcode = ''.join([c * 2 for c in hexcode])

        if len(hexcode) != 6 or any(c not in '0123456789ABCDEFabcdef' for c in hexcode):
            await ctx.send("Invalid HEX code. Please provide a valid 3 or 6 digit HEX color code.")
            return

        try:
            rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
            color_name = self.closest_color_name(rgb)
            hsl = self.rgb_to_hsl(rgb)
            cmyk = self.rgb_to_cmyk(rgb)

            img = Image.new("RGB", (256, 128), rgb)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            file = discord.File(buffer, filename="color.png")
            embed = discord.Embed(
                title=f"Color Preview: #{hexcode.upper()}",
                description=(
                    f"**RGB:** `{rgb}`\n"
                    f"**HSL:** `{hsl}`\n"
                    f"**CMYK:** `{cmyk}`\n"
                    f"**Name:** `{color_name}`"
                ),
                color=int(hexcode, 16)
            )
            embed.set_image(url="attachment://color.png")
            await ctx.send(file=file, embed=embed)

        except Exception as e:
            await ctx.send(f"Something went wrong: {e}")
