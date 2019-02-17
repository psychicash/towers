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
            if value2 in right_side_blue:
                return True
            else:
                return False
        elif value1 in left_side_yellow:
            if value2 in right_side_yellow:
                return True
            else:
                return False
    elif side == 'up':
        if value1 in up_side_blue:
            if value2 in down_side_blue:
                return True
            else:
                return False
        elif value1 in up_side_yellow:
            if value2 in down_side_yellow:
                return True
            else:
                return False
    elif side == 'right':
        if value1 in right_side_blue:
            if value2 in left_side_blue:
                return True
            else:
                return False
        elif value1 in right_side_yellow:
            if value2 in left_side_yellow:
                return True
            else:
                return False
    elif side == 'down':
        if value1 in down_side_blue:
            if value2 in up_side_blue:
                return True
            else:
                return False
        elif value1 in down_side_yellow:
            if value2 in up_side_yellow:
                return True
            else:
                return False


def validate_sides(x, y, grid, value):
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # adjacent squares
        # check_wang(value1, value2, side) - side being the side of value 1 we are checking

        checking_position = (x + new_position[0], y + new_position[1])
        side_checked = ''

        if checking_position[0] > (len(grid) - 1) or checking_position[0] < 0 or checking_position[1] > (len(grid[len(grid) - 1]) - 1) or checking_position[1] < 0:
            print("Out of bounds")
            print(str(x) + " is the x and the y is " + str(y))
            print(str(new_position[0]) + str(new_position[1]))
            continue

        if new_position[1] == -1:
            side_checked = 'left'
        elif new_position[1] == 1:
            side_checked = 'right'
        elif new_position[0] == -1:
            side_checked = 'up'
        elif new_position[0] == 1:
            side_checked = 'down'

        checking = check_wang(value, grid[checking_position[0]][checking_position[1]], side_checked)
        if checking == False:
            return False
        else:
            continue
    return True

def wang_set(width, height):
    grid = []

    for i in range(height):
        grid1 = []
        for j in range(width):
            grid1.append(0)
        grid.append(grid1)

    grid[0][0] = random.choice(list(range(0,15)))

    for i in range(height):
        for j in range(width):
            if i == 0 and j == 0:
                print("both are 0")
                continue
            else:
                acceptable = False
                box_pool = list(range(0, 15))
                while acceptable == False:
                    new_value = random.choice(box_pool)
                    x = validate_sides(i, j, grid, new_value)
                    if x == False:
                        box_pool.remove(new_value)
                    else:
                        box_pool = list(range(0, 15))
                        acceptable = True
                grid[i][j] = new_value

    #print(grid)
    return grid