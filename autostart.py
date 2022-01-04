import os
import time
from things import choose, admin
import win32gui
import win32con
import win32process
import keyboard
import mouse
import sys as sus # amogus
import json
import requests
import pystray
import psutil
import traceback
from colorama import init, Fore, Back, Style
import threading
from PIL import Image
import subprocess
init()

# required to detect mouse and keyboard events on programs running with admin perms

checkadmin = True

try:
	if checkadmin: admin.forceadmin(__file__)
except SystemExit:
	sus.exit(0)
except:
	print('admin is required to detect mouse and keyboard events in programs running with admin perms!')
	print('also required for afterburner profile changing to work')
	print('if u want to disable this function, change checkadmin variable in the code to False')
	os.system('pause')
	sus.exit(0)

# this works most of the time
# get the window required for choose prompts and make sure its the correct one
# now this wont work if user alt tabs to another console window with the title saloading... but oh well who does that anyway? right...?
win = win32gui.GetForegroundWindow()
os.system('title saloading')
time.sleep(0.5)
if not any(psutil.Process(win32process.GetWindowThreadProcessId(win)[1]).name() == name for name in ['cmd.exe', 'OpenConsole.exe', 'WindowsTerminal.exe', 'powershell.exe']) or not 'saloading' in win32gui.GetWindowText(win):
	print('keep the cmd window focused while loading thanky')
	os.system('pause')
	sus.exit(0)
os.chdir(os.path.dirname(__file__))

os.system('title salad autostart+')


version = 1


real_print = print
with open('text/saladautostartplus.txt') as f:
	t1 = f.read()

def print(*args, end='\n'):
	strn = ' '.join([str(arg) for arg in args])
	real_print(strn + Style.RESET_ALL, end=end)

def clear():
	os.system('cls')
	print(t1)

def exit():
	os.system('pause')
	sus.exit(0)

clear()

def save(cfg):
	with open('config.json', 'w+') as f:
		f.write(json.dumps(cfg))


# first time config setup
if not os.path.isfile('config.json'):
	clear()
	print("no config file found! want to make a new one?")
	ch = choose.create([f'{Fore.GREEN}yes', f'{Fore.RED}no'], win)
	if ch[1] == 0:
		cfg = {}

		clear()
		print(f'{Fore.YELLOW}config setup 1/7: inactivity time')
		print('start mining after how many minutes of afk?')
		while True:
			try:
				inp = int(input('>>> '))
				break
			except KeyboardInterrupt:
				exit()
			except:
				print(f'{Fore.RED}should be a number')
		cfg['afk_minutes'] = inp

		clear()
		print(f'{Fore.YELLOW}config setup 2/7: mining afterburner profile')
		print('apply which afterburner profile when mining? type "none" for no profile')
		while True:
			try:
				inp = input('>>> ')
				if inp == 'none':
					inp = 0
					break
				if inp.isdigit():
					inp = int(inp)
					if not (1<=inp<=5):
						print(f'{Fore.RED}should be a number from 1 to 5')
						continue
					break
				print(f'{Fore.RED}must be a number or "none"')
				continue
			except KeyboardInterrupt:
				exit()
		cfg['mining_profile'] = inp

		clear()
		print(f'{Fore.YELLOW}config setup 3/7: default afterburner profile')
		print('apply which afterburner profile when back from afk? type "none" for no profile')
		while True:
			try:
				inp = input('>>> ')
				if inp == 'none':
					inp = 0
					break
				if inp.isdigit():
					inp = int(inp)
					if not (1<=inp<=5):
						print(f'{Fore.RED}should be a number from 1 to 5')
						continue
					break
				print(f'{Fore.RED}must be a number or "none"')
				continue
			except KeyboardInterrupt:
				exit()
		cfg['normal_profile'] = inp

		clear()
		print(f'{Fore.YELLOW}config setup 4/7: kill processes')
		print('which processes should be killed before afk mining?\ngpu intensive tasks (like games) running in the background may reduce hashrate and profits.')
		print('\ntip: open task manager, right click a process and click details.\nthe highlighted name is what u are looking for (ends with .exe)')
		print('\ncontinue by typing "next"')
		proc = []
		while True:
			try:
				inp = input('>>> ')
				if inp == 'next':
					break
				if inp.split('.')[len(inp.split('.'))-1] == 'exe':
					print(f'{Fore.GREEN}added {inp} to the list')
					proc.append(inp)
				else:
					print(f'{Fore.RED}invalid process name! a process name must end with ".exe"')
			except KeyboardInterrupt:
				exit()
		cfg['kill_processes'] = proc

		clear()
		print(f'{Fore.YELLOW}config setup 5/7: anti afk processes')
		print('which processes should prevent afk mining? (if that process is running, dont activate afk mining)')
		print('could be useful while going afk in games or while watching a video')
		print('\ntip: open task manager, right click a process and click details.\nthe highlighted name is what u are looking for (ends with .exe)')
		print('\ncontinue by typing "next"')
		proc = []
		while True:
			try:
				inp = input('>>> ')
				if inp == 'next':
					break
				if inp.split('.')[len(inp.split('.'))-1] == 'exe':
					print(f'{Fore.GREEN}added {inp} to the list')
					proc.append(inp)
				else:
					print(f'{Fore.RED}invalid process name! a process name must end with ".exe"')
			except KeyboardInterrupt:
				exit()
		cfg['prevent_processes'] = proc

		clear()
		print(f'{Fore.YELLOW}config setup 6/7: better mining')
		print('allow changing settings in commonly used programs which could be decreasing hashrates?')
		print('wallpaper engine - pause the animated wallpaper while afk')
		print('geforce experience instant replay - turn off while afk')
		print('[more might be added later]')
		set5 = choose.create([f'{Fore.GREEN}yes', f'{Fore.RED}no'], win)
		cfg['common_fix'] = True if not set5[1] else False

		clear()
		print(f'{Fore.YELLOW}config setup 7/7: mining')
		print('how do u want to start the miner while afk?')
		set6 = choose.create([f'{Fore.CYAN}run a batch file', f'{Fore.GREEN}run whatever salad uses'], win)
		if set6[1] == 0:
			print('\nenter the name of the file:')
			print('(it must be in the same folder as autostart.py)')
			while True:
				file = input('>>> ')
				if not os.path.isfile(file):
					print(f'{Fore.RED}couldnt find that file! make sure its in the same folder as autostart.py')
					continue
				break
			cfg['miner'] = {
				"type": "batch",
				"run": file
			}
		else:
			print('\nif u are currently mining with salad, stop.')
			print('press start, wait for confirmation to appear here (should take a few seconds) and hit stop.')
			print('if nothing happens for a minute, try another method or scream at sharky to fix his broken code')
			print('...')
			r = 0
			path = os.getenv('APPDATA')
			path = path + '/salad'
			found = False
			while True:
				with open(path + '/logs/main.log') as f:
					lines = f.readlines()
					for line in lines:
						if 'Starting plugin' in line:
							print(f'{Fore.GREEN}miner found!')

							params = line.split('Starting plugin')[1].split(':')
							miner_folder = params[0][1:]
							del params[0]
							params = ':'.join(params)[1:]
							params = path + f'/plugin-bin/{miner_folder}/' + params

							print(f'params: {params}')
							cfg['miner'] = {
								"type": "salad",
								"run": params
							}
							found = True
							break
				if found: break
				r += 1
				time.sleep(1)

		cfg['settings'] = {
			'check_updates': True,
			'logging': 0,
			'hide_to_tray': False
		}
		clear()
		print(f'{Fore.YELLOW}finishing setup...')
		print('looking for afterburner and wallpaper engine (if installed)')
		print('will probably only work for windows')

		def find(name, path):
			for root, dirs, files in os.walk(path):
				if name in files:
					return os.path.join(root, name)
			return None

		ab_path = find('MSIAfterburner.exe', 'C:/Program Files (x86)')
		if not ab_path:
			print('couldnt find msi afterburner! do u have it installed?')
			wp_installed = choose.create([f'{Fore.GREEN}yes', f'{Fore.RED}no'], win)
			if wp_installed[1] == 0:
				while True:
					print('enter the path to MSIAfterburner.exe or the afterburner installation folder')
					print('tip: task manager -> right click msi afterburner -> details -> open file location')
					print('(paste to console by right clicking the window)')
					fol = input('>>> ')
					if os.path.isfile(fol):
						ab_path = fol
						break
					elif 'MSIAfterburner.exe' in os.listdir():
						ab_path = os.path.join(fol, 'MSIAfterburner.exe')
						break
			else:
				print('why?!')
		else:
			print('found afterburner')

		we_path = find('wallpaper32.exe', 'C:/Program Files')
		if not we_path:
			print('couldnt find wallpaper engine! do u have it installed?')
			wp_installed = choose.create([f'{Fore.GREEN}yes', f'{Fore.RED}no'], win)
			if wp_installed[1] == 0:
				while True:
					print('enter the path to wallpaper32.exe, the wallpaper engine installation folder or steamlibrary folder')
					print('tip: task manager -> right click wallpaper engine -> details -> open file location')
					print('(paste to console by right clicking the window)')
					fol = input('>>> ')
					if os.path.isfile(fol):
						we_path = fol
						break
					elif 'wallpaper32.exe' in os.listdir():
						we_path = os.path.join(fol, 'wallpaper32.exe')
						break
					else:
						if 'SteamLibrary' in fol:
							we_path = find('wallpaper32.exe', fol)
							if we_path:
								break
		else:
			print('found wallpaper engine')

		cfg['programs'] = {
			'afterburner': ab_path,
			'wallpaper_engine': we_path
		}

		with open('config.json', 'w+') as f:
			f.write(json.dumps(cfg))
		clear()
		print(f'{Back.GREEN}config setup complete!')
		exit()


	elif ch[1] == 1:
		print('\nmake sure there is a config.json file in the same folder as autostart.py!')
		exit()

# verify config
try:
	with open('config.json') as f:
		cfg = json.load(f)
	if not list(cfg.keys()) == ['afk_minutes', 'mining_profile', 'normal_profile', 'kill_processes', 'prevent_processes', 'common_fix', 'miner', 'settings', 'programs']:
		print(list(cfg.keys()))
		print(f'{Back.RED}ur config file is corrupt! delete it and complete the config setup again')
		exit()
	print(f'{Fore.GREEN}config loaded')
except SystemExit:
	sus.exit(0)
except KeyboardInterrupt:
	sus.exit(0)
except:
	print(f'{Back.RED}ur config file is corrupt! delete it and complete the config setup again')
	exit()
s = '    '

# check updates
cfg['settings']['version'] = version
if cfg['settings']['check_updates']:
	print(f'{Fore.CYAN}checking for updates...')
	r = requests.get(url='https://fun.shruc.ml/sap/version', timeout=5)
	if r.status_code == 200:
		if r.json()['latest'] == cfg['settings']['version']:
			print('up to date')
		else:
			print(f'{Fore.GREEN}UPDATE AVAILABLE! go to [insert link here] and download the latest version!')
			print('...or u can just disable this message in settings')
			os.system('pause')
	else:
		print(f'{Fore.RED}failed to check version! the server could be down (or ur internet is bad)')
		os.system('pause')

# choose is pain :keqingdespair:
tray_bye = False
while True:
	clear()
	if tray_bye: sus.exit(0) # YOU BETTER EXIT
	print(f'{s}version: {version}\n')
	main = choose.create([f'{Fore.GREEN}start', 'settings', 'open github page', 'exit'], win)
	main = main[1]
	if main == 3:
		print('bye bye')
		break
	elif main == 2:
		os.system('start [insert link here]')
	elif main == 0:
		try:
			if cfg['settings']['hide_to_tray']:
				def show_console():
					icon.stop()
					win32gui.ShowWindow(win, win32con.SW_SHOW)

				def adios():
					global tray_bye
					icon.stop()
					stop.set()
					icon.notify('bye bye')
					tray_bye = True

				icon = pystray.Icon('test name', Image.open('things/icon.png'), menu=pystray.Menu(
						pystray.MenuItem(
								'salad autostart+ menu',
								adios,
								#checked=False,
								#radio=False,
								visible=True,
								enabled=False
							),
						pystray.MenuItem(
								'show console',
								show_console,
								#checked=False,
								#radio=False,
								visible=True,
								enabled=True
							),
						pystray.MenuItem(
								'exit',
								adios,
								#checked=False,
								#radio=False,
								visible=True,
								enabled=True
							)
					))
				win32gui.ShowWindow(win, win32con.SW_HIDE)
				icon.run_detached()
				time.sleep(1)
				icon.notify('look im down here!')

			timer = cfg['afk_minutes']*60
			# bug: reset prints keep invading the personal space of other prints below
			# smh not respecting bovid social distancing rules of 1 line
			# process list only updates every 5 seconds due to cpu going goodbye
			knum = 0
			afkrun = False
			def reset_kb(h):
				global timer
				if timer == cfg['afk_minutes']*60: #antispammy
					return
				print(f'{Fore.CYAN}keyboard input: reset timer to {cfg["afk_minutes"]*60} seconds')
				timer = cfg['afk_minutes']*60
			def reset_ms(h):
				global timer
				if timer == cfg['afk_minutes']*60: #antispammy
					return
				print(f'{Fore.CYAN}mouse moved: reset timer to {cfg["afk_minutes"]*60} seconds')
				timer = cfg['afk_minutes']*60
			stop = threading.Event()
			class procs(threading.Thread):
				def __init__(self):
					threading.Thread.__init__(self)
				def run(self):
					while not stop.is_set():
						global knum
						global afkrun
						knum = 0
						afkrun = False
						for proc in psutil.process_iter():
							if any(proc.name() == name for name in cfg['kill_processes']):
								knum += 1
							if any(proc.name() == name for name in cfg['prevent_processes']):
								print(f'{Fore.YELLOW}anti afk process running: {proc.name()}')
								timer = cfg["afk_minutes"]*60
								afkrun = True
						time.sleep(5)

			# i hope u dont have a lot of processes running!
			checkproc = procs()
			checkproc.start()

			keyboard.on_press(reset_kb)
			mouse.hook(reset_ms)
			while not tray_bye:
				clear()
				delay = time.time()
				timer -= 1
				print('ctrl+c to stop')
				print(f'{Fore.LIGHTGREEN_EX}seconds remaining: {timer}')
				if cfg['settings']['hide_to_tray']: print('\nhiding the process back to tray requires stopping and starting again. maybe ill fix this later')
				if knum > 0: print(f'{Fore.RED}{knum} active processes will be killed')
				if not afkrun: print(f'no anti afk processes running')
				try:
					time.sleep(1-(time.time()-delay))
				except KeyboardInterrupt:
					raise(KeyboardInterrupt)
				except:
					pass
				if timer <= 0:
					print('\nafked enough - starting miner')
					for proc in psutil.process_iter():
						if any(proc.name() == name for name in cfg['kill_processes']):
							print(f'{Fore.RED}killing {proc.name()}')
							os.system(f'taskkill /f /im {proc.name()}')
					if cfg['common_fix']:
						if cfg['programs']['wallpaper_engine']:
							print('wallpaper engine off')
							os.system(f'"{cfg["programs"]["wallpaper_engine"]}" -control pause')
						# todo finish nvidia geforce thing later
					if cfg['mining_profile'] != 'none' and cfg['programs']['afterburner']:
						if cfg['normal_profile'] == 'none':
							keyboard.write('ctrl+d') # why are you mining without an overclock?!
						else:
							os.system(f'"{cfg["programs"]["afterburner"]}" -profile{cfg["mining_profile"]}')
					miner = subprocess.Popen(f'{cfg["miner"]["run"]}', creationflags=subprocess.CREATE_NEW_CONSOLE)
					print('mining')
					if cfg['settings']['hide_to_tray']: icon.notify('miner started')
					while timer <= 0:
						time.sleep(1)
					print('welcome back')
					if cfg['settings']['hide_to_tray']: icon.notify('welcome back (miner stopped)')
					for child in psutil.Process(miner.pid).children(recursive=True):
						child.kill()
					miner.kill() # above thing should kill the cmd itself as well but why not
					if cfg['programs']['afterburner']:
						print('afterburner set normal profile')
						if cfg['normal_profile'] == 'none':
							keyboard.write('ctrl+d') # now there is a proper way to reset oc in command line but this is easier
						else:
							os.system(f'"{cfg["programs"]["afterburner"]}" -profile{cfg["normal_profile"]}')
					if cfg['common_fix']:
						if cfg['programs']['wallpaper_engine']:
							print('wallpaper engine on')
							os.system(f'"{cfg["programs"]["wallpaper_engine"]}" -control play')


		except KeyboardInterrupt:
			stop.set()
			print(f'{Fore.RED}ctrl+c - exiting')

	elif main == 1:
		while True:
			clear()
			print(f'{s}check for updates: check version every launch')
			print(f'{s}hide to tray: hide salad autostart+ to tray after selecting start')
			print(f'{s}logging: nothing for now\n')
			sett = choose.create([f'check for updates: {"yes" if cfg["settings"]["check_updates"] else "no"}', \
				f'hide to tray: {"yes" if cfg["settings"]["hide_to_tray"] else "no"}', f'logging: {cfg["settings"]["logging"]}', 'change config', f'{Fore.GREEN}back'], win)
			sett = sett[1]
			print('')
			if sett == 4:
				break
			elif sett == 1:
				cfg['settings']['hide_to_tray'] = not cfg['settings']['hide_to_tray']
				save(cfg)
			elif sett == 0:
				cfg['settings']['check_updates'] = not cfg['settings']['check_updates']
				save(cfg)
			elif sett == 2:
				log = choose.create(['0', '1', '2'], win)
				cfg['settings']['logging'] = log[1]
				save(cfg)
			elif sett == 3:
				while True:
					clear()
					print(f'{s}changing config\n')
					conf = choose.create([f'afk minutes: {cfg["afk_minutes"]}', f'afterburner normal profile: {cfg["normal_profile"]}', f'afterburner mining profile: {cfg["mining_profile"]}', 'configure process killing', 'configure anti afk processes', f'allow common low hashrate fixes: {"yes" if cfg["common_fix"] else "no"}', 'configure miner', f'{Fore.GREEN}back'], win)
					conf = conf[1]
					print('')
					if conf == 7:
						break
					elif conf == 5:
						cfg['common_fix'] = not cfg['common_fix']
						save(cfg)
					elif conf == 0:
						print(f'{s}{Fore.YELLOW}start mining after how many minutes of afk?')
						while True:
							try:
								inp = int(input(f'{s}>>> '))
								break
							except KeyboardInterrupt:
								exit()
							except:
								print(f'{s}{Fore.RED}should be a number')
						cfg['afk_minutes'] = inp
						save(cfg)
					elif conf == 1:
						print(f'{s}{Fore.YELLOW}apply which afterburner profile when ? type "none" for no profile')
						while True:
							try:
								inp = input(f'{s}>>> ')
								if inp == 'none':
									inp = 0
									break
								if inp.isdigit():
									inp = int(inp)
									if not (1<=inp<=5):
										print(f'{s}{Fore.RED}should be a number from 1 to 5')
										continue
									break
								print(f'{s}{Fore.RED}must be a number or "none"')
								continue
							except KeyboardInterrupt:
								exit()
						cfg['normal_profile'] = inp
						save(cfg)
					elif conf == 2:
						print(f'{s}{Fore.YELLOW}apply which afterburner profile when mining? type "none" for no profile')
						while True:
							try:
								inp = input(f'{s}>>> ')
								if inp == 'none':
									inp = 0
									break
								if inp.isdigit():
									inp = int(inp)
									if not (1<=inp<=5):
										print(f'{s}{Fore.RED}should be a number from 1 to 5')
										continue
									break
								print(f'{s}{Fore.RED}must be a number or "none"')
								continue
							except KeyboardInterrupt:
								exit()
						cfg['mining_profile'] = inp
						save(cfg)
					elif conf == 3:
						while True:
							# im like 4 while trues deep already :ohgodsaveme:
							clear()
							print(f'{s}{Fore.YELLOW}process killing - kill these processes when afk mining begins')
							print(f'{s}select a process (white) to remove it or add another\n')
							proch = [f'{Fore.GREEN}back', f'{Fore.CYAN}add']
							for process in cfg['kill_processes']:
								proch.append(f'{Fore.WHITE}' + process)
							pro = choose.create(proch, win)
							pro = pro[1]
							if pro == 0:
								break
							elif pro == 1:
								clear()
								print(f'{s}{Fore.YELLOW}add a process to kill before starting afk mining')
								print(f'\n{s}tip: open task manager, right click a process and click details.\n{s}the highlighted name is what u are looking for (ends with .exe)')
								while True:
									try:
										inp = input(f'{s}>>> ')
										if inp == 'next':
											break
										if inp.split('.')[len(inp.split('.'))-1] == 'exe':
											print(f'{s}{Fore.GREEN}added {inp} to the list')
											break
										else:
											print(f'{s}{Fore.RED}invalid process name! a process name must end with ".exe"')
									except KeyboardInterrupt:
										exit()
								cfg['kill_processes'].append(inp)
								save(cfg)
							else:
								del cfg['kill_processes'][int(pro)-2]
								save(cfg)
					elif conf == 4:
						while True:
							# im like 4 while trues deep already :ohgodsaveme:
							clear()
							print(f'{s}{Fore.YELLOW}anti afk processes - dont afk mine if at least one of these is running')
							print(f'{s}select a process (white) to remove it or add another\n')
							proch = [f'{Fore.GREEN}back', f'{Fore.CYAN}add']
							for process in cfg['prevent_processes']:
								proch.append(f'{Fore.WHITE}' + process)
							pro = choose.create(proch, win)
							pro = pro[1]
							if pro == 0:
								break
							elif pro == 1:
								clear()
								print(f'{s}{Fore.YELLOW}add a process that will prevent afk mining')
								print(f'\n{s}tip: open task manager, right click a process and click details.\n{s}the highlighted name is what u are looking for (ends with .exe)')
								while True:
									try:
										inp = input(f'{s}>>> ')
										if inp == 'next':
											break
										if inp.split('.')[len(inp.split('.'))-1] == 'exe':
											print(f'{s}{Fore.GREEN}added {inp} to the list')
											break
										else:
											print(f'{s}{Fore.RED}invalid process name! a process name must end with ".exe"')
									except KeyboardInterrupt:
										exit()
								cfg['prevent_processes'].append(inp)
								save(cfg)
							else:
								del cfg['prevent_processes'][int(pro)-2]
								save(cfg)
					elif conf == 6:
						clear()
						print(f'{s}{Fore.YELLOW}how do u want to start the miner while afk?')
						print(f'{s}currently using: {f"{Fore.CYAN}batch file" if cfg["miner"]["type"]=="batch" else f"{Fore.GREEN}salad"}\n')
						set6 = choose.create([f'{Fore.CYAN}run a batch file', f'{Fore.GREEN}run whatever salad uses', f'{Fore.LIGHTGREEN_EX}back'], win)
						if set6[1] == 0:
							print(f'\n{s}{Fore.YELLOW}enter the name of the file:')
							print(f'{s}(it must be in the same folder as autostart.py)')
							while True:
								file = input(f'{s}>>> ')
								if not os.path.isfile(file):
									print(f'{s}{Fore.RED}couldnt find that file! make sure its in the same folder as autostart.py')
								break
							cfg['miner'] = {
								"type": "batch",
								"run": file
							}
							save(cfg)
						elif set6[1] == 1:
							print(f'\n{s}if u are currently mining with salad, stop.')
							print(f'{s}press start, wait for confirmation to appear here (should take a few seconds) and hit stop.')
							print(f'{s}if nothing happens for a minute, try another method or scream at sharky to fix his broken code')
							print(f'{s}...')
							path = os.getenv('APPDATA')
							path = path + '/salad'
							found = False
							while True:
								with open(path + '/logs/main.log') as f:
									lines = f.readlines()
									for line in lines:
										if 'Starting plugin' in line:
											print(f'{s}{Fore.GREEN}miner found!')

											params = line.split('Starting plugin')[1].split(':')
											miner_folder = params[0][1:]
											del params[0]
											params = ':'.join(params)[1:]
											params = path + f'/plugin-bin/{miner_folder}/' + params

											print(f'{s}params: {params}')
											cfg['miner'] = {
												"type": "salad",
												"run": params
											}
											found = True
											break
								if found: break
								time.sleep(1)
							os.system('pause')
							save(cfg)



exit()