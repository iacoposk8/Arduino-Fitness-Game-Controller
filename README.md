# Arduino Fitness Game Controller
This project showcases an innovative Arduino-based controller that simulates the left analog stick of a gamepad, enabling control of in-game movements through physical activity. The controller is designed to be mounted on the user's back and integrates with exercise equipment like treadmills, stationary bikes, and ellipticals.

## Watch the demo video on YouTube
[![Demo video of the project](https://img.youtube.com/vi/4EYHZWyAiZI/0.jpg)](https://www.youtube.com/watch?v=4EYHZWyAiZI)

![Demo gif of the project](https://github.com/iacoposk8/Arduino-Fitness-Game-Controller/blob/main/images/controller.gif?raw=true)

## How to use

### Requirements

* Arduino nano
* GY-521 MPU-6050 accelerometer

### Electrical connections
<img src="https://github.com/iacoposk8/Arduino-Fitness-Game-Controller/blob/main/images/arduino.jpg?raw=true" alt="Electrical connections" width="584" height="auto">


### Arduino code
Upload the code from the Accelerometer.ino file to your Arduino.
This code simply reads the accelerometer and sends the data to the serial port which will then be read by Controller.py

### Controller code
The Controller.py file will simulate the xbox joystick and by reading the data from the arduino it will move the left analog stick.

I still need to create a requirements.txt file, but these commands probably install all the dependencies:
```
pip install pyserial
pip install numpy
pip install vgamepad
pip install matplotlib
```
