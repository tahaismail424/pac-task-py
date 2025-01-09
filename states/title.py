from psychopy import visual, event, core

def title_screen(win):
    """Title screen that appears at the start of every experiment run"""
    # Create UI components
    title = visual.TextStim(
        win, 
        text="Welcome to Pac-man! Please confirm experimental setup",
        pos=(0, 250),
        height=20,
        color="white"
        )
    components = {
        "start_button": visual.Rect(
            win, 
            width=200, height=50, 
            fillColor="green", 
            pos=(0, -250)
        ),
        "start_text": visual.TextStim(
            win, 
            text="Start Experiment", 
            pos=(0, -250), height=20, 
            color="white"
        ),
         "speed_input": visual.TextBox2(
            win, 
            text="5", 
            editable=True,
            pos=(0, 175), 
            size=(150, 50),
            color="white",
            borderColor="white"
        ),
        "speed_label": visual.TextStim(
            win, 
            text="Prey Max Speed:", 
            pos=(-300, 175), 
            height=20, 
            color="white",
        ),
          "speed_label_2": visual.TextStim(
            win, 
            text="NOTE: player max speed = 10",
            pos=(225, 175),
            height=20,
            color="white"
        ),
        "trials_input": visual.TextBox2(
            win, 
            text="10", 
            editable=True,
            pos=(0, 100), 
            size=(150, 50),
            color="white",
            borderColor="white"
        ),
        "trials_label": visual.TextStim(
            win,
            text="Number of Trials:",
            pos=(-300, 100),
            height=20, 
            color="white"
        ),
        "spread_label_1": visual.TextStim(
            win, 
            text="Trial Type Distribution",
            pos=(-300, 0),
            height=20,
            color="white"
        ),
        "spread_label_2": visual.TextStim(
            win, 
            text="0 = 100% single prey",
            pos=(200, 20),
            height=20,
            color="white"
        ),
         "spread_label_3": visual.TextStim(
            win, 
            text="100 = 100% multi prey",
            pos=(200, -20),
            height=20,
            color="white"
        ),
         "spread_input": visual.TextBox2(
            win, 
            text="50", 
            editable=True,
            pos=(0, 0), 
            size=(150, 50),
            color="white",
            borderColor="white"
        ),
        
        "prey_label": visual.TextStim(
            win, 
            text="Prey Options:",
            pos=(-300, -75),
            height=20,
            color="white"
        ),
        "prey_slider": visual.Slider(
            win,
            ticks=[0, 1],
            labels=["3", "5"],
            pos=(0, -75),
            granularity=1,
            style="rating",
            size=(100, 20)
        ),
         "dupe_label": visual.TextStim(
            win, 
            text="Allow Duplicate Prey:",
            pos=(-300, -150),
            height=20,
            color="white"
        ),
        "dupe_slider": visual.Slider(
            win,
            ticks=[0, 1],
            labels=["No", "Yes"],
            pos=(0, -150),
            granularity=1,
            style="rating",
            size=(100, 20)
        ),
        
    }
    
    # Default parameters
    params = {
        "speed": 10,
        "trials": 10,
        "trial_type_distribution": 50,
        "target_count": 5,
        "allow_dupes": False
    }

    # Main loop for title screen
    while True:
        title.draw()
        # draw all title components
        for component in components.values():
            component.draw()
        win.flip()

        # check for valid mouser esponses on slider
        # components["speed_slider"].getMouseResponses()

        # quit game loop on 'esc' press
        keys = event.getKeys()
        if "escape" in keys:
            core.quit()

        # respond to mouse clicks in UI components
        mouse = event.Mouse()
        # return func and pass params to experiment loop
        # check mouse cl
        # if start button clicked
        if mouse.isPressedIn(components["start_button"]):
            params["speed"] = int(components["speed_input"].text)
            params["trials"] = int(components["trials_input"].text)
            params["trial_type_distribution"] = int(components["spread_input"].text)
            params["target_count"] = 3 if components["prey_slider"].markerPos == 0 else 5
            params["allow_dupes"] = bool(components["dupe_slider"].markerPos)
            win.clearBuffer()
            print(params)
            return params # Pass parameters to game loop

