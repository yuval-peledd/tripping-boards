'''
This file is a part of My-PyChess application.
In this file, we manage the chess gameplay for multiplayer section of this
application.
'''
import asyncio
import time

from chess.externalinputcontroller import ExternalInputController
from chess.lib import *

# Define event handler for external input controller

def ceildiv(a, b):
    return -(a // -b)

# run main code for chess
async def main(win, mode, timer, load, movestr=""):
    start(win, load)

    moves = movestr.split()

    side, board, flags = convertMoves(moves)
    clock = pygame.time.Clock()
    sel = prevsel = [0, 0]

    if timer is not None:
        timer = list(timer)
    while True:
        looptime = getTime()
        clock.tick(25)

        timedelta = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starttime = getTime()
                if prompt(win):
                    return 0
                timedelta += getTime() - starttime
            elif event.type == ExternalInputController.CUSTOM_EVENT_ID:
                print("Custom event ID received. Command is " + str(event.command))
                normalized_command = int(event.command) + 1
                x = normalized_command % 8
                y = ceildiv(normalized_command, 8)
                if isOccupied(side, board, [x, y]):
                    sound.play_click(load)

                prevsel = sel
                sel = [x, y]

                if isValidMove(side, board, flags, prevsel, sel):
                    starttime = getTime()
                    promote = getPromote(win, side, board, prevsel, sel)
                    animate(win, side, board, prevsel, sel, load)

                    timedelta += getTime() - starttime
                    timer = updateTimer(side, mode, timer)

                    side, board, flags = makeMove(
                        side, board, prevsel, sel, flags, promote)
                    if isChecked(side, board):
                        sound.play_check(load)
                    moves.append(encode(prevsel, sel, promote))


            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Remove comment to return the close game button
                # if 460 < x < 500 and 0 < y < 50:
                #     starttime = getTime()
                #     if prompt(win):
                #         return 1
                #     timedelta += getTime() - starttime

                if 50 < x < 450 and 50 < y < 450:
                    x, y = x // 50, y // 50
                    if load["flip"] and side:
                        x, y = 9 - x, 9 - y

                    if isOccupied(side, board, [x, y]):
                        sound.play_click(load)

                    prevsel = sel
                    sel = [x, y]

                    if isValidMove(side, board, flags, prevsel, sel):
                        starttime = getTime()
                        promote = getPromote(win, side, board, prevsel, sel)
                        animate(win, side, board, prevsel, sel, load)

                        timedelta += getTime() - starttime
                        timer = updateTimer(side, mode, timer)

                        side, board, flags = makeMove(
                            side, board, prevsel, sel, flags, promote)
                        if isChecked(side, board):
                            sound.play_check(load)
                        moves.append(encode(prevsel, sel, promote))

                # Remove comment to return undo and save buttons
                # else:
                #     sel = [0, 0]
                #     if 350 < x < 500 and 460 < y < 490:
                #         starttime = getTime()
                #         if prompt(win, saveGame(moves, mode=mode, timer=timer)):
                #             return 1
                #         timedelta += getTime() - starttime
                #
                #     elif 0 < x < 80 and 0 < y < 50 and load["allow_undo"]:
                #         moves = undo(moves)
                #         side, board, flags = convertMoves(moves)

        gameDone = showScreen(win, side, board, flags, sel, load)
        timer = showClock(win, side, mode, timer, looptime, timedelta)
        await asyncio.sleep(1)

        if gameDone:
            return True
