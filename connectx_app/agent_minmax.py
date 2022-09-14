import numpy as np
import random #6.35
class saved_hash():
  def __init__(self,flag,value):
    self.flag = flag
    self.value = value


def ordering_moves(valid_moves,position,mask):
  oppo = position ^ mask
  final_valid_moves = []
  for col in valid_moves:
    child_position, child_mask = make_move(position, mask, col)
    nb_of_threes = connected_three(child_position, child_position ^ child_mask, False)
    final_valid_moves.append([nb_of_threes,col])
  
  final_valid_moves.sort(reverse=True)
  return [move[1] for move in final_valid_moves]

def pvs(position, mask, depth, color, alpha, beta):
  alpha_original = alpha
  ordered = [3,2,4,1,5,0,6]
  is_terminal = bool(check_four_aligned(position) + check_four_aligned(position ^ mask))
  valid_moves = [i for i in ordered if not (mask >> (i*7+5)) & 1]
  #hash_position = hash((position,mask,position ^ mask))

  # if hash_position in seen:
  #   stored = seen[hash_position]
  #   if stored.flag == 'EXACT':
  #     return seen[hash_position].value
  #   elif stored.flag == 'LOWERB':
  #     alpha = max(alpha, stored.value)
  #   elif stored.flag == 'UpperBB':
  #     beta = min(beta, stored.value)
    
  #   if alpha >= beta:
  #     return stored.value
    
  if depth == 0 or is_terminal:
      return color * get_euristic(position, mask, depth) 
  #value = -np.Inf
  for col in valid_moves:
    if color == -1:
      child_position, child_mask = make_move(position ^ mask, mask, col)
      child_position = child_position ^ child_mask
    else:
      child_position, child_mask = make_move(position, mask, col)

    if col == valid_moves[0]:
      value = -pvs(child_position, child_mask, depth-1, -color, -beta, -alpha)
    else:
      value = -pvs(child_position, child_mask, depth-1, -color, -alpha - 1, -alpha)
      if alpha < value < beta:
        value = -pvs(child_position, child_mask, depth-1, -color, -beta, -value)
    alpha = max(alpha, value)

    if alpha >= beta:
      break
  

  # if value <= alpha_original:
  #   flag = 'UPPERB'
  # elif value >= beta:
  #   flag = 'LowerB'
  # else:
  #   flag = 'EXACT'

  # seen[hash_position] = saved_hash(flag,value)
  return alpha

def negmax(position, mask, depth, color):
  ordered = [3,2,4,1,5,0,6]
  is_terminal = bool(check_four_aligned(position) + check_four_aligned(position ^ mask))
  valid_moves = [i for i in ordered if not (mask >> (i*7+5)) & 1]
  
  if depth == 0 or is_terminal:
      return color * get_euristic(position, mask, depth) 
  value = -np.Inf
  for col in valid_moves:
    if color == -1:
      child_position, child_mask = make_move(position ^ mask, mask, col)
      child_position = child_position ^ child_mask
    else:
      child_position, child_mask = make_move(position, mask, col)

    value = max(value, -negmax(child_position, child_mask, depth-1, -color)) 
  return value

def negmax_pruning(position, mask, depth, color, alpha, beta):
  alpha_original = alpha
  ordered = [3,2,4,1,5,0,6]
  is_terminal = bool(check_four_aligned(position) + check_four_aligned(position ^ mask))
  valid_moves = [i for i in ordered if not (mask >> (i*7+5)) & 1]
  hash_position = hash((position,mask,position ^ mask))

  if hash_position in seen:
    stored = seen[hash_position]
    if stored.flag == 'EXACT':
      return seen[hash_position].value
    elif stored.flag == 'LOWERB':
      alpha = max(alpha, stored.value)
    elif stored.flag == 'UpperBB':
      beta = min(beta, stored.value)
    
    if alpha >= beta:
      return stored.value
    
  if depth == 0 or is_terminal:
      return color * get_euristic(position, mask, depth) 
  value = -np.Inf
  for col in valid_moves:
    if color == -1:
      child_position, child_mask = make_move(position ^ mask, mask, col)
      child_position = child_position ^ child_mask
    else:
      child_position, child_mask = make_move(position, mask, col)

    value = max(value, -negmax_pruning(child_position, child_mask, depth-1, -color, -beta, -alpha)) 
    alpha = max(alpha,value)
    if alpha >= beta or alpha > 90000000:
      break
  

  if value <= alpha_original:
    flag = 'UPPERB'
  elif value >= beta:
    flag = 'LowerB'
  else:
    flag = 'EXACT'

  seen[hash_position] = saved_hash(flag,value)
  return value


def make_move(position, mask, col):
  new_oppo = position ^ mask
  new_mask = mask | (mask + (1 << (col*7)))
  new_position = new_oppo ^ new_mask
  return new_position, new_mask

def score_move(grid,mask, col, depth):
  
  new_position, new_mask = make_move(grid, mask, col)
  score = minimax(new_position, new_mask, depth, False, -np.Inf, np.Inf )
  #score = get_euristic(new_position, new_mask)
  return score

def score_move_negmax(grid,mask, col, depth):
  
  new_position, new_mask = make_move(grid, mask, col)
  score = -negmax_pruning(new_position, new_mask, depth, -1, -np.Inf, np.Inf)
  #score = get_euristic(new_position, new_mask)
  return score

def score_move_pvs(grid,mask, col, depth):
  
  new_position, new_mask = make_move(grid, mask, col)
  score = -pvs(new_position, new_mask, depth, False, -np.Inf, np.Inf )
  #score = get_euristic(new_position, new_mask)
  return score


#check the alignement of 3 dangerous consecutive peeble in one direction
def Check_3_alligned(position, oppo, code):
  #import random
  #import numpy as np
  #horizontal check : code = nb line + 1
  #vertical check : code = 1
  #diagonal / check : code = nb line + 2
  #diagonal \ check : code = nb line
  check = position & (position >> code)
  check = check & (check >> code)
  check = check >> code
  comparator = check & oppo
  check = check - comparator
  final_check = check

  check = position & (position >> code)
  check = position & (check >> code * 2)
  check = check << code
  comparator = check & (oppo | position)
  check = check - comparator
  final_check = final_check | check
  
  check = position & (position << code)
  check = check & (check << code)
  check = check << code
  comparator = check & oppo
  check = check - comparator
  final_check = final_check | check

  check = position & (position << code)
  check = position & (check << code * 2)
  check = check >> code
  comparator = check & (oppo | position)
  check = check - comparator
  final_check = final_check | check

  return final_check

#check the alignement of 3 dangerous consecutive peeble in all directions for all player
def connected_three(position,oppo, check_oppo = True):   
  check = Check_3_alligned(position, oppo, 7)
  check = check | Check_3_alligned(position, oppo, 1)
  check = check | Check_3_alligned(position, oppo, 6)
  check = check | Check_3_alligned(position, oppo, 8)
  # print(make_board(check)) 
  # print("check connected 3")
  if check_oppo:
    check_oppo = Check_3_alligned(oppo, position, 7)
    check_oppo = check_oppo | Check_3_alligned(oppo, position, 1)
    check_oppo = check_oppo | Check_3_alligned(oppo, position, 6)
    check_oppo = check_oppo | Check_3_alligned(oppo, position, 8)
  # print(make_board(check)) 
  # print("check connected 4")
    return [count_set_bits(check),count_set_bits(check_oppo)]


  return count_set_bits(check)

#check the alignement of 3 dangerous consecutive peeble in one direction
def Check_2_alligned(position, oppo, code):
  #horizontal check : code = nb line + 1
  #vertical check : code = 1
  #diagonal / check : code = nb line + 2
  #diagonal \ check : code = nb line
  number_of_two = [0, 0]
  check1 = position & (position >> code)
  check1 = check1 >> code
  comparator = check1 & oppo
  check1 = check1 - comparator
  count_set_bits(check1)
  
  check2 = position & (position << code)
  check2 = check2 << code
  comparator = check2 & oppo
  check2 = check2 - comparator
  return check2 | check1

#check the alignement of 2 dangerous consecutive peeble in all directions for all player
def connected_two(position,oppo):
  

  check = Check_2_alligned(position, oppo, 7)
  check = check | Check_2_alligned(position, oppo, 1)
  check = check | Check_2_alligned(position, oppo, 6)
  check = check | Check_2_alligned(position, oppo, 8)

  check_oppo = Check_2_alligned(oppo, position, 7)
  check_oppo = check_oppo | Check_2_alligned(oppo, position, 1)
  check_oppo = check_oppo | Check_2_alligned(oppo, position, 6)
  check_oppo = check_oppo | Check_2_alligned(oppo, position, 8)

  return [count_set_bits(check),count_set_bits(check_oppo)]

def check_four_aligned(position):
  # Horizontal check
  m = position & (position >> 7)
  if m & (m >> 14):
      return 1
  # Diagonal \
  m = position & (position >> 6)
  if m & (m >> 12):
      return 1
  # Diagonal /
  m = position & (position >> 8)
  if m & (m >> 16):
      return 1
  # Vertical
  m = position & (position >> 1)
  if m & (m >> 2):
      return 1
  # Nothing found
  return 0

def get_euristic(position, mask, depth):
  oppo = position ^ mask
  number_of_3 = connected_three(position,oppo)
  number_of_2 = connected_two(position,oppo)
  number_of_4 = [check_four_aligned(position),check_four_aligned(oppo)]
  euristic = number_of_3[0] * 100 - number_of_3[1] * 100 + (number_of_4[0] * 100000000 * (depth +1)) - (number_of_4[1] * 100000000 * (depth +1))
  #return number_of_2
  return euristic


#count nb on bits set to 1 (except the top most row)
def count_set_bits(check):
        count = 0
        check = check & int('0111111011111101111110111111011111101111110111111',2)
        while (check): 
            count += check & 1
            check >>= 1
        return count 

def make_board(position, mask):
  position = str(bin(position))
  mask = str(bin(mask))
  board = np.zeros((7,7))
  for col in range(0, 7, 1):
    for row in range(6, -1, -1):
        if position[-1] == "1":
          i = 1
        elif mask[-1] == "1":
          i = 2
        else:
          i = 0
        board[row,col] = i
        if position[-2] == 'b':
          position = position[:-1]
          position = position + "00"

        if mask[-2] == 'b':
          mask = mask[:-1]
          mask = mask + "00"

        position = position[:-1]
        mask = mask[:-1]
  return board

          
def get_position_mask_bitmap(board, player):
  position, mask = '', ''
  # Start with right-most column
  for j in range(6, -1, -1):
      # Add 0-bits to sentinel 
      mask += '0'
      position += '0'
      # Start with bottom row
      for i in range(0, 6):
          mask += ['0', '1'][board[i, j] != 0]
          position += ['0', '1'][board[i, j] == player]
  return int(position, 2), int(mask, 2)
  #return position, mask

def minimax_hash(position, mask, depth, maximizingPlayer, alpha, beta):
  ordered = [3,2,4,1,5,0,6]
  is_terminal = bool(check_four_aligned(position) + check_four_aligned(position ^ mask))
  valid_moves = [i for i in ordered if not (mask >> (i*7+5)) & 1]
  
  if depth == 0 or is_terminal:
      return get_euristic(position, mask, depth) 

  if maximizingPlayer:
      valid_moves = ordering_moves(valid_moves,position,mask)
      value = -np.Inf
      for col in valid_moves:
          child_position, child_mask = make_move(position, mask, col)
          hash_position = hash((child_position,child_mask,child_position ^ child_mask))
          if hash_position in seen:
            value = seen[hash_position]
          else:
            value = max(value, minimax_hash(child_position, child_mask, depth-1, False, alpha, beta))
            seen[hash_position] = value
          alpha = max(alpha, value)
          if value >= beta:
            break
      return value
  else:
      valid_moves = ordering_moves(valid_moves,position ^ mask,mask)
      value = np.Inf
      for col in valid_moves:
          child_position, child_mask = make_move(position ^ mask, mask, col)
          child_position = child_position ^ child_mask
          hash_position = hash((child_position,child_mask,child_position ^ child_mask))

          if hash_position in seen:
            value = seen[hash_position]
          else:
            value = min(value, minimax_hash(child_position, child_mask, depth-1, True, alpha, beta))
            seen[hash_position] = value
          beta = min(beta, value)
          if value <= alpha:
            break
      return value



def my_agent_binary_negmax(obs, config, test = False, depth= 6, player = 1): #20 = 10.58
  ordered = [3,2,4,1,5,0,6]
  global seen
  seen = {}
  if test:
    columns = 7
    rows = 6
    board = obs
    player = player
  else:
    columns = config.columns
    rows = config.rows
    board = obs.board
    player = obs.mark

  # Convert the board to a 2D grid
  grid = np.asarray(board).reshape(rows, columns)
  grid, mask = get_position_mask_bitmap(grid,player)

  # Get list of valid moves
  valid_moves = [i for i in ordered if not (mask >> (i*7+5)) & 1]

  # Use the heuristic to assign a score to each possible board in the next step
  scores = dict(zip(valid_moves, [score_move_negmax(grid, mask, col, depth) for col in valid_moves]))

  # Get a list of columns (moves) that maximize the heuristic
  max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
  # Select at random from the maximizing columns
  #return scores
  if not mask:
    return 3
  if test :
    return scores
  return random.choice(max_cols)

def check_winner(board):
  grid = np.asarray(board).reshape(6, 7)
  position, mask = get_position_mask_bitmap(grid,1)
  return check_four_aligned(position), check_four_aligned(position ^ mask)
  