from more_itertools import last


def check_valid_move(board,move):
    '''
    check if the move is valid
    
    '''
    print(board)
    if move==None:
        return False
    else:
        if board[move]!=0:
            return False
        else:
            return True

def winner(board):
    '''
    vérifie qui gagne
    '''
    return 1