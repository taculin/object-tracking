# UPDATE: Bugs and fixes

## UPDATED 19Sep2018 1100H
- Updated [RAtools.exe](https://drive.google.com/file/d/1pbeZFwPtqcXQVSFYhjS631vZdC0FRajY/view?usp=sharing) for method 2 is now available for download. To activate autoframe by default:

    > RAtools click 00 ON

Toggle this value by pressing 'a' during execution.


## UPDATED 18Sep2018 2300H
- Incorporated the auto skip feature that was requested earlier. You can toggle the value to ON or OFF by pressing 'a' during execution. To activate by default, use the following commands for method 1.a, method 1.b, and method 2 respectively:
    > click('00',True)
    
    > python RAtools.py click 00 ON
    
    > RAtools click 00 ON



## UPDATED 18Sep2018 0900H
- Fixed Windows executable [RAtools.exe](https://drive.google.com/file/d/1pbeZFwPtqcXQVSFYhjS631vZdC0FRajY/view?usp=sharing) now available for download

## UPDATED 18Sep2018 0020H
- Enhanced RAclicker.py and [RAtools.exe](https://drive.google.com/file/d/1pbeZFwPtqcXQVSFYhjS631vZdC0FRajY/view?usp=sharing) to display status while extracting frames.
- Linux executable [RAtools](https://drive.google.com/file/d/1da5lnPgdgYCE7ag7tEKE2UCIrBQ4cMsl/view?usp=sharing)

## UPDATED 16Sep2018 1800H
Fixed bug (unable to extract frames) in files RAclicker.py for method 1 and [RAtools.exe](https://drive.google.com/file/d/1pbeZFwPtqcXQVSFYhjS631vZdC0FRajY/view?usp=sharing) for method 2. Both can be downloaded from this site.


# RAtools.py source file

## decom(fname)
Decomposes the video file into frames.
## click(fname)
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
- a toggles the auto frame skip configuration


## mapModel(fname)
Maps the current perspective to the target perspective by clicking the features from the current to the equiavalent feature to the target perspective. When it closes, the homography matrix H is computed and is saved in a file. Key commands:
- l  (small L or spaces) go to next frame
- r      go to next frame
- d deletes the last entry
- q,**esc** exit
## recon(fname, lastFr, scale)
This method transforms the ntxy to the target pespective, warp the frame, and reconstruct the video. The last frame number must be specified, as frames 0<=lastFr will be reconstructed. Also the output window can be scaled, with value 1 being default, 0.5 means half the size of the video window.

    > RAtools recon 00 10000 0.75
    
recontructs a video file 00 for frames 0 to 10000 and the image size is reduced to 75% of the original size.
Hint: The execution can be aborted anytime by hitting q or esc.


# RAtools Standalone File
Can be downloaded [here](https://drive.google.com/file/d/1pbeZFwPtqcXQVSFYhjS631vZdC0FRajY/view?usp=sharing). The purpose of this file is for freezing (executable). Functions can be invoked by specifying it at the command line during execution. If the name of the video is 00.mp4, then the functions are executed as follows:

    > RAtools decom 00
    > RAtools click 00 <ON>
    > RAtools map 00
    > RAtools recon 00 10000 0.75


