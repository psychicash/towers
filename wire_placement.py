from main import get_image
import pygame



class Cl_Wire(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.location = []
        self.location.append(x)
        self.location.append(y)
        self.filename = filename
        img = self.filename
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = (self.location[1] * 100) + 100
        self.rect.y = (self.location[0] * 100) + 50


def wire_placement(grid, towers, path_of_wires):
    wire_objects = []
    #sets bunker location to use for setting bunker wire
    bunker = [(ix, iy) for ix, row in enumerate(grid) for iy, i in enumerate(row) if i == 'B']
    bunker_img = get_image('./images/sprites/wires/tile014.png')
    wire_objects.append(Cl_Wire(bunker[0][0], bunker[0][1], bunker_img))

    pow = []
    for i in range(len(path_of_wires)):
        pow += path_of_wires[i]
    path_of_wires = pow
    path_of_wires = list(set(path_of_wires))
    #now we have all the nodes used in the path
    path_of_wires.sort()
    print(path_of_wires)

    for i in range(len(path_of_wires)):
        if grid[path_of_wires[i][0]][path_of_wires[i][1]] == 0:
            grid[path_of_wires[i][0]][path_of_wires[i][1]] = 'W'

    for i in range(len(path_of_wires)):
        x = path_of_wires[i][0]
        y = path_of_wires[i][1]
        total = -1
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # adjacent squares
            checking_position = (x + new_position[0], y + new_position[1])

            side_checked = ''
            if new_position[1] == -1:
                side_checked = 'left'
            elif new_position[1] == 1:
                side_checked = 'right'
            elif new_position[0] == -1:
                side_checked = 'up'
            elif new_position[0] == 1:
                side_checked = 'down'

            if checking_position[0] > (len(grid) - 1) or checking_position[0] < 0 or checking_position[1] > (
                    len(grid[len(grid) - 1]) - 1) or checking_position[1] < 0:
                continue
            else:
                if grid[checking_position[0]][checking_position[1]] == 'W' or grid[checking_position[0]][checking_position[1]] == 'B' or grid[checking_position[0]][checking_position[1]] == 'T':
                    if side_checked == 'left':
                        total += 8
                    elif side_checked == 'right':
                        total += 2
                    elif side_checked == 'up':
                        total += 1
                    elif side_checked == 'down':
                        total += 4
        if total < 0:
            pass
        else:
            if total < 10:
                total = str(0) + str(total)
            elif total >= 10:
                total = str(total)
            temp_image = get_image('./images/sprites/wires/tile0{0}.png'.format(total))
            print(total)
            print(x, y)
            wire_objects.append(Cl_Wire(x,y, temp_image))
    return wire_objects













            # def validate_sides(x, y, grid, proposed_value):
            #     for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # adjacent squares
            #         checking_position = (x + new_position[0], y + new_position[1])
            #         side_checked = ''
            #
            #         if new_position[1] == -1:
            #             side_checked = 'left'
            #         elif new_position[1] == 1:
            #             side_checked = 'right'
            #         elif new_position[0] == -1:
            #             side_checked = 'up'
            #         elif new_position[0] == 1:
            #             side_checked = 'down'
            #
            #         if checking_position[0] > (len(grid) - 1) or checking_position[0] < 0 or checking_position[1] > (
            #                 len(grid[len(grid) - 1]) - 1) or checking_position[1] < 0:
            #             continue
            #         else:
            #             print(side_checked)
            #             print("the x is " + str(x) + " and the y is " + str(y) + " and the grid is...")
            #             print(grid)
            #             checking = check_wang(proposed_value, grid[checking_position[0]][checking_position[1]],
            #                                   side_checked)
            #             if checking == False:
            #                 return False
            #             else:
            #                 continue
            #     return True
