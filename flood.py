"""Flood-fill to count chambers in a cave.
CS 210 project.
<Jacob Dirkx>, <10/29/23>
Credits: Myself
"""
import doctest
import cave
import config
import cave_view

def scan_cave(cavern: list[list[str]]) -> int:
    """Scans the cave for air pockets.  Returns the number of
    air pockets encountered after filling each one.
    """
    chambers = 0
    for row_i in range(len(cavern)):
        for col_i in range(len(cavern[0])):
            if cavern[row_i][col_i] == config.AIR:
                fill(cavern, row_i, col_i)
                cave_view.change_water()
                chambers+=1
    return chambers

def fill(cavern: list[list[str]], row_i: int, col_i: int):
    """Pours water into cell at row_i, col_i, then checks
    the cells surrounding it to fill them as well via recursion.
    """
    cavern[row_i][col_i] = config.WATER
    cave_view.fill_cell(row_i, col_i)
    #upward
    row_up_i = row_i - 1
    if (row_up_i >= 0 and row_up_i < len(cavern)
        and cavern[row_up_i][col_i] == config.AIR):
        fill(cavern, row_up_i, col_i)
    #downward
    row_down_i = row_i + 1
    if (row_down_i >= 0 and row_down_i < len(cavern)
        and cavern[row_down_i][col_i] == config.AIR):
        fill(cavern, row_down_i, col_i)
    #left
    col_left_i = col_i -1
    if (col_left_i >= 0 and col_left_i < len(cavern)
        and cavern[row_i][col_left_i] == config.AIR):
        fill(cavern, row_i, col_left_i)
    #right
    col_right_i = col_i +1
    if (col_right_i >= 0 and col_right_i <= len(cavern)
        and cavern[row_i][col_right_i] == config.AIR):
        fill(cavern, row_i, col_right_i)

def main():
    doctest.testmod()
    cavern = cave.read_cave(config.CAVE_PATH)
    cave_view.display(cavern,config.WIN_WIDTH, config.WIN_HEIGHT)
    chambers = scan_cave(cavern)
    print(f"Found {chambers} chambers")
    cave_view.redisplay(cavern)
    cave_view.prompt_to_close()

if __name__ == "__main__":
    main()

