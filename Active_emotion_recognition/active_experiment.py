# Purple Gaze Active Emotion Recognition task
# Author: Tomas D'Amelio

if __name__ == "__main__":
    ########################################################################

    ##### PURPLE GAZE IMPORT ######
    from PurpleGaze import PurpleGaze
    from PurpleGazeAnalyzer import ReadPurpleGaze, MakeReport

    ##################################
    # Init Purple Gaze Calibration and Cameraview software
    # Experiment will start once calibration is finished
    calibration = PurpleGaze.calibration(validation = False, parameters = "C:\Purple Gaze Lab5")
    # calibration = None
    # Cameraview is supposed to keep running in background
    # PurpleGaze.cameraview() #second monitor
    ##################################

    from psychopy import core, visual, data, event, constants
    # from psychopy.preferences import prefs
    from psychopy.hardware import keyboard

    # import random 
    import os
    import time

    from params import params
    import instructions

    import numpy as np

    ########################################################################
    # GUI for subject information

    # Form
    info_dict = {
        'Subject_id': 'S6',
        'Age': 21,
        'Gender': ['Male', 'Female', 'Non-binary', 'Rather not say'],
        'Group': ['Test', 'Control'],
    }

    # Order of forms
    order = ['Subject_id', 'Age', 'Gender', 'Group']

    ### UNCOMMENT THIS TO USE THE FORMS. It's commented for practicity.###
    # Instantiate dialog box
    # my_dlg = gui.DlgFromDict(info_dict, title=params.exp_name,
    #                          order=order)
    # if my_dlg.OK == False:
    #     core.quit()  # user pressed cancel

    info_dict['date'] = data.getDateStr()

    ##########################################################################
    # Experiment data settings

    # create folder to save experiment data for each subject
    subject_folder = subject_folder = params['results_folder'] + f"{info_dict['Subject_id']}/"

    os.makedirs(subject_folder, exist_ok=True)

    # Name of .csv file to save the data
    file_name = info_dict['Subject_id'] + '_' + \
                params['exp_name'] + '_' + info_dict['date']

    #########################################################################
    # Create experiment handler
    exp = data.ExperimentHandler(name=params['exp_name'],
                                 # version='0.1',
                                 extraInfo=info_dict,
                                 runtimeInfo=True,
                                 originPath='./active_experiment.py',
                                 savePickle=True,
                                 saveWideText=True,
                                 dataFileName=subject_folder + file_name)

    ##########################################################################
    # Set stimuli
    # Basic emotion names
    basic_emotions = {'1': '1. Anger', '2': '2. Fear', '3': '3. Disgust',
                      '4': '4. Joy', '5': '5. Sadness', '6': '6. Surprise'}

    # Basic emotion positions
    pos_basic_emotions = [(-7.0, 4.0), (0.0, 4.0), (7.0, 4.0),
                          (-7.0, -4.0), (0.0, -4.0), (7.0, -4.0)]

    # pos_basic_emotions = [(-18.0, 18.0), (-18.0, 0.0),
    #   (-18.0, -18.0), (18.0, 18.0), (18.0, 0.0), (18.0, -18.0)]

    ##########################################################################
    # Create a window
    win = visual.Window(allowGUI=None,
                        size=params['display_size'],
                        monitor='testMonitor',
                        winType='pyglet',
                        useFBO=True,
                        # units='pix',
                        units='deg',
                        fullscr=params['fullscreen'],
                        color='black')

    info_dict['frame_rate'] = win.getActualFrameRate()

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
    ########                    PRACTICE BLOCK                        ########
    ##########################################################################

    # Create practice instructions ('text' visual stimuli)
    for _, value in sorted(instructions.active_instructions_text.items())[:3]:
        instruction_practice = visual.TextStim(win,
                                               height=params['text_height'],
                                               pos=[0, 0],
                                               text=value,
                                               wrapWidth=80)
        instruction_practice.draw()
        # Flip the front and back buffers
        win.flip()

        # To begin the Experimetn with Spacebar or RightMouse Click
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
    practice_trials = data.TrialHandler(
        trialList=data.importConditions('./active_practice_conditions.csv'),
        originPath=-1, nReps=1, method='random', name='practice')

    exp.addLoop(practice_trials)

    pg.log('Annotation', txt='Practice Block begun')
    scr_idlog = 0
    trial_idlog = 0

    # Loop over trials handler
    for trial in practice_trials:

        # Create fixation cross 2
        fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                                      tex=None, mask='cross', size=2)

        # Create visual stimulus for emotional faces
        mov = visual.MovieStim3(win=win, filename=trial['movie_path'],
                                size=(1024, 768), pos=[0, 0], noAudio=True)

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

        # Flush the buffers
        kb.clearEvents()

        # Clock reset
        kb.clock.reset()

        # log information of the stimuli to the eytracker BDF file
        pg.log("ScreenIn", screenname=f"{trial['movie_path']}: {scr_idlog}", screenid=scr_idlog,
               condition=trial['emotion'],
               duration=params['stim_time'], trialname=f'trial_{trial_idlog}',
               stims=[[trial['movie_path'], [int(mov.size[0]), int(mov.size[1])], [int(mov.pos[0]), int(mov.pos[1])]]])

        while mov.status != constants.FINISHED:
            mov.draw()
            win.flip()
            keys = kb.getKeys(['space'], waitRelease=True)
            if keys:
                # log BDF and metadata
                pg.log('Annotation', txt='Response given ' + str(keys))
                practice_trials.addData('RT_space', [key.rt for key in keys][0])
                break

        # Write BDF and metadata
        pg.log("ScreenOut", screenname=f"{trial['movie_path']}: {scr_idlog}")


        # Draw visual stimulus for emotional faces
        pg.log('Annotation', txt='Emotions presented')
        for emotion, position in zip(basic_emotions.values(), pos_basic_emotions):
            emotion_response = visual.TextStim(
                win, text=str(emotion), height=params['text_height'],
                pos=position)
            emotion_response.draw()

        win.flip()

        # Get key response
        key, rt = event.waitKeys(keyList=basic_emotions.keys(),
                                 timeStamped=core.Clock())[0]
        # log response
        pg.log('Annotation', txt='Response key and rt'+str(key)+','+str(rt))

        practice_trials.addData('emotion_key', key)
        practice_trials.addData('emotion_rt', rt)

        # Get correct/incorrect response
        if str(key) == str(trial['correct_response']):
            response = 'correct'
        else:
            response = 'incorrect'
        practice_trials.addData('response', response)

        # Inter Trial Interval(ITI) with blank screen
        win.flip()
        core.wait(params['iti'])

        scr_idlog += 1
        trial_idlog += 1
        exp.nextEntry()

    pg.log('Annotation', txt='Practice Block ended')

    ##########################################################################
    ########                        TEST BLOCK                        ########
    ##########################################################################

    # Create test instructions ('text' visual stimulus)
    instruction_test = visual.TextStim(win,
                                       height=params['text_height'],
                                       pos=[0, 0],
                                       text=instructions.active_instructions_text['4_test_text'],
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
    trials = data.TrialHandler(
        trialList=data.importConditions('./active_conditions.csv'),
        originPath=-1, nReps=1, method='random', name='test')

    exp.addLoop(trials)

    pg.log('Annotation', txt='Test Block begun')
    scr_idlog = 0
    trial_idlog = 0

    # Loop over trials handler
    for trial in trials:

        # Create fixation cross 2
        fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                                      tex=None, mask='cross', size=2)

        # Create visual stimulus for emotional faces
        mov = visual.MovieStim3(win=win, filename=trial['movie_path'], size=(
            1024, 768), pos=[0, 0], noAudio=True)

        # Draw fixation
        pg.log("ScreenIn", screenname=f'Fixation: {scr_idlog}', screenid=scr_idlog, trialname=f'trial_{trial_idlog}',
               stims=[['fixation_cross', [int(fixation.size[0]), int(fixation.size[1])],
                       [int(fixation.pos[0]), int(fixation.pos[1])]]])
        fixation.draw()
        win.flip()
        core.wait(params['fixation_time'])
        # log fixation
        pg.log("ScreenOut", screenname=f'Fixation: {scr_idlog}')


        # Flush the buffers
        kb.clearEvents()

        # Clock reset
        kb.clock.reset()

        # log information of the stimuli to the eytracker BDF file
        pg.log("ScreenIn", screenname=f"{trial['movie_path']}: {scr_idlog}", screenid=scr_idlog,
               condition=trial['emotion'],
               duration=params['stim_time'], trialname=f'trial_{trial_idlog}',
               stims=[[trial['movie_path'], [int(mov.size[0]), int(mov.size[1])], [int(mov.pos[0]), int(mov.pos[1])]]])

        while mov.status != constants.FINISHED:
            mov.draw()
            win.flip()
            keys = kb.getKeys(['space'], waitRelease=True)
            if keys:
                pg.log('Annotation', txt='Response given ' + str(keys))
                trials.addData('RT_space', [key.rt for key in keys][0])
                break

        # Write BDF and metadata
        pg.log("ScreenOut", screenname=f"{trial['movie_path']}: {scr_idlog}")

        # Draw visual stimulus for emotional faces
        pg.log('Annotation', txt='Emotions presented')
        for emotion, position in zip(basic_emotions.values(), pos_basic_emotions):
            emotion_response = visual.TextStim(
                win, text=str(emotion), height=params['text_height'],
                pos=position)
            emotion_response.draw()

        win.flip()

        # Get key response
        key, rt = event.waitKeys(keyList=basic_emotions.keys(),
                                 timeStamped=core.Clock())[0]
        pg.log('Annotation', txt='Response key and rt'+str(key)+','+str(rt))

        trials.addData('emotion_key', key)
        trials.addData('emotion_rt', rt)

        # Get correct/incorrect response
        if str(key) == str(trial['correct_response']):
            response = 'correct'
        else:
            response = 'incorrect'
        trials.addData('response', response)

        # Inter Trial Interval(ITI) with blank screen
        win.flip()
        core.wait(params['iti'])
        scr_idlog += 1
        trial_idlog += 1
        exp.nextEntry()

    pg.log('Annotation', txt='Test Block ended')

    # trials.saveAsText(fileName= subject_folder + file_name + '.csv')

    ##########################################################################
    ###################### Feedback + Goodbye message ######################## 
    kb.clearEvents()
    n_corr = np.count_nonzero(trials.data['response'] == 'correct')
    if n_corr == 1:
        msg_trial = 'trial'
    else:
        msg_trial = 'trials'
    msg = "You got %i %s correct!" % (n_corr, msg_trial)

    feedback_msg = visual.TextStim(win,
                                   height=params['text_height'],
                                   pos=[0, +6],
                                   text=msg,
                                   wrapWidth=80)

    goodbye_msg = visual.TextStim(win,
                                  height=params['text_height'],
                                  pos=[0, -6],
                                  text=instructions.active_instructions_text['5_goodbye_text'],
                                  wrapWidth=80)

    feedback_msg.draw()
    goodbye_msg.draw()
    win.flip()

    event.waitKeys(maxWait=params['stim_time'], keyList=['space'])

    # Task shutdown
    pg.exit()
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
