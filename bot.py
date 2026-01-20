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
@bot.tree.command(name="mensaje", description="Envía un anuncio profesional")
@app_commands.describe(texto="Contenido del mensaje")
async def mensaje(interaction: discord.Interaction, texto: str):
    # Evita el error de "La aplicación no responde"
    await interaction.response.defer(ephemeral=True)

    if not interaction.user.guild_permissions.administrator:
        await interaction.followup.send("❌ No tienes permisos.", ephemeral=True)
        return

    embed = discord.Embed(
        title="📢 ANUNCIO OFICIAL",
        description=texto,
        color=discord.Color.from_rgb(180, 0, 0),
        timestamp=discord.utils.utcnow() # CORRECCIÓN AQUÍ
    )
    embed.set_footer(text="Equipo de Administración")

    await interaction.channel.send(embed=embed)
    await interaction.followup.send("✅ Enviado.")

# ================== COMANDO !pagos ==================
@bot.command(name="pagos")
async def pagos(ctx):
    embed = discord.Embed(
        title="💳 Métodos de Pago",
        description=(
            "Aceptamos los siguientes métodos de pago:\n\n"
            "• <:l_ppal:1463190933708210328>  **PayPal**\n"
            "• <:l_bzm:1463190383071592488>  **Bizum**\n"
            "• <:l_btc:1463190321713250305>  **Criptomonedas**\n\n"
            "Para más información, abre un ticket."
        ),
        color=discord.Color.from_rgb(1, 1, 1),
        timestamp=discord.utils.utcnow() # CORRECCIÓN AQUÍ
    )
    embed.set_footer(text="Pagos seguros y verificados")
    
    await ctx.send(embed=embed)

bot.run(TOKEN)
