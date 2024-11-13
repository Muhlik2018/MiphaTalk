import sys
from datetime import datetime
from GPTInteract import GPTReply
from GPTInteract import GPTToText
from WakeUpWord import WakeUpDetect
from SupportingFunction import EditAudioFile
from SupportingFunction import RecordAudio
from Desktop import PetView
from SupportingFunction import RecordAudio
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import threading
from SupportingFunction import GetKey


def record_sound(controlView,key):
# Example usage
    chatHistory=[{'role': 'system', 'content': 'You are mipha, a character from legends of Zelda'}]
    print("start")
    controlView.setIdling()
    while True:
        # frames=record_audio(0.5)
        # if  not frames is False:
        print("start catch hot word")
        isHotword=WakeUpDetect.detection()
        if isHotword:
            now = datetime.now()
            current_time = now.strftime("%H%M%S")
            controlView.setTalking(txt="Hi")
            EditAudioFile.multiOsSound("./Resources/Audio/Hear.mp3",False)
            controlView.setThinking()
            print("catch question...")
            main_frames =RecordAudio.record_audio(10,5)
            while not main_frames is False:
                audio_file_path="MAIN"+current_time+".wav"
                RecordAudio.save_audio(main_frames,audio_file_path)
                print("to text...")
                maintext=GPTToText.speechToText(audio_file_path,key)
                print("get answer...")
                EditAudioFile.multiOsRm(audio_file_path)
                GPTOutput=GPTReply.getGPTReply(maintext,chatHistory,key)
                chatHistory=GPTOutput[0]
                controlView.setTalking(txt=GPTOutput[1])
                EditAudioFile.multiOsSound(GPTOutput[2])
                if len(chatHistory)>=10:
                    chatHistory.pop(1)
                    chatHistory.pop(2)
                main_frames =RecordAudio.record_audio(10,5)
            EditAudioFile.multiOsSound("./Resources/Audio/Goodbye2.mp3",False)
            controlView.setIdling()
        else:
            print("No sound detected in this round")


class recordThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        record_sound(pet,key=GetKey.getKey())

class viewThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        app = QApplication(sys.argv)
        pet = PetView.DesktopPet()
        app.exec()



thread1 = recordThread(1, "Thread-1", 1)
# thread2 = viewThread(1, "Thread-2", 1)
app = QApplication(sys.argv)
pet = PetView.DesktopPet()
thread1.start()
app.exec()
