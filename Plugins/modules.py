import base64
import datetime
import os
import random
import time
from threading import Thread

import disnake
import requests as req
from disnake.ext import commands, tasks

from bot.handlers.tools import Nuking, Tools
from bot.utils.functions import *

MAIN_COLOR = disnake.Color.from_rgb(47, 49, 54)
COMMANDS_CHANNEL = 1195455328603619358