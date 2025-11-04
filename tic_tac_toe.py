# tic_tac_toe.py
import random

def print_board(b):
    print()
    for i in range(3):
        print(" " + " | ".join(b[i*3:(i+1)*3]))
        if i < 2:
            print("---+---+---")
    print()

def check_winner(board, mark):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    return any(all(board[i]==mark for i in triple) for triple in wins)

def board_full(board):
    return all(cell != " " for cell in board)

def player_move(board):
    while True:
        try:
            pos = int(input("Enter position (1-9): ").strip())
            if pos < 1 or pos > 9:
                print("Choose 1 through 9.")
                continue
            if board[pos-1] != " ":
                print("Cell already taken. Choose another.")
                continue
            board[pos-1] = "X"
            break
        except ValueError:
            print("Enter a number 1-9.")

def computer_move(board):
    avail = [i for i,c in enumerate(board) if c == " "]
    pos = random.choice(avail)
    board[pos] = "O"
    print(f"Computer placed O in position {pos+1}.")

def play_game():
    print("Tic-Tac-Toe: You = X, Computer = O")
    board = [" "] * 9
    print_board(board)

    while True:
        player_move(board)
        print_board(board)
        if check_winner(board, "X"):
            print("Congratulations — you win! 🎉")
            break
        if board_full(board):
            print("It's a draw.")
            break

        computer_move(board)
        print_board(board)
        if check_winner(board, "O"):
            print("Computer wins. Better luck next time!")
            break
        if board_full(board):
            print("It's a draw.")
            break

if __name__ == "__main__":
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break
