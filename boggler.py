"""Boggler:  Boggle game solver. CS 210, Fall 2023.
Jacob Dirkx
Credits: Myself
"""
import doctest
import config
import sys
import board_view

DICT_PATH = "06-Boggle-main/data/dict.txt"
# Boggle rules
MIN_WORD = 3   # A word must be at least 3 characters to count
# Possible search outcomes
NOPE = "Nope"       # Not a match, nor a prefix of a match
MATCH = "Match"     # Exact match to a valid word
PREFIX = "Prefix"   # Not an exact match, but a prefix (keep searching!)
# Board dimensions
N_ROWS = 4
N_COLS = N_ROWS
BOARD_SIZE = N_ROWS * N_COLS
# Special character in position that is already in use
IN_USE = "@"
#Possible points for a single word
#3-4 = 1, 5 = 2, 6 = 3, 7 = 5, 8+ = 11
POINTS = [0, 0, 0, 1, 1, 2, 3, 5, 11,
          11, 11, 11, 11, 11, 11, 11, 11 ]

def read_dict(path: str) -> list[str]:
    """Returns ordered list of valid, normalized words from dictionary.
    """
    dictlist =[]
    with open(path,"r") as dict:
        lines = dict.read().splitlines()
        for word in lines:
            if (allowed(word)) == True:
                dictlist.append(normalize(word))
    return(dictlist)

def allowed(s: str) -> bool:
    """Is s a legal Boggle word? Must be 3+ letters and only letters"""
    x = False
    if len(s) >= MIN_WORD:
        x = s.isalpha()
    return(x)
        
def normalize(s: str) -> str:
    """Canonical for strings in dictionary or on board"""
    return s.upper()

def search(candidate: str, word_list: list[str]) -> str:
    """Determine whether candidate is a MATCH, a PREFIX of a match, or a big NOPE
    Note word list MUST be in sorted order."""
    low = 0
    high = len(word_list)
    mid = (low + high)//2
    x = NOPE
    while low < high:
        mid = (low + high)//2 
        if word_list[mid] == candidate:
            x = MATCH
            break
        if word_list[mid].startswith(candidate):
            x = PREFIX
        if low == high:
            if word_list[mid] != candidate:
                break
        if word_list[mid] < candidate:
            low = mid + 1
        if word_list[mid] > candidate:
            high = mid - 1
    return x

def get_board_letters() -> str:
    """Get a valid string to form a Boggle board
    from the user.  May produce diagnostic
    output and quit."""
    while True:
        board_string = input("Boggle board letters (or 'return' to exit)> ")
        if allowed(board_string) and len(board_string) == config.BOARD_SIZE:
            return board_string
        elif len(board_string) == 0:
            print(f"OK, sorry it didn't work out")
            sys.exit(0)
        else:
            print(f'"{board_string}" is not a valid Boggle board')
            print(f'Please enter exactly {config.BOARD_SIZE} letters (or empty to quit)')
        return normalize(board_string)


def unpack_board(letters: str, rows=config.N_ROWS) -> list[list[str]]:
    """Unpack a single string of characters into
    a square matrix of individual characters, N_ROWS x N_ROWS.
    """
    board = []
    x = 0
    for i in range(rows):
        board.append([])
        while len(board[i]) < 4 and x < len(letters):
            board[i].append(letters[x])
            x += 1
    return board


def boggle_solve(board: list[list[str]], words: list[str]) -> list[str]:
    """Find all the words that can be made by traversing
    the boggle board in all 8 directions.  Returns sorted list without
    duplicates.
    """
    solutions = []

    def solve(row: int, col: int, prefix: str):
        """Recurssive function to find and append words"""
        if row < config.N_ROWS and row >= 0:
            if col < config.N_COLS and col >= 0:
                letter = board[row][col]
                if letter != IN_USE:
                    prefix = prefix + letter
                    status = search(prefix, words)
                    board[row][col] = IN_USE  # Prevent reusing
                    board_view.mark_occupied(row, col)
                    if status == MATCH: 
                        solutions.append(prefix)
                        board_view.celebrate(prefix)
                    if status == PREFIX or status == MATCH:
                        for d_row in [0, -1, 1]:
                            for d_col in [0, -1, 1]:
                                solve(row+d_row,col+d_col,prefix)
                    board[row][col] = letter
                    board_view.mark_unoccupied(row, col)


    # Look for solutions starting from each board position
    for row_i in range(config.N_ROWS):
        for col_i in range(config.N_COLS):
            solve(row_i, col_i, "")

    # Return solutions without duplicates, in sorted order
    solutions = list(set(solutions))
    return sorted(solutions)

def word_score(word: str) -> int:
    """Standard point value in Boggle"""
    assert len(word) <= 16
    return POINTS[len(word)]

def score(solutions: list[str]) -> int:
    """Sum of scores for each solution"""
    score = 0
    for word in solutions:
        score = score + word_score(word)
    return score

def test_it():
    """A little extra work to keep text display from
    interfering with doctests.
    """
    saved_flag = config.TEXT_VIEW
    config.TEXT_VIEW = False
    doctest.testmod(verbose=True)
    config.TEXT_VIEW = saved_flag


def main():
    words = read_dict(DICT_PATH)
    board_string = get_board_letters()
    board_string = normalize(board_string)
    board = unpack_board(board_string)
    board_view.display(board)
    solutions = boggle_solve(board, words)
    print(solutions)
    print(f"{score(solutions)} points")
    board_view.prompt_to_close()
    
if __name__ == "__main__":
    test_it()
    main()
