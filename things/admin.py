def forceadmin(path):
	import ctypes
	import sys
	import win32com.shell.shell as shell
	import win32con
	if not ctypes.windll.shell32.IsUserAnAdmin(): # dont forkbomb myself -_-
		params = '/c start "C:\\Program Files\\Python37\\python.exe" ' + str(path)
		showCmd = win32con.SW_SHOWNORMAL
		shell.ShellExecuteEx(nShow=showCmd, lpVerb='runas', lpFile='cmd', lpParameters=params)
		sys.exit(0)