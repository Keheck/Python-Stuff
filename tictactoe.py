board: list[list[bool]] = [[None] * 3] * 3


def win_condition() -> tuple[bool, int]:
    # vertical and horizontal
    for i in range(3):
        if (board[i][0] is not None and board[i][0] == board[i][1] == board[i][2]) or (board[0][i] is not None and board[0][i] == board[1][i] == board[2][i]):
            return (True, 1 if board[i])