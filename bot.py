import os
import io
import requests
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# ================== CONFIG ==================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1462154477040701605

if not TOKEN:
    raise ValueError("❌ No se encontró la variable de entorno DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ================== EVENTO DE BIENVENIDA (PILLOW + MD) ==================
@bot.event
async def on_member_join(member):
    # --- 1. CONFIGURACIÓN ---
    ID_CANAL_BIENVENIDA = 1462161394324607161
    URL_FONDO = "https://i.imgur.com/eB2c79T.png"
    channel = member.guild.get_channel(ID_CANAL_BIENVENIDA)
    
    # --- 2. GENERACIÓN DE IMAGEN PERSONALIZADA ---
    if channel:
        try:
            # Descargar fondo
            response_fondo = requests.get(URL_FONDO)
            fondo = Image.open(io.BytesIO(response_fondo.content)).convert("RGBA")
            
            # Descargar avatar del usuario
            avatar_url = member.display_avatar.url
            response_avatar = requests.get(avatar_url)
            avatar = Image.open(io.BytesIO(response_avatar.content)).convert("RGBA")
            
            # Hacer el avatar circular
            size = (280, 280)
            avatar = avatar.resize(size, Image.LANCZOS)
            mask = Image.new('L', size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0) + size, fill=255)
            
            output_avatar = Image.new('RGBA', size, (0, 0, 0, 0))
            output_avatar.paste(avatar, (0, 0), mask)

            # Pegar avatar en el centro
            pos_x = (fondo.width // 2) - (size[0] // 2)
            pos_y = (fondo.height // 2) - (size[1] // 2) - 40
            fondo.paste(output_avatar, (pos_x, pos_y), output_avatar)

            # Añadir texto
            draw = ImageDraw.Draw(fondo)
            # Intentamos usar una fuente estándar de sistema, si no la básica
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()

            texto1 = f"BIENVENIDO/A {member.name.upper()}"
            texto2 = "GRACIAS POR UNIRTE A MNZ LEAKS"

            # Centrar textos
            w1 = draw.textlength(texto1, font=font)
            draw.text(((fondo.width - w1) // 2, pos_y + size[1] + 30), texto1, fill="white", font=font)
            
            w2 = draw.textlength(texto2, font=font)
            draw.text(((fondo.width - w2) // 2, pos_y + size[1] + 80), texto2, fill="white", font=font)

            # Enviar al canal
            with io.BytesIO() as img_bin:
                fondo.save(img_bin, 'PNG')
                img_bin.seek(0)
                file = discord.File(fp=img_bin, filename='welcome.png')
                await channel.send(content=f"¡Bienvenido/a {member.mention}! Mira nuestros servicios en <#1462235098198970611>", file=file)
        
        except Exception as e:
            print(f"Error en imagen de bienvenida: {e}")
            await channel.send(f"¡Bienvenido/a {member.mention} a MNZ Leaks!")

    # --- 3. MENSAJE DIRECTO (MD) ---
    try:
        embed_md = discord.Embed(
            title="🚀 ¡Bienvenido a MNZ Leaks!",
            description=(
                f"Hola **{member.name}**, es un placer tenerte aquí.\n\n"
                "En **MNZ Leaks** somos expertos en optimización de PC y FiveM. "
                "Nuestra meta es que juegues con el máximo rendimiento y los mejores FPS del mercado.\n\n"
                "**¿Por dónde empezar?**\n"
                "• Revisa `!opti` para conocer nuestras ventajas.\n"
                "• Mira las pruebas reales en el servidor.\n"
                "• Si quieres mejorar tu PC hoy mismo, abre un ticket con `/ticket`.\n\n"
                "Estamos a tu disposición para cualquier duda."
            ),
            color=discord.Color.from_rgb(1, 1, 1)
        )
        embed_md.set_footer(text="MNZ Leaks • Calidad y Rendimiento")
        if member.guild.icon:
            embed_md.set_thumbnail(url=member.guild.icon.url)
            
        await member.send(embed=embed_md)
    except:
        pass # El usuario tiene MDs cerrados

# ================== VENTANA EMERGENTE (MODAL) ==================
class AnuncioModal(discord.ui.Modal, title='Redactar Anuncio Oficial'):
    texto_anuncio = discord.ui.TextInput(
        label='Contenido del anuncio',
        style=discord.TextStyle.paragraph,
        placeholder='Escribe aquí tu anuncio...',
        required=True,
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📢 ANUNCIO OFICIAL",
            description=self.texto_anuncio.value,
            color=discord.Color.from_rgb(180, 0, 0),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Equipo de Administración • Mensaje oficial")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ Anuncio publicado.", ephemeral=True)

# ================== READY ==================
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print(f"✨ Comandos sincronizados.")
    except Exception as e:
        print(f"❌ Error: {e}")

# ================== COMANDOS AYUDA ==================
@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="📚 Menú de Comandos - MNZ Leaks",
        description="Lista de comandos disponibles:",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="🚀 `!opti`", value="Optimización.", inline=True)
    embed.add_field(name="💳 `!pagos`", value="Métodos de pago.", inline=True)
    embed.add_field(name="⭐ `!reseñas`", value="Valoraciones.", inline=True)
    embed.set_footer(text="MNZ Leaks")
    await ctx.send(embed=embed)

@bot.command(name="status")
async def status(ctx):
    embed = discord.Embed(
        title="🌐 Estado de los Servicios",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="🛠️ Optimización", value="🟢 **OPERATIVO**", inline=False)
    embed.add_field(name="🎮 Soporte FiveM", value="🟢 **OPERATIVO**", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="contacto")
async def contacto(ctx):
    embed = discord.Embed(
        title="📞 Contacto Directo",
        description="📩 **Tickets:** Abre un ticket.\n👤 **Dueños:** <@703511537809096705> o <@481118936583110675>",
        color=discord.Color.purple(),
        timestamp=discord.utils.utcnow()
    )
    await ctx.send(embed=embed)

@bot.tree.command(name="mensaje", description="Enviar anuncio oficial")
async def mensaje(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Sin permisos.", ephemeral=True)
        return
    await interaction.response.send_modal(AnuncioModal())

@bot.command(name="opti")
async def opti(ctx):
    embed = discord.Embed(
        title="🚀 OPTIMIZACIÓN MNZ LEAKS",
        description="Lleva tu PC al siguiente nivel con la optimización más completa y segura.\n\n📈 **FPS de Infarto:** +200 FPS en algunos casos.\n🛡️ **100% Seguro:** Sin Overclock y anti-SS.",
        color=discord.Color.from_rgb(1, 1, 1),
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="📊 Resultados", value="[Ver pruebas](https://discord.com/channels/1462154477040701605/1462235098198970611)")
    await ctx.send(embed=embed)

@bot.command(name="pagos")
async def pagos(ctx):
    embed = discord.Embed(
        title="💳 Métodos de Pago",
        description="• PayPal `!paypal` \n• Bizum `!bizum` \n• Cripto `!crypto` ",
        color=discord.Color.from_rgb(1, 1, 1)
    )
    await ctx.send(embed=embed)

@bot.command(name="paypal")
async def paypal(ctx):
    embed = discord.Embed(title="PayPal", description="`fmunozfdez@gmail.com` (Amigos/Familia)", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command(name="bizum")
async def bizum(ctx):
    embed = discord.Embed(title="Bizum", description="`+34 609 55 07 14`", color=discord.Color.from_rgb(31, 191, 179))
    await ctx.send(embed=embed)

@bot.command(name="crypto")
async def crypto(ctx):
    await ctx.send("Contacte con soporte para crypto.")

@bot.command(name="reseñas")
async def reseñas(ctx):
    embed = discord.Embed(title="⭐ VALORACIÓN", description="1️⃣ `/vouch` \n2️⃣ 5 estrellas \n3️⃣ Tu experiencia.", color=discord.Color.from_rgb(255, 215, 0))
    await ctx.send(embed=embed)

# ================== TICKETS ==================
class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Close", style=discord.ButtonStyle.secondary, emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo Admins.", ephemeral=True)
            return
        await interaction.channel.delete()

class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Compra", emoji="<:emojidollar:1462171745917210735>", value="compra"),
            discord.SelectOption(label="Soporte", emoji="<:emojitio:1462159167920799754>", value="soporte"),
        ]
        super().__init__(placeholder="Categoría...", options=options)

    async def callback(self, interaction: discord.Interaction):
        ID_STAFF = 1462155140059365643
        guild = interaction.guild
        cat_id = 1462161096013250791 if self.values[0] == "compra" else 1462161017068064889
        category = guild.get_channel(cat_id)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.get_role(ID_STAFF): discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        
        ch = await guild.create_text_channel(name=f"{self.values[0]}-{interaction.user.name}", category=category, overwrites=overwrites)
        embed = discord.Embed(description="Staff contactará contigo pronto.", color=discord.Color.from_rgb(1, 1, 1))
        embed.set_footer(text="MNZ Leaks")
        if guild.icon: embed.set_thumbnail(url=guild.icon.url)
        
        await ch.send(content=f"{interaction.user.mention} <@&{ID_STAFF}>", embed=embed, view=TicketControlView())
        await interaction.response.send_message(f"Ticket en {ch.mention}", ephemeral=True)

class TicketLauncher(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())

@bot.tree.command(name="ticket")
async def ticket(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator: return
    embed = discord.Embed(title="🎫 TICKETS", description="Selecciona categoría abajo.", color=discord.Color.from_rgb(1, 1, 1))
    await interaction.channel.send(embed=embed, view=TicketLauncher())
    await interaction.response.send_message("Panel enviado.", ephemeral=True)

@bot.command(name="munoz")
async def munoz(ctx):
    embed = discord.Embed(description="Asi se ve el colega", color=discord.Color.from_rgb(1, 1, 1))
    embed.set_image(url="https://i.imgur.com/L5e0OfQ.png")
    await ctx.send(embed=embed)

bot.run(TOKEN)
