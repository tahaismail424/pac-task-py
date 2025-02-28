from psychopy import event, core, visual
from movement import MoveCalculator
import numpy as np
import pandas as pd

def run_trial(win, player, active_targets):
    """Runs a single trial of the pacman game"""
    # Frame rate for consistent motion
    frame_rate = 60
    dt = 1 / frame_rate
    clock = core.Clock()
    window_width = win.clientSize[0]
    window_height = win.clientSize[1]

    trial_duration = 20
    player_caught_prey = False
    prey_caught = None

    # create move calculator object
    move_calculator = MoveCalculator(
        window_width, window_height, 10, 
        {
            "wall": 6,
            "position": 5,
            "player_distance": 1.5,
            "npc_distance": 0.5,
            "momentum": 0.33
        }
    )

    # set positions
    player.shape.pos = (0, 0)
    active_targets[0].shape.pos = (-200, -200)
    if len(active_targets) > 1:
        active_targets[1].shape.pos = (200, 200)

    # initialize numpy arrays
    player_positions = np.empty((60 * 20, 2))
    prey_positions = np.empty((60 * 20, 2, 2))

    frame = 0
    paused = False
    # run game loop
    while clock.getTime() < trial_duration:
        # Handle keyboard inputsinputs
        keys = event.getKeys()
        if "escape" in keys:
            core.quit()  # Exit game
        if "p" in keys:
            paused = not paused  # Toggle pause state
        
        # handle pause loop
        if paused:
            # Draw the shapes in current pos
            player.shape.draw()
            for target in active_targets:
                target.shape.draw()

            # draw pause overlay
            pause_text = visual.TextStim(win, text="| |", height=40, color="white", pos=(0, 0))
            pause_text.draw()
            win.flip()

            # Wait until "p" is pressed again
            while True:
                keys = event.getKeys()
                if "p" in keys:
                    paused = False
                    break
                core.wait(0.1)  # Avoid busy waiting
            
            # Resume trial clock
            clock.reset(clock.getTime())  # Adjust clock to preserve elapsed time

        # move player according to joystick movement
        player.move()
        # adjust position for numpy vector space
        player_pos_x, player_pos_y = player.shape.pos[0] + window_width // 2, player.shape.pos[1] + window_height // 2
        player_pos = np.array([player_pos_x, player_pos_y])
        player_positions[frame] = player_pos
        for index, target in enumerate(active_targets):
            # record prey position
            target_pos_x, target_pos_y = target.shape.pos[0] + window_width // 2, target.shape.pos[1] + window_height // 2
            prey_positions[frame, index] = np.array([target_pos_x, target_pos_y])

            # first populate pos of other NPCs
            other_pos = []
            for target2 in active_targets:
                if target2 == target:
                    continue
                else:
                    other_pos_x, other_pos_y = target2.shape.pos[0] + window_width // 2, target2.shape.pos[1] + window_height // 2
                    other_pos.append(np.array([other_pos_x, other_pos_y]))
            target.move(move_calculator, player_pos=player_pos, other_npcs=other_pos)

            # check for cllisions
            if target.check_collision(player):
                player_caught_prey = True
                prey_caught = target
                print(f"Hit {target.color_name} square!")
                break
        
        # cut loop if player catches prey
        if player_caught_prey:
            break
            
        # Draw objects
        win.clearBuffer()
        player.shape.draw()
        for target in active_targets:
            target.shape.draw()
        
        win.flip()
        core.wait(dt)
        frame += 1
    
    # save and return trial data
    # Record trial result
    trial_result = {
        "trial_type": "multi" if len(active_targets) > 1 else "single",
        "prey_colors": " ".join([target.color_name for target in active_targets]),
        "prey_speeds": " ".join([str(target.speed) for target in active_targets]),
        "prey_caught": None,
        "result": "success" if player_caught_prey else "timeout",
        "time_elapsed": clock.getTime(),
    }
    # add prey caught speeed if prey was caught
    if player_caught_prey:
        trial_result["prey_caught"] = prey_caught.speed

    return pd.DataFrame(trial_result, index=[0]), player_positions, prey_positions