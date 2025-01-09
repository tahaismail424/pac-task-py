import numpy as np
import pandas as pd
import random
import sdl2
from psychopy.hardware import keyboard
from objects import Player, Target
from states.trial import run_trial
from states.intermission import intermission_screen

def run_experiment(win, params):
    """Runs the experiment loop and collects data for n trials"""
    # Initialize experiment variables
    n_trials = params["trials"] if params["trials"] else 10
    prey_speed = params["speed"] if params["speed"] else 9
    trial_type_distribution = params["trial_type_distribution"] if params["trial_type_distribution"] else 50
    target_count = params["target_count"] if params["target_count"] else 5
    allow_dupes = params["allow_dupes"] if params["allow_dupes"] else False

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

    cur_speed = prey_speed
    # create targets and player
    # initialize objects
    player = Player(win, joystick, kb)
    colors = ["red", "aqua", "pink", "orange", "blue"]
    # randomlize color order
    np.random.shuffle(colors)
    delta_speed = prey_speed / 5
    targets = []
    for target_number in range(5):
        target = Target(win, color=colors[target_number], start_pos=(0, 0), speed=cur_speed)
        targets.append(target)
        cur_speed -= delta_speed
    targets_3 = targets.copy()
    targets_3.pop(1)
    targets_3.pop(-2)

    # Initialize trial-level DataFrame and arrays
    trial_data_df = pd.DataFrame(
        columns=["trial_type", "prey_colors", 
                 "prey_speeds", "prey_caught", 
                 "result", "time_elapsed"]
        )
    trial_player_arrs = []
    trial_prey_arrs = []

    # experiment loop
    for trial_index, trial_type in enumerate(trials):
        # Prepare for trial
        print(f"Starting Trial {trial_index + 1}: {trial_type}")
        if target_count == 5:
            if trial_type == "single":
                active_targets = random.sample(targets, 1)
            elif trial_type == "multi" and allow_dupes:
                active_targets = random.choices(targets, k=2)
            else:
                active_targets = random.sample(targets, 2)
        elif target_count == 3:
            if trial_type == "single":
                active_targets = random.sample(targets_3, 1)
            elif trial_type == "multi" and allow_dupes:
                active_targets = random.choices(targets_3, k=2)
            else:
                active_targets = random.sample(targets_3, 2)

        # Intermission screen
        intermission_screen(win, joystick)

        # Run trial
        trial_row, trial_player_arr, trial_prey_arr = run_trial(win, player, active_targets)
        trial_data_df = pd.concat([trial_data_df, trial_row], ignore_index=True)
        trial_player_arrs.append(trial_player_arr)
        trial_prey_arrs.append(trial_prey_arr)
    
    print("Experiment complete!")
    return (trial_data_df, np.array(trial_player_arrs), np.array(trial_prey_arrs))

