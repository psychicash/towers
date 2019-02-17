import random

def check_wang(value1, value2, side):
    #side is the side of value 1 that is touching value2
    left_side_blue = (0, 1, 2, 3, 4, 5, 6, 7)
    left_side_yellow = (8, 9, 10, 11, 12, 13, 14, 15)
    up_side_blue = (0, 2, 4, 6, 8, 10, 12, 14)
    up_side_yellow = (1, 3, 5, 7, 9, 11, 13, 15)
    right_side_blue = (0, 1, 4, 5, 8, 9, 12, 13)
    right_side_yellow = (2, 3, 6, 7, 10, 11, 14, 15)
    down_side_blue = (0, 1, 2, 3, 8, 9, 10, 11)
    down_side_yellow = (4, 5, 6, 7, 12, 13, 14, 15)


    if side == 'left':
        if value1 in left_side_blue:
            if value2 not in right_side_blue:
                print("left side blue, right side not blue")
                return False
            else:
                print("left side blue, right side blue")
                return True
        elif value1 in left_side_yellow:
            if value2 not in right_side_yellow:
                return False
            else:
                return True
    elif side == 'up':
        if value1 in up_side_blue:
            if value2 not in down_side_blue:
                return False
            else:
                return True
        elif value1 in up_side_yellow:
            if value2 not in down_side_yellow:
                return False
            else:
                return True
    elif side == 'right':
        if value1 in right_side_blue:
            if value2 not in left_side_blue:
                return False
            else:
                return True
        elif value1 in right_side_yellow:
            if value2 not in left_side_yellow:
                return False
            else:
                return True
    elif side == 'down':
        if value1 in down_side_blue:
            if value2 not in up_side_blue:
                return False
            else:
                return True
        elif value1 in down_side_yellow:
            if value2 not in up_side_yellow:
                return False
            else:
                return True



def wang_set(width, height):
    grid = []


    for i in range(height):
        grid1 = []
        for j in range(width):
            grid1.append(0)
        grid.append(grid1)

    grid[0][0] = random.choice(range(0,15))

    for i in range(height):
        for j in range(width):
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # adjacent squares
                #check_wang(value1, value2, side) - side being the side of value 1 we are checking

                box_pool = list(range(0,15))
                checking_position = (i + new_position[0], j + new_position[1])
                side_checked = ''

                if checking_position[0] > (len(grid) - 1) or checking_position[0] < 0 or checking_position[1] > (len(grid[len(grid)-1]) -1) or checking_position[1] < 0:
                    continue

                if new_position[1] == -1:
                    side_checked = 'left'

                elif new_position[1] == 1:
                    side_checked = 'right'

                elif new_position[0] == -1:
                    side_checked = 'up'

                elif new_position[0] == 1:
                    side_checked = 'down'


                new_value = random.choice(box_pool)
                acceptable = False

                while acceptable == False:
                    x = check_wang(grid[i][j], new_value, side_checked)
                    if x == False:
                        print("x is false")
                        box_pool.remove(new_value)
                        print(box_pool)
                        print(new_value)
                        new_value = random.choice(box_pool)
                        print(new_value)
                    else:
                        print("x is true")
                        grid[i][j] = new_value
                        acceptable = True

    #print(grid)
    return grid