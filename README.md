# Purple Gaze Example Experiments

 This repository was done to provide different examples on how to integrate the [Purple Gaze](https://purplegaze.io/) python module for eye-tracking recording to different experiments programmed using the python library psychopy. The experiments in this repository are replicates of previously published experiments.

To run without eye-tracking device run first:

    gladius_test_server.py

**Requirements:**

- `purple_gaze_module`
- `psychopy >= 2020.1.2`

---------
# Experiments on this repository

- Antisaccade
- Content pictures
- Facial emotion recognition
  - Active experiment (with videos)
  - Passive experiment (with images)
- Sliding Window
- Visual Paired Comparison

All experiments have a README file of their own to look into more deeply.
## Antisaccade

In the anti-saccade task, the participant begins each trial by looking at a fixation cross. Then, a stimulus appears on the side of the screen. When this happens, the participant must look to the other side of the screen, inhibiting the saccade reflex. Failures in such inhibition are related to neurological disorders at the level of the frontal cortex.

## Content pictures

The content picture experiment is a really basic experiment in which two kind (urban vs natural) of complex figures are displayed for 6s, one at a time. Participants are asked to only attentively observe each picture.

## Facial emotion recognition

### Passive Experiment

This eye-tracking paradigm is known as the "emotional face task". It simply consists of the simultaneous presentation of two faces to the participants, on the left and the right side of the screen. One of these faces has emotional content, while the other is a neutral facial expression

### Active Experiment

In this experiment, twelve emotional videos corresponding to six basic emotions (i.e. anger, fear, disgust, joy, sadness, and surprise) are presented. After each presentation, participants are required to recognize the emotional expression.

## Sliding Windows
.
## Visual Paired Comparison

This task consists on showing two identical stimuli at the same time to participants in a familiarization phase. And in a second phase of testing, participants are shown only 1 familiar stimulus along side a new novel stimulus. In this phase participants are expected to take more time looking at the novel stimulus than the familiar one. This task has two versions programmed `By trial` and `By blocks` where the way of switching between familiarization and test changes.
