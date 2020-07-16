import numpy as np
import pygame
import sys
import math
import tkinter as tk
# pylint: disable=no-member

SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
RADIUS = int(SQUARESIZE/2 - 3)
EMPTY_SLOT = 0


def create_board():
    global row_count
    global column_count
    board = np.zeros((int(row_count), int(column_count)))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[int(row_count)-1][col] == 0


def get_next_open_row(board, col):
    for r in range(int(row_count)):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    for r in range(int(row_count)):
        for c in range(int(column_count)):
            if board[r][c] != EMPTY_SLOT and board[r][c] == piece:
                if c + 3 < int(column_count) and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True
                if r + 3 < int(row_count):
                    if board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                        return True
                    if (c + 3) < int(column_count) and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                        return True
                    if (c - 3) >= 0 and board[r+1][c-1] == piece and board[r+2][c-2] == piece and board[r+3][c-3] == piece:
                        return True
    return False


def draw_board(board, screen, guiHeight):
    for c in range(int(column_count)):
        for r in range(int(row_count)):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)
                                            * SQUARESIZE, SQUARESIZE, SQUARESIZE))

            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+(SQUARESIZE/2)), int(((r) * SQUARESIZE)+SQUARESIZE+(SQUARESIZE/2))), RADIUS)
    for c in range(int(column_count)):
        for r in range(int(row_count)):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARESIZE+(SQUARESIZE/2)), guiHeight - int((r * SQUARESIZE)+(SQUARESIZE/2))), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARESIZE+(SQUARESIZE/2)), guiHeight - int((r * SQUARESIZE)+(SQUARESIZE/2))), RADIUS)
    pygame.display.update()


def quit(startMenu):
    global game_over
    game_over = True
    startMenu.destroy()


def start(startMenu, numOfRows, numOfColumns):
    global row_count
    global column_count
    row_count = numOfRows.get()
    column_count = numOfColumns.get()
    startMenu.destroy()


def main():
    global row_count
    row_count = 6
    global column_count
    column_count = 7
    global game_over
    game_over = False
    startMenu = tk.Tk()
    tk.Label(startMenu, text="Number of Rows").pack()

    numOfRows = tk.Entry(startMenu)
    numOfRows.focus_force()
    numOfRows.pack()

    tk.Label(startMenu, text="Number of Columns").pack()

    numOfColumns = tk.Entry(startMenu)
    numOfColumns.pack()

    playBtn = tk.Button(startMenu, text='Play',
                        command=lambda: start(startMenu, numOfRows, numOfColumns))
    playBtn.config(width=20)
    playBtn.pack(pady=8)
    startMenu.bind("<Return>", lambda event: start(
        startMenu, numOfRows, numOfColumns))
    quitBtn = tk.Button(startMenu, text='Quit',
                        command=lambda: quit(startMenu))
    quitBtn.config(width=20)
    quitBtn.pack()
    size = tuple(int(_) for _ in startMenu.geometry().split('+')[0].split('x'))
    x = int(startMenu.winfo_screenwidth()) / 2 - size[0] / 2
    y = int(startMenu.winfo_screenheight()) / 2 - size[1] / 2
    startMenu.geometry("220x200+%d+%d" % (x - 110, y - 110))
    startMenu.title("Connect 4 Game")
    startMenu.wm_attributes('-toolwindow', 1)
    startMenu.protocol('WM_DELETE_WINDOW', None)
    startMenu.resizable(False, False)
    startMenu.mainloop()

    if not game_over:
        board = create_board()
        turn = 0

        pygame.init()
        pygame.display.set_caption("Connect 4 Game - Player 1's Turn")
        guiWidth = int(column_count) * SQUARESIZE
        guiHeight = (int(row_count)+1) * SQUARESIZE

        size = (guiWidth, guiHeight)
        screen = pygame.display.set_mode(size)
        draw_board(board, screen, guiHeight)
        pygame.display.update()
        myfont = pygame.font.SysFont("Arial", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, guiWidth, SQUARESIZE))
                posX = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(
                        screen, RED, (posX, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(
                        screen, YELLOW, (posX, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, guiWidth, SQUARESIZE))

                # Ask for Player 1 Input

                if turn == 0:
                    posX = event.pos[0]
                    col = int(math.floor(posX/SQUARESIZE))
                    next_turn = is_valid_location(board, col)
                    if next_turn:
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            print_board(board)
                            label = myfont.render("Player 1 Wins!!", 1, RED)
                            screen.blit(
                                label, (round((guiWidth/2) - len("Player 1 Wins!!")*12), round(10)))
                            game_over = True
                # # Ask for Player 2 Input
                else:
                    posX = event.pos[0]
                    col = int(math.floor(posX/SQUARESIZE))
                    next_turn = is_valid_location(board, col)
                    if next_turn:
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            print_board(board)
                            label = myfont.render("Player 2 Wins!!", 1, YELLOW)
                            screen.blit(
                                label, ((guiWidth/2) - len("Player 2 Wins!!")*12, 10))
                            game_over = True
                print_board(board)
                draw_board(board, screen, guiHeight)
                if next_turn:
                    turn += 1
                    turn = turn % 2
                    titleString = "Connect 4 Game - Player " + \
                        str(turn+1) + "'s Turn"
                    pygame.display.set_caption(titleString)

                if game_over:
                    titleString = "Connect 4 Game - Player " + \
                        str((turn+1) % 2+1) + " Wins"
                    pygame.display.set_caption(titleString)
                    pygame.time.wait(3500)


if __name__ == '__main__':
    main()
