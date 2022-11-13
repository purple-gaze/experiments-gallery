# Purple Gaze Antisaccade task
# Author: Tomas D'Amelio

if __name__ == "__main__":
    ########################################################################

    ##### PURPLE GAZE IMPORT ######
    from PurpleGaze import PurpleGaze
    from PurpleGazeAnalyzer import ReadPurpleGaze

    ##################################
    # Init Purple Gaze Calibration and Cameraview software
    # Experiment will start once calibration is finished
    calibration = PurpleGaze.calibration(validation = False, parameters = "C:\Purple Gaze Lab5")
    # calibration = None
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

    import random

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
    info_dict['exp_name'] = 'antisaccade'

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
                                 originPath='./antisaccade.py',
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
                        units='deg',
                        fullscr=params['fullscreen'],
                        color='black')

    info_dict['frame_rate'] = win.getActualFrameRate()

    # experimental info saved in metadata, used in final report
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
    # pg_filename = str(info_dict['Subject_id']) + '.bdf'
    pg = PurpleGaze(path=subject_folder, subject_id=str(info_dict['Subject_id']),
                    message_screen=params['message_screen'],
                    exp_info=exp_info,
                    calibration_object=calibration)
    pg.exp_info.update(params)
    pg.exp_info.update(info_dict)

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
                                       text=instructions.instructions_text['initial_text'],
                                       wrapWidth=80)

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
    trials = data.TrialHandler(trialList=data.importConditions('./antisacc_conditions.csv'), originPath=-1,
                               nReps=1, method='random', name='test')

    exp.addLoop(trials)

    pg.log('Annotation', txt='Test Block begun')
    scr_idlog = 0
    trial_idlog = 0

    # Loop over trials handler
    for trial in trials:
        # Create fixation cross 2
        fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                                      tex=None, mask='cross', size=2)

        # create visual stim for emotional and neutral faces
        cue_side = random.choice([-1, 1])  # randomization of position in screen of each stimulus
        cue_circle = visual.Circle(win=win, radius=0.5, edges=32, fillColor=trial['color'], size=3,
                                   pos=[-12 * cue_side, 0])

        rect_left = visual.Rect(win=win, fillColor=None, lineColor='white', size=3, pos=[-12, 0])
        rect_right = visual.Rect(win=win, fillColor=None, lineColor='white', size=3, pos=[12, 0])

        # Draw fixation
        # Log BDF and metadata
        pg.log("ScreenIn", screenname=f'Fixation: {scr_idlog}', screenid=scr_idlog, trialname=f'trial_{trial_idlog}',
               stims=[['fixation_cross', [int(fixation.size[0]), int(fixation.size[1])],
                       [int(fixation.pos[0]), int(fixation.pos[1])]]])
        fixation.draw()
        win.flip()
        core.wait(params['fixation_time'])
        # Write BDF and metadata
        pg.log("ScreenOut", screenname=f'Fixation: {scr_idlog}')

        # Log BDF and metadata
        pg.log("ScreenIn", screenname=f"{trial['trial']}: {scr_idlog}", screenid=scr_idlog,
               condition=trial['color'], duration=params['cue_time'], trialname=f'trial_{trial_idlog}')
        # draw the visual stimuli faces and fixation cross
        cue_circle.draw()
        fixation.draw()
        rect_left.draw()
        rect_right.draw()

        win.flip()
        core.wait(params['cue_time'])
        # Write BDF and metadata
        pg.log("ScreenOut", screenname=f"{trial['trial']}: {scr_idlog}")

        # Flush the buffers
        kb.clearEvents()

        rect_left.draw()
        rect_right.draw()
        win.flip()
        # No need to log stim out here
        # pg.log_stim(name='target', duration=params['target_time'])
        core.wait(params['target_time'])

        # Inter Trial Interval(ITI) with blank screen
        win.flip()
        # Log when the stim dissapears from screen to the BDF
        # pg.log_stim_out()

        core.wait(params['iti'])
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
                                  text=instructions.instructions_text['goodbye_text'],
                                  wrapWidth=80)

    goodbye_msg.draw()
    win.flip()

    event.waitKeys(maxWait=params['cue_time'], keyList=['space'])

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
