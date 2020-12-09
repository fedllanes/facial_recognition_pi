# Facial recognizition using a raspberry pi.
#### ------------------------------------------------------------------------------------
#### Warning: This was my first ever proyect, the coding practices used may not be the best. I was a complete begginer at the time of making this.
#### There's a full report in word report in spanish in the repository.
#### ------------------------------------------------------------------------------------

This proyect uses a raspberry pi 3B and its camera to detect people, to for example, open a door. 
The idea of this proyect is to make a script where you can add new users, tweak the parameters and pick a GPIO pin to activate once a face has been detected. Everything will be saved on a log, and users can also be deleted at any time. There's a terminal interface to make things simpler. 

## Requirements 

* A Raspberry Pi Model 3 or superior. 
* A camera module 

## Installation

Once you are in your raspberry pi terminal, you need to execute the following commands to install all the necessary dependencies. 

* sudo apt-get update && sudo apt-get upgrade 
* sudo apt-get install build-essential cmake unzip pkg-config 
* sudo apt-get install libjpeg-dev libpng-dev libtiff-dev 
* sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev 
* sudo apt-get install libxvidcore-dev libx264-dev 
* sudo apt-get install libgtk-3-dev 
* sudo apt-get install libcanberra-gtk* 
* sudo apt-get install libatlas-base-dev gfortran 
* wget https://bootstrap.pypa.io/get-pip.py 
* sudo python3 get-pip.py 
* sudo pip3 install numpy 
* sudo apt-get install python3-opencv 
* sudo apt-get install libboost-all-dev 
* sudo pip3 install scipy 
* sudo pip3 install scikit-image 
* sudo pip3 install dlib 
* sudo pip3 install face_recognition 
* sudo pip3 install imutils 
* git clone https://github.com/fedllanes/facial_recognition_pi.git 
