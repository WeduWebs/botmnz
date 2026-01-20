import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# ================== CONFIG ==================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("❌ No se encontró la variable de entorno DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================== READY ==================
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

# ================== /mensaje ==================
@bot.tree.command(name="mensaje", description="Envía un anuncio profesional")
@app_commands.describe(texto="Contenido del mensaje")
async def mensaje(interaction: discord.Interaction, texto: str):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ No tienes permisos para usar este comando.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📢 ANUNCIO OFICIAL",
        description=texto,
        color=discord.Color.from_rgb(180, 0, 0)  # ROJO
    )

    embed.set_footer(text="Equipo de Administración • Mensaje oficial")
    embed.set_timestamp()

    await interaction.response.send_message(embed=embed)

# ================== !pagos ==================
@bot.command()
async def pagos(ctx):

    embed = discord.Embed(
        title="💳 Métodos de Pago",
        description=(
            "Aceptamos los siguientes métodos de pago:\n\n"
            "• <:I_paypal:1089104791453569106> **PayPal**\n"
            "• <:bizum2:1322968080460156970> **Bizum**\n"
            "• <:I_bank:1089229057167740998> **Transferencia bancaria**\n"
            "• <:logoscryptosbitcoin:1431600912539058186> **Criptomonedas**\n\n"
            "Para más información, abre un ticket."
        ),
        color=discord.Color.from_rgb(0, 0, 0)  # NEGRO
    )

    embed.set_footer(text="Pagos seguros y verificados")
    embed.set_timestamp()

    await ctx.send(embed=embed)

# ================== RUN ==================
bot.run(TOKEN)
