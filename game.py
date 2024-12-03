# Initialize environment
from psychopy import visual, event, core
from psychopy.hardware import joystick, keyboard
from objects import Player, Target

# joystick hardware integration
joystick.backend = "pyglet"
joy = None
if joystick.getNumJoysticks() > 0:
    joy = joystick.Joystick(0)
else:
    print("No joystick detected!")

kb = keyboard.Keyboard()
# Create game widnow 
win = visual.Window(size=(800, 600), color=(0, 0, 0), units="pix")

# Frame rate for consistent motion
frame_rate = 60
dt = 1 / frame_rate
clock = core.Clock()


# initialize objects
player = Player(win, joy, kb)
blue_square = Target(win, color="blue", start_pos=(-200, 0))
orange_square = Target(win, color="orange", start_pos=(200, 0))

targets = [blue_square, orange_square]


# run game loop
running = True
while running:
    keys = event.getKeys()
    if "escape" in keys:
        running = False # Exit game if hit escape

    # move player according to joystick movement
    player.move()
    player.move_keyboard()
    for target in targets:
        target.move()

        # check for cllisions
        if target.check_collision(player):
            print(f"Hit {target.shape.fillColor} square!")
            running = False
        
    # Draw objects
    win.clearBuffer()
    player.shape.draw()
    for target in targets:
        target.shape.draw()
    
    win.flip()
    core.wait(dt)

# once game over close clock and window
win.close()
core.quit()