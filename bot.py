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

# ELIMINAMOS EL HELP POR DEFECTO AQUÍ
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ================== EVENTO DE BIENVENIDA OPTIMIZADO ==================
@bot.event
async def on_member_join(member):
    # IDs y URLs originales
    ID_CANAL_BIENVENIDA = 1462161394324607161
    URL_FONDO = "https://i.imgur.com/eB2c79T.png"
    channel = member.guild.get_channel(ID_CANAL_BIENVENIDA)
    
    if channel:
        try:
            # 1. Descargar el fondo con un User-Agent para evitar bloqueos
            headers = {"User-Agent": "Mozilla/5.0"}
            resp_fondo = requests.get(URL_FONDO, headers=headers, timeout=10)
            fondo = Image.open(io.BytesIO(resp_fondo.content)).convert("RGBA")
            
            # 2. Descargar el avatar del usuario
            avatar_url = member.display_avatar.with_format("png").url
            resp_avatar = requests.get(avatar_url, headers=headers, timeout=10)
            avatar_img = Image.open(io.BytesIO(resp_avatar.content)).convert("RGBA")
            
            # 3. Crear el círculo para el avatar
            size = (280, 280)
            avatar_img = avatar_img.resize(size, Image.LANCZOS)
            
            mask = Image.new('L', size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0) + size, fill=255)
            
            # Crear imagen transparente para el avatar circular
            circular_avatar = Image.new('RGBA', size, (0, 0, 0, 0))
            circular_avatar.paste(avatar_img, (0, 0), mask)

            # 4. Posicionar el avatar en el centro del fondo
            # Ajustamos un poco hacia arriba para dejar espacio al texto
            pos_x = (fondo.width // 2) - (size[0] // 2)
            pos_y = (fondo.height // 2) - (size[1] // 2) - 50 
            fondo.paste(circular_avatar, (pos_x, pos_y), circular_avatar)

            # 5. Escribir el texto (con control de errores de fuente)
            draw = ImageDraw.Draw(fondo)
            try:
                # Intentamos cargar una fuente básica. Si Railway no la tiene, usará la default
                font = ImageFont.load_default()
            except:
                font = None

            texto_bienvenida = f"BIENVENIDO/A {member.name.upper()}"
            
            if font:
                # Calculamos el centro del texto
                w = draw.textlength(texto_bienvenida, font=font)
                draw.text(((fondo.width - w) // 2, pos_y + size[1] + 40), texto_bienvenida, fill="white", font=font)

            # 6. Preparar el archivo para enviar
            with io.BytesIO() as img_bin:
                fondo.save(img_bin, format='PNG')
                img_bin.seek(0)
                discord_file = discord.File(fp=img_bin, filename=f'bienvenida_{member.id}.png')
                
                # Enviar imagen personalizada
                await channel.send(
                    content=f"¡Bienvenido/a {member.mention}! Pásate por <#1462235098198970611> para ver lo que hacemos.", 
                    file=discord_file
                )
        
        except Exception as e:
            # Si algo falla en el proceso de Pillow, enviamos la bienvenida normal para no dejar al usuario sin saludo
            print(f"Error generando imagen personalizada: {e}")
            await channel.send(f"¡Bienvenido/a {member.mention} a MNZ Leaks! Pásate por <#1462235098198970611>.")

    # --- EL MD SE MANTIENE IGUAL PORQUE DICES QUE FUNCIONA BIEN ---
    try:
        embed_md = discord.Embed(
            title="🚀 ¡Bienvenido a MNZ Leaks!",
            description=(
                f"Hola **{member.name}**, es un placer tenerte con nosotros.\n\n"
                "En **MNZ Leaks** nos especializamos en llevar tu rendimiento al límite. "
                "Si estás cansado de los tirones en FiveM o quieres ganar esos FPS extra para competir, "
                "estás en el lugar adecuado.\n\n"
                "**¿Qué puedes hacer ahora?**\n"
                "• Mira nuestros resultados en el canal de pruebas.\n"
                "• Usa `!opti` en el servidor para ver qué ofrecemos.\n"
                "• Si estás listo para mejorar tu PC, abre un ticket con `/ticket`.\n\n"
                "Cualquier duda, el staff estará encantado de ayudarte."
            ),
            color=discord.Color.from_rgb(1, 1, 1)
        )
        embed_md.set_footer(text="MNZ Leaks • Calidad y Rendimiento garantizado")
        if member.guild.icon:
            embed_md.set_thumbnail(url=member.guild.icon.url)
        await member.send(embed=embed_md)
    except:
        pass

# ================== VENTANA EMERGENTE (MODAL) ==================
class AnuncioModal(discord.ui.Modal, title='Redactar Anuncio Oficial'):
    texto_anuncio = discord.ui.TextInput(
        label='Contenido del anuncio',
        style=discord.TextStyle.paragraph,
        placeholder='Escribe aquí tu anuncio... Puedes usar la tecla Enter para separar párrafos.',
        required=True,
        min_length=1,
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
        await interaction.response.send_message("✅ Anuncio publicado con éxito.", ephemeral=True)

# ================== READY ==================
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print(f"✨ Comandos sincronizados correctamente.")
    except Exception as e:
        print(f"❌ Error en sincronización: {e}")

# ================== COMANDOS DE INFORMACIÓN Y AYUDA ==================

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="📚 Menú de Comandos - MNZ Leaks",
        description="Aquí tienes la lista de comandos disponibles para obtener ayuda e información:",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="🚀 `!opti`", value="Información detallada sobre la optimización.", inline=True)
    embed.add_field(name="💳 `!pagos`", value="Métodos de pago aceptados.", inline=True)
    embed.add_field(name="⭐ `!reseñas`", value="Cómo dejar tu valoración correctamente.", inline=True)
    embed.add_field(name="🟢 `!status`", value="Estado de los servicios de optimización.", inline=True)
    embed.add_field(name="📞 `!contacto`", value="Vías de contacto directo con soporte.", inline=True)
    
    embed.set_footer(text="MNZ Leaks • Calidad y Rendimiento")
    await ctx.send(embed=embed)

@bot.command(name="status")
async def status(ctx):
    embed = discord.Embed(
        title="🌐 Estado de los Servicios",
        description="Verifica la disponibilidad de nuestros servicios en tiempo real:",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="🛠️ Optimización Windows", value="🟢 **OPERATIVO**", inline=False)
    embed.add_field(name="🎮 Soporte FiveM", value="🟢 **OPERATIVO**", inline=False)
    embed.add_field(name="🎟️ Sistema de Tickets", value="🟢 **OPERATIVO**", inline=False)
    
    embed.set_footer(text="Última actualización")
    await ctx.send(embed=embed)

@bot.command(name="contacto")
async def contacto(ctx):
    embed = discord.Embed(
        title="📞 Contacto Directo",
        description=(
            "¿Tienes dudas antes de comprar? ¿Necesitas soporte técnico?\n\n"
            "📩 **Tickets:** Abre un ticket en el canal correspondiente.\n"
            "👤 **Dueño:** <@703511537809096705> o <@481118936583110675> (Menciona solo si es urgente).\n"
            "⏰ **Horario:** Respondemos lo más rápido posible (09:00 - 22:00 CET)."
        ),
        color=discord.Color.purple(),
        timestamp=discord.utils.utcnow()
    )
    await ctx.send(embed=embed)

# ================== SLASH COMMAND /mensaje (MODAL) ==================
@bot.tree.command(name="mensaje", description="Abre un formulario para enviar un anuncio oficial")
async def mensaje(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando administrativo.", ephemeral=True)
        return
    await interaction.response.send_modal(AnuncioModal())

# ================== COMANDO !opti ==================
@bot.command(name="opti")
async def opti(ctx):
    embed = discord.Embed(
        title="🚀 OPTIMIZACIÓN MNZ LEAKS",
        description=(
            "Lleva tu PC al siguiente nivel con la optimización más completa y segura del mercado.\n\n"
            "✅ **Sin recortes de funciones:** Optimizamos el Sistema Operativo al completo sin quitar ninguna funcionalidad de Windows, a diferencia de otras optimizaciones.\n\n"
            "⚡ **Rendimiento Máximo:** Eliminamos todos los ajustes que limitan tu ordenador y ralentizan tu sistema.\n\n"
            "📈 **FPS de Infarto:** Aumenta tus FPS de forma drástica (¡hasta **+200 FPS** en algunos casos!) y elimina esas caídas que arruinan tu jugabilidad.\n\n"
            "🎮 **FiveM & Más:** Diseñada específicamente para FiveM, pero ideal para cualquier juego competitivo.\n\n"
            "🛡️ **100% Seguro:** Sin Overclock y a prueba de cualquier Anticheat o SS (Napse, etc.). No tendrás ningún problema.\n\n"
            "💻 **Universal:** Sirve para cualquier PC con cualquier componente.\n\n"
            "💎 **Calidad/Precio:** Contamos con el **precio más bajo** garantizado para una optimización de este nivel."
        ),
        color=discord.Color.from_rgb(1, 1, 1), # COLOR NEGRO AJUSTADO
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="📊 Mira los Resultados",
        value="[Haz clic aquí para ver pruebas reales](https://discord.com/channels/1462154477040701605/1462235098198970611)",
        inline=False
    )
    
    embed.set_footer(text="MNZ Leaks • Calidad y Rendimiento")
    await ctx.send(embed=embed)

# ================== COMANDO !pagos ==================
@bot.command(name="pagos")
async def pagos(ctx):
    embed = discord.Embed(
        title="💳 Métodos de Pago",
        description=(
            "Aceptamos los siguientes métodos de pago. Para ver los datos de envío, usa el comando correspondiente:\n\n"
            "• <:l_ppal:1463190933708210328> **PayPal** -> Escribe `!paypal` \n"
            "• <:l_bzm:1463190383071592488> **Bizum** -> Escribe `!bizum` \n"
            "• <:l_btc:1463190321713250305> **Criptomonedas** -> Escribe `!crypto` \n\n"
            "Para más información, abre un ticket."
        ),
        color=discord.Color.from_rgb(1, 1, 1),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Pagos seguros y verificados")
    await ctx.send(embed=embed)

@bot.command(name="paypal")
async def paypal(ctx):
    embed = discord.Embed(
        title="<:l_ppal:1463190933708210328> Información de PayPal",
        description="**Paypal:** `fmunozfdez@gmail.com` \n**Modalidad:** Family & Friends",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name="bizum")
async def bizum(ctx):
    embed = discord.Embed(
        title="<:l_bzm:1463190383071592488> Información de Bizum",
        description="**Bizum:** `+34 609 55 07 14` \n**Concepto:** Sin concepto",
        color=discord.Color.from_rgb(31, 191, 179)
    )
    await ctx.send(embed=embed)

@bot.command(name="crypto")
async def crypto(ctx):
    embed = discord.Embed(
        title="<:l_btc:1463190321713250305> Información de Cripto",
        description="Contacte con soporte para más información.",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

# ================== COMANDO !reseñas ==================
@bot.command(name="reseñas")
async def reseñas(ctx):
    embed = discord.Embed(
        title="⭐ DEJA TU VALORACIÓN",
        description=(
            "Tu opinión es muy importante para nosotros. Si has utilizado nuestro servicio, "
            "por favor deja una reseña siguiendo estos pasos:\n\n"
            "1️⃣ Usa el comando **/vouch**.\n"
            "2️⃣ Selecciona una valoración de **5 estrellas** (⭐⭐⭐⭐⭐).\n"
            "3️⃣ Cuéntanos tu experiencia (el **antes y después** del servicio).\n"
            "4️⃣ No olvides **adjuntar una prueba** (captura de pantalla)."
        ),
        color=discord.Color.from_rgb(255, 215, 0),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Sistema de Valoraciones • MNZ Leaks")
    await ctx.send(embed=embed)

# ================== SISTEMA DE TICKETS PROFESIONAL MNZ ==================

class TicketControlView(discord.ui.View):
    """Vista con botón de cierre restringido a Administradores."""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.secondary, emoji="🔒", custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # VERIFICACIÓN DE SEGURIDAD: Solo admins pueden cerrar
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo los Administradores pueden cerrar este ticket.", ephemeral=True)
            return

        await interaction.response.send_message("Cerrando ticket...", ephemeral=True)
        await interaction.channel.delete()

class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Comprar Optimización", 
                description="Abre un ticket para adquirir nuestros servicios.",
                emoji="<:emojidollar:1462171745917210735>", 
                value="compra"
            ),
            discord.SelectOption(
                label="Soporte / Dudas", 
                description="Si tienes problemas técnicos o preguntas generales.",
                emoji="<:emojitio:1462159167920799754>", 
                value="soporte"
            ),
        ]
        super().__init__(placeholder="Selecciona una categoría...", min_values=1, max_values=1, options=options, custom_id="ticket_select")

    async def callback(self, interaction: discord.Interaction):
        ID_ROL_STAFF = 1462155140059365643
        ID_CAT_COMPRA = 1462161096013250791
        ID_CAT_SOPORTE = 1462161017068064889

        guild = interaction.guild
        staff_role = guild.get_role(ID_ROL_STAFF)
        
        if self.values[0] == "compra":
            category = guild.get_channel(ID_CAT_COMPRA)
            ticket_name = f"🛒-{interaction.user.name}"
        else:
            category = guild.get_channel(ID_CAT_SOPORTE)
            ticket_name = f"🛠️-{interaction.user.name}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
            staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True)
        }

        channel = await guild.create_text_channel(name=ticket_name, category=category, overwrites=overwrites)
        
        # DISEÑO ESTILO IMAGEN CON FOOTER Y THUMBNAIL
        embed_welcome = discord.Embed(
            description=(
                "Los staffs se pondrán en contacto contigo lo antes posible, evita mencionarlos sin su permiso.\n"
                "Gracias."
            ),
            color=discord.Color.from_rgb(1, 1, 1)
        )
        
        if interaction.guild.icon:
            embed_welcome.set_thumbnail(url=interaction.guild.icon.url)
            embed_welcome.set_author(name="MNZ Leaks", icon_url=interaction.guild.icon.url)
            
        embed_welcome.set_footer(text="MNZ Leaks • Soporte Profesional")
        
        await channel.send(content=f"{interaction.user.mention} <@&{ID_ROL_STAFF}>", embed=embed_welcome, view=TicketControlView())
        await interaction.response.send_message(f"✅ Ticket abierto en {channel.mention}", ephemeral=True)

class TicketLauncher(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())

# COMANDO SLASH /TICKET
@bot.tree.command(name="ticket", description="Muestra el panel de creación de tickets")
async def ticket(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🎫 SISTEMA DE TICKETS",
        description=(
            "Si necesitas contactar con nosotros, selecciona la categoría que mejor se adapte a tu necesidad en el menú de abajo.\n\n"
            "**Categorías:**\n"
            "<:emojidollar:1462171745917210735> **Compras:** Para adquirir optimizaciones.\n"
            "<:emojitio:1462159167920799754> **Soporte:** Dudas técnicas o problemas."
        ),
        color=discord.Color.from_rgb(1, 1, 1)
    )
    
    if interaction.guild.icon:
        embed.set_thumbnail(url=interaction.guild.icon.url)
    
    embed.set_footer(text="MNZ Leaks • Calidad y Rendimiento")
    
    await interaction.channel.send(embed=embed, view=TicketLauncher())
    await interaction.response.send_message("Panel enviado.", ephemeral=True)

# COMANDO BROMA !MUNOZ
@bot.command(name="munoz")
async def munoz(ctx):
    embed = discord.Embed(
        description="Asi se ve el colega",
        color=discord.Color.from_rgb(1, 1, 1)
    )
    embed.set_image(url="https://i.imgur.com/L5e0OfQ.png")
    await ctx.send(embed=embed)

bot.run(TOKEN)
