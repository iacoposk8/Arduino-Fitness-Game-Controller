#python -m pip install pyserial
import serial
import time
import json
import os
import traceback
import platform
import serial.tools.list_ports
import numpy as np
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import vgamepad as vg
gamepad = vg.VX360Gamepad()

class Accelerometer:
	def Action(self, line):
		self.xpos = float((sum(self.accy_sample) / len(self.accy_sample)) / self.x_range)
		
		if self.xpos > 1:
			self.xpos = 1.0
		if self.xpos < -1:
			self.xpos = -1.0
		if self.xpos < self.x_threshold and self.xpos > (self.x_threshold * -1):
			self.xpos = 0
		'''else:
			print(self.xpos)'''

		self.ypos = float((max(self.acc_sample) - 1) / self.y_max_speed)
		if self.ypos > 1:
			self.ypos = 1.0
		if self.ypos < -0:
			self.ypos = 0.0
		
		print(self.ypos)

		if self.show_plot:
			self.y["custom"].append(self.xpos)
			self.y["custom"] = self.y["custom"][(self.x_plot * -1):]
			self.lines["custom"].set_ydata(self.y["custom"])

	def move_joystick(self):
		while True:
			try:
				joystick_ypos = 0
				if self.ypos >= self.speed["walk"]:
					joystick_ypos = 1

				#print(self.xpos,self.ypos)
				gamepad.left_joystick_float(x_value_float=self.xpos, y_value_float=joystick_ypos)

				if self.ypos >= self.speed["run"]:
					gamepad.right_trigger_float(self.ypos)
				else:
					gamepad.right_trigger_float(0)

				if self.ypos >= self.speed["fast_run"]:
					gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
				else:
					gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
				
				gamepad.update()

				#gamepad.reset()
				#gamepad.update()
				
				if self.xpos == 0 and self.ypos == 0:
					#time.sleep(0.1)
					gamepad.reset()
					gamepad.update()
			except AttributeError:
				continue

			time.sleep(0.1)

	def __init__(self):
		#The lower the value, the less movement of the shoulders to turn
		self.x_range = 0.8 

		#threshold which, if exceeded, will start the curve
		'''self.x_curve_light_threshold = 0.4
		self.x_curve_strong_threshold = 0.8 '''
		self.x_threshold = 0.4
		
		#the lower the value, the lower the speed at which we should run to make our character go at maximum speed
		self.y_max_speed = 2.5

		self.speed = {
			"walk": 0.06,
			"run": 0.3,
			"fast_run": 0.7
		}
		
		#the higher the value, the less the left analog stick y-position flickers, but the return to zero position will be slower
		self.n_sample_x = 2
		self.n_sample_y = 10

		self.baudrate = 38400 #19200 31250 38400 57600 74880 115200
		self.show_value = False
		self.show_plot = False
		self.x_plot = 200
		self.debug = True
		automatic_choice_port = True

		#temp acc gyro accAngle gyroAngle angle
		self.data_type = "acc"

		self.acc_sample = []
		self.accy_sample = []
		
		ports = serial.tools.list_ports.comports()
		probable_port = 1
		if not automatic_choice_port:
			print("Ports:")
		for i in range(len(ports)):
			if "CH340" in ports[i]:
				probable_port = i
			if not automatic_choice_port:
				print("["+str(i)+"]",ports[i])

		if automatic_choice_port:
			port = probable_port
		else:
			port = input("Select the port: ")
		self.arduino = serial.Serial(port=str(ports[int(port)]).split("-")[0].strip(), baudrate=self.baudrate, timeout=0.1) #'/dev/ttyUSB0'

		self.maxVal = {
			"acc": 4,
			"gyro": 500,
			"accAngle": 150,
			"gyroAngle": 500,
			"angle": 500
		}

		if "Windows" in platform.system():
			clear_cmd = "cls"
		else:
			clear_cmd = "clear"
		self.clear = lambda: os.system(clear_cmd)

		#self.start()
		x = threading.Thread(target=self.read_sensor, args=())
		x.start()

		x = threading.Thread(target=self.move_joystick, args=())
		x.start()

		if self.show_plot:
			self.y = {"X": [0] * self.x_plot, "Y": [0] * self.x_plot, "Z": [0] * self.x_plot, "custom": [0] * self.x_plot}
			self.y["X"][0] = self.maxVal[self.data_type]
			self.y["X"][1] = self.maxVal[self.data_type] * -1

			fig = plt.figure()
			ax = fig.add_subplot(1, 1, 1)

			self.lines = {}
			self.lines["X"] = ax.plot(self.y["X"], animated=True)[0]
			self.lines["Y"] = ax.plot(self.y["Y"], animated=True)[0]
			self.lines["Z"] = ax.plot(self.y["Z"], animated=True)[0]
			self.lines["custom"] = ax.plot(self.y["custom"], animated=True)[0]

			ani = animation.FuncAnimation(fig, self.animate, interval=100, blit=True)
			plt.show()

	def animate(self, i):
		return [self.lines["X"], self.lines["Y"], self.lines["Z"], self.lines["custom"]]

	def read_sensor(self):
		start_time = 0
		read_start = False
		while True:
			try:
				line = self.arduino.readline()
				if not line:
					continue

				line = line.decode("utf-8").rstrip()
				if line == "":
					continue

				line = json.loads(line)

				if self.show_value:
					self.clear()

				#for cord in ["X", "Y", "Z"]:
				for cord in ["Y"]:
					par = self.data_type + cord
					if par in line:
						if self.show_value:
							print(par+": "+str(line[par]))

						if self.show_plot:
							self.y[cord].append(line[self.data_type + cord])
							self.y[cord] = self.y[cord][(self.x_plot * -1):]
							self.lines[cord].set_ydata(self.y[cord])

				accel_mag = np.sqrt((line["accX"] ** 2 + line["accY"] ** 2 + line["accZ"] ** 2))
				self.acc_sample.append(accel_mag)
				self.acc_sample = self.acc_sample[self.n_sample_y * -1:]

				self.accy_sample.append(line["accY"])
				self.accy_sample = self.accy_sample[self.n_sample_x * -1:]

				read_start = True

				self.Action(line)
				#time.sleep(1 / 115200)
				time.sleep(1 / self.baudrate)
			except json.decoder.JSONDecodeError:
				#print("ERROR")
				if read_start == False or self.debug:
					print(line)
			except UnicodeDecodeError:
				pass
			except KeyboardInterrupt:
				break
			except:
				traceback.print_exc()

Accelerometer()