# define classes for game objects
import sdl2
from psychopy import visual, event, core
import random 
import numpy as np

# Player (Pacman)
class Player:
    def __init__(self, win, joystick, keyboard, max_speed=10):
        self.shape = visual.Circle(win, radius=20, fillColor="yellow", lineColor="yellow")
        self.x, self.y = 0, 0 # Initial position
        self.joystick = joystick
        self.win = win
        self.kb = keyboard
        self.max_speed = max_speed

    def move(self):
        if self.joystick:
            # joystick is on scale of [-32000, 32000]
            sdl2.SDL_JoystickUpdate()
            x_axis = sdl2.SDL_JoystickGetAxis(self.joystick, 0)  # X-axis
            y_axis = -sdl2.SDL_JoystickGetAxis(self.joystick, 1)  # Y-axis

            # introduce stabilizer - 0 values less than abs(3000)
            x_axis = x_axis if abs(x_axis) > 8000 else 0
            y_axis = y_axis if abs(y_axis) > 8000 else 0

            # rescale values to have max speed of player
            scale_factor = 32000 / self.max_speed
            x_axis /= scale_factor
            y_axis /= scale_factor

            # set position
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
    def __init__(self, win, color, start_pos, speed):
        self.shape = visual.Rect(win, width=30, height=30, fillColor=color, lineColor=color)
        self.shape.pos = start_pos
        self.speed = speed
        self.color_name = color
        self.win = win
        self.prev_positions = []

    def move(self, move_calculator, player_pos, other_npcs):
        self_x, self_y = self.shape.pos[0] + self.win.clientSize[0] // 2, self.shape.pos[1] + self.win.clientSize[1] // 2
        self_apos = np.array([self_x, self_y])
        self.prev_positions.append(self_apos)
        if len(self.prev_positions) > 10:
            self.prev_positions.pop(0)

        # calculate movement vec
        movement_vec = move_calculator.calculate_next_move(
            self_apos, player_pos, other_npcs, self.prev_positions
        )
        pos_vec = tuple(self.speed * movement_vec +  self_apos)

        # readjust position to be within bounds
        pos_vec_x_adj = min(self.win.clientSize[0], max(0, pos_vec[0]))
        pos_vec_y_adj = min(self.win.clientSize[1], max(0, pos_vec[1]))

        # readjust position to psychopy axis
        self_npos_x, self_npos_y = pos_vec_x_adj - self.win.clientSize[0] // 2, pos_vec_y_adj - self.win.clientSize[1] // 2

        # set position
        self.shape.pos = (self_npos_x, self_npos_y)

    def check_collision(self, player):
        return self.shape.overlaps(player.shape)