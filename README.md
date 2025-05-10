This repository has 2 diffrent types of code arduino and python code.

dependencies for lython code:
ultralytics
pyserial


Most of the code is to do with computer vision. There is 2 trained models called best.pt and last.pt. You can you any of these since it depends on the situation which one is the best so just play around with it. All the code expect the arduino code in the folder called "MotersAndAll" works with computer vision AI.

There is 4 python apps and here is the instructions for each python app.


images.py: make sure the images folder exist and that there is images in it.

video.py: make shure the videos folder is there with videos.

webcam.py: make sure therenis a camera on the desktop you are ruining the code on.

arduino_test.py: Make sure there is a camera and that there is a arduino connected to the pc on the com3 port and using serial connection of 9600. and that the code called computervision.ino is uploaded on the conneted arduino.


MotersAndAll is the "dumb" code of this project there is almost no logic and no AI,just the moters move forward if nothing is in 10cm of the distance sensor and the cervo does a sweep every 5 seconds. This need a 12v of power to run since the moters needs a lots of voltage to start moving.