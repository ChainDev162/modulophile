# Moderation Bot

A Discord moderation bot built using `discord.py` with features to assist in managing servers. This bot provides essential moderation tools such as muting, banning, warning, and purging messages. Additionally, it is designed with ease of customization in mind.

## Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ChainDev162/moderationbot.git
   cd moderationbot
   ```

2. **Install Required Dependencies**
   Make sure you have Python 3.8 or later installed. Then, install dependencies:
   ```bash
   pip install discord --break-system-packages
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory and add the following:
   ```env
   TOKEN=your_discord_token
   ```

4. **Run the Bot**
   Once everything is set up, you can run the bot with:
   ```bash
   python main.py
   ```

## Getting familiar with the codebase

This project is fairly simple to get started with. The main logic is contained within the `main.py` file. The bot's functionality is divided into several files (aka cogs) in `commands_` for better organization and maintainability.

## Contributing

Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open-source and available under the [MIT License](LICENSE).

