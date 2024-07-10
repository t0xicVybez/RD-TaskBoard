# RD-Taskboard

RD-Taskboard is a Discord bot for Kanban-style task management within your server. Organize projects with boards, lists, and cards.

## Features

- **Boards**: Create and manage multiple project boards
- **Lists**: Organize tasks into customizable lists (e.g., "To Do", "In Progress", "Done")
- **Cards**: Add, move, and delete task cards with priorities (high, medium, low)
- **Authorization**: Restrict bot usage to specific roles and channels
- **Data Persistence**: Save all data to a JSON file

## Commands

- `/create_board <name>`: Create a new board
- `/create_list <board> <name>`: Create a new list in a board
- `/add_card <board> <list> <title> <description> <priority>`: Add a card to a list
- `/move_card <board> <from_list> <to_list> <card_index>`: Move a card between lists
- `/delete_card <board> <list> <card_index>`: Delete a card from a list
- `/list_boards`: Show all boards
- `/list_board_content <board>`: Show all lists and cards in a board
- `/help`: Display all commands and usage

## Setup

1. Create a Discord Bot:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" tab and click "Add Bot"
   - Under "Token", click "Copy" to get your bot token
   - In the "OAuth2" tab, under "Scopes", select "bot" and "applications.commands"
   - Under "Bot Permissions", select necessary permissions (e.g., Read Messages/View Channels, Send Messages, Manage Messages)
   - Use the generated URL to invite the bot to your server

2. Clone the repository:
   ```
   git clone https://github.com/t0xicVybez/RD-TaskBoard.git
   cd RD-Taskboard
   ```

3. Install dependencies:
   ```
   pip install discord.py==2.3.2
   ```

4. Configure the bot:
   Edit `rd_taskboard/taskbot.py`:
   ```python
   TOKEN = 'your_bot_token_here'
   GUILD_ID = your_server_id_here
   ROLE_ID = role_id_for_bot_usage
   CHANNEL_ID = channel_id_for_bot_commands
   DATA_FILE = 'taskboard_data.json'
   ```

5. Run the bot:
   ```
   python taskbot.py
   ```

## Usage

1. Ensure you have the required role in the specified channel
2. Use slash commands to manage your tasks and projects
3. View board content to get an overview of your project status

## Contributing

Contributions welcome! Please submit a Pull Request.

## License

This project is licensed under the MIT License.
