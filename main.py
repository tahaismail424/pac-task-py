from psychopy import visual, event, core
from states.experiment import run_experiment
from states.title import title_screen

# Create game window
win = visual.Window(size=(800, 600), color=(0, 0, 0), units="pix")

# run game loop
running = True
while running:
    keys = event.getKeys()
    if "escape" in keys:
        running = False
    params = title_screen(win)
    experiment_out = run_experiment(win, params)
    win.flip()