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
