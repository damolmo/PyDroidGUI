# PyDroidGUI - PyDroid with user interface

# Dependencias
import os

#======================== Beginning of dependencies ==============
print("-----------------------------\nInstalling core components...\nPlease wait\n-----------------------------")
os.system("pip3 install wheel")
os.system("pip3 install wget")
os.system("pip3 install pysimplegui")
# =================== End of dependencies ===========================================


# ======================= Beginning of Imports ===================
import PySimpleGUI as sg
import os.path
import lzma
import wget # Allows URL downloads
import time # Allows to sleep the code execution
import lzma # Allows .xz extraction for gsi files
import sys
import tarfile
from pathlib import Path
import zipfile
from datetime import datetime
import subprocess
import subprocess
from zipfile import ZipFile
from os.path import exists
from pathlib import Path
# ==================== End of imports ================================


# ============================ Beginning of Functions ====================

def date_str():
	return '{}'.format(datetime.now().strftime(DATE_FORMAT))

def zip_name(path):
	cur_dir = Path(path).resolve()
	parent_dir = cur_dir.parents[0]
	zip_filename = '{}/{}_{}.zip'.format(parent_dir, cur_dir.name, date_str())
	p_zip = Path(zip_filename)
	n = 1
	while p_zip.exists():
		zip_filename = ('{}/{}_{}_{}.zip'.format(parent_dir, cur_dir.name,
											 date_str(), n))
		p_zip = Path(zip_filename)
		n += 1
	return zip_filename


def all_files(path):
	for child in Path(path).iterdir():
		yield str(child)
		if child.is_dir():
			for grand_child in all_files(str(child)):
				yield str(Path(grand_child))

def zip_dir(path):
	zip_filename = zip_name(path)
	zip_file = zipfile.ZipFile(zip_filename, 'w')
	print('create:', zip_filename)
	for file in all_files(path):
		print('adding... ', file)
		zip_file.write(file)
	zip_file.close()

def check_adb_device():
	try:
		my_device_model = subprocess.check_output("cd platform-tools & adb shell getprop ro.product.model", shell=True, )
		my_device_model = my_device_model.decode("utf-8")
		my_device_model = str(my_device_model)
		my_device_model = my_device_model.replace(" ", "")

	except subprocess.CalledProcessError as e:
		my_device_model = str("No ADB device found\n")

	return my_device_model

def check_fastboot_device():
	try:
		my_device_model = subprocess.check_output("cd platform-tools & fastboot devices", shell=True, )
		my_device_model = my_device_model.decode("utf-8")
		my_device_model = str(my_device_model)
		my_device_model = my_device_model.replace(" ", "")

	except subprocess.CalledProcessError as e:
		my_device_model = str("No ADB device found\n")

	return my_device_model

def install_tools(adb_linux, linux) :
	linux = wget.download(adb_linux,linux) #Download the platform-tools-latest-linux.zip from Google server
	with ZipFile('platform-tools-latest-linux.zip') as zipObj:
		zipObj.extractall() #Extracts the downloaded file into a subdir called /platform-tools
	os.system("rm platform-tools-latest-linux.zip ")


def android_tools_exists(adb_linux, linux) :
	exists = False
	if os.path.exists("platform-tools") :
		exists = True

	else :
		install_tools(adb_linux, linux)

	return exists

def check_for_updates(version) :
	message = False

	# Read the version string from an external text document
	os.system("rm -f version.txt")
	os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroid/Linux/src/version.txt")
	version_str = Path('version.txt').read_text()
	version_str = version_str.replace('\n', '')
	os.system("rm -f version.txt")

	# Check if the latest version is installed
	if version_str != version :
		message = True

	return message

def latest_version() :
	# Read the version string from an external text document
	os.system("rm -f version.txt")
	os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroid/Linux/src/version.txt")
	version_str = Path('version.txt').read_text()
	version_str = version_str.replace('\n', '')
	os.system("rm -f version.txt")

	return version_str

def latest_changelog() :
	# Read the version string from an external text document
	os.system("rm -f changelog.txt")
	os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroid/Linux/src/changelog.txt")
	changelog_str = Path('changelog.txt').read_text()
	os.system("rm -f changelog.txt")

	return changelog_str


def runCommand(cmd):
	""" run shell command

	@param cmd: command to execute
	@param timeout: timeout for command execution

	@return: (return code from command, command output)
	"""

	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output = ''
	for line in p.stdout:
		line = line.decode(errors='replace' if (sys.version_info) < (3, 5)
						   else 'backslashreplace').rstrip()
		output += line
		print(line)
		if window:
			window.Refresh()

	retval = p.wait(timeout)

	return (retval, output)


def device_search():
	my_adb_model = check_adb_device()
	my_fastboot_model = check_fastboot_device()

	if my_adb_model == "No ADB device found" and my_fastboot_model == "No ADB device found" :
		my_device_model = my_adb_model

	elif my_adb_model != "No ADB device found" and my_adb_model !="" :
		my_device_model = my_adb_model

	elif my_fastboot_model != "No ADB device found" and my_fastboot_model !="" :
		my_device_model = my_fastboot_model

	else :
		my_device_model = my_adb_model

	return "Device : " +  my_device_model

def refresh():
	window['refresh'].update(specs())

def refresh_logo():
	window['render'].update(device_render())

def battery_level() :

	try :
		level = "unknown"
		level = subprocess.check_output("cd platform-tools & adb shell dumpsys battery | grep level", shell=True, )
		level = level.decode("utf-8")
		level = str(level)
		level = level.replace(" level: ", "")
		level = level.replace("\n", "")
		level = level + "%"

	except subprocess.CalledProcessError as e:
		level = str("unknown\n")

	return "Battery : " + level

def manufacturer() :

	try :
		level = "unknown"
		level = subprocess.check_output("cd platform-tools & adb shell getprop ro.product.manufacturer", shell=True, )
		level = level.decode("utf-8")
		level = str(level)
		level = level.replace(" level: ", "")

	except subprocess.CalledProcessError as e:
		level = str("unknown\n")

	return "Manufacturer : " + level

def brand() :

	try :
		brand = subprocess.check_output("cd platform-tools & adb shell getprop ro.product.manufacturer", shell=True, )
		brand = brand.decode("utf-8")
		brand = brand.replace("\n", "")
		brand = str(brand)

	except subprocess.CalledProcessError as e:
		brand = str("unknown\n")

	return brand

def android_version() :

	try :
		version = subprocess.check_output("cd platform-tools & adb shell getprop ro.build.version.release", shell=True, )
		version = version.decode("utf-8")
		version = str(version)

	except subprocess.CalledProcessError as e:
		version = str("unknown\n")

	return "Android version : " + version

def specs() :
	return  manufacturer() + android_version() + device_search() + battery_level()

def device_render() :
	img_src = "src/device.png"
	render = brand()

	if render == "Xiaomi" or render == "xiaomi" :
		img_src = "src/xiaomi.png"

	elif render == "Oneplus" or render == "oneplus" :
		img_src = "src/oneplus.png"

	elif render == "Google" or render == "google" :
		img_src = "src/google.png"

	elif render == "Samsung" or render == "samsung" :
		img_src = "src/samsung.png"

	elif render == "Sony" or render == "sony" :
		img_src = "src/sony.png"

	elif render == "Huawei" or render == "huawei" :
		img_src = "src/huawei.png"

	elif render == "Motorola" or render == "motorola" :
		img_src = "src/motorola.png"

	elif render == "BQ" :
		img_src = "src/bq.png"

	elif render == "HTC" :
		img_src = "src/htc.png"

	elif render == "LGE" :
		img_src = "src/lge.png"

	elif render == "ZTE" :
		img_src = "src/zte.png"

	elif render == "OPPO" :
		img_src = "src/oppo.png"


	return img_src

  

# ======================== End of Functions ================================

# =================== Beginning of variables=============
# Static URLs
adb_linux ="https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
pydroidtools = "https://github.com/daviiid99/PyDroid/raw/Linux/Main.py"

# Packages names
usb = "Google_USB.zip"
linux = "platform-tools-latest-linux.zip"
gsi_image_xz = "system.img.xz"
gsi_image = "system.img"
ota_package = "android_ota.zip"

# Other variables
DATE_FORMAT = '%y%m%d'
user = 0 # For keyboard input 
version = "1.0"
# ==================== End of variables ===================

# ================= Beginning of Main =====================
#android_tools_exists(adb_linux, linux)

menu = [
		[sg.Image("src/logo.png", background_color='#4285f4'), sg.Text("v" + version, size=(5), background_color='#4285f4')],
		[sg.Button("Check for Updates", font='7', button_color='#3ddc84'), sg.Button("Reinstall Platform-Tools",button_color='#3ddc84', font='7', key="tools")],
		[sg.Text("\n" * 1, background_color='#4285f4' )],
		[sg.Image(device_render(),  background_color='#4285f4', key='render'), sg.Text(specs(), background_color='#4285f4',  key="refresh", visible=True ), sg.Text("        ", background_color='#4285f4'),  sg.Button("Refresh", key="search", button_color='#3ddc84', font='7')],
		[sg.Text( background_color='#4285f4')],
		[sg.Button('Search for ADB Devices', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Search for Fastboot Devices', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
		[sg.Button('Android Device Logcat', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Android Device Backup', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
		[sg.Button('Send file over ADB', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Sideload OTA package', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
		[sg.Button('Install Android App', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Uninstall Android App', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
		[sg.Button('Flash a Generic System Image', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Unlock Android Bootloader', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
		[sg.Button('Backup Current boot.img', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Modify Current DPI', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
		]

layout = [
	[
		sg.Column(menu, background_color='#4285f4'),

	]
		]

console = [
        [sg.Multiline(size=(110, 30), echo_stdout_stderr=True, reroute_stdout=True, autoscroll=True, background_color='black', text_color='white', key='-MLINE-')],
        [sg.T('Promt> '), sg.Input(key='-IN-', focus=True, do_not_clear=False)],
        [sg.Button('Run', bind_return_key=True), sg.Button('Exit')]]


adb = [[sg.Text("Searching for ADB devices...")],
		[sg.Image("skate.gif")],
		[sg.Text("\n" * 2 )],
		]

window = sg.Window("PyDroidGUI", layout,background_color='#4285f4')
window.set_icon("src/icon.png")



while True :
	window.refresh()
	event, values = window.read()

	if event == "opt1" :
		message = os.system("adb devices")
		sg.Print('ADB Device Found\nIf your device is not found, check your USB cable \n\n', do_not_reroute_stdout=False)
		print = sg.Print
		print(device_search())

	elif event == "search" :
		refresh()
		refresh_logo()

	elif event == "tools":
		window = sg.Window('Realtime Shell Command Output', console)
		event, values = window.read()
		sp = sg.execute_command_subprocess(values['-IN-'], pipe_output=True, wait=False)
		results = sg.execute_get_results(sp, timeout=1)
		print(results[0])

		os.system("rm -rf platform-tools")
		sg.Print("\nDownloading %s from Google server, please wait..." % linux)
		android_tools_exists(adb_linux, linux)
		tools = True
		print("\nAndroid Platform-Tools Installation Succeeded!")

	elif event == sg.WIN_CLOSED:
		break

window.close()