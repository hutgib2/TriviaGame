import pygame
from game.trivia_game import TriviaGame
import asyncio

async def main():
    game = TriviaGame()
    await game.run()
    
asyncio.run(main())