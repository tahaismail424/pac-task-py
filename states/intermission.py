from psychopy import visual, core, event
import sdl2

def intermission_screen(win, joystick):
    """Screen that is presented between trials.
    Waits for player input to begin next trial
    """
    message = visual.TextStim(
        win, 
        text="Tilt joystick to begin next trial",
        height=30,
        color="white"
        )
    message.draw()
    win.flip()

    # Wait for joystick input
    core.wait(1)
    while True:
        # quit game if esc pressed
        keys = event.getKeys()
        if "escape" in keys:
            core.quit()  # Exit game

        # otherwise break loop if joystick tilted
        sdl2.SDL_JoystickUpdate()
        x_axis = sdl2.SDL_JoystickGetAxis(joystick, 0)
        y_axis = sdl2.SDL_JoystickGetAxis(joystick, 1)
        if abs(x_axis) > 8000 or abs(y_axis) > 8000:
            break

