import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime

# ================== CONFIG ==================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1462154477040701605

if not TOKEN:
    raise ValueError("❌ No se encontró la variable de entorno DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
        synced = await bot.tree.sync(guild=guild)
        print(f"✨ Comandos sincronizados: {len(synced)}")
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
            "✅ **Sin recortes de funciones:** Optimizamos el Sistema Operativo al completo sin quitar ninguna funcionalidad de Windows.\n\n"
            "📈 **FPS de Infarto:** Aumenta tus FPS de forma drástica (¡hasta **+200 FPS**) y elimina tirones.\n\n"
            "🛡️ **100% Seguro:** Sin Overclock y a prueba de cualquier Anticheat o SS (Napse, etc.).\n\n"
            "💎 **Calidad/Precio:** Contamos con el **precio más bajo** del sector."
        ),
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(
        name="📊 Mira los Resultados",
        value="[Haz clic aquí para ver pruebas reales](https://discord.com/channels/1462154477040701605/1462235098198970611)",
        inline=False
    )
    await ctx.send(embed=embed)

# ================== COMANDO !pagos ==================
@bot.command(name="pagos")
async def pagos(ctx):
    embed = discord.Embed(
        title="💳 Métodos de Pago",
        description=(
            "Escribe el comando para ver los datos de envío:\n\n"
            "• <:l_ppal:1463190933708210328> **PayPal** -> `!paypal` \n"
            "• <:l_bzm:1463190383071592488> **Bizum** -> `!bizum` \n"
            "• <:l_btc:1463190321713250305> **Criptomonedas** -> `!crypto` "
        ),
        color=discord.Color.from_rgb(1, 1, 1),
        timestamp=discord.utils.utcnow()
    )
    await ctx.send(embed=embed)

@bot.command(name="paypal")
async def paypal(ctx):
    embed = discord.Embed(title="PayPal", description="**Correo:** `fmunozfdez@gmail.com` \n**F&F**", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command(name="bizum")
async def bizum(ctx):
    embed = discord.Embed(title="Bizum", description="**Número:** `+34 609 55 07 14` \n**Sin concepto**", color=discord.Color.from_rgb(31, 191, 179))
    await ctx.send(embed=embed)

@bot.command(name="crypto")
async def crypto(ctx):
    embed = discord.Embed(title="Crypto", description="Contacte con soporte para info.", color=discord.Color.orange())
    await ctx.send(embed=embed)

# ================== COMANDO !reseñas ==================
@bot.command(name="reseñas")
async def reseñas(ctx):
    embed = discord.Embed(
        title="⭐ DEJA TU VALORACIÓN",
        description="1️⃣ **/vouch**\n2️⃣ **5 estrellas**\n3️⃣ **Antes/Después**\n4️⃣ **Captura de prueba**",
        color=discord.Color.from_rgb(255, 215, 0),
        timestamp=discord.utils.utcnow()
    )
    await ctx.send(embed=embed)

bot.run(TOKEN)
