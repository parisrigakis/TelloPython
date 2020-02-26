# TelloPython (Tested on Windows 7/10)

## Tello Face Recognition Follow Mode
Clone/Download all the files in the repository. Having all the files on the same folder run FollowFace.py.
The drone will take off and start looking for a face to follow, the video feed will be visible on the computer screen
on an opencv window. If a face is not found after 15 seconds the drone will land. If you want to quit the follow mode and
save the captured video press the ESCAPE key while having the opencv window open.
### Requirements
+ python 2.7.16
+ pygame 1.9.6
+ opencv-python 3.4.2.17

## Tello Dynamic Obstacle Avoidance
Clone/Download the standalone tello_colision.py script and run it. The drone will take off and hover at 1 meter above the ground.
You can try to collide with the drone gently and it will relocate properly. Press CTRL+C on the command window running the script and the drone will land after a short delay.
### Requirements
+ python 2.7.16
