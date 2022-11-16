# Purple Gaze Experiments Gallery

This repository includes examples on how to integrate the [Purple Gaze](https://purplegaze.io/) python module for eye-tracking recording to various experiments programmed using the python library PsychoPy. The experiments in this repository are replicates of previously published experiments.

To run without eye-tracking device run first:

    gladius_test_server.py

**Requirements:**

- `purple_gaze_module`
- `psychopy >= 2020.1.2`

---------
# Experiments in this repository

- Anti-Saccade
- Content pictures
- Facial emotion recognition
  - Active experiment (with videos)
  - Passive experiment (with images)
- Sliding Window
- Visual Paired Comparison

All experiments have a README file of their own to look into more deeply.

## Anti-Saccade

In the Anti-Saccade task, the participant begins each trial by looking at a fixation cross. A cue appears that hints to the participant where the stimulus is going to appear. Then, a stimulus appears on the side of the screen. The stimulus is either a green or a red circle. When the green circle appears, the participant should make an eye movement toward the green circle (”Pro-Saccade”). But when the red circle appears, the participant must look to the other side of the screen, inhibiting the saccade reflex (”Anti-Saccade”). Failures in such inhibition are related to neurological disorders at the level of the frontal cortex (Wilcockson et al., 2019). 

## Content pictures

In this experiment, 2 categories of complex images are displayed: natural and urban images. Participants are instructed to carefully observe the images for 6 seconds. Images are presented in a random order.

## Facial emotion recognition

### Passive Experiment

This eye-tracking paradigm is known as the "emotional face task". It simply consists of the simultaneous presentation of two faces to the participants, on the left and the right side of the screen. One of these faces has emotional content, while the other is a neutral facial expression.

### Active Experiment

In this experiment, twelve emotional videos corresponding to six basic emotions (i.e. anger, fear, disgust, joy, sadness, and surprise) are presented. After each presentation, participants are required to recognize the emotional expression.

## Sliding Window

This sliding window experiment is adapted from Samadani et al. (2016) and Samadani et al. (2015) for concussion detection. The participants begin the trial by reading the instructions on the screen. During the trial, a grey mask with a square aperture will cover the entire screen. Behind the mask, a selected video will be played without audio sounds as the aperture slides along the edges of the screen at a fixed speed. The participants are asked to watch the video through this moving aperture. Disconjugate eye movements have been associated with structural brain damage and concussion (Samadani et al. 2015). The aperture should be around 1/8 the size of the screen. Both the aperture size and speed are tunable in the script.

## Visual Paired Comparison

The experimental task is an adapted version of the Visual Paired Comparison methodology described in different articles trying to automatically assess dementia such as Bott et al, (2017) and Crutcher et al, (2009).

This eye-tracking paradigm is known as the "Visual Paired Comparison" or VPC. In this task participants are first shown two identical stimuli, this phase is called `Familiarization`. Afterward, in a second phase called `Test` participants are shown at the same time one of the previously seen 'familiar' stimuli and one unseen stimulus, the 'novel' one.
