from psychopy import visual, core
import sdl2

def intermission_screen(win, joystick):
    message = visual.TextStim(
        win, 
        text="Tilt joystick to begin next trial",
        height=30,
        color="white"
        )
    message.draw()
    win.flip()

    # Wait for joystick input
    core.wait(2)
    while True:
        sdl2.SDL_JoystickUpdate()
        x_axis = sdl2.SDL_JoystickGetAxis(joystick, 0)
        y_axis = sdl2.SDL_JoystickGetAxis(joystick, 1)
        if abs(x_axis) > 8000 or abs(y_axis) > 8000:
            break

