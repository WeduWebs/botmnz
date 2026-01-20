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

# ================== SLASH COMMAND /mensaje ==================
@bot.tree.command(name="mensaje", description="Abre un formulario para enviar un anuncio con párrafos")
async def mensaje(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)
        return
    await interaction.response.send_modal(AnuncioModal())

# ================== COMANDO !pagos ==================
@bot.command(name="pagos")
async def pagos(ctx):
    embed = discord.Embed(
        title="💳 Métodos de Pago",
        description=(
            "Aceptamos los siguientes métodos de pago:\n\n"
            "• <:l_ppal:1463190933708210328> **PayPal**\n"
            "• <:l_bzm:1463190383071592488> **Bizum**\n"
            "• <:l_btc:1463190321713250305> **Criptomonedas**\n\n"
            "Para más información, abre un ticket."
        ),
        color=discord.Color.from_rgb(1, 1, 1),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Pagos seguros y verificados")
    await ctx.send(embed=embed)

# ================== NUEVO COMANDO !reseñas ==================
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
            "4️⃣ No olvides **adjuntar una prueba** (captura de pantalla).\n\n"
            "¡Gracias por confiar en nosotros!"
        ),
        color=discord.Color.from_rgb(255, 215, 0), # Color Dorado/Oro
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Sistema de Valoraciones • MNZ Leaks")
    
    await ctx.send(embed=embed)

# ================== EJECUCIÓN ==================
bot.run(TOKEN)
