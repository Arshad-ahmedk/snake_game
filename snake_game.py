import curses
from random import randint

# Setup window
curses.initscr()
win = curses.newwin(20, 60, 0, 0)  # height, width, begin_y, begin_x
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# Snake and food
snake = [(4, 10), (4, 9), (4, 8)]
food = (10, 20)

win.addch(food[0], food[1], '*')

# Game logic
ESC = 27
key = curses.KEY_RIGHT
score = 0

# Previous key to prevent crashing on multiple keys pressed
prev_key = key

while key != ESC:
    win.addstr(0, 2, 'Score: ' + str(score) + ' ')
    win.timeout(150 - (len(snake) // 5 + len(snake) // 10) % 120)

    event = win.getch()
    if event in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        prev_key = key
        key = event

    if (key == curses.KEY_LEFT and prev_key == curses.KEY_RIGHT) or \
       (key == curses.KEY_RIGHT and prev_key == curses.KEY_LEFT) or \
       (key == curses.KEY_UP and prev_key == curses.KEY_DOWN) or \
       (key == curses.KEY_DOWN and prev_key == curses.KEY_UP):
        key = prev_key

    # Calculate the new coordinates of the head of the snake
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    # Wrap around if the snake hits the boundary
    if y == 0:
        y = 18
    elif y == 19:
        y = 1
    if x == 0:
        x = 58
    elif x == 59:
        x = 1

    # Insert new head and check for collisions
    snake.insert(0, (y, x))
    if snake[0] in snake[1:]:
        break

    if snake[0] == food:
        score += 1
        food = ()
        while food == ():
            food = (randint(1, 18), randint(1, 58))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '*')
    else:
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    win.addch(snake[0][0], snake[0][1], '#')

curses.endwin()
print(f"Final score = {score}")
