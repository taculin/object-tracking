#UPDATE:
UPDATED THE [RAtools.exe] (https://drive.google.com/file/d/1pbeZFwPtqcXQVSFYhjS631vZdC0FRajY/view?usp=sharing) file. Please download this version as of 16 Sep 2018 1800H.



# RAclicker
## decom(fname)
Decomposes the video file into frames.
## clicker(fname)
Collects ground truth by clicking moving vehicles. The result is an ntxy file. The following are the key commands:
- l,' '  (small L or spaces) go to next frame
- r      go to next frame
- f skip to frame (user input)
- \+ increment car number
- \- decrement car number
- c skip to car number (user input)
- d deletes the last entry
- s save to disk
- z jump to frame of last entry
- q,**esc** exit

# RAmapper
## mapModel(fname)
Maps the current perspective to the target perspective by clicking the features from the current to the equiavalent feature to the target perspective. When it closes, the homography matrix H is computed and is saved in a file. Key commands:
- l  (small L or spaces) go to next frame
- r      go to next frame
- d deletes the last entry
- q,**esc** exit
## recon(fname, lastFr, scale)
This method transforms the ntxy to the target pespective, warp the frame, and reconstruct the video. The last frame number must be specified, as frames 0<=lastFr will be reconstructed. Also the output window can be scaled, with value 1 being default, 0.5 means half the size of the video window.



# RAtools

This is the RAclicker and RAmapper combined which can be downloaded [here](https://drive.google.com/file/d/1pbeZFwPtqcXQVSFYhjS631vZdC0FRajY/view?usp=sharing). The purpose of this file is for freezing (executable). Functions can be invoked by specifying it at the command line during execution. If the name of the video is 00.mp4, then the functions are executed as follows:

    > RAtools decom 00
    > RAtools click 00
    > RAtools map 00
    > RAtools recon 10000 0.75


