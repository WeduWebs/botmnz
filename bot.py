import os
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

# ELIMINAMOS EL HELP POR DEFECTO AQUÍ
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

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
            "👤 **Dueño:** <@1462154477040701605> (Menciona solo si es urgente).\n"
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

bot.run(TOKEN)
