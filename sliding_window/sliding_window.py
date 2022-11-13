# Purple Gaze sliding window task
# Author: Lucy(Mingfang) Zhang

if __name__ == "__main__":
    ########################################################################

    ##### PURPLE GAZE IMPORT ######
    from PurpleGaze import PurpleGaze
    from PurpleGazeAnalyzer import ReadPurpleGaze

    ##################################
    # Init Purple Gaze Calibration and Cameraview software
    # Experiment will start once calibration is finished
    # calibration = PurpleGaze.calibration(validation = False, parameters = "C:\Purple Gaze Lab5")
    calibration = None
    # Cameraview is supposed to keep running in background
    # PurpleGaze.cameraview() #second monitor
    ##################################

    from psychopy import core, visual, data, event
    # from psychopy.preferences import prefs
    from psychopy.hardware import keyboard

    # import random
    import os
    import time

    from params import params
    import instructions

    ########################################################################
    # GUI form for subject information

    # Form
    info_dict = {
        'Subject_id': 'S10',
        'Age': 21,
        'Gender': ['Male', 'Female', 'Non-binary', 'Rather not say'],
        'Group': ['Test', 'Control'],
    }

    # Order of forms
    order = ['Subject_id', 'Age', 'Gender', 'Group']

    ### UNCOMMENT THIS TO USE THE FORMS. It's commented for coding practicity.###
    # # Instantiate dialog box
    # my_dlg = gui.DlgFromDict(info_dict, title=params.exp_name,
    #                          order=order)
    # if my_dlg.OK == False:
    #     core.quit()  # user pressed cancel

    info_dict['date'] = data.getDateStr()
    info_dict['exp_name'] = 'sliding_window'

    ##########################################################################
    # Experiment data settings

    # create folder to save experiment data for each subject
    subject_folder = params['results_folder'] + f"{info_dict['Subject_id']}/"

    os.makedirs(subject_folder, exist_ok=True)

    # Name of .csv file to save the data
    file_name = info_dict['Subject_id'] + '_' + \
                params['exp_name'] + '_' + info_dict['date']

    ##########################################################################
    # Create experiment handler
    exp = data.ExperimentHandler(name=params['exp_name'],
                                 # version='0.1',
                                 extraInfo=info_dict,
                                 runtimeInfo=True,
                                 originPath='./sliding_window.py',
                                 savePickle=True,
                                 saveWideText=True,
                                 dataFileName=subject_folder + file_name)

    ##########################################################################
    # Create a window
    win = visual.Window(allowGUI=False,
                        size=params['display_size'],
                        monitor='testMonitor',
                        winType='pyglet',
                        useFBO=True,
                        units='pix',
                        fullscr=params['fullscreen'],
                        color='black',
                        allowStencil=True)

    info_dict['frame_rate'] = win.getActualFrameRate()

    # info saved in metadata used for final report
    exp_info = {'fullscreen': params['fullscreen'],
                'main_screen': params['main_screen'],
                'display_size': params['display_size'],
                }
    exp_info.update(info_dict)

    ############## TO RUN IN MAC AND LINUX ##############
    # if os.name == 'posix':
    #     launchHubServer(window=win)
    #####################################################

    ##########################################################################
    # init PurpleGaze
    pg = PurpleGaze(path=subject_folder, subject_id=str(info_dict['Subject_id']),
                    message_screen=params['message_screen'],
                    exp_info=exp_info,
                    calibration_object=calibration)

    # 'q' to quit experiment
    event.globalKeys.add(key='q', func=core.quit, name='shutdown')
    # setting keyboard for experiment
    kb = keyboard.Keyboard()

    pg.log('Annotation', txt='Expt Started')

    ##########################################################################
    ########                        TEST BLOCK                        ########
    ##########################################################################

    # Create test instructions ('text' visual stimulus)
    instruction_test = visual.TextStim(win,
                                       height=params['text_height'],
                                       pos=[0, 0],
                                       text=instructions.sliding_instructions_text['initial_text'],
                                       wrapWidth=params['display_size'][0] - 200)

    # Draw test instructions
    instruction_test.draw()

    # Flip the front and back buffers
    win.flip()

    # To begin the Experimetn with Spacebar or LeftMouse Click
    press_button = True
    while press_button:
        keys = event.getKeys(keyList=['space'])

        mouse = event.Mouse(visible=False, win=win)
        mouse_click = mouse.getPressed()

        if 'space' in keys or 1 in mouse_click:
            press_button = False

    # Wait until 'space' is pressed
    # event.waitKeys(keyList=['space',], timeStamped=False)

    # Create trial handler
    trials = data.TrialHandler(trialList=data.importConditions('./sliding_window.csv'), originPath=-1,
                               nReps=1, method='random', name='test')

    exp.addLoop(trials)

    pg.log('Annotation', txt='Test Block begun')
    scr_idlog = 0
    trial_idlog = 0

    # Loop over trials handler
    for trial in trials:

        if event.getKeys('q'):
            win.close()
            core.quit()

        # get vid stimulus
        trialClock = core.Clock()
        movie = visual.MovieStim3(
            win=win, name='movie', units='',
            noAudio=False,
            filename=trial['vid_path'],
            ori=0.0, pos=(0, 0), opacity=None,
            loop=False, anchor='center',
            depth=-3.0,
        )

        # draw aperture
        monitor_width, monitor_height = params['display_size']

        aper_size = params['aperture_size']  # get aperture size from params file
        aperture = visual.Aperture(win, size=aper_size, shape='square',
                                   pos=(-(monitor_width / 2 - aper_size / 2), monitor_height / 2 - aper_size / 2))


        # function that gives moving aperture
        def get_aper_pos(trial_time, speed, a=monitor_width, b=monitor_height):  # speed is pixels
            total_dist = trial_time * 1000 * speed
            relative_dist = total_dist % (2 * (a + b - aper_size * 2))
            if relative_dist <= a - aper_size:
                x = relative_dist - (a / 2 - aper_size / 2)
                y = b / 2 - aper_size / 2
            elif a - aper_size <= relative_dist <= a + b - aper_size * 2:
                x = a / 2 - aper_size / 2
                y = b / 2 - aper_size / 2 - (relative_dist - (a - aper_size))
            elif a + b - aper_size * 2 <= relative_dist <= 2 * a + b - aper_size * 3:
                x = a / 2 - aper_size / 2 - (relative_dist - (a + b - aper_size * 2))
                y = -(b / 2 - aper_size / 2)
            elif 2 * a + b - aper_size * 3 <= relative_dist <= 2 * (a + b - aper_size * 2):
                x = - (a / 2 - aper_size / 2)
                y = b / 2 - aper_size / 2 - (2 * (a + b - aper_size * 2) - relative_dist)
            return x, y


        # Draw vid
        pg.log_event('vid start')
        win.flip()

        # start trialclock
        trialClock.reset()
        while trialClock.getTime() < trial['time']:
            aperture.enabled = True
            aperture.pos = get_aper_pos(trialClock.getTime(), params['aperture_speed'])
            # log information of the stimuli to the eyetracker BDF file
            # here instead of logging movie position and size, log aperture position and size
            pg.log("ScreenIn", screenname=f"{trial['vid_path']}: {scr_idlog}", screenid=scr_idlog,
                   duration=trial['time'], trialname=f'trial_{trial_idlog}',
                   stims=[
                       [trial['vid_path'], [int(aperture.size[0]), int(aperture.size[1])],
                        [int(aperture.pos[0]), int(aperture.pos[1])]]])

            # gaze_dot.draw()
            movie.draw(win)
            win.flip()
        pg.log("ScreenOut", screenname=f"{trial['vid_path']}: {scr_idlog}")

        aperture.enabled = False

        # Flush the buffers
        kb.clearEvents()

        # Inter Trial Interval(ITI) with blank screen
        win.flip()
        # Log when the stim dissapears from screen to the BDF
        scr_idlog += 1
        trial_idlog += 1
        exp.nextEntry()

    pg.log('Annotation', txt='Test Block ended')

    # trials.saveAsText(fileName= subject_folder + file_name + '.csv')

    ##########################################################################
    ###################### Feedback + Goodbye message ########################
    kb.clearEvents()

    goodbye_msg = visual.TextStim(win,
                                  height=params['text_height'],
                                  pos=[0, -0],
                                  text=instructions.sliding_instructions_text['goodbye_text'],
                                  wrapWidth=params['display_size'][0] - 200)

    goodbye_msg.draw()
    win.flip()

    event.waitKeys(maxWait=2, keyList=['space'])

    # Task shutdown
    pg.exit()

    # close psychopy windowd
    win.close()
    pg.exit(show_metadata=params['show_metadata'])

    ############ OPTIONAL: Converting BDF file to CSV #############
    # Clock to quit bdf before trying to open it
    # Some computers take more or less time in closing the file.
    # change it accordingly if error "file has already been opened"
    time.sleep(60)

    ReadPurpleGaze(pg.subject_id + '.bdf', pg.subject_id, subject_folder)
    csv_file = subject_folder + pg.subject_id + '_PG_formatted.csv'
    # MakeReport(csv_file, report_path=subject_folder, subject_id=pg.subject_id)
    ################################################################

    # Finish psychopy thread
    core.quit()
