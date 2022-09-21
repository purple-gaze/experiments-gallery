# Settings and experimental parameters to config specific experimental design values
# All values that need modification should be set here. 
# In order not to change original experiment code


params = dict(

##########################################################################
########                        SETTINGS                          ########
##########################################################################
exp_name = 'Content_pictures',

results_folder = './results/' ,

stim_folder = './stims/',
    
#sets the experiment screen (0: primary screen, 1: secondary screen)
main_screen = 0,
#sets the message screen (-1: no messages, 0: primary screen, 1: secondary screen)
message_screen = 0,
#set 1 to show metadata info at the end of the experiment
show_metadata=1,

#make experiment fullscreen
fullscreen = False,

display_size = (1980, 1024), # in pixels



##########################################################################
########                   EXERIMENTAL PARAMS                     ########
##########################################################################
text_height = 1,

stim_size =  (1280, 960), #in pixels 

fixation_time = 1, #in seconds

stim_time = 6, #in seconds

iti = 1.0, #in seconds

)
