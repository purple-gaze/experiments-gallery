# Settings and experimental parameters to config specific experimental design values
# All values that need modification should be set here. 
# In order not to change original experiment code


params = dict(
    ##########################################################################
    ########                        SETTINGS                          ########
    ##########################################################################
    exp_name='Sliding_window',

    results_folder='./results/',

    display_size=(1920, 1080),  # in pixels

    fullscreen=True,

    # sets the experiment screen (0: primary screen, 1: secondary screen)
    main_screen=0,
    # sets the message screen (-1: no messages, 0: primary screen, 1: secondary screen)
    message_screen=0,
    # set 1 to show metadata info at the end of the experiment
    show_metadata=1,

    # text_height = 2
    text_height=35,

    ##########################################################################
    ########                   EXERIMENTAL PARAMS                     ########
    ##########################################################################

    aperture_size=500,

    aperture_speed=0.5

)
