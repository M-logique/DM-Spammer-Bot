import os
import random
from ctypes import CDLL, c_char_p


spammer = CDLL("./shared/spammer.so")
spammer.SendDirectMessages.argtypes = [c_char_p, c_char_p]



class Tools:



    @staticmethod
    def chunker(text, chunk_size: int) -> list:
        length = len(text)
        num = 0
        chunks = []

        while num < length:
            chunks.append(text[num:length-(length-(chunk_size))+num:])
            num+=chunk_size

        return chunks
    

    @staticmethod
    def send_direct_message(user_id: int, message: str, /):
        """Will send direct messages to a user using the C-shared extension"""

        user_id = str(user_id).encode()
        message = message.encode()

        spammer.SendDirectMessages(user_id, message)