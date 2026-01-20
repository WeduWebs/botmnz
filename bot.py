import discord
from discord.ext import commands
from discord import app_commands

TOKEN = "MTQ2MzE2NzQ5OTI4NDc3OTA4MA.GjkgOw.Ma3vwLgIPBSjJruTsXlrss08FWDobkl-x23QpU"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)


# SLASH COMMAND /mensaje (solo administradores)
@bot.tree.command(name="mensaje", description="Envía un mensaje profesional")
@app_commands.describe(texto="El mensaje que quieres enviar")
async def mensaje(interaction: discord.Interaction, texto: str):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ No tienes permisos para usar este comando.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📢 Anuncio Importante",
        description=texto,
        color=discord.Color.blue()
    )

    embed.set_footer(text="Equipo de Administración")
    embed.set_timestamp()

    await interaction.response.send_message(embed=embed)


# COMANDO !pagos
@bot.command()
async def pagos(ctx):

    embed = discord.Embed(
        title="💳 Métodos de Pago",
        description=(
            "Aceptamos los siguientes métodos de pago:\n\n"
            "• **PayPal**\n"
            "• **Bizum**\n"
            "• **Criptomonedas**\n\n"
        ),
        color=discord.Color.green()
    )

    embed.set_footer(text="Pagos seguros y verificados")

    await ctx.send(embed=embed)


bot.run(TOKEN)
