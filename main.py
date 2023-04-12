import sys
import os
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from intent_classifier import *
from asr import *
from slot_detection import *

# move file

# create file
# create folder
# delete file
# list files and folders in directory
# change directory

# edit file with vim
# write and save file to vim

utterances = {
# 'MOVE_FILE':["Move this file to the Documents folder.",
#                             "I want to move the file to the Desktop.",
#                             "Can you move the file in the Downloads folder to the Pictures folder?",
#                             "Please move the file that I just opened to the Music folder.",
#                             "How do I move the file in the Recycle Bin to the Videos folder?",
#                             "Move the file with today\’s date to the Backup folder.",
#                             "Show me how to move the file in the Dropbox folder to the OneDrive folder.",
#                             "Move all the files in the Work folder to the Personal folder.",
#                             "What is the easiest way to move the file in the Google Drive folder to the iCloud folder?",
#                             "Move the file that I just downloaded to the USB drive."],

            'CREATE_FILE':["Create a new file",
                            "I want to make a new file",
                            "New file",
                            "Create file",
                            "Make a new file",
                            "Can you make me a new file",
                            "Is it possible for you to produce a file",
                            "New file",
                            "Generate a file",
                            "Construct a new file",
                            "Construct",
                            "Create a file",
                            "Create a new file for me",
                            "File",
                            "I want to create a new file"],

            'CREATE_FOLDER':["Create a new folder",
                            "I want to make a new folder",
                            "New folder",
                            "Create folder",
                            "Make a new folder",
                            "Can you make me a new folder",
                            "Is it possible for you to produce a folder",
                            "New folder",
                            "Generate a folder",
                            "Construct a new folder",
                            "Construct folder",
                            "Create a folder",
                            "Create a new folder for me",
                            "Folder",],

            'DELETE_FILE':["Can you delete the file",
                            "Delete file",
                            "The file delete",
                            "I want to delete a file",
                            "I want the file deleted",
                            "Will you delete a file for me",
                            "File delete",
                            "Delete the file",
                            "I am going to delete a file",
                            "Remove the file",
                            "I want to remove a file",],

            'LIST':["Show me the files",
                    "I want to see the files",
                    "List",
                    "Show the files",
                    "List the files",
                    "What is in here",
                    "Where am i",
                    "Display the files",
                    "Show files",
                    "Show",
                    "Show the directories",
                    "Show me files",
                    "I want to see files",
                    "What files are there",
                    "Show files and folders"],

            'MOVE':["I want to change directories",
                    "Change directory",
                    "Move into a new folder",
                    "Go to this folder",
                    "Go to the movies folder",
                    "Move",
                    "Change",
                    "Go to another folder",
                    "Change folders",
                    "Move directories",
                    "Go to folder",
                    "Take me to another folder",
                    "Take me to the folder",
                    "Go to a new directory",
                    "I want to see the directory",
                    "I want to see the folder",
                    "I want to go to the"
                    "Navigate to the folder",
                    "Navigate",
                    "Take me to the folder",
                    "Take me to"],
                    
            # 'EDIT':["I want to edit a file",
            #         "Edit file",
            #         "Edit",
            #         "Edit the file temp.txt",
            #         "Manipulate the file",
            #         "Make edits to the file",
            #         "Change the file",
            #         "Make changes to the file",
            #         "Can you edit the file",
            #         "Please edit the file",],
            }
            # 'WRITE_SAVE':["I want to write and save the file",
            #             "Write and save",
            #             "Create a new file and save it",
            #             "Create and save",
            #             "Write and store",
            #             "Make a new file and save it",
            #             "Write and save a new file",
            #             "Write save",
            #             "I want a new file and I want to save it",
            #             "New file and save",]}

def list_directory(path, filestructure):
    path_list = path.split()
    print(path_list)
    # if path only has home
    #return ''.join(list(filestructure.keys()))

    if len(path_list) == 0:
        return ' '.join(list(filestructure.keys()))
    else:
        past = filestructure
        for dir in path_list:
            past = past[dir]
        return ' '.join(list(past.keys()))

def change_path(dir, path, filestructure):
    path_list = path.split()
    # check if path actually exists
    past = filestructure
    for dir in path_list:
        past = past[dir]
    
    if dir in past.keys():
        print('new path: ', path + ' ' + dir)
        return path + ' ' + dir
    else:
        return path

def create_file(path, struct, filename, content=""):
    path = path.split()
    if len(path) == 0:
        if filename in struct.keys():
            the_try = 1
            filename2 = filename + '({})'.format(the_try)
            while filename2 in struct.keys():
                the_try += 1
                filename2 = filename + '({})'.format(the_try)
            
            filename = filename2

        # add the file
        struct[filename] = content
        return
    create_file(' '.join(path[1:]), struct[path[0]], filename)
    return

def delete_file(path, struct, filename):
    print('path: ', path)
    path = path.split()
    if len(path) == 0:
        print('keys: ', struct.keys())
        if filename in struct.keys():
            # delete the file
            del struct[filename]
            return True
        else:
            return False
    return delete_file(' '.join(path[1:]), struct[path[0]], filename)

# def move_file(path, struct, filename, depth):
#     path = path.split()
#     if len(path) == 0:

    

def create_folder(path, struct, foldername:str):
    path = path.split()
    if len(path) == 0:
        # create the folder
        if foldername in struct.keys():
            the_try = 1
            foldername2 = foldername + '({})'.format(the_try)
            while foldername2 in struct.keys():
                the_try += 1
                foldername2 = foldername + '({})'.format(the_try)
                
            foldername = foldername2
            
        struct[foldername] = {}
        return
    create_folder(' '.join(path[1:]), struct[path[0]], foldername)
    return

class Conch():
    def __init__(self):
        self.path = ""
        self.filestructure = {'firstdirectory':{'testfile.txt':"This is the content of the file."}, 'seconddirectory':{'testfile2.txt':"Contents of the file."}}
        self.command_history = []
        self.command_idx = -1
        self.command_distance = -1
        self.window()
    
    def previous_command(self):
        if self.command_idx == -1:
            self.lineedit.setText("")
        else:
            self.command_idx -= 1
            old_command = self.command_history[self.command_idx]
            self.lineedit.setText(old_command)
    
    def update_console(self):
        #self.console.appendPlainText("{} - Test".format(datetime.datetime.now().strftime('%m/%d/%Y-%H:%M:%S')))

        if self.lineedit.text() == '':
            recorded_audio = record_audio(int(self.timeedit.text()))
            
            transcription = detect_spoken(recorded_audio)[0]
        else:
            transcription = self.lineedit.text()

        if transcription[-1] == '.':
            transcription = transcription[:-1]

        self.command_history.append(transcription)
        self.command_distance += 1
        self.command_index = self.command_distance

        #self.console.appendPlainText("Transcription: {}".format(transcription))
        detectedIntent = detectIntent(transcription, utterances, list(utterances.keys()))

        #self.console.appendPlainText("Detected Intent: {}".format(detectedIntent))
        self.console.appendPlainText("{} - Transcription: {} - Detected Intent: {}".format(datetime.datetime.now().strftime('%m/%d/%Y-%H:%M:%S'), transcription, detectedIntent))

        print('detected intent: ', detectedIntent)
        if detectedIntent == 'MOVE_FILE':
            # I NEED TO FIGURE OUT HOW TO GET THE FILE AND DIRECTORY FROM ASR
            pass

        elif detectedIntent == 'CREATE_FILE':
            # I NEED TO FIGURE OUT HOW TO GET THE FILE AND CONTENTS FROM ASR
            subs = '.txt'
            res = [i for i in transcription.split() if subs in i]
            if len(res) == 0:
                filename = 'temp.txt'
            else:
                filename = res[0].lower()
            create_file(self.path, self.filestructure, filename)
            
        elif detectedIntent == 'CREATE_FOLDER':
            # I NEED TO FIGURE OUT HOW TO GET THE DIRECTORY FROM ASR
            new_dir = detect_slot(transcription, "What is the name of the folder the user wants to go to?")['answer']
            new_dir = ''.join(new_dir.split()).lower()
            create_folder(self.path, self.filestructure, new_dir)

        elif detectedIntent == 'DELETE_FILE':
            # I NEED TO FIGURE OUT HOW TO GET THE FILE FROM ASR
            subs = '.txt'
            res = [i for i in transcription.split() if subs in i]
            if len(res) == 0:
                filename = 'temp.txt'
            else:
                filename = res[0]

            success = delete_file(self.path, self.filestructure, filename)
            if success:
                self.console.appendPlainText("Successfully deleted {}".format(filename))
            else:
                self.console.appendPlainText("ERROR: Could not delete the specified file. It might not exist.")

        elif detectedIntent == 'LIST':
            self.console.appendPlainText("Files: {}".format(list_directory(self.path, self.filestructure)))
            self.console.appendPlainText("PATH: {}".format('/'.join(self.path.split())))

        elif detectedIntent == 'MOVE':
            keywords = ["up", "back", "out", "higher", "upper", "previous"]
            res = [i for i in transcription.split() if i in keywords]
            if len(res) >= 1:
                self.path = ' '.join(self.path.split()[:-1])
            else:
                # I NEED TO FIGURE OUT HOW TO GET THE DIRECTORY FROM ASR
                new_dir = detect_slot(transcription, "What is the name of the folder the user wants to go to?")['answer']
                new_dir = ''.join(new_dir.split()).lower()
                self.path = change_path(new_dir, self.path, self.filestructure)
            self.console.appendPlainText("PATH: {}".format('/'.join(self.path.split())))

        elif detectedIntent == 'EDIT':
            # I NEED TO FIGURE OUT HOW TO GET THE FILE FROM ASR
            pass
        elif detectedIntent == 'WRITE_SAVE':
            # I NEED TO FIGURE OUT HOW TO GET THE FILE FROM ASR
            pass
        
        print("update_console")
        print(self.filestructure)
        self.lineedit.setText('')
        self.console.appendPlainText("")

    def window(self):
        app = QApplication(sys.argv)

        w = QWidget()
        WINDOW_WIDTH=600
        WINDOW_HEIGHT=400
        w.setGeometry(200,200,WINDOW_WIDTH,WINDOW_HEIGHT)

        seconds = QLabel(w)
        seconds.setText("Seconds")
        seconds.move(522, 40)

        dur = QLabel(w)
        dur.setText("Recording Duration")
        dur.move(455, 20)

        timeedit = QLineEdit(w)
        timeedit.setGeometry(0,0,20,20)
        timeedit.setReadOnly(False)
        timeedit.move(500,40)
        timeedit.setText("4")
        self.timeedit = timeedit

        # ----- setup console ----- #
        lineedit=QLineEdit(w)
        lineedit.setGeometry(0,0,WINDOW_WIDTH-40,20)
        lineedit.setReadOnly(False)
        lineedit.returnPressed.connect(self.update_console)
        #lineedit.keyPressEvent(QKeyEvent.key()).connect(self.previous_command)
        
        console = QPlainTextEdit(w)
        console.setGeometry(0,0,WINDOW_WIDTH,300)
        console.setReadOnly(True)
        lineedit.move(3,w.height()-lineedit.height()-3)
        console.move(0,w.height()-console.height()-lineedit.height()-3)

        #lineedit.setText(os.getcwd() + ">")
        self.lineedit = lineedit

        button = QPushButton(w)
        button.setGeometry(w.width()-40,w.height()-27,40,30)
        button.clicked.connect(self.update_console)
        button.setCursor(Qt.PointingHandCursor)
        button.setText("Rc")
        self.button = button
        # ----- ----- #

        b = QLabel(w)
        b.setText("Welcome to the voice controlled terminal.\nThis is a work in progess.\nYou can verbally execute commands such as \'ls\', \'cd\', etc.\nwith commands such as \'move to a new directory\'" )

        #b2 = QLabel(w)
        #b2.setText(str(self.filestructure))
        #self.b2 = b2

        b.move(50,10)
        #b2.move(50,30)
        w.setWindowTitle("Conch")
        w.show()
        self.console = console
        sys.exit(app.exec_())

if __name__ == '__main__':
    Conch()