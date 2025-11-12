# Lostey Reply BOT 🤖

A Discord bot that intelligently detects mentions of "Badlion" and responds contextually based on account availability.

## 📋 Description

**Lostey Reply BOT** is a Discord bot designed to monitor server conversations for mentions of "Badlion" (in both English and Arabic: "بادليون"). The bot provides dynamic responses based on:

- **Account Availability**: Checks if accounts are available or claimed
- **Context Detection**: Recognizes whether users are asking about "room" or "channel"
- **Smart DM Handling**: Automatically falls back to sending messages in the first available text channel if DMs are disabled
- **Bilingual Support**: Works with both English and Arabic text

### Key Features

✨ **Bilingual Detection**: Recognizes "badlion" and "بادليون"
🔍 **Context-Aware**: Detects "room"/"روم" and "channel"/"قناة"
💬 **Smart Messaging**: Adapts responses based on account status and context
📍 **Fallback Support**: Handles disabled DMs by posting in available channels
🌍 **Multi-Language Support**: Full Arabic and English support

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Discord.py library (v2.0+)
- python-dotenv for environment variable management

### Setup

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd Lostey_Reply_BOT
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root:

   Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

   Or create manually:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   EMPTY=False
   ```

   - `DISCORD_TOKEN`: Your Discord bot token (get it from [Discord Developer Portal](https://discord.com/developers/applications))
   - `EMPTY`: Set to `True` if all Badlion accounts are claimed, `False` if some are available

4. **Invite the bot to your server**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your bot application
   - Go to OAuth2 → URL Generator
   - Select scopes: `bot` and `applications.commands`
   - Select permissions: `Send Messages`, `Read Message History`, `Mention @everyone`
   - Copy the generated URL and open it in your browser

## 🚀 Usage

Run the bot:
```bash
python bot.py
```

The bot will automatically:
1. Listen for messages containing "badlion" or "بادليون"
2. Check account availability based on the `EMPTY` environment variable
3. Respond with appropriate messages
4. Handle DM availability and fall back to channels if needed

### Slash Commands

The bot provides two slash commands (use `/` to trigger):

- **`/status`** — Check the current account availability status (works for everyone)
- **`/toggle-empty`** — Toggle account availability on/off (admins only)

## 📦 Dependencies

- **discord.py**: Discord API wrapper
- **python-dotenv**: Environment variable management

See `requirements.txt` for all dependencies.

## ⚙️ Configuration

### Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DISCORD_TOKEN` | string | required | Your Discord bot token |
| `EMPTY` | boolean | False | Whether all accounts are claimed |

### Message Patterns

The bot detects the following patterns (case-insensitive, Unicode-aware):

- **Badlion**: `badlion` or `بادليون`
- **Room**: `room` or `روم`
- **Channel**: `channel` or `قناة`

## 👤 Author

- **3bdoabk** © 2025

## 📄 License

Please check the repository for license information.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Made with ❤️ by 3bdoabk**
