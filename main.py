#!/usr/bin/env python

import os, math, time, scrollphat, sys, socket, psutil

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ip = s.getsockname()[0]
s.close()

#print(ip)

i = 0

scrollphat.set_brightness(30)

while True:
	scrollphat.clear()
	f = os.popen("date")
	for i in f.readlines():
		mytime = i[11:-13]
	scrollphat.write_string("Time: " + mytime + "     ", 11)
	for i in range(0, scrollphat.buffer_len() - 11):
		scrollphat.scroll()
		time.sleep(0.08)

	scrollphat.clear()
	scrollphat.write_string("IP: " + ip + "    ", 11)
	for i in range(0, scrollphat.buffer_len() - 11):
		scrollphat.scroll()
		time.sleep(0.08)
	

	scrollphat.clear()
	f = os.popen("/opt/vc/bin/vcgencmd measure_temp")
	mytemp = ""
	for i in f.readlines():
		mytemp += i
		firstchar  = mytemp[5:-6]
		secondchar = mytemp[6:-5]
		thirdchar  = mytemp[8:-3]
	scrollphat.write_string("System temperature: " + firstchar + secondchar + "." + thirdchar + " C       ", 11)
	for i in range(0, scrollphat.buffer_len()-11):
		scrollphat.scroll()
		time.sleep(0.08)
sys.exit()
