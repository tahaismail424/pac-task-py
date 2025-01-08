from psychopy import visual, event, core
from movement import MoveCalculator
import numpy as np

def run_trial(win, player, active_targets):
    # Frame rate for consistent motion
    frame_rate = 60
    dt = 1 / frame_rate
    clock = core.Clock()
    window_width = win.clientSize[0]
    window_height = win.clientSize[1]

    trial_duration = 20
    player_caught_prey = False

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
    active_targets[0].shape.pos = (0, -200)
    if len(active_targets) > 1:
        active_targets[1].shape.pos = (0, 200)

    # run game loop
    while clock.getTime() < trial_duration:
        keys = event.getKeys()
        if "escape" in keys:
            print("Pause filler")
        # move player according to joystick movement
        player.move()
        # adjust position for numpy vector space
        player_pos_x, player_pos_y = player.shape.pos[0] + window_width // 2, player.shape.pos[1] + window_height // 2
        player_pos = np.array([player_pos_x, player_pos_y])
        for target in active_targets:
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
                print(f"Hit {target.shape.fillColor} square!")
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