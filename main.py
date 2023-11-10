#!/usr/bin/env python3
#
# The file creates and runs an instance of Connect 4.

from game.game import Game

if __name__ == "__main__":
    GAME = Game()
    GAME.create_scenes()
    GAME.run()