# Arduino Fitness Game Controller
This project showcases an innovative Arduino-based controller that simulates the left analog stick of a gamepad, enabling control of in-game movements through physical activity. The controller is designed to be mounted on the user's back and integrates with exercise equipment like treadmills, stationary bikes, and ellipticals.

## Watch the demo video on YouTube
[![Demo video of the project](https://github.com/iacoposk8/Arduino-Fitness-Game-Controller/blob/main/images/yt_play.jpg?raw=true)](https://www.youtube.com/watch?v=4EYHZWyAiZI)

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
The Controller.py file will simulate the Xbox joystick and by reading the data from the arduino it will move the left analog stick.

I still need to create a requirements.txt file, but these commands probably install all the dependencies:
```
pip install pyserial
pip install numpy
pip install vgamepad
pip install matplotlib
```
### Configurations

In the first lines that follow `def __init__(self):` there are a few variables to configure to make the best use of the controller.

When we run we have vertical and horizontal oscillations that we could represent graphically as a sinusoid.
However, when we use a joystick, if we want to go in a direction, for example forward, we will not intermittently tap our analog stick, but we will tilt it forward while keeping it in that position.
So, if we took the raw data from the accelerometer while we are running, our character would continue to stop and start turning right and left at each of our steps.
So the code takes a sample of measurements and makes an average.
The larger the sample, the fewer errors there will be, but there will be a delay in executing the command.

The lower the value, the less movement of the shoulders to turn
```
self.x_range = 0.8
```

Threshold which, if exceeded, will start the curve
```
self.x_threshold = 0.4
```

The lower the value, the lower the speed at which we should run to make our character go at maximum speed
```
self.y_max_speed = 2.5
```

Speed with which we want, walk, run and run fast
Speed with which we want, walk, run and fast run
Currently the fast run is activated by pressing the "A" button on the Xbox controller. If you want to change it just change the lines:
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
and
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
With one of the commands that can be found here:
[https://pypi.org/project/vgamepad](https://pypi.org/project/vgamepad).

```
self.speed = {
	"walk": 0.06,
	"run": 0.3,
	"fast_run": 0.7
}
```

The higher the value, the less the left analog stick y-position flickers, but the return to zero position will be slower
```
self.n_sample_x = 2
self.n_sample_y = 10
```

If set to True the code will automatically find the right port, if it doesn't work, set it to False and during execution it will show you all the ports to choose from
```
automatic_choice_port = True
```

Optional ability to enable various types of debugging with graphs and logs
```
self.show_value = False
self.show_plot = False
self.x_plot = 200
self.debug = True
```
