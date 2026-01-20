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
    # Cuadro de texto de estilo párrafo para permitir saltos de línea (Enter)
    texto_anuncio = discord.ui.TextInput(
        label='Contenido del anuncio',
        style=discord.TextStyle.paragraph,
        placeholder='Escribe aquí tu anuncio... Puedes usar la tecla Enter para separar párrafos.',
        required=True,
        min_length=1,
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Creamos el embed con el contenido del cuadro de texto
        embed = discord.Embed(
            title="📢 ANUNCIO OFICIAL",
            description=self.texto_anuncio.value,
            color=discord.Color.from_rgb(180, 0, 0),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Equipo de Administración • Mensaje oficial")
        
        # Enviamos el anuncio al canal donde se usó el comando
        await interaction.channel.send(embed=embed)
        # Respondemos al usuario de forma privada para confirmar
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
    # Verificación de administrador
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        return

    # Llamamos a la ventana emergente definida arriba
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

# ================== EJECUCIÓN ==================
bot.run(TOKEN)
