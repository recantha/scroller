# Import necessary libraries
import os, glob, math, time, sys, socket, psutil

# Try to set-up Scroll pHAT, set flag if not available
try:
	import scrollphat
	scrollphat.set_brightness(30)
	scrollphat_connected = True
except:
	scrollphat_connected = False

# Try to connect to network and get IP. If not connected, set flag
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	ip = s.getsockname()[0]
	s.close()
	network_connected = True

except:
	ip = "Not connected"
	network_connected = False

# Set-up external temperature sensor
try:
	os.system("modprobe w1-gpio")
	os.system("modprobe w1-therm")
	base_dir = "/sys/bus/w1/devices"
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'
	temp = read_temp()
	ext_temperature_connected = True

except:
	ext_temperature_connected = False

def read_temp_raw():
	f = open(device_file, "r")
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	try:
		lines = read_temp_raw()
	
		while lines[0].strip()[-3:] != "YES":
			time.sleep(0.2)
			lines = read_temp_raw()
	
		equals_pos = lines[1].find("t=")
	
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			return temp_c, temp_f
		else:
			return -1.0,-1.0
	except:
		return -1.0,-1.0

def display(message):
	if scrollphat_connected:
		scrollphat.clear()
		scrollphat.write_string(message + "       ", 11)
		for i in range(0, scrollphat.buffer_len() - 11):
			scrollphat.scroll()
			time.sleep(0.08)
	else:
		print(message)
		time.sleep(0.1)

def get_system_temperature():
	f = os.popen("/opt/vc/bin/vcgencmd measure_temp")
	mytemp = ""
	for i in f.readlines():
		mytemp += i
		firstchar  = mytemp[5:-6]
		secondchar = mytemp[6:-5]
		thirdchar  = mytemp[8:-3]

	return firstchar + secondchar + "." + thirdchar + " C"

while True:
	# Display time if network is connected
	if network_connected:
		f = os.popen("date")
		for i in f.readlines():
			mytime = i[11:-13]
		display("Date: " + mytime)

	# Display IP if network is connected
	if network_connected:
		display("IP: " + ip)
	else:
		display("Not connected to network")

	# Get system temperature and display
	display("Sys temp: " + get_system_temperature())

	if ext_temperature_connected:
		temperature_c, temperature_f = read_temp()
		display("Ext temp: " + str(temperature_c) + " C / " + str(temperature_f) + " F")
		time.sleep(1)

sys.exit()
