# Settings and experimental parameters to config specific experimental design values
# All values that need modification should be set here. 
# In order not to change original experiment code

params = dict(
    ##########################################################################
    ########                        SETTINGS                          ########
    ##########################################################################
    exp_name='Active_emotion_recognition',

    results_folder='./results/',

    display_size=(1980, 1024),  # in pixels,

    fullscreen=False,

    # text_height = 2,
    text_height=1,
    # sets the experiment screen (0: primary screen, 1: secondary screen)
    main_screen=0,
    # sets the message screen (-1: no messages, 0: primary screen, 1: secondary screen)
    message_screen=0,
    # set 1 to show metadata info at the end of the experiment
    show_metadata=1,

    ##########################################################################
    ########                   EXERIMENTAL PARAMS                     ########
    ##########################################################################

    fixation_time=1,

    stim_time=6,

    iti=1,

)
