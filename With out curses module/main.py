from collections import deque
import os
from random import randint


def print_screen():
	print(6 * " ", end="")
	for cell in SCREEN:
		if cell[0] == 0 or cell[1] == 0 or cell[0] == (HEIGHT - 1) or cell[1] == (WIDTH - 1):
			print("#", end="")
		elif cell == SNAKE_HEAD:
			print("x", end="")
		elif cell in SNAKE_BODY:
			print("o", end="")
		elif cell == APPLE:
			print("$", end="")	
		else:
			print(" ", end="")
		
		if cell[1] == (WIDTH - 1):
			print("")
			print(6 * " ", end="")

def update_snake():
	global eaten, SNAKE_HEAD
	SNAKE_BODY.appendleft(SNAKE_HEAD)
	new_head = SNAKE_HEAD[0] + direction[0] , SNAKE_HEAD[1] + direction[1]
	SNAKE_HEAD = new_head	
	if not eaten:
		SNAKE_BODY.pop()
	eaten = False

def place_apple():
	row = randint(1, HEIGHT-2)
	col = randint(1, WIDTH-2)
	if (row, col) in SNAKE_BODY or (row, col) == SNAKE_HEAD:
		row, col = place_apple()
	return (row, col)

def eat_apple():
	global eaten, APPLE
	if SNAKE_HEAD == APPLE:
		eaten = True
		APPLE = place_apple()

def is_collision():
	if SNAKE_HEAD[0] == 0 or SNAKE_HEAD[1] == 0 or SNAKE_HEAD[0] == (HEIGHT - 1) or SNAKE_HEAD[1] == (WIDTH - 1) or SNAKE_HEAD in SNAKE_BODY:
		return True

def quit_game():
	os.system("clear")
	print("            <<GAME OVER>>")


#Game arena config				
WIDTH = 35
HEIGHT = 16
SCREEN = [(row, col) for row in range(HEIGHT) for col in range(WIDTH)]

#Snake starting
SNAKE_HEAD = (HEIGHT//2, 5)
SNAKE_BODY = deque([(HEIGHT//2, 4), (HEIGHT//2, 3)])

# w: up, s: down, a: left, d: right
DIRECTION = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
REVERSE = {"w": (1, 0), "s": (-1, 0), "a": (0, 1), "d": (0, -1)}

direction = DIRECTION ["d"]
eaten = False

APPLE = place_apple()

#Game
while True:
	if is_collision():
		quit_game()
		break
		
	os.system("clear")
	print_screen()
	text = input("move: ")	
	if text == "q":
		quit_game()
		break	
			
	if REVERSE.get(text, direction) != direction:
		#counter reverse snake move
		direction = DIRECTION[text]
		
	update_snake()
	eat_apple()
