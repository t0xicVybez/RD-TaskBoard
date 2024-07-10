import discord
from discord import app_commands
from discord.ext import commands
import json
import os

# Bot configuration
TOKEN = 'your token'
GUILD_ID = 1111  # Replace with your server's ID
ROLE_ID = 1111  # Replace with the role ID required to use commands
CHANNEL_ID = 111  # Replace with the channel ID where the bot listens and posts
DATA_FILE = 'ChangeDataBaseName.json'

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Data structure
boards = {}

# Priority colors
PRIORITY_COLORS = {
    "high": discord.Color.red(),
    "medium": discord.Color.yellow(),
    "low": discord.Color.green()
}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(boards, f)

def load_data():
    global boards
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            boards = json.load(f)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    load_data()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

def is_authorized(interaction: discord.Interaction):
    return interaction.user.get_role(ROLE_ID) is not None and interaction.channel.id == CHANNEL_ID

# ... [other commands remain the same] ...

@bot.tree.command(name="delete_card", description="Delete a card from a list")
@app_commands.describe(board="Name of the board", list="Name of the list", card_index="Index of the card to delete (starting from 0)")
async def delete_card(interaction: discord.Interaction, board: str, list: str, card_index: int):
    if not is_authorized(interaction):
        await interaction.response.send_message(embed=discord.Embed(title="Error", description="You don't have permission to use this command.", color=discord.Color.red()), ephemeral=True)
        return
    
    if board not in boards:
        await interaction.response.send_message(embed=discord.Embed(title="Error", description=f"Board '{board}' does not exist.", color=discord.Color.red()), ephemeral=True)
    elif list not in boards[board]["lists"]:
        await interaction.response.send_message(embed=discord.Embed(title="Error", description=f"List '{list}' does not exist in board '{board}'.", color=discord.Color.red()), ephemeral=True)
    elif card_index < 0 or card_index >= len(boards[board]["lists"][list]):
        await interaction.response.send_message(embed=discord.Embed(title="Error", description=f"Invalid card index for list '{list}'.", color=discord.Color.red()), ephemeral=True)
    else:
        deleted_card = boards[board]["lists"][list].pop(card_index)
        save_data()
        embed = discord.Embed(title="Card Deleted", description=f"Card deleted from list '{list}' in board '{board}'.", color=PRIORITY_COLORS[deleted_card['priority']])
        embed.add_field(name="Title", value=deleted_card['title'], inline=False)
        embed.add_field(name="Description", value=deleted_card['description'], inline=False)
        embed.add_field(name="Priority", value=deleted_card['priority'].capitalize(), inline=False)
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Show all available commands and how to use them")
async def help_command(interaction: discord.Interaction):
    if not is_authorized(interaction):
        await interaction.response.send_message(embed=discord.Embed(title="Error", description="You don't have permission to use this command.", color=discord.Color.red()), ephemeral=True)
        return
    
    help_embed = discord.Embed(title="Available Commands", description="Here are all the available commands and how to use them:", color=discord.Color.blue())
    help_embed.add_field(name="/create_board", value="Create a new board\nUsage: `/create_board name:\"Board Name\"`", inline=False)
    help_embed.add_field(name="/create_list", value="Create a new list in a board\nUsage: `/create_list board:\"Board Name\" name:\"List Name\"`", inline=False)
    help_embed.add_field(name="/add_card", value="Add a card to a list\nUsage: `/add_card board:\"Board Name\" list:\"List Name\" title:\"Card Title\" description:\"Card Description\" priority:\"high/medium/low\"`", inline=False)
    help_embed.add_field(name="/move_card", value="Move a card from one list to another\nUsage: `/move_card board:\"Board Name\" from_list:\"Source List\" to_list:\"Destination List\" card_index:0`", inline=False)
    help_embed.add_field(name="/delete_card", value="Delete a card from a list\nUsage: `/delete_card board:\"Board Name\" list:\"List Name\" card_index:0`", inline=False)
    help_embed.add_field(name="/list_boards", value="Show all boards\nUsage: `/list_boards`", inline=False)
    help_embed.add_field(name="/list_board_content", value="Show all lists and cards in a board\nUsage: `/list_board_content board:\"Board Name\"`", inline=False)
    help_embed.add_field(name="/help", value="Show this help message\nUsage: `/help`", inline=False)
    help_embed.set_footer(text="Note: All commands can only be used in the designated channel by users with the required role.")
    
    await interaction.response.send_message(embed=help_embed)

if __name__ == '__main__':
    bot.run(TOKEN)