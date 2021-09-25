import asyncio
import os
import uuid
from datetime import datetime

import qrcode

FILE_PATH = './api/static/qr-code-'


class TokensStorage:
    # todo make self.__tokens dict
    def __init__(self):
        self.__tokens = []
        self.__delay = 15

    @staticmethod
    def __generate_token():
        """[Generates unique token for qrcode]

        Returns:
            [str]: [Unique token]
        """
        return str(uuid.uuid4())

    def generate_qrcode(self, data: str):
        """[Generates QR-code .png image]

        Args:
            data (str): [Text data for QR-code]

        Returns:
            [str]: [Unique QR-code token]
        """
        try:
            token = self.__generate_token()
            filename = FILE_PATH + token + '.png'
            # generate qr code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=0,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#0d1117", back_color="white")
            # save qr code to file
            img.save(filename)
            self.__add(token)
            return token

        except Exception as e:
            print('Error:', e)

    def __add(self, token: str):
        """[Adds QR-code token with current time (in seconds) into storage]

        Args:
            token (str): [Unique QR-code token]
        """
        seconds = datetime.today().timestamp()
        self.__tokens.append((token, seconds))

    def __delete(self, index: int):
        """[Deletes QR-code image by index of token]

        Args:
            index (int): [Index of QR-code token]
        """
        try:
            os.remove(FILE_PATH + f'{self.__tokens[index][0]}.png')
            del self.__tokens[index]

        except Exception as e:
            print('Error:',  e)

    async def find_and_delete(self, token: str):
        """[Finds QR-code by token and deletes it with delay]

        Args:
            token (str): [Unique QR-code token]
        """
        await asyncio.sleep(self.__delay)
        for ind, item in enumerate(self.__tokens):
            if item[0] == token:
                self.__delete(ind)
                break
