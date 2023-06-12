import os, sys
from os.path import join, getsize
import zipfile
import getpass
import shutil
import platform 

class ESP_FIRMWARE():
    def __init__(self):
        self.now_size = 0
        self.files_size = 0
        self.str_files_size = None

    def getdirsize(self, dir):
        size = 0
        for root, dirs, files in os.walk(dir):
            size += sum([getsize(join(root, name)) for name in files])
        return size
        
    def copy2_verbose(self, src, dst):
        shutil.copy2(src,dst)
        self.now_size += getsize(dst)
        str_now_size = str(int(self.now_size/1024/1024)) + "MB"
        #print(f'prcessing：{int(self.now_size / self.files_size * 100)}% ({str_now_size}/{self.str_files_size}): {dst}')
        print(f'prcessing：{int(self.now_size / self.files_size * 100)}% ({str_now_size}/{self.str_files_size})')
        
    def copy_esp32(self):
        genUserName = getpass.getuser()
        print("\r\nPC system: " + platform.system() + "\r\n")    

        if platform.system() == "Windows":
            local_dir = "C:\\Users\\" + genUserName + "\\AppData\\Local\\Arduino15\\packages"
            target_dir = local_dir + "\\freenove"
        elif platform.system() == "Darwin":
            local_dir = "/Users/" + genUserName + "/Library/Arduino15/packages"
            target_dir = local_dir + "/freenove"
        elif platform.system() == "Linux":
            local_dir = "/home/" + genUserName + "/.arduino15/packages"
            target_dir = local_dir + "/freenove"
        else:
            local_dir = "./"
            target_dir = local_dir + "freenove"
            print("Note that the file cannot be extracted to the specified location and has been placed in a peer directory.")
            print("Please copy the file manually.\r\n")
            print("Copy the freenove folder to the Arduino15/packages folder directory on your computer.")
        print("Target dir: " + target_dir + "\r\n")

        if os.path.exists(target_dir):
            print("Folder exists, delete it: " + target_dir + "\r\n")
            print("Please wait patiently.\r\n")
            shutil.rmtree(target_dir)
            
        print("Begin to copytree files, please wait patiently.\r\n")

        if platform.system() == "Windows":
            self.files_size=self.getdirsize("./Freenove/Windows")
            self.str_files_size = str(int(self.files_size/1024/1024)) + "MB"
            shutil.copytree("./Freenove/Windows", target_dir, copy_function=self.copy2_verbose)
        elif platform.system() == "Linux":
            self.files_size=self.getdirsize("./Freenove/Linux")
            self.str_files_size = str(int(self.files_size/1024/1024)) + "MB"
            shutil.copytree("./Freenove/Linux", target_dir, copy_function=self.copy2_verbose)
        else:
            self.files_size=self.getdirsize("./Freenove/Mac")
            self.str_files_size = str(int(self.files_size/1024/1024)) + "MB"
            shutil.copytree("./Freenove/Mac", target_dir, copy_function=self.copy2_verbose)

        print("The files have been extracted, please restart the Arduino IDE.\r\n")


if __name__ == '__main__':
    app = ESP_FIRMWARE()
    app.copy_esp32()