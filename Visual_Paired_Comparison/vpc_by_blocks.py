# Purple Gaze Passive Emotion Recognition Task
# Author: Tomas D'Amelio

if __name__ == "__main__":
    ########################################################################

    ##### PURPLE GAZE IMPORT ######
    from PurpleGaze import PurpleGaze
    from PurpleGazeAnalyzer import ReadPurpleGaze, MakeReport

    ##################################
    # Init Purple Gaze Calibration and Cameraview software
    # Experiment will start once calibration is finished
    calibration = PurpleGaze.calibration(validation=False, parameters="C:\Purple Gaze Lab5")
    calibration = None
    # Cameraview is supposed to keep running in background
    # PurpleGaze.cameraview() #second monitor
    ##################################

    from psychopy import core, visual, data, event, gui
    # from psychopy.preferences import prefs
    from psychopy.hardware import keyboard

    # import random 
    import os
    import time

    from params import params
    import instructions

    import random

    ########################################################################
    # GUI for subject information

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
    # Instantiate dialog box
    my_dlg = gui.DlgFromDict(info_dict, title=params['exp_name'],
                             order=order)
    if my_dlg.OK == False:
        core.quit()  # user pressed cancel

    info_dict['date'] = data.getDateStr()
    info_dict['exp_name'] = params['exp_name']

    ##########################################################################
    # Experiment data settings

    # create folder to save experiment data for each subject
    subject_folder = params['results_folder'] + f"{info_dict['Subject_id']}/"

    os.makedirs(subject_folder, exist_ok=True)

    # Name of .csv file to save the data
    file_name = info_dict['Subject_id'] + '_' + \
                params['exp_name'] + '_' + info_dict['date']

    # Create experiment handler
    exp = data.ExperimentHandler(name=params['exp_name'],
                                 # version='0.1',
                                 extraInfo=info_dict,
                                 runtimeInfo=True,
                                 originPath='./vpc_by_blocks.py',
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

    # info for metadata and final report
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

    # 'q' to quit experiment
    event.globalKeys.add(key='q', func=core.quit, name='shutdown')
    # setting keyboard for experiment
    kb = keyboard.Keyboard()

    pg.log('Annotation', txt='Expt Started')

    ##########################################################################
    ########                 FAMILIARIZATION BLOCK                    ########
    ##########################################################################

    # Create test instructions ('text' visual stimulus)
    instruction_test = visual.TextStim(win,
                                       height=params['text_height'],
                                       pos=[0, 0],
                                       text=instructions.passive_instructions_text['familiar_text'],
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

    ### TRIAL BEGIN #####
    # Create trial handler
    trials = data.TrialHandler(trialList=data.importConditions('./familiarization_conditions.csv'), originPath=-1,
                               nReps=1, method='random', name='familiarization')

    exp.addLoop(trials)

    pg.log('Annotation', txt='Familiarisation Block begun')
    scr_idlog = 0
    trial_idlog = 0

    # Loop over trials handler
    for trial in trials:
        # Create fixation cross 2
        fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                                      tex=None, mask='cross', size=2)

        # create visual stim
        right_stim = visual.ImageStim(win=win, image=trial['stim'], size=[16, 12], pos=[-12, 0])
        left_stim = visual.ImageStim(win=win, image=trial['stim'], size=[16, 12], pos=[12, 0])

        # Log BDF and metadata
        pg.log("ScreenIn", screenname=f'Fixation: {scr_idlog}', screenid=scr_idlog, trialname=f'trial_{trial_idlog}',
               stims=[['fixation_cross', [int(fixation.size[0]), int(fixation.size[1])],
                       [int(fixation.pos[0]), int(fixation.pos[1])]]])
        # Draw fixation
        pg.log_event('Fixation')
        fixation.draw()
        win.flip()
        core.wait(params['fixation_time'])
        # Write BDF and metadata
        pg.log("ScreenOut", screenname=f'Fixation: {scr_idlog}')

        # Log BDF and metadata
        pg.log("ScreenIn", screenname=f"{trial['stim']}: {scr_idlog}", screenid=scr_idlog,
               duration=params['familiarization_time'], trialname=f'trial_{trial_idlog}',
               stims=[[trial['stim'], [int(left_stim.size[0]), int(left_stim.size[1])], [int(left_stim.pos[0]), int(left_stim.pos[1])]]])
        # draw the visual stimuli faces and fixation cross
        right_stim.draw()
        left_stim.draw()
        win.flip()

        # time of the stim in screen
        core.wait(params['familiarization_time'])
        # log information of the stimuli to the eytracker BDF file
        pg.log("ScreenOut", screenname=f"{trial['stim']}: {scr_idlog}")


        # Flush the buffers
        kb.clearEvents()

        # Inter Trial Interval(ITI) with blank screen
        win.flip()
        # stims dissapear from Screen

        core.wait(params['iti'])

        scr_idlog += 1
        trial_idlog += 1
        exp.nextEntry()

    pg.log('Annotation', txt='Familiarisation Block ended')

    ##########################################################################
    ########                 TEST BLOCK                    ########
    ##########################################################################

    # Create test instructions ('text' visual stimulus)
    instruction_test = visual.TextStim(win,
                                       height=params['text_height'],
                                       pos=[0, 0],
                                       text=instructions.passive_instructions_text['test_text'],
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

    ### TRIAL BEGIN #####
    # Create trial handler
    trials = data.TrialHandler(trialList=data.importConditions('./test_conditions.csv'), originPath=-1,
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
        target_side = random.choice([-1, 1])  # randomization of position in screen of each stimulus
        familiar_stim = visual.ImageStim(win=win, image=trial['familiar'], size=[16, 12], pos=[-12 * target_side, 0])
        novel_stim = visual.ImageStim(win=win, image=trial['novel'], size=[16, 12], pos=[12 * target_side, 0])
        exp.addData('pos_image ', target_side)

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
        pg.log("ScreenIn", screenname='stim', screenid=scr_idlog,
               duration=params['test_time'], trialname=f'trial_{trial_idlog}',
               stims=[[trial['familiar'], [int(familiar_stim.size[0]), int(familiar_stim.size[1])],
                       [int(familiar_stim.pos[0]), int(familiar_stim.pos[1])]]])
        pg.log("ScreenIn", screenname='stim', screenid=scr_idlog,
               duration=params['test_time'], trialname=f'trial_{trial_idlog}',
               stims=[[trial['novel'], [int(novel_stim.size[0]), int(novel_stim.size[1])],
                       [int(novel_stim.pos[0]), int(novel_stim.pos[1])]]])

        # draw the visual stimuli faces and fixation cross
        familiar_stim.draw()
        novel_stim.draw()
        win.flip()

        # time of the stim in screen
        core.wait(params['test_time'])
        pg.log("ScreenOut", screenname='stim')


        # Flush the buffers
        kb.clearEvents()

        # Inter Trial Interval(ITI) with blank screen
        win.flip()
        # stims dissapear from Screen

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
                                  text=instructions.passive_instructions_text['goodbye_text'],
                                  wrapWidth=80)

    goodbye_msg.draw()
    win.flip()

    event.waitKeys(maxWait=params['iti'], keyList=['space'])

    # Task shutdown
    win.close()
    pg.exit(show_metadata=params['show_metadata'])

    ############ OPTIONAL: Converting BDF file to CSV #############
    # Clock to quit bdf before trying to open it
    # Some computers take more or less time in closing the file.
    # change it accordingly if error "file has already been opened"
    time.sleep(60)

    ReadPurpleGaze(pg.subject_id + '.bdf', pg.subject_id, subject_folder)
    csv_file = subject_folder + pg.subject_id + '_PG_formatted.csv'
    MakeReport(csv_file, report_path=subject_folder, subject_id=pg.subject_id)
    ################################################################

    # Finish psychopy thread
    core.quit()
