from collections import deque
import curses
from curses import textpad
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
import time
from random import randint

class Snake():
	def __init__(self, window, box):
		self.window = window
		self.box = box
		self.body_list = deque()
		self.score = 0
		self.direction = ord("d")
		self.eaten = False
		for i in range(4):
			self.body_list.append([box[0][0]+5-i, box[0][0]+3])
		self.DIRECTION = {
            ord("w"): self.move_up,
            ord("s"): self.move_down,
            ord("a"): self.move_left,
            ord("d"): self.move_right
        }
		self.OPPOSITE = {
            ord("w"): ord("s"),
            ord("s"): ord("w"),
            ord("a"): ord("d"),
            ord("d"): ord("a")
        }
		"""self.DIRECTION = {
			KEY_UP: self.move_up,
			KEY_DOWN: self.move_down,
			KEY_LEFT: self.move_left,
			KEY_RIGHT: self.move_right
		}"""
		"""self.OPPOSITE = {
			KEY_UP: KEY_DOWN, 
			KEY_DOWN: KEY_UP,
			KEY_LEFT: KEY_RIGHT,
			KEY_RIGHT: KEY_LEFT,
		}"""
	def food_eaten(self):
		self.eaten = True
		self.score += 1
		
	def update(self):
		if not self.eaten:
			end = self.body_list.pop()
			self.window.addstr(end[1], end[0], " ")
		self.DIRECTION[self.direction]()
		self.eaten = False
       
	def change_direction(self, direction):
		if self.direction != self.OPPOSITE[direction]:
			self.direction = direction
    	
	def render(self):
		for i, body in enumerate(self.body_list):
			if i == 0:
				self.window.addstr(body[1], body[0], "X")
			else:
				self.window.addstr(body[1], body[0], "O")

	def collision(self):
		for i, body in enumerate(self.body_list):
			if i > 0 and self.body_list[0] == body:
				return True
		return False
					
	def move_up(self):
		new_head = [self.body_list[0][0], self.body_list[0][1]-1]
		if new_head[1] <= self.box[0][0]:
			new_head[1] = self.box[1][0] - 1
		self.body_list.appendleft(new_head)
		
	def move_down(self):
		new_head = [self.body_list[0][0], self.body_list[0][1]+1]
		if new_head[1] >= self.box[1][0]:
			new_head[1] = self.box[0][0] + 1
		self.body_list.appendleft(new_head)
		
	def move_left(self):
		new_head = [self.body_list[0][0]-1, self.body_list[0][1]]
		if new_head[0] <= self.box[0][1]:
			new_head[0] = self.box[1][1] - 1
		self.body_list.appendleft(new_head)
		
	def move_right(self):
		new_head = [self.body_list[0][0]+1, self.body_list[0][1]]
		if new_head[0] >= self.box[1][1]:
			new_head[0] = self.box[0][1] + 1
		self.body_list.appendleft(new_head)					

	
class Food():
	def __init__(self, window, box, snake):
		self.window = window
		self.box = box
		self.snake = snake
		self.position = None
		self.reset()
	    
	def render(self):
		self.window.addstr(self.position[1], self.position[0], "*")
					
	def reset(self):
		self.position = None
		while self.position is None:
			self.position = [randint(self.box[0][1]+1, self.box[1][1]-1), 
                                        randint(self.box[0][0]+1, self.box[1][0]-1)]
			if self.position in self.snake.body_list:
				self.position = None		

	
def game(scr):
	curses.curs_set(0)
	scr.nodelay(1)
	scr.timeout(150)
	sh, sw = scr.getmaxyx()
	box = [(3, 3), (sh-3, sw-15)]
	textpad.rectangle(scr, box[0][0], box[0][1], box[1][0], box[1][1])
	snake = Snake(scr, box)
	food = Food(scr, box, snake)
	
	while not snake.collision():	
		snake.render()
		food.render()
		scr.addstr(box[0][0], box[1][1]-10, f"Score:{snake.score}")		
		key = scr.getch()
		#if key in [KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP]:
		if key in [ord("w"), ord("s"),ord("a"),ord("d")]:
			snake.change_direction(key)			
		snake.update()
		if food.position == snake.body_list[0]:
			snake.food_eaten()
			food.reset()
			
	y = (box[0][0] + box[1][0])//2
	x = ((box[0][1] + box[1][1])//2) - 4
	scr.addstr(y, x, "Game Over")
	scr.addstr(y+1, x, f"Score:{snake.score}")
	scr.refresh()
	time.sleep(3)
	
	
curses.wrapper(game)

