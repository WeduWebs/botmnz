import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# ================== CONFIG ==================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# Asegúrate de que el ID sea un INT, no un STRING
GUILD_ID = 1462154477040701605  

if not TOKEN:
    raise ValueError("❌ No se encontró la variable de entorno DISCORD_TOKEN")

# Intents: ¡MUY IMPORTANTE ACTIVARLOS EN EL PORTAL DE DISCORD!
intents = discord.Intents.default()
intents.message_content = True  # Necesario para !pagos
intents.members = True          # Recomendado

bot = commands.Bot(command_prefix="!", intents=intents)

# ================== READY ==================
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    
    # Sincronización mejorada
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"✨ Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"❌ Error sincronizando comandos: {e}")

# ================== SLASH COMMAND /mensaje ==================
@bot.tree.command(name="mensaje", description="Envía un anuncio profesional")
@app_commands.describe(texto="Contenido del mensaje")
async def mensaje(interaction: discord.Interaction, texto: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ No tienes permisos para usar este comando.", ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📢 ANUNCIO OFICIAL",
        description=texto,
        color=discord.Color.from_rgb(180, 0, 0)
    )
    embed.set_footer(text="Equipo de Administración • Mensaje oficial")
    embed.set_timestamp()

    await interaction.response.send_message(embed=embed)

# ================== COMANDO !pagos ==================
@bot.command(name="pagos")
async def pagos(ctx):
    embed = discord.Embed(
        title="💳 Métodos de Pago",
        description=(
            "Aceptamos los siguientes métodos de pago:\n\n"
            "• **PayPal**\n" # Asegúrate que los IDs de emoji son correctos
            "• **Bizum**\n"
            "• **Transferencia bancaria**\n"
            "• **Criptomonedas**\n\n"
            "Para más información, abre un ticket."
        ),
        color=discord.Color.from_rgb(1, 1, 1) # El negro puro (0,0,0) a veces falla, usa (1,1,1)
    )
    embed.set_footer(text="Pagos seguros y verificados")
    embed.set_timestamp()
    await ctx.send(embed=embed)

# ================== RUN ==================
bot.run(TOKEN)
