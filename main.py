from psychopy import visual, event
import argparse
from datetime import datetime
import os
import numpy as np
from states.experiment import run_experiment
from states.title import title_screen

# parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Run the experiment and save outputs.")
    parser.add_argument("--output-dir", required=False, help="Path to the output directory")
    return parser.parse_args()

# create experiment folder
def create_experiment_folder(output_dir, start_time, end_time):
    folder_name = f"experiment_{start_time}_to_{end_time}"
    experiment_path = os.path.join(output_dir, folder_name)
    os.makedirs(experiment_path, exist_ok=True)
    return experiment_path

# save experiment data - pandas df as csv and numpy arrays as .npy
def save_experiment_data(output_path, trial_data_df, player_positions, prey_positions):
    # save DataFrame
    trial_data_path = os.path.join(output_path, "trial_data.csv")
    trial_data_df.to_csv(trial_data_path, index=False)

    # save numpy arrays
    player_positions_path = os.path.join(output_path, "player_positions.npy")
    prey_positions_path = os.path.join(output_path, "prey_positions.npy")
    np.save(player_positions_path, player_positions)
    np.save(prey_positions_path, prey_positions)

if __name__ == "__main__":
    # parse args
    args = parse_args()

    # Create game window
    win = visual.Window(size=(800, 600), color=(0, 0, 0), units="pix")
    
    # run game loop
    running = True
    while running:
        keys = event.getKeys()
        if "escape" in keys:
            running = False

        # record experiment start time
        start_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # run experiment with params specified in title
        params = title_screen(win)
        experiment_out = run_experiment(win, params)
        win.flip()

        # record experiment end
        end_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # create output folder
        output_dir = args.output_dir if args.output_dir else f'{os.path.dirname(os.path.abspath(__file__))}/default_outputs'
        experiment_folder = create_experiment_folder(
            output_dir, start_time, end_time
            )

        # save data
        save_experiment_data(
            experiment_folder,
            experiment_out[0],
            experiment_out[1],
            experiment_out[2]
            )

        