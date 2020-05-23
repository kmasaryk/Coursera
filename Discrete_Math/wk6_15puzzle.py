#!/usr/bin/env python

"""
For reference, the positions in a 2 x 2 grid can be referred to thusly:
tl tr
bl br
"""

# just for testing - remove when done
import sys
import os
import time
import copy

PAUSE_AFTER_MOVE = False
PRINT_MSGS = False
REDRAW_SCREEN = False
DEBUG = False
moves = []

# Standard position
#tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

# Quiz example
#tiles = [1, 2, 3, 4, 5, 6, 7, 8, 13, 9, 11, 12, 10, 14, 15, 0]

# position 1 & 2 test
#tiles = [0, 1, 3, 4, 5, 2, 7, 8, 9, 6, 11, 12, 13, 10, 14, 15]

# may not be solvable.
#tiles = [1, 2, 4, 12, 14, 3, 9, 5, 7, 10, 0, 6, 8, 13, 11, 15]

# solving second row (may not be solvable
#tiles = [1, 2, 3, 4, 14, 10, 12, 0, 7, 9, 6, 5, 8, 13, 11, 15]

# solve position 7 & 8 (may not be solvable)
#tiles = [1, 2, 3, 4, 5, 6, 12, 9, 0, 14, 13, 15, 7, 8, 10, 11]

# solve only 9 & 13 on the left (may not be solveable)
#tiles = [1, 2, 3, 4, 5, 6, 7, 8, 14, 13, 0, 9, 10, 12, 11, 15]

# only 9 & 13 difficult since 13 is right above 9 (solvable)
#tiles = [1, 2, 3, 4, 5, 6, 7, 8, 13, 15, 14, 11, 9, 12, 0, 10]

# solve only 10 & 14 (solvable)
#tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 14, 11, 13, 15, 0, 10]

# solve only 11 & 15
#tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 13, 14, 0, 11]

# full - solvable random
#tiles = [2, 5, 4, 12, 14, 1, 9, 3, 7, 10, 0, 6, 8, 13, 11, 15]

# full - solvable random
#tiles = [1, 6, 8, 2, 3, 14, 15, 4, 0, 9, 11, 10, 13, 5, 7, 12]

# full - solvable random
#tiles = [2, 3, 8, 4, 1, 11, 14, 12, 9, 15, 5, 6, 13, 0, 10, 7]

# full - solvable random
#tiles = [1, 5, 6, 4, 11, 9, 2, 7, 10, 0, 8, 13, 14, 3, 15, 12]

# full - solvable random
#tiles = [3, 5, 10, 1, 7, 2, 8, 4, 9, 13, 6, 12, 0, 11, 14, 15]

# full - solvable random
#tiles = [1, 11, 2, 4, 5, 8, 0, 14, 10, 7, 6, 3, 9, 13, 15, 12]

# full - solvable random
#tiles = [0, 15, 1, 4, 5, 6, 10, 8, 9, 7, 3, 14, 13, 2, 11, 12]


def print_grid():
    if REDRAW_SCREEN:
        time.sleep(.1)
        os.system('clear')
        
    print('')
    
    for i in range(16):
        print('{:2}'.format(tiles[i]), end='')
        if (i + 1) % 4 != 0:
            print(' | ', end='')
        else:
            print('')

    print('')

def pause():
    # wait for a keypress
    input()

def track_move(tile, msg):
    global moves
    moves.append(tile)
    
    #print_grid()
    
    if msg and PRINT_MSGS:
        print(msg)
        
    if PAUSE_AFTER_MOVE:
        pause()
    
def get_col(idx):
    """Return the column number (start at 1) for the tile at idx."""
    row = int(idx / 4)
    col = int(idx - (row * 4)) + 1
    
    return col
    
def move_z_right():
    z_idx = tiles.index(0)
    tiles[z_idx] = tiles[z_idx + 1]
    tiles[z_idx + 1] = 0
    track_move(tiles[z_idx], "Move z right")

def move_z_left():
    z_idx = tiles.index(0)
    tiles[z_idx] = tiles[z_idx - 1]
    tiles[z_idx - 1] = 0
    track_move(tiles[z_idx], "Move z left")    

def move_z_up():
    z_idx = tiles.index(0)
    tiles[z_idx] = tiles[z_idx - 4]
    tiles[z_idx - 4] = 0
    track_move(tiles[z_idx], "Move z up")    

def move_z_down():
    z_idx = tiles.index(0)
    tiles[z_idx] = tiles[z_idx + 4]
    tiles[z_idx + 4] = 0
    track_move(tiles[z_idx], "Move z down")    
    
def move_z(dst_idx, vert_first=True):
    """Move the zero tile to dst_idx in the tiles list."""
    # int() works like a floor function so we don't need math.floor().
    z_row = int(tiles.index(0) / 4)
    dst_idx_row = int(dst_idx / 4)
    
    if vert_first:
        while z_row < dst_idx_row:
            move_z_down()
            z_row += 1
            
        while z_row > dst_idx_row:
            move_z_up()
            z_row -= 1

        while tiles.index(0) < dst_idx:
            move_z_right()
            
        while tiles.index(0) > dst_idx:
            move_z_left()
    else:
        while get_col(tiles.index(0)) < get_col(dst_idx):
            move_z_right()
            
        while get_col(tiles.index(0)) > get_col(dst_idx):
            move_z_left()
            
        while z_row < dst_idx_row:
            move_z_down()
            z_row += 1
            
        while z_row > dst_idx_row:
            move_z_up()
            z_row -= 1

def cycle_left(z_start, repeat=1):
    """Cycle the 2 x 2 grid counter-clockwise 'repeat' revolutions."""
    if DEBUG:
        print(f"Rotate counter_clockwise {repeat} times.")
        
    for i in range(repeat):
        if z_start == 'bl':
            move_z_up()
            move_z_right()
            move_z_down()
            move_z_left()
        elif z_start == 'br':
            move_z_left()
            move_z_up()
            move_z_right()
            move_z_down()
        elif z_start == 'tl':
            move_z_right()
            move_z_down()
            move_z_left()
            move_z_up()

def cycle_right(z_start, repeat=1):
    """Cycle the 2 x 2 grid clockwise 'repeat' revolutions."""
    if DEBUG:
        print(f"Rotate clockwise {repeat} times.")
        
    for i in range(repeat):
        if z_start == 'br':
            move_z_up()
            move_z_left()
            move_z_down()
            move_z_right()
        elif z_start == 'bl':
            move_z_right()
            move_z_up()
            move_z_left()
            move_z_down()
        elif z_start == 'tl':
            move_z_down()
            move_z_right()
            move_z_up()
            move_z_left()
            
def move_tile_up(tile, dst_idx):
    dst_row = int(dst_idx / 4)
    cur_row = int(tiles.index(tile) / 4)
    vert_first = True

    while cur_row > dst_row:
        # Check special case where z is directly above tile.
        if tiles.index(0) == tiles.index(tile) - 4:
            # Move z down and we're done with this iteration.
            if DEBUG:
                print(f"z is directly above tile {tile} so move z down.")
            move_z_down()
            cur_row = int(tiles.index(tile) / 4)
            continue

        # If z is directly below tile then we need to move L/R first.
        if tiles.index(0) - 4 == tiles.index(tile):
            if DEBUG:
                print(f"z is directly below tile {tile} so move z L/R first.")
            if tiles.index(0) + 1 % 4 != 0:
                move_z_right()
            else:
                move_z_left()

        # Move z to be on same row
        if int(tiles.index(0) / 4) < int(tiles.index(tile) / 4):
            move_z_down()
            continue
        elif int(tiles.index(0) / 4) > int(tiles.index(tile) / 4):
            move_z_up()
            continue

        # Move z to be directly left or right of tile.
        if ((tiles.index(tile) + 1) % 4 != 0
            and get_col(tiles.index(0)) > get_col(tiles.index(tile))):
            # Move z to be to the right of tile.
            move_z(tiles.index(tile) + 1, vert_first)
        else:
            # Move z to be to the left of tile.
            move_z(tiles.index(tile) - 1, vert_first)

        if tiles[tiles.index(tile) - 4] < tile:
            # Tile above 'tile' already solved. Move tile right first
            # Move z to the br
            move_z(tiles.index(tile) + 5)
            cycle_right('br')
            move_z_right()
            continue
        elif tiles[tiles.index(0) - 4] < tile:
            # Tile above z already solved. Move z around tile to other side.
            move_z_down()
            move_z(tiles.index(tile) + 1, False)
            continue
        
        # Move the tile up now.
        if tiles.index(0) < tiles.index(tile):
            # z is to the left
            cycle_left('bl')
        else:
            cycle_right('br')

        cur_row = int(tiles.index(tile) / 4)

def move_tile_down(tile, dst_idx):
    dst_row = int(dst_idx / 4)
    cur_row = int(tiles.index(tile) / 4)

    while cur_row < dst_row:
        # Move z to be br or bl of tile.
        if (tiles.index(tile) + 1) % 4 != 0:
            # Move z to be to the bottom right of tile.
            move_z(tiles.index(tile) + 5)
            cycle_left('br')
        else:
            # Move z to be to the bottom left of tile.
            move_z(tiles.index(tile) + 3)
            cycle_right('bl')

        cur_row = int(tiles.index(tile) / 4)
        
def leftsolve_move_tile(tile, dst_idx):
    dst_row = int(dst_idx / 4)
    cur_row = int(tiles.index(tile) / 4)

    # z should always be on the bottom row
    if int(tiles.index(0) / 4) != 3:
        move_z_down()
        cur_row = int(tiles.index(tile) / 4)

    while cur_row != dst_row:
        # z & the tile must be on bottom row.
        if DEBUG:
            print(f"Need to move tile {tile} up")
        if tiles.index(0) < tiles.index(tile):
            while tiles.index(0) < tiles.index(tile) - 1:
                move_z_right()
            cycle_left('bl')
        else:
            while tiles.index(0) > tiles.index(tile) + 1:
                move_z_left()
            cycle_right('br')
        cur_row = int(tiles.index(tile) / 4)

    # Should be on correct row now so move tile left.
    if DEBUG:
        print(f"Tile {tile} is on correct row.")
    while tiles.index(tile) != dst_idx:
        # Move z to bl
        while tiles.index(0) != tiles.index(tile) + 3:
            if tiles.index(0) >= tiles.index(tile) + 4:
                move_z_left()
            else:
                move_z_right()
        cycle_left('bl')
        
        
def move_tile(tile, dst_idx):
    """Move tile 'tile' to index 'dst_idx'"""
    dst_row = int(dst_idx / 4)
    cur_row = int(tiles.index(tile) / 4)
    if cur_row != dst_row:
        if cur_row > dst_row:
            if DEBUG:
                print(f"Need to move tile {tile} up")
            move_tile_up(tile, dst_idx)
        elif cur_row < dst_row:
            if DEBUG:
                print(f"Need to move tile {tile} down")
            # This condition is only possible for p2.
            move_tile_down(tile, dst_idx)

    # Should be on the right row now so need to move left or right.
    if DEBUG:
        print(f"Tile {tile} is on the correct row")
    while tiles.index(tile) != dst_idx:
        if tiles.index(tile) < dst_idx:
            # Move z to br.
            move_z(tiles.index(tile) + 5)
            cycle_right('br')
        else:
            # Move z to bl.
            move_z(tiles.index(tile) +3)
            cycle_left('bl')

def solve_top(p1, p2):
    """
    p1 = leftmost position (top left)
    p2 = position just right of p1 (top right)
    Requirement: All positions below p1 & p2 have not been solved yet.
    """
    # First, check if tiles p1 & p2 are already in the correct position:
    if tiles.index(p1) == p1 - 1 and tiles.index(p2) == p2 - 1:
        # Tiles are both already in the solved position so nothing to do.
        if DEBUG:
            print(f"Tiles {p1} & {p2} are already in the solved position")
        return

    if tiles.index(p1) != p1:
        # p1 tile is not in the position we want (which is actually 1 tile
        # right of it's solved position).
        if DEBUG:
            print(f"Tile {p1} in wrong position")
        move_tile(p1, p1)
        if DEBUG:
            print(f"Tile {p1} in correct position")

    # Check for special case where p2 is immediately left of p1.
    if tiles.index(p2) == tiles.index(p1) - 1:
        move_z(tiles.index(p2) + 4)
        cycle_left('bl')
        cycle_right('tl') # implement this
        cycle_right('bl')
        cycle_left('tl')
        
    if tiles.index(p2) != p2 + 4 - 1:
        if DEBUG:
            print(f"Tile {p2} in wrong position")
        move_tile(p2, p2 + 4 - 1)
        if DEBUG:
            print(f"Tile {p2} in correct position")

    # 2x2 grid should now look like this:
    # ? p1
    # ? p2
    
    # Final 3-cycle counter-clockwise rotation to put them both into place.
    # Move zero tile to position bl
    move_z(tiles.index(p2) - 1, False)
    cycle_left('bl')

def solve_left_check_p1_below_p2(p1, p2):
    # Check for the special case where p1 is directly below p2 and both are
    # against the left side.
    if (((p2 == 13 and get_col(tiles.index(p2)) == 1)
        or p2 == 14 and get_col(tiles.index(p2)) == 2)
        and tiles.index(p2) == tiles.index(p1) - 4):
        if int(tiles.index(0) / 4) != 3:
            move_z_down()
        while tiles.index(0) != tiles.index(p1) + 1:
            move_z_left()
        cycle_left('br')
        cycle_right('bl')
        cycle_right('br')
        cycle_left('bl')
    

    
def solve_left(p1, p2):
    """
    p1 = top position
    p2 = position just below p1
    Requirement: all positions to the right of p1 & p2 have not been solved yet.
    """
    # First, check if tiles p1 & p2 are already in the correct position.
    if tiles.index(p1) == p1 - 1 and tiles.index(p2) == p2 -1:
        if DEBUG:
            print(f"Tiles {p1} & {p2} are already in the solved position.")
        return

    # Check for the special case where p1 is directly below p2 and both are
    # against the left side.
    solve_left_check_p1_below_p2(p1, p2)

    if tiles.index(p2) != p2 - 4 - 1:
        if DEBUG:
            print(f"Tile {p2} in wrong position")
        leftsolve_move_tile(p2, p2 - 4 - 1)
    if DEBUG:
        print(f"Tile {p2} in correct postion")

    if tiles.index(p1) != p1 + 1 - 1:
        if DEBUG:
            print(f"Tile {p1} in wrong position")
        if tiles.index(0) == tiles.index(p2) + 4:
            # z is directly below p2 so move it right first and then check for
            # special case where p1 below p2.
            move_z_right()
            solve_left_check_p1_below_p2(p1, p2)
        leftsolve_move_tile(p1, p1 + 1 - 1)
    if DEBUG:
        print(f"Tile {p1} in correct postion")

    # 2x2 grid should now look like this:
    # p2 p1
    # ?  ?

    # Final 3-cycle counter-clockwise rotation to put them both into place.
    move_z(tiles.index(p1) + 4)
    cycle_left('br')

        
#print("Starting grid")
#print_grid()
#pause()

def solution(position):
    global tiles
    tiles = copy.deepcopy(position)
    
    # We solve positions in pairs.
    soln_pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 13), (10, 14), (11, 15)]

    for pair in soln_pairs:
        if pair[0] < 8:
            solve_top(pair[0], pair[1])
        else:
            solve_left(pair[0], pair[1])

    return moves
            
position = [0, 15, 1, 4, 5, 6, 10, 8, 9, 7, 3, 14, 13, 2, 11, 12]
print(solution(position))
#print(f"moves = {moves}")


