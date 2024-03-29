import random
import curses

# Initialize screen
stdscr = curses.initscr()
curses.curs_set(0)
sh, sw = stdscr.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# Initialize colors
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
w.attron(curses.color_pair(1))

# Initial position and snake
snake_x = sw // 4
snake_y = sh // 2
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

# Food position
food = [sh // 2, sw // 2]
w.addch(food[0], food[1], curses.ACS_PI)

# Initial direction
key = curses.KEY_RIGHT

# Game logic
while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # Check if snake hits the wall or itself
    if (snake[0][0] in [0, sh]) or (snake[0][1] in [0, sw]) or (snake[0] in snake[1:]):
        curses.endwin()
        quit()

    # New head position
    new_head = [snake[0][0], snake[0][1]]

    # Determine new head position based on direction
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Insert new head
    snake.insert(0, new_head)

    # Check if snake eats the food
    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh - 1),
                random.randint(1, sw - 1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    # Draw snake
    for i, c in enumerate(snake):
        if i == 0:
            w.addch(c[0], c[1], curses.ACS_CKBOARD)
        else:
            w.addch(c[0], c[1], curses.ACS_CKBOARD, curses.color_pair(1))

    w.refresh()
