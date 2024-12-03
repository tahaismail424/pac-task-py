# define classes for game objects

from psychopy import visual, event, core
import random 

# Player (Pacman)
class Player:
    def __init__(self, win, joystick, keyboard):
        self.shape = visual.Circle(win, radius=20, fillColor="yellow", lineColor="yellow")
        self.x, self.y = 0, 0 # Initial position
        self.joystick = joystick
        self.kb = keyboard

    def move(self):
        if self.joystick:
            x_axis = self.joystick.getX() * 10 # Scale joystick movement as needed
            y_axis = self.joystick.getY() * 10
            self.x += x_axis
            self.y += y_axis
            self.shape.pos = (self.x, self.y)
        
    def move_keyboard(self):
        keys = self.kb.getKeys(["left", "right", "up", "down"], waitRelease=False)
        for key in keys:
            if key.name == "left":
                self.x -= 10
            elif key.name == "right":
                self.x += 10
            elif key.name == "up":
                self.y += 10
            elif key.name == "down":
                self.y -= 10
        self.shape.pos = (self.x, self.y)

# Target Squares
class Target:
    def __init__(self, win, color, start_pos):
        self.shape = visual.Rect(win, width=30, height=30, fillColor=color, lineColor=color)
        self.shape.pos = start_pos
        self.speed = random.choice([2, -2]), random.choice([2, -2])

    def move(self):
        x, y = self.shape.pos
        dx, dy = self.speed
        x += dx
        y += dy

        # Bounce off walls
        if abs(x) > 400 or abs(y) > 300:
            dx *= -1
            dy *= -1
        self.speed = dx, dy
        self.shape.pos = (x, y)

    def check_collision(self, player):
        return self.shape.overlaps(player.shape)