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
    # my_dlg = gui.DlgFromDict(info_dict, title=params.exp_name,
    #                          order=order)
    # if my_dlg.OK == False:
    #     core.quit()  # user pressed cancel

    info_dict['date'] = data.getDateStr()
    info_dict['exp_name'] = 'passive_experiment'

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
                                 originPath='./passive_experiment.py',
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
                    calibration_object=calibration)  # we pass information to the experiment info of the session json file

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
                                       text=instructions.passive_instructions_text['1_initial_text'],
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
    trials = data.TrialHandler(trialList=data.importConditions('./passive_conditions.csv'), originPath=-1,
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
        neutral_stim = visual.ImageStim(win=win, image=trial['neutral'], size=[16, 12], pos=[-12 * target_side, 0])
        emotional_stim = visual.ImageStim(win=win, image=trial['emotional'], size=[16, 12], pos=[12 * target_side, 0])

        # log fixation
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

        # draw the visual stimuli faces and fixation cross
        # log neutural stimulus
        pg.log("ScreenIn", screenname=f"{trial['emotional_emotion']}: {scr_idlog}", screenid=scr_idlog,
               condition=trial['emotional_emotion'],
               duration=params['passive_stim_time'], trialname=f'trial_{trial_idlog}',
               sstims=[[trial['neutral'], [int(neutral_stim.size[0]), int(neutral_stim.size[1])],
                       [int(neutral_stim.pos[0]), int(neutral_stim.pos[1])]]])
        #
        # log emotional stimulus
        pg.log("ScreenIn", screenname=f"{trial['emotional_emotion']}: {scr_idlog}", screenid=scr_idlog,
               condition=trial['emotional_emotion'],
               duration=params['passive_stim_time'], trialname=f'trial_{trial_idlog}',
               stims=[[trial['emotional'], [int(emotional_stim.size[0]), int(emotional_stim.size[1])],
                       [int(emotional_stim.pos[0]), int(emotional_stim.pos[1])]]])

        neutral_stim.draw()
        emotional_stim.draw()
        fixation.draw()
        win.flip()



        # time of the stim in screen
        core.wait(params['passive_stim_time'])
        # Write BDF and metadata
        pg.log("ScreenOut", screenname=f"{trial['emotional_emotion']}: {scr_idlog}")
        # Flush the buffers
        kb.clearEvents()

        # Inter Trial Interval(ITI) with blank screen
        win.flip()

        core.wait(params['iti'])
        pg.log_event('End Trial')

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
                                  text=instructions.passive_instructions_text['5_goodbye_text'],
                                  wrapWidth=80)

    goodbye_msg.draw()
    win.flip()

    event.waitKeys(maxWait=params['passive_stim_time'], keyList=['space'])

    # Task shutdown
    pg.exit()
    win.close()

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
