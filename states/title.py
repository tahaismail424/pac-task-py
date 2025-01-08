from psychopy import visual, event, core

def title_screen(win):
    # Create UI components
    title = visual.TextStim(
        win, 
        text="Welcome to Pac-man! Please confirm experimental setup",
        pos=(0, 250),
        height=40,
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
            win, text="Start Experiment", 
            pos=(0, -250), height=20, 
            color="white"
        ),
        "speed_slider": visual.Slider(
            win, 
            ticks=[1, 5, 10, 15, 20],
            labels=["1", "5", "10", "15", "20"],
            pos=(0, 150),
            granularity=1,
            style="rating",
            size=(0.8, 0.1)
        ),
        "speed_label": visual.TextStim(
            win, text="Prey Max Speed:", 
            pos=(-300, 150), 
            height=20, 
            color="white"
        ),
        "trials_input": visual.TextBox2(
            win, 
            text="10", 
            pos=(0, 50), 
            size=(150, 50),
            color="white",
            borderColor="white"
        ),
        "trials_label": visual.TextStim(
            win,
            text="Number of Trials:",
            pos=(-300, 50),
            height=20, 
            color="white"
        ),
        "spread_label": visual.TextStim(
            win, 
            text="Trial Type Distribution:",
            pos=(-300, -50),
            height=20,
            color="white"
        ),
        "spread_slider": visual.Slider(
            win,
            ticks=[0, 25, 50, 75, 100],
            labels=["0%", "25%", "50%", "75%", "100%"],
            pos=(0, -150),
            granularity=1,
            style="slider",
            size=(0.8, 0.1)
        ),
        "spread_text_left": visual.TextStim(
            win,
            text="Single-Prey",
            pos=(-300, -150),
            height=20,
            color="white"
        ),
        "spread_text_right": visual.TextStim(
            win,
            text="Multi-Prey",
            pos=(300, -150),
            height=20,
            color="white"
        )
    }
    
    # Default parameters
    params = {
        "speed": 10,
        "trials": 10,
        "trial_type_distribution": 50
    }

    # Main loop for title screen
    while True:
        title.draw()
        # draw all title components
        for component in components.values():
            component.draw()
        win.flip()

        # quit game loop on 'esc' press
        keys = event.getKeys()
        if "escape" in keys:
            core.quit()

        # respond to mouse clicks in UI components
        mouse = event.Mouse()
        # return func and pass params to experiment loop
        # if start button clicked
        if mouse.isPressedIn(components["start_button"]):
            params["speed"] = components["speed_slider"].markerPos
            params["trials"] = int(components["trials_input"].text)
            params["trial_type_distribution"] = components["spread_slider"].markerPos
            params["target_count"] = 5
            win.clearBuffer()
            return params # Pass parameters to game loop

