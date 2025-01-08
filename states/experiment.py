import numpy as np
import random
import sdl2
from psychopy.hardware import keyboard
from objects import Player, Target
from states.trial import run_trial
from states.intermission import intermission_screen

def run_experiment(win, params):
    # Initialize experiment variables
    n_trials = params["trials"] if params["trials"] else 10
    prey_speed = params["speed"] if params["speed"] else 9
    trial_type_distribution = params["trial_type_distribution"] if params["trial_type_distribution"] else 50
    target_count = params["target_count"]

    # initialize keyboard and joystick
    sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
    joystick = sdl2.SDL_JoystickOpen(0)  # Open the first joystick
    if not joystick:
        print("No joystick detected!")
        return None

    kb = keyboard.Keyboard()

    # determine trial distribution
    n_multi_prey = int(n_trials * (trial_type_distribution / 100))
    n_single_prey = n_trials - n_multi_prey
    trials = ["multi"] * n_multi_prey + ["single"] * n_single_prey
    np.random.shuffle(trials) # randomize trial order

    # trial data - empty for now
    trial_data = []

    cur_speed = prey_speed
    # create targets and player
    # initialize objects
    player = Player(win, joystick, kb)
    colors = ["red", "aqua", "pink", "orange", "blue"]
    # randomlize color order
    np.random.shuffle(colors)
    delta_speed = prey_speed / target_count
    targets = []
    for target_number in range(target_count):
        target = Target(win, color=colors[target_number], start_pos=(0, 0), speed=cur_speed)
        targets.append(target)
        cur_speed -= delta_speed


    # experiment loop
    for trial_index, trial_type in enumerate(trials):
        # Prepare for trial
        print(f"Starting Trial {trial_index + 1}: {trial_type}")
        if trial_type == "single":
            active_targets = random.sample(targets, 1)
        else:
            active_targets = random.sample(targets, 2)

        # Intermission screen
        intermission_screen(win, joystick)

        # Run trial
        trial_res = run_trial(win, player, active_targets)
        trial_data.append(trial_res)
    
    print("Experiment complete!")
    return trial_data

