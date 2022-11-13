# Settings and experimental parameters to config specific experimental design values
# All values that need modification should be set here. 
# In order not to change original experiment code


params = dict(
    ##########################################################################
    ########                        SETTINGS                          ########
    ##########################################################################
    exp_name='Visual_Paired_Comparison',

    results_folder='./results/',

    display_size=(1800, 900),  # (1920, 1080), # in pixels

    fullscreen=False,

    # text_height = 2
    text_height=1,

    ##########################################################################
    ########                   EXERIMENTAL PARAMS                     ########
    ##########################################################################

    fixation_time=1,

    familiarization_time=5,

    delay=5,  # 120,

    test_time=5,

    iti=2,

)
