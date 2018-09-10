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
## recon(fname)
This is supposed to transform the ntxy to the target pespective, warp the frame, and reconstruct the video
