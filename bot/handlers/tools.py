import os
import random

from aiohttp import ClientSession


class Tools:


    
    @staticmethod
    def api(endpoint: str):
        base_api = "https://discord.com/api/v10/"
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]

        return base_api+endpoint 

    @staticmethod
    def chunker(text, chunk_size: int) -> list:
        length = len(text)
        num = 0
        chunks = []

        while num < len(text):
            chunks.append(text[num:length-(length-(chunk_size))+num:])
            num+=chunk_size

        return chunks
    
    # @staticmethod
    # def information(guild_id: str, token: str):
    #     url = Tools.api("users/@me")
    #     headers = {"Authorization": "Bot %s" % token}

    #     user = req.get(url, headers=headers)

    #     url = Tools.api(f"/guilds/{guild_id}")
    #     guild = req.get(url, headers=headers)


    #     info_dict = {
    #         "user": user.json(),
    #         "guild": guild.json()
    #     }
    #     return info_dict


    @staticmethod
    async def send_message(token: str, channel: int, message: str):
        try:
            url = Tools.api(f"channels/{channel}/messages")

            headers = {"Authorization": "Bot %s" % token}

            payload = {
                "content": message
            }


            async with ClientSession() as session:
                async with session.post(url, json=payload, 
                                        headers=headers) as resp:
                    
                    return resp.status == 200

            
        except: return False

    