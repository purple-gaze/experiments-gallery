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
    calibration = PurpleGaze.calibration(validation = False, parameters = "C:\Purple Gaze Lab5")
    # calibration = None
    # Cameraview is supposed to keep running in background
    # PurpleGaze.cameraview() #second monitor
    ##################################
    

    from psychopy import core, visual, data,event, gui
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
<<<<<<< HEAD
    # my_dlg = gui.DlgFromDict(info_dict, title=params['exp_name'],
    #                          order=order)
    # if my_dlg.OK == False:
    #     core.quit()  # user pressed cancel
=======
    my_dlg = gui.DlgFromDict(info_dict, title=params['exp_name'],
                             order=order)
    if my_dlg.OK == False:
        core.quit()  # user pressed cancel
>>>>>>> 87a5515e444a02dac226f668343575e78dec647f

    info_dict['date'] = data.getDateStr()
    info_dict['exp_name'] = params['exp_name']

    ##########################################################################
    # Experiment data settings

    # create folder to save experiment data for each subject
    subject_folder = params['results_folder'] + f"{info_dict['Subject_id']}/"

    os.makedirs(subject_folder, exist_ok = True)

    # Name of .csv file to save the data
    file_name = info_dict['Subject_id'] + '_' + \
        params['exp_name'] + 'by_trial_' + '_' + info_dict['date']
        

    # Create experiment handler
    exp = data.ExperimentHandler(name=params['exp_name'] + 'by_trial',
                                # version='0.1',
                                extraInfo=info_dict,
                                runtimeInfo=True,
                                originPath='./vcp_by_trials.py',
                                savePickle=True,
                                saveWideText=True,
                                dataFileName= subject_folder + file_name)



    ##########################################################################
    # Create a window
    win = visual.Window(allowGUI=False,
                        size= params['display_size'],
                        monitor='testMonitor',
                        winType= 'pyglet',
                        useFBO= True, 
                        units='deg',
                        fullscr=params['fullscreen'],
                        color='black')
    

    info_dict['frame_rate'] = win.getActualFrameRate()


    ############## TO RUN IN MAC AND LINUX ##############
    # if os.name == 'posix':
    #     launchHubServer(window=win)
    #####################################################

    # 'q' to quit experiment
    # event.globalKeys.add(key='q', func=core.quit, name='shutdown')
    # setting keyboard for experiment
    kb = keyboard.Keyboard()
    
    ##########################################################################
    # init PurpleGaze
    # pg_filename = str(info_dict['Subject_id']) + '.bdf'
    pg = PurpleGaze(path = subject_folder , subject_id = str(info_dict['Subject_id']), handle_messages=True, calibration_object=calibration)
    # we pass information to the experiment info of the session json file
    pg.exp_info.update(params)
    pg.exp_info.update(info_dict)


    
    ##########################################################################
    ########                      BLOCK                              ########
    ##########################################################################

    # Create test instructions ('text' visual stimulus)
    instruction_test = visual.TextStim(win,
                                    height=params['text_height'],
                                    pos=[0, 0],
                                    text=instructions.passive_instructions_text['by_trial_text'],
                                    wrapWidth=80)

    # Draw test instructions
    instruction_test.draw()

    # Flip the front and back buffers
    win.flip()

    # To begin the Experimetn with Spacebar or LeftMouse Click
    press_button = True
    while press_button:
        keys = event.getKeys(keyList =['space'])
        
        mouse = event.Mouse(visible = False, win = win)
        mouse_click = mouse.getPressed()
        
        if 'space' in keys or 1 in mouse_click:
            press_button = False
        
    # Wait until 'space' is pressed
    # event.waitKeys(keyList=['space',], timeStamped=False)


    ### TRIAL BEGIN #####
    # Create trial handler
    trials = data.TrialHandler(trialList=data.importConditions('./test_conditions.csv'), originPath=-1,
                            nReps=1, method='random', name = 'vcp_by_trial')

    exp.addLoop(trials)

    pg.log_event('Expt Started')

    pg.log_event('Test Block begun')
    # Loop over trials handler
    for trial in trials:
        # Create fixation cross 2
        fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                                    tex=None, mask='cross', size=2)
        
        #create visual stim
        right_stim = visual.ImageStim(win=win, image= trial['familiar'], size=[16,12], pos=[-12,0])
        left_stim = visual.ImageStim(win=win, image= trial['familiar'], size=[16,12], pos=[12,0])

        # Draw fixation
        pg.log_event('Fixation')
        fixation.draw()
        win.flip()
        core.wait(params['fixation_time'])
        
        #draw the visual stimuli faces and fixation cross
        right_stim.draw()
        left_stim.draw()
        win.flip()
        
        #log information of the stimuli to the eytracker BDF file
        # as we have two stims, here we can pass one as stim name and the other as condition
        pg.log_stim(name = trial['familiar'], condition = 'familiarization', duration = params['familiarization_time'])
        # TO DO: include log of position
        
        #time of the stim in screen
        core.wait(params['familiarization_time'])

        # Flush the buffers
        kb.clearEvents()

        # Inter Phase Interval(IPI) with blank screen
        win.flip()
        #Log when the stim dissapears from screen to the BDF
        pg.log_stim_out()
        
        core.wait(params['delay'])
        pg.log_event('End Familiarization')

        #create visual stim for emotional and neutral faces
        target_side= random.choice([-1,1]) # randomization of position in screen of each stimulus
        familiar_stim = visual.ImageStim(win=win, image= trial['familiar'], size=[16,12], pos=[-12 * target_side,0])
        novel_stim = visual.ImageStim(win=win, image= trial['novel'], size=[16,12], pos=[12 * target_side,0])
        exp.addData('pos_image ', target_side)

        # Draw fixation
        # pg.log_event('Fixation')
        # fixation.draw()
        # win.flip()
        # core.wait(params['fixation_time'])
        
        #draw the visual stimuli faces and fixation cross
        familiar_stim.draw()
        novel_stim.draw()
        win.flip()
        
        #log information of the stimuli to the eytracker BDF file
        # as we have two stims, here we can pass one as stim name and the other as condition
        pg.log_stim(name = trial['familiar']+ trial['novel'], condition = 'test', duration = params['test_time'])
        # TO DO: include log of position
        
        #time of the stim in screen
        core.wait(params['test_time'])

        # Flush the buffers
        kb.clearEvents()

        # Inter Trial Interval(ITI) with blank screen
        win.flip()
        # stims dissapear from Screen
        
        #Log when the stim dissapears from screen to the BDF
        pg.log_stim_out()
        
        core.wait(params['iti'])
        pg.log_event('End Test')
        
        exp.nextEntry()

    pg.log_event('Test Block ended')

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
    pg.exit()
    win.close()

    ############ OPTIONAL: Converting BDF file to CSV #############
    # Clock to quit bdf before trying to open it
    # Some computers take more or less time in closing the file.
    # change it accordingly if error "file has already been opened"
    time.sleep(60)

    ReadPurpleGaze(pg.subject_id + '.bdf', pg.subject_id, subject_folder)
    csv_file = subject_folder + pg.subject_id + '_PG_formatted.csv'
    MakeReport(csv_file, report_path =subject_folder, subject_id =  pg.subject_id)
    ################################################################

    # Finish psychopy thread
    core.quit()

