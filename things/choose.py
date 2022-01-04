def create(options, active_window):
	import os
	import time
	import keyboard
	import win32gui
	global menu_position
	global menu_pressed
	global menu_options
	global menu_active_window
	from colorama import init, Style
	init()
	os.system('things\\cursor.bat 0')
	print('\u001B[1A', end='\r')
	menu_active_window = active_window
	menu_options = options
	#os.system('title menu')
	menu_position = 0
	menu_pressed = False
	# keyboard on_press_key doesnt allow passing arguments
	# so have to use global -_-
	def process_key(key):
		global menu_position
		global menu_pressed
		global menu_options
		global menu_active_window
		if win32gui.GetForegroundWindow() == menu_active_window:
			if key.scan_code == 72:
				menu_position -= 1
			elif key.scan_code == 80:
				menu_position += 1
			elif key.scan_code == 28:
				menu_pressed = True

			if menu_position > len(options)-1:
				menu_position = 0
			if menu_position < 0:
				menu_position = len(options)-1
		else:
			keyboard.send(key.name)

	kup = keyboard.on_press_key('up', process_key, suppress=True) # up
	kdown = keyboard.on_press_key('down', process_key, suppress=True) # down
	kenter = keyboard.on_press_key('enter', process_key, suppress=True) # enter

	while True:
		time.sleep(0.05)

		for i in range(0, len(options)):
			if i == menu_position:
				print(f'{Style.RESET_ALL} -> ' + str(options[i]) + f'{Style.RESET_ALL}')
			else:
				print('    ' + str(options[i]) + f'{Style.RESET_ALL}   ')

		if menu_pressed:
			os.system('things\\cursor.bat 1')
			print('\u001B[1A', end='\r')
			keyboard.unhook(kup)
			keyboard.unhook(kdown)
			keyboard.unhook(kenter)
			return (options[menu_position], menu_position)

		print('\u001B[' + str(len(options)) + 'A', end='\r')