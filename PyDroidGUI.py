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
from subprocess import PIPE, Popen
import platform
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
    for file in all_files(path):
        zip_file.write(file)
    zip_file.close()

def check_adb_device():
    try:
        my_device_model = subprocess.check_output("cd platform-tools & adb shell getprop ro.product.model", shell=True, )
        my_device_model = my_device_model.decode("utf-8")
        my_device_model = str(my_device_model)
        my_device_model = my_device_model.replace(" ", "")

    except subprocess.CalledProcessError as e:
        my_device_model = str("unknown\n")

    return my_device_model

def check_fastboot_device():
    try:
        my_device_model = subprocess.check_output("cd platform-tools & fastboot devices", shell=True, )
        my_device_model = my_device_model.decode("utf-8")
        my_device_model = str(my_device_model)
        my_device_model = my_device_model.replace(" ", "")

    except subprocess.CalledProcessError as e:
        my_device_model = str("unknown\n")

    return my_device_model

def install_tools(adb_linux, linux) :
    linux = os.system("wget %s " % adb_linux) #Download the platform-tools-latest-linux.zip from Google server
    with ZipFile('platform-tools-latest-linux.zip') as zipObj:
        zipObj.extractall() #Extracts the downloaded file into a subdir called /platform-tools

    if platform.system() == "Linux" :
        os.system("rm platform-tools-latest-linux.zip ")

    else :
        os.system("del /f platform-tools-latest-linux.zip ")


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
    if platform.system() == "Linux" :
        os.system("rm -f version.txt")
    else :
        os.system("del /f version.txt")
    
    os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroid/Linux/src/version.txt")
    version_str = Path('version.txt').read_text()
    version_str = version_str.replace('\n', '')

    if platform.system() == "Linux" :
        os.system("rm -f version.txt")
    else :
        os.system("del /f version.txt")

    # Check if the latest version is installed
    if version_str != version :
        message = True

    return message

def latest_version() :
    # Read the version string from an external text document
    if platform.system() == "Linux" :
        os.system("rm -f version.txt")
    else :
        os.system("del /f version.txt")

    os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroidGUI/main/src/version.txt")
    version_str = Path('version.txt').read_text()
    version_str = version_str.replace('\n', '')

    if platform.system() == "Linux" :
        os.system("rm -f version.txt")
    else :
        os.system("del /f version.txt")

    return version_str

def latest_changelog() :
    # Read the version string from an external text document
    if platform.system() == "Linux" :
        os.system("rm -f changelog.txt")
    else :
        os.system("del /f changelog.txt")

    os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroidGUI/main/src/changelog.txt")
    changelog_str = Path('changelog.txt').read_text()

    if platform.system() == "Linux" :
        os.system("rm -f changelog.txt")
    else :
        os.system("del /f changelog.txt")

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

    if my_adb_model == "unknown" and my_fastboot_model == "unknown" :
        my_device_model = my_adb_model

    elif my_adb_model != "unknown" and my_adb_model !="" :
        my_device_model = my_adb_model

    elif my_fastboot_model != "unknown" and my_fastboot_model !="" :
        my_device_model = my_fastboot_model

    else :
        my_device_model = my_adb_model

    return "Device : " +  my_device_model

def model():
    my_adb_model = check_adb_device()
    my_fastboot_model = check_fastboot_device()

    if my_adb_model == "unknown" and my_fastboot_model == "unknown" :
        my_device_model = my_adb_model

    elif my_adb_model != "unknown" and my_adb_model !="" :
        my_device_model = my_adb_model

    elif my_fastboot_model != "unknown" and my_fastboot_model !="" :
        my_device_model = my_fastboot_model

    else :
        my_device_model = my_adb_model

    return my_device_model

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

    if "100%" in level :
        level = "charged"

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

    if render == "Xiaomi" or render == "xiaomi" or render == "XIAOMI" :
        img_src = "src/xiaomi.png"

    elif render == "Oneplus" or render == "oneplus" or render == "ONEPLUS" :
        img_src = "src/oneplus.png"

    elif render == "Google" or render == "google" or render == "XIAOMI":
        img_src = "src/google.png"

    elif render == "Samsung" or render == "samsung"  or render == "SAMSUNG" :
        img_src = "src/samsung.png"

    elif render == "Sony" or render == "sony" or render == "SONY" :
        img_src = "src/sony.png"

    elif render == "Huawei" or render == "huawei" or render == "HUAWEI" :
        img_src = "src/huawei.png"

    elif render == "Motorola" or render == "motorola" or render == "XIAOMI" :
        img_src = "src/motorola.png"

    elif render == "BQ" or render == "bq" or render == "BQ" :
        img_src = "src/bq.png"

    elif render == "HTC" or render == "htc" or render == "HTC" :
        img_src = "src/htc.png"

    elif render == "LGE" or render == "lge" or render == "LGE" :
        img_src = "src/lge.png"

    elif render == "ZTE" or render == "zte" or render == "ZTE" :
        img_src = "src/zte.png"

    elif render == "OPPO" or render == "oppo" or render == "OPPO" :
        img_src = "src/oppo.png"

    elif render == "HMD Global" or render == "hmd global" or render == "HMD GLOBAL" :
        img_src = "src/nokia.png"

    elif render == "Lenovo" or render == "lenovo" or render == "LENOVO" :
        img_src = "src/lenovo.png"


    return img_src

def window_changelog(title):
    changelog = [[sg.Text("New Available version : %s              \n\n Changelog :                        \n%s" % (latest_version(), latest_changelog()), background_color='#4285f4')],
            [sg.Button("Perform Update", button_color='#3ddc84', font='5', size=(16,2),), sg.Button("Cancel", button_color='#3ddc84', font='5', size=(16,2),)]]

    return sg.Window(title, changelog, background_color='#4285f4')

def window_version(title):
    version = [[sg.Text("PyDroid is already updated\nCurrent installed version : %s \nLatest Available Version : %s " % (version, latest_version()), background_color='#4285f4')],
          [sg.Button("Cancel", button_color='#3ddc84', font='5', size=(16,2),)]]


    return sg.Window(title, version, background_color='#4285f4')

def window_tools(title):
    tools = [[sg.Text("\nReinstall Android platform-tools ?", background_color='#4285f4')],
            [sg.Button("Perform Update", button_color='#3ddc84', font='5', size=(16,2),), sg.Button("Cancel", button_color='#3ddc84', font='5', size=(16,2),)]]

    return sg.Window(title, tools, background_color='#4285f4')

def window_logcat(title):
    logcat = [[sg.Text("\nCatch Android Device Logcat ?", background_color='#4285f4')],
            [sg.Button("Ok", button_color='#3ddc84', font='5', size=(16,2),), sg.Button("Cancel", button_color='#3ddc84', font='5', size=(16,2),)]]

    return sg.Window(title, logcat, background_color='#4285f4')

def window_unlock(title):
    unlock = [[sg.Text("\n\nWARNING!!\nBootloader Unlock will ONLY work with Google Pixel\nAndroid One, Motorola and Sony Devices\n\nIf you're using an unlockable device, enable\nSettings > System > Developer Options >\nOEM unlock > Enable\n", background_color='#4285f4')],
                [[sg.Image("src/fastboot.png", background_color='#4285f4')]],
                [[sg.Text("\nPress VOL- + POWER to boot into FASTBOOT mode", background_color='#4285f4')]],
                [sg.Button("Unlock Bootloader", button_color='#3ddc84', font='5', size=(16,2),), sg.Button("Cancel", button_color='#3ddc84', font='5', size=(16,2),)]]

    return sg.Window(title, unlock, background_color='#4285f4')

def window_boot(title):
    boot = [[sg.Text("\nDump Android Boot.img\n\nChoose your partitions scheme ", background_color='#4285f4')],
            [sg.Button("A-Only Partition", button_color='#3ddc84', font='5', size=(16,2),), sg.Button("A|B Partitions", button_color='#3ddc84', font='5', size=(16,2),), sg.Button("Cancel", button_color='#3ddc84', font='5', size=(16,2),)]]

    return sg.Window(title, boot, background_color='#4285f4')

def window_gsi(title) : 

    gsi = [[sg.FileBrowse( key="-FILE-")],
          [sg.Image()],
          [sg.Button("Flash GSI")],
          [sg.Button("Exit")],

    ]
    return sg.Window(title, gsi, background_color='#4285f4', finalize=True)

def window_control(title) : 

    gsi = [[sg.Button("Reboot Recovery", button_color='#3ddc84', size=(20,2), font='5')],
          [sg.Button("Reboot System  ", button_color='#3ddc84', size=(20,2), font='5')],
          [sg.Button("Reboot Fastboot", button_color='#3ddc84', size=(20,2), font='5')],
          [sg.Button("PowerOff Phone", button_color='#3ddc84', size=(20,2), font='5')],

    ]
    return sg.Window(title, gsi, background_color='#4285f4', finalize=True)



def install_py(pydroid, script) :
    linux = wget.download(pydroid,script) #Download the platform-tools-latest-linux.zip from Google server

def window_success(title):
    changelog = [[sg.Text("\nOperation completed succesfully!", background_color='#4285f4')],
            [sg.Button("Ok", button_color='#3ddc84', font='5', size=(16,2),)]]

    return sg.Window(title, changelog, background_color='#4285f4')

def device_backup(allowed) :
    os.system("mkdir backup") # Create a temp dir

    for dirs in allowed:
        os.system("cd platform-tools & adb pull sdcard/%s backup " % dirs )  # Place all allowed dirs into the temp dir

    
    zipdir = zip_dir("backup") # Bundle all the allowed dirs into a zip file

    # Remove the temp dir
    if platform.system() == "Linux" :
        os.system("rm -rf backup")

    else :
        os.system("rmdir /S /Q backup")


def window_backup(title) : 
          
    gsi = [
          [sg.Image("src/backup.png", background_color='#4285f4')] ,
          [sg.Text("\nChoose the folders and click start :\n", background_color='#4285f4')],
          [sg.Checkbox('DCIM', key='DCIM',  background_color='#4285f4')],
          [sg.Checkbox('PICTURES', key='PICTURES',  background_color='#4285f4')],
          [sg.Checkbox('DOWNLOADS', key='DOWNLOADS',  background_color='#4285f4')],
          [sg.Checkbox('MUSIC', key='MUSIC',  background_color='#4285f4')],
          [sg.Checkbox('DOCUMENTS', key='DOCUMENTS',  background_color='#4285f4')],
          [sg.Button('Start', button_color='#3ddc84', font='5', size=(16,2), key="start")]], 

    return sg.Window(title, gsi, background_color='#4285f4', finalize=True)



  

# ======================== End of Functions ================================

# =================== Beginning of variables=============
# Static URLs
adb_linux ="https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
adb_windows ="https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
pydroid = "https://github.com/daviiid99/PyDroidGUI/raw/main/PyDroidGUI.py"
script = "Main.py"

# Packages names
usb = "Google_USB.zip"
linux = "platform-tools-latest-linux.zip"
windows ="platform-tools-latest-windows.zip"
gsi_image_xz = "system.img.xz"
gsi_image = "system.img"
ota_package = "android_ota.zip"

# Other variables
DATE_FORMAT = '%y%m%d'
user = 0 # For keyboard input 
version = "1.0"
# ==================== End of variables ===================

# ================= Beginning of Main =====================
android_tools_exists(adb_linux, linux)

menu = [
        [sg.Image("src/logo.png", background_color='#4285f4'), sg.Text("v" + version, size=(5), background_color='#4285f4')],
        [sg.Button("Check for Updates", font='7', button_color='#3ddc84', key="update"), sg.Button("Reinstall Platform-Tools",button_color='#3ddc84', font='7', key="tools")],
        [sg.Text("\n" * 1, background_color='#4285f4' )],
        [sg.Image(device_render(),  background_color='#4285f4', key='render'), sg.Text(specs(), background_color='#4285f4',  key="refresh", visible=True ),sg.Button("Control", key="power", button_color='#3ddc84', font='7', visible=False), sg.Button("Refresh", key="search", button_color='#3ddc84', font='7')],
        [sg.Text( background_color='#4285f4')],
        [sg.Button('Search for ADB Devices', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Search for Fastboot Devices', button_color='#3ddc84', font='5', size=(16,2), key="opt2")],
        [sg.Button('Android Device Logcat', button_color='#3ddc84', font='5', size=(16,2), key="opt3"), sg.Button('Android Device Backup', button_color='#3ddc84', font='5', size=(16,2), key="backup")],
        [sg.Button('Send file over ADB', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Sideload OTA package', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
        [sg.Button('Install Android App', button_color='#3ddc84', font='5', size=(16,2), key="opt1"), sg.Button('Uninstall Android App', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
        [sg.Button('Flash a Generic System Image', button_color='#3ddc84', font='5', size=(16,2), key="optgsi"), sg.Button('Unlock Android Bootloader', button_color='#3ddc84', font='5', size=(16,2), key="opt0")],
        [sg.Button('Backup Current boot.img', button_color='#3ddc84', font='5', size=(16,2), key="optboot"), sg.Button('Modify Current DPI', button_color='#3ddc84', font='5', size=(16,2), key="opt1")],
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
        [sg.Text("\n" * 2 )]]


window = sg.Window("PyDroidGUI", layout,background_color='#4285f4')
window.set_icon("src/icon.png")



while True :

    window.refresh()
    event, values = window.read()

    if event == "opt1" :
        message = os.system("cd platform-tools & adb devices")
        sg.Print('ADB Devices Found\nIf your device is not found, check your USB cable \n\n', do_not_reroute_stdout=False)
        print = sg.Print
        print(device_search())

    elif event == "opt2" :
        message = os.system("cd platform-tools & fastboot devices")
        sg.Print('Fastboot Devices Found\nIf your device is not found, check your USB cable \n\n', do_not_reroute_stdout=False)
        print = sg.Print

    elif event == "opt3" :
        window_update = window_logcat("Get Android Device Logcat")
        event, values = window_update.read()

        if event == "Ok" :
            my_device_model = model()
            logcat = "logcat" + "-" + my_device_model + ".txt"
            logcat = logcat.replace("\n.txt", ".txt")
            os.system("cd platform-tools & adb logcat -d -b main -b system -b events -v time > %s" % logcat)
            window_sucess = window_success("Success")
            event, values = window_sucess.read()

            if event == "Ok" or event == sg.WIN_CLOSED:
                window_update.close()
                window_sucess.close()

        elif event == "Cancel" or event == sg.WIN_CLOSED:
            window_update.close()

    elif event == "opt0" :
        window_update = window_unlock("Get Android Device Logcat")
        event, values = window_update.read()

        if event == "Unlock Bootloader" :
            os.system("cd platform-tools & fastboot flashing unlock")
            window_sucess = window_success("Success")
            event, values = window_sucess.read()

            if event == "Ok" or event == sg.WIN_CLOSED:
                window_update.close()
                window_sucess.close()

        elif event == "Cancel" or event == sg.WIN_CLOSED:
            window_update.close()
        
    elif event == "update" :
        if check_for_updates(version) == True :
            window_update = window_changelog("Check for Updates")
            event, values = window_update.read()

            if event == "Perform Update" :

                if platform.system() == "Linux" :
                    os.system("rm -f PyDroidGUI.py")
                else :
                    os.system("del /f PyDroidGUI.py")

                os.system("wget https://github.com/daviiid99/PyDroidGUI/raw/main/PyDroidGUI.py")
                os.system("python3 PyDroidGUI.py")
                window_sucess = window_success("Success")
                event, values = window_sucess.read()

                if event == "Ok" or event == sg.WIN_CLOSED:
                    window_update.close()
                    window_sucess.close()

            elif event == "Cancel" or event == sg.WIN_CLOSED:
                window_update.close()
        
        else :
            window_update = window_version("PyDroid Version")
            event, values = window_update.read()

            if event == "Cancel" or event == sg.WIN_CLOSED:
                window_update.close()

    elif event == "optboot" :
        window_update = window_boot("Get Android Device Logcat")
        event, values = window_update.read()
        my_device_model = model()
        my_device_model_img = my_device_model + ".img"
        my_device_model_img = my_device_model_img.replace("\n.img", ".img")

        if event == "A-Only Partition" :
            os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot boot_%s" % my_device_model_img)
            window_sucess = window_success("Success")
            event, values = window_sucess.read()

            if event == "Ok" or event == sg.WIN_CLOSED:
                window_update.close()
                window_sucess.close()

        elif event == "A|B Partitions" :
            os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot_a boot_a_%s" % my_device_model_img)
            os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot_b boot_b_%s" % my_device_model_img)
            window_sucess = window_success("Success")
            event, values = window_sucess.read()

            if event == "Ok" or event == sg.WIN_CLOSED:
                window_update.close()
                window_sucess.close()

        elif event == "Cancel" or event == sg.WIN_CLOSED:
                window_update.close()
        
    elif event == "optgsi" :
        window_update = window_gsi("Flash a Generic System Image")
        event, values = window_update.read()

        if event == "Flash GSI" :
            print(values["-FILE-"])

    elif event == "search" :
        refresh()
        refresh_logo()
        if brand() != "unknown\n" and check_adb_device() !="unknown\n" :
            window["power"].update(visible=True)

        elif "unknown\n" in brand() :
            window["power"].update(visible=False)
            

    elif event == "tools":

        if platform.system() == "Linux" :
            adb = adb_linux
            file = linux

        else :
            adb = adb_windows
            file = windows

        if android_tools_exists(adb, file) == True :

            window_update = window_tools("Reinstall Platform-Tools")
            event, values = window_update.read()

            if event == "Perform Update" :

                if platform.system() == "Linux" :
                    os.system("rm -rf platform-tools")
                else :
                    os.system("rmdir /S /Q platform-tools")

                android_tools_exists(adb_linux, linux)

                window_sucess = window_success("Success")
                event, values = window_sucess.read()

                if event == "Ok" or event == sg.WIN_CLOSED:
                    window_update.close()
                    window_sucess.close()

            elif event == "Cancel" or event == sg.WIN_CLOSED:
                window_update.close()

    elif event == "power" :
        window_update = window_control("Device Control")
        event, values = window_update.read()

        if event == "Reboot Recovery" :
            os.system("cd platform-tools & adb shell reboot recovery")
            window_update.close()

        elif event == "Reboot System  " :
            os.system("cd platform-tools & adb reboot system")
            window_update.close()

        elif event == "Reboot Fastboot" :
            os.system("cd platform-tools & adb shell reboot bootloader")
            window_update.close()

        elif event == "PowerOff Phone" :
            os.system("cd platform-tools & adb shell reboot -p")
            window_update.close()

        elif event == sg.WIN_CLOSED:
            window_update.close()

    elif event == "backup" :
        window_update = window_backup("Device Backup")
        event, values = window_update.read()
        allowed = []

        if event == "start" :
           
            if values["DCIM"] == True :
                allowed.append("DCIM")

            if values["PICTURES"] == True :
                allowed.append("Pictures")

            if values["DOWNLOADS"] == True :
                allowed.append("Download")

            if values["MUSIC"] == True :
                allowed.append("Music")

            if values["DOCUMENTS"] == True :
                allowed.append("Documents")

        device_backup(allowed)

        window_update.close()

    elif event == sg.WIN_CLOSED:
        break

window.close()