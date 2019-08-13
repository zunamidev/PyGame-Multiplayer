import os
from assets.game import multiplayer


def join():
    os.system('python3 assets/socket/Client.py  Game-54')
    multiplayer.multiplayer()