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
		my_device_model = str("No ADB device found")

	return my_device_model

def check_fastboot_device():
	try:
		my_device_model = subprocess.check_output("cd platform-tools & fastboot devices", shell=True, )
		my_device_model = my_device_model.decode("utf-8")
		my_device_model = str(my_device_model)
		my_device_model = my_device_model.replace(" ", "")

	except subprocess.CalledProcessError as e:
		my_device_model = str("No ADB device found")

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

	return my_device_model

def refresh():
	window['refresh'].update(device_search())

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
version = "1.0-7"
# ==================== End of variables ===================

# ================= Beginning of Main =====================

menu = [[sg.Text("PyDroid is an Android Platform-Tools UI")],
		[sg.Image("logo.png")],
		[sg.Text("\n")],
		[sg.Button("Check for Updates"), sg.Button("Reinstall Platform-Tools")],
		[sg.Text("\n" * 1 )],
		[sg.Text("Current Android Device: ")],
		[sg.Image("device.png"), sg.Text(device_search(),  key="refresh", visible=True ), sg.Text("        "),  sg.Button("Refresh", key="search")],


		]


opciones = [[sg.Text("Choose one of the following options :\n")],
			[sg.Button('Search for ADB Devices', size=(18,2), key="opt1"), sg.Text(""), sg.Button("Search for Fastboot Devices", size=(18,2))],
			[sg.Button('Android Device Logcat', size=(18,2)), sg.Text(""), sg.Button("Flash a Generic System Image", size=(18,2))],
			[sg.Button('Unlock Android Device Bootloader', size=(18,2)), sg.Text(""), sg.Button("Uninstall Android App", size=(18,2))],
			[sg.Button('Install Android App', size=(18,2)), sg.Text(""), sg.Button("Android Device Backup", size=(18,2))],
			[sg.Button('Backup Current boot.img', size=(18,2)), sg.Text(""), sg.Button("Send file over ADB", size=(18,2))],
			[sg.Button('Sideload OTA file', size=(18,2)), sg.Text(""), sg.Button("Modify Current DPI", size=(18,2))],
]


layout = [
	[
		sg.Column(menu),
		sg.VSeperator(),
		sg.Column(opciones),
	]
]


adb = [[sg.Text("Searching for ADB devices...")],
		[sg.Image("skate.gif")],
		[sg.Text("\n" * 2 )],
		]

window = sg.Window("PyDroidGUI", layout)


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



	elif event == sg.WIN_CLOSED:
		break

window.close()