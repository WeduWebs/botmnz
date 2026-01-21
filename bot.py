import os
import io
import requests
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

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

# ================== EVENTO DE BIENVENIDA (EMBED NEGRO + GIF MNZ) ==================
@bot.event
async def on_member_join(member):
    ID_CANAL_BIENVENIDA = 1462161394324607161
    URL_GIF = "https://i.imgur.com/zpYHEFQ.gif"
    channel = member.guild.get_channel(ID_CANAL_BIENVENIDA)
    
    if channel:
        total_miembros = member.guild.member_count
        
        # Embed Negro con Título MNZ LEAKS
        embed = discord.Embed(
            title="MNZ LEAKS",
            description=f"**Bienvenida**\n\nTe damos la bienvenida a **MNZ Leaks**\n{member.mention} ya somos {total_miembros} personas en el discord",
            color=discord.Color.from_rgb(0, 0, 0) 
        )
        embed.set_image(url=URL_GIF)
        embed.set_footer(text="MNZ Leaks. | Bienvenida")
        
        await channel.send(embed=embed)

    # --- MENSAJE DIRECTO (MD) ---
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
                "• Si estás listo para mejorar tu PC, abre un ticket.\n\n"
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

# ================== VENTANA EMERGENTE (MODAL) PROFESIONAL ==================
class AnuncioModal(discord.ui.Modal, title='Redactar Anuncio Oficial'):
    texto_anuncio = discord.ui.TextInput(
        label='Contenido del anuncio',
        style=discord.TextStyle.paragraph,
        placeholder='Escribe aquí el cuerpo del mensaje...',
        required=True,
        min_length=1,
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Creamos un Embed con un diseño mucho más cuidado
        embed = discord.Embed(
            title="📢  ANUNCIO OFICIAL",
            description=f"\n{self.texto_anuncio.value}\n",
            color=discord.Color.from_rgb(0, 0, 0), # Negro elegante
            timestamp=discord.utils.utcnow()
        )

        # 1. Autor: Aparece arriba en pequeño con la foto del Admin
        embed.set_author(
            name=f"Publicado por {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url
        )

        # 2. Thumbnail: El logo del servidor en la esquina superior derecha
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)

        # 3. Footer: Más limpio y con el nombre del servidor
        embed.set_footer(
            text=f"{interaction.guild.name} • Sistema de Comunicación",
            icon_url=interaction.guild.icon.url if interaction.guild.icon else None
        )

        # Enviamos el mensaje al canal
        await interaction.channel.send(embed=embed)
        
        # Confirmación invisible para el admin
        await interaction.response.send_message("✅ El anuncio se ha publicado con formato profesional.", ephemeral=True)
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
    # Creamos un Embed con estética profesional
    embed = discord.Embed(
        title="🌐 ESTADO DE LOS SERVICIOS",
        description=(
            "A continuación se detalla la disponibilidad de nuestros servicios en tiempo real.\n"
            "Si experimentas algún problema, abre un ticket."
        ),
        color=discord.Color.from_rgb(0, 0, 0), # Negro puro
        timestamp=discord.utils.utcnow()
    )

    # Añadimos los campos de estado con mejor formato
    embed.add_field(
        name="🛠️ Optimización Windows", 
        value="> 🟢 **OPERATIVO**", 
        inline=False
    )
    embed.add_field(
        name="🎮 Soporte FiveM", 
        value="> 🟢 **OPERATIVO**", 
        inline=False
    )
    embed.add_field(
        name="🎟️ Sistema de Tickets", 
        value="> 🟢 **OPERATIVO**", 
        inline=False
    )

    # Thumbnail: El logo del servidor
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)

    # Footer profesional con logo
    embed.set_footer(
        text=f"{ctx.guild.name} • Monitorización de Red",
        icon_url=ctx.guild.icon.url if ctx.guild.icon else None
    )

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
        color=discord.Color.from_rgb(1, 1, 1),
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
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.secondary, emoji="🔒", custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo los Administradores pueden cerrar este ticket.", ephemeral=True)
            return
        await interaction.response.send_message("Cerrando ticket...", ephemeral=True)
        await interaction.channel.delete()

class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Compras", description="Abre un ticket para adquirir nuestros servicios.", emoji="<:emojidollar:1462171745917210735>", value="compra"),
            discord.SelectOption(label="Soporte / Dudas", description="Si tienes problemas técnicos o preguntas generales.", emoji="<:emojitio:1462159167920799754>", value="soporte"),
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
        
        embed_welcome = discord.Embed(
            description=("Los staffs se pondrán en contacto contigo lo antes posible, evita mencionarlos sin su permiso.\nGracias."),
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

@bot.tree.command(name="ticket", description="Muestra el panel de creación de tickets")
async def ticket(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)
        return
    embed = discord.Embed(
        title="🎫 SISTEMA DE TICKETS",
        description=("Si necesitas contactar con nosotros, selecciona la categoría que mejor se adapte a tu necesidad en el menú de abajo.\n\n**Categorías:**\n<:emojidollar:1462171745917210735> **Compras:** Para adquirir optimizaciones.\n<:emojitio:1462159167920799754> **Soporte:** Dudas técnicas o problemas."),
        color=discord.Color.from_rgb(1, 1, 1)
    )
    if interaction.guild.icon:
        embed.set_thumbnail(url=interaction.guild.icon.url)
    embed.set_footer(text="MNZ Leaks • Calidad y Rendimiento")
    await interaction.channel.send(embed=embed, view=TicketLauncher())
    await interaction.response.send_message("Panel enviado.", ephemeral=True)

@bot.command(name="munoz")
async def munoz(ctx):
    embed = discord.Embed(description="Asi se ve el colega", color=discord.Color.from_rgb(1, 1, 1))
    embed.set_image(url="https://i.imgur.com/L5e0OfQ.png")
    await ctx.send(embed=embed)
# ================== SISTEMA DE VERIFICACIÓN (BOTÓN Y ROL) ==================

class VerificacionView(discord.ui.View):
    """Clase para el botón de verificación persistente."""
    def __init__(self):
        super().__init__(timeout=None) # Importante: None hace que el botón no expire

    @discord.ui.button(
        label="Verificarse", 
        style=discord.ButtonStyle.success, 
        emoji="✅", 
        custom_id="boton_verificacion_mnz" # ID única para que el bot lo reconozca tras reiniciar
    )
    async def verificacion_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ID_ROL_VERIFICADO = 1462154710625550479
        rol = interaction.guild.get_role(ID_ROL_VERIFICADO)

        if not rol:
            await interaction.response.send_message("❌ Error: No se encuentra el rol de verificación.", ephemeral=True)
            return

        if rol in interaction.user.roles:
            await interaction.response.send_message("¡Ya estás verificado!", ephemeral=True)
        else:
            try:
                await interaction.user.add_roles(rol)
                await interaction.response.send_message("✅ Te has verificado correctamente. ¡Bienvenido a MNZ Leaks!", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("❌ No tengo permisos suficientes para darte el rol. Revisa mi jerarquía.", ephemeral=True)

# ================== COMANDO SLASH /setup-verificacion ==================

@bot.tree.command(name="setup-verificacion", description="Envía el mensaje de verificación al canal")
async def setup_verificacion(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🛡️ SISTEMA DE VERIFICACIÓN",
        description=(
            "Bienvenido a **MNZ Leaks**.\n\n"
            "Para acceder al resto de canales, por favor pulsa el botón de abajo.\n\n"
            "⚠️ **Al verificarte aceptas las normas del servidor.**"
        ),
        color=discord.Color.from_rgb(0, 0, 0) # Color Negro
    )
    
    if interaction.guild.icon:
        embed.set_thumbnail(url=interaction.guild.icon.url)
    
    embed.set_footer(text="MNZ Leaks • Verificación obligatoria")

    # Enviamos el embed con el botón
    await interaction.channel.send(embed=embed, view=VerificacionView())
    await interaction.response.send_message("✅ Panel de verificación enviado.", ephemeral=True)
    # ================== COMANDO SLASH /CLEAR (LIMPIEZA) ==================

@bot.tree.command(name="clear", description="Limpia mensajes del canal o de un usuario específico")
@app_commands.describe(
    cantidad="Número de mensajes a eliminar del canal actual",
    usuario="Usuario del cual quieres borrar todos sus mensajes recientes"
)
async def clear(interaction: discord.Interaction, cantidad: int = None, usuario: discord.Member = None):
    # Verificación de permisos de administrador
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        return

    # Caso 1: No se ha pasado ningún parámetro
    if cantidad is None and usuario is None:
        await interaction.response.send_message("⚠️ Debes especificar una `cantidad` o un `usuario`.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True) # Evita que el comando expire si tarda mucho

    # CASO A: Borrar mensajes de un usuario en todo el servidor (mensajes recientes)
    if usuario:
        deleted_total = 0
        await interaction.followup.send(f"⏳ Buscando y eliminando mensajes de {usuario.mention} en todo el servidor...", ephemeral=True)
        
        for channel in interaction.guild.text_channels:
            try:
                # Limitamos a 100 por canal para no saturar el bot, puedes subirlo si quieres
                def check(m): return m.author == usuario
                deleted = await channel.purge(limit=100, check=check)
                deleted_total += len(deleted)
            except:
                continue
        
        await interaction.followup.send(f"✅ Se han eliminado **{deleted_total}** mensajes de {usuario.mention} encontrados en el servidor.", ephemeral=True)

    # CASO B: Borrar X cantidad de mensajes en el canal actual
    elif cantidad:
        if cantidad <= 0:
            await interaction.followup.send("❌ La cantidad debe ser mayor a 0.", ephemeral=True)
            return
            
        deleted = await interaction.channel.purge(limit=cantidad)
        await interaction.followup.send(f"✅ Se han eliminado **{len(deleted)}** mensajes del canal.", ephemeral=True)
        # ================== SISTEMA DE MODERACIÓN Y ANTI-SPAM ==================

# --- 1. COMANDO /WARN ---
@bot.tree.command(name="warn", description="Añade un aviso a un usuario (3 warns = Expulsión)")
@app_commands.describe(usuario="Usuario a avisar", razon="Motivo del aviso")
async def warn(interaction: discord.Interaction, usuario: discord.Member, razon: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        return

    if usuario.guild_permissions.administrator:
        await interaction.response.send_message("❌ No puedes poner un warn a otro administrador.", ephemeral=True)
        return

    # Definir nombres de roles de warn
    nombres_warns = ["Warn 1", "Warn 2", "Warn 3"]
    roles_actuales = [r for r in usuario.roles if r.name in nombres_warns]
    proximo_warn = len(roles_actuales) + 1

    # Crear o buscar el rol necesario
    rol_obj = discord.utils.get(interaction.guild.roles, name=f"Warn {proximo_warn}")
    if not rol_obj:
        rol_obj = await interaction.guild.create_role(name=f"Warn {proximo_warn}", color=discord.Color.orange())

    # Aplicar el rol
    await usuario.add_roles(rol_obj)

    # Crear Embed de aviso
    embed = discord.Embed(
        title="⚠️ USUARIO ADVERTIDO",
        description=f"El usuario {usuario.mention} ha recibido un aviso.",
        color=discord.Color.from_rgb(255, 0, 0)
    )
    embed.add_field(name="Razón", value=razon, inline=False)
    embed.add_field(name="Aviso número", value=f"{proximo_warn} / 3", inline=True)
    embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
    embed.set_footer(text="MNZ Leaks • Moderación")

    await interaction.channel.send(embed=embed)
    await interaction.response.send_message(f"✅ Warn aplicado a {usuario.name}.", ephemeral=True)

    # Si llega a 3 warns, expulsar
    if proximo_warn >= 3:
        try:
            await usuario.send(f"Has sido expulsado de **MNZ Leaks** por acumular 3 avisos. Última razón: {razon}")
            await usuario.kick(reason="Acumulación de 3 warns")
            await interaction.channel.send(f"👢 {usuario.name} ha sido expulsado automáticamente tras recibir su tercer warn.")
        except Exception as e:
            await interaction.channel.send(f"❌ No pude expulsar a {usuario.name}: {e}")

# --- 2. EVENTO ANTI-EVERYONE / ANTI-HERE ---
@bot.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author.bot:
        return

    # Verificar si el mensaje contiene @everyone o @here
    if "@everyone" in message.content or "@here" in message.content:
        # Si NO es administrador, banear
        if not message.author.guild_permissions.administrator:
            try:
                razon_ban = "Intento de mención masiva (@everyone/@here) sin permisos."
                
                # Enviar MD al usuario antes del ban
                try:
                    await message.author.send(f"Has sido baneado de **MNZ Leaks**. Razón: {razon_ban}")
                except: pass

                await message.author.ban(reason=razon_ban, delete_message_days=1)
                
                # Avisar en el canal
                embed_ban = discord.Embed(
                    title="🚫 USUARIO BANEADO AUTOMÁTICAMENTE",
                    description=f"{message.author.mention} ha sido baneado por intentar usar menciones masivas.",
                    color=discord.Color.red()
                )
                embed_ban.add_field(name="Razón", value=razon_ban)
                await message.channel.send(embed=embed_ban)
                
                # Borrar el mensaje que causó el baneo
                await message.delete()
            except Exception as e:
                print(f"Error al banear por mención masiva: {e}")

    # IMPORTANTE: Esto permite que otros comandos !prefix sigan funcionando
    await bot.process_commands(message)
    # ================== COMANDO BROMA !PABLECHO ==================
@bot.command(name="pablecho")
async def pablecho(ctx):
    embed = discord.Embed(
        description="**El colega en cuestión:**",
        color=discord.Color.from_rgb(0, 0, 0), # Negro profesional
        timestamp=discord.utils.utcnow()
    )
    
    # Imagen de la broma
    embed.set_image(url="https://i.imgur.com/0qowNru.png")
    
    # Logo del servidor en pequeño (Thumbnail)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
        
    # Footer profesional
    embed.set_footer(
        text=f"{ctx.guild.name} • MNZ Humor", 
        icon_url=ctx.guild.icon.url if ctx.guild.icon else None
    )
    
    await ctx.send(embed=embed)
# ================== SLASH COMMAND /RENAME (SILENCIOSO Y FUNCIONAL) ==================
@bot.tree.command(name="rename", description="Cambia el nombre del canal actual de forma silenciosa")
@app_commands.describe(nombre="El nuevo nombre para este canal")
async def rename(interaction: discord.Interaction, nombre: str):
    # Verificación de permisos de administrador
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        return

    # Usamos defer con ephemeral=True para evitar el error de "La aplicación no respondió"
    # Esto le dice a Discord que el bot está procesando la solicitud.
    await interaction.response.defer(ephemeral=True)

    try:
        # Realizamos el cambio de nombre
        await interaction.channel.edit(name=nombre)
        
        # Confirmamos solo al administrador que se ha realizado con éxito
        await interaction.followup.send(f"✅ Canal renombrado a `{nombre}` con éxito.", ephemeral=True)

    except discord.Forbidden:
        await interaction.followup.send("❌ Error: No tengo permisos suficientes (revisa mi jerarquía de roles).", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Ocurrió un error inesperado: {e}", ephemeral=True)
bot.run(TOKEN)
