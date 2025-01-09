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
        "speed_slider": visual.Slider(
            win, 
            ticks=[0, 2.5, 5, 7.5, 10],
            labels=["0", "2.5", "5", "7.5", "10"],
            pos=(0, 175),
            granularity=0,
            style="slider",
            size=(300, 20)
        ),
        "speed_label": visual.TextStim(
            win, 
            text="Prey Max Speed:", 
            pos=(-300, 175), 
            height=20, 
            color="white",
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
        "spread_label": visual.TextStim(
            win, 
            text="Trial Type Distribution:",
            pos=(0, 25),
            height=20,
            color="white"
        ),
        "spread_slider": visual.Slider(
            win,
            ticks=[0, 25, 50, 75, 100],
            #labels=["0%", "25%", "50%", "75%", "100%"],
            pos=(0, 0),
            granularity=0,
            style="slider",
            size=(300, 20)
        ),
        "spread_text_left": visual.TextStim(
            win,
            text="Single-Prey",
            pos=(-300, 0),
            height=20,
            color="white"
        ),
        "spread_text_right": visual.TextStim(
            win,
            text="Multi-Prey",
            pos=(300, 0),
            height=20,
            color="white"
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
            ticks=[3, 5],
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
            params["speed"] = components["speed_slider"].markerPos
            params["trials"] = int(components["trials_input"].text)
            params["trial_type_distribution"] = components["spread_slider"].markerPos
            params["target_count"] = components["prey_slider"].markerPos
            params["allow_dupes"] = bool(components["dupe_slider"].markerPos)
            win.clearBuffer()
            print(params)
            return params # Pass parameters to game loop

