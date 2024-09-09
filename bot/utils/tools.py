import sys
from ctypes import CDLL, c_char_p

spammer = CDLL("./shared/spammer.so") if not sys.platform.startswith('win') else CDLL("./shared/spammer.dll")
spammer.SendDirectMessages.argtypes = [c_char_p, c_char_p]
spammer.SendChannelMessages.argtypes = [c_char_p, c_char_p, c_char_p]


from threading import Thread


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

        Thread(target=spammer.SendDirectMessages, args=(user_id, message)).start()

    @staticmethod
    def send_channel_message(channel_ids: str, message: str, user_id: int,/):
        """Will send direct messages to a user using the C-shared extension"""

        content = f'<@{user_id}>'.encode()
        message = str(message).encode()
        channel_ids = channel_ids.encode()

        Thread(target=spammer.SendChannelMessages, args=(channel_ids, message, content)).start()