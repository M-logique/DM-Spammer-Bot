from discord import AllowedMentions, Intents

from bot.core.client import Client

if __name__ == "__main__":
    client = Client(
        intents=Intents.all(),
        allowed_mentions=AllowedMentions.none()
    )
    
    client.run()

# comment