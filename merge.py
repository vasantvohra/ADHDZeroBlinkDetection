import Tkinter as tk   # python3

TITLE_FONT = ("Helvetica", 18, "bold")

import cv2
import numpy as np
import time
import sys
import os
from pygame import mixer

#import statistics

from PIL import Image
import glob
from time import gmtime, strftime



TITLE_FONT = ("Helvetica", 18, "bold")
global rateTime
rateTime=0
patientTimeLog = open("patientBlinkTime.txt", 'a')

def alert():
     mixer.init()
     alert=mixer.Sound('beep-07.wav')
     alert.play()
     time.sleep(0.1)
     alert.play()



def initializeFiles(name,age):
    patientLog = open("patientBlinkRate.txt", 'w')
    patientLog.truncate()
    print >> patientLog, 'Name:', name
    print >> patientLog, 'Age:', age

    patientTimeLog = open("patientBlinkTime.txt", 'w')
    patientTimeLog.truncate()
    print >> patientTimeLog, 'Name:', name
    print >> patientTimeLog, 'Age:', age

class AdhdGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("ADD-ZERO")

        self.frames = {}
        self.frames["StartPage"] = StartPage(parent=container, controller=self)
        self.frames["PageOne"] = PageOne(parent=container, controller=self)
        self.frames["PageTwo"] = PageTwo(parent=container, controller=self)
        self.frames["PageThree"] = PageThree(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["PageOne"].grid(row=0, column=0, sticky="nsew")
        self.frames["PageTwo"].grid(row=0, column=0, sticky="nsew")
        self.frames["PageThree"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        '''GUI FIRST PAGE'''
        label_1 = tk.Label(self, text="ADHD Zero", font=TITLE_FONT)
        label_1.config(font=("Courier", 44))
        label_1.pack(side="top", fill="x", pady=10)
        label_2 = tk.Label(self, text="Patient Name")
        label_3 = tk.Label(self, text="Patient Age")
        label_4 = tk.Label(self, text="cons doctor")
        entry_1 = tk.Entry(self)
        entry_2 = tk.Entry(self)
        entry_3 = tk.Entry(self)

        label_1.grid(row=0, column=1)
        label_2.grid(row=3, sticky= "W")
        label_3.grid(row=4, sticky= "W")
        label_4.grid(row=5, sticky= "W")

        entry_1.grid(row=3, column=1)
        entry_2.grid(row=4, column=1)
        entry_3.grid(row=5, column=1)

        def saveData():
            pName = entry_1.get()
            pAge = entry_2.get()
            cDoctor = entry_3.get()
            if len(entry_1.get()) == 0 or len(entry_2.get()) == 0 or len(entry_3.get()) == 0:
                print("Alert", "Please make sure that all fields are not empty")
            else:
		initializeFiles(pName,pAge)
                controller.show_frame("PageOne")

        button_1 = tk.Button(self, text="Start", command=saveData)
        button_2 = tk.Button(self, text="Exit", command=self.quit)
        button_1.grid(row=9, column=3)
        button_2.grid(row=9, column=4)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label_1 = tk.Label(self, text="Test Configuration", font=TITLE_FONT)
        label_1.config(font=("Courier", 34))
        label_1.grid(row=1, sticky="W")
        label_2 = tk.Label(self, text="Blinking Rate")
        entry_1 = tk.Entry(self)
        label_2.grid(row=3, sticky="W")
        entry_1.grid(row=3, column=1)
        cameraFrameIsChecked = tk.IntVar()
        logIsChecked = tk.IntVar()
        trainIsChecked = tk.IntVar()

        def saveDataAndProceed():
            if len(entry_1.get()) != 0 and trainIsChecked.get() == 1:
                global rateTime
                rateTime = float(entry_1.get())
                controller.show_frame("PageThree")
            elif len(entry_1.get()) != 0 and trainIsChecked.get() == 0:
                global rateTime
                rateTime = float(entry_1.get())
                controller.show_frame("PageTwo")
            else:
                print("Alert", "Please Fill in Blinking Rate Field")

        cameraFrameCB = tk.Checkbutton(self, text="Show Camera Frame", variable=cameraFrameIsChecked)
        logCB = tk.Checkbutton(self, text="Log Blinks TimeStamps", variable=logIsChecked)
        trainCB = tk.Checkbutton(self, text="Set Application for Training", variable=trainIsChecked)
        cameraFrameCB.grid(row=5, column=0, sticky="W")
        logCB.grid(row=6, column=0, sticky="W")
        trainCB.grid(row=7, column=0, sticky="W")
        button_1 = tk.Button(self, text="Start", command=saveDataAndProceed)
        button_1.grid(row=10, column=2)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        '''GUI FIRST PAGE'''
        def looping():

                face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                eye_cascade = cv2.CascadeClassifier("CustomBlinkCascade.xml")

                cap = cv2.VideoCapture(0)
                x = 0
                y = 0
                h = 0
                w = 0
                ey = 0
                ex = 0
                eh = 0
                ew = 0
                Blinks = 0
                img = np.zeros((800, 800, 3), np.uint64)
                start = True
                total = 2.0
                blinkDetected = False
                oneEyeDetected = False
                blinkDetectionThreshold = 0.5
                rateStart = True
                timeNow = 0
                timeLater = 0
                rateTotal = 0
                rate = 0
                blinksTemp = 0
                rateBlinks = 0
                rateCount = 0
                ratenumber =0
                max = 0.0
                min = 10000.0
                ratenumber=1
                average =0
                font = cv2.FONT_HERSHEY_SIMPLEX
                blinkRateArray= []
                standardDeviation = 0
                tempForDecimials=0.0

                while cap.isOpened():
                    if rateStart == True:
                        timeNow = time.time()
                        rateStart = False
                        blinksTemp = Blinks

                    timeLater = time.time()
                    rateTotal = timeLater - timeNow
                    if rateTotal > rateTime:
                        patientLog = open("patientBlinkRate.txt", 'a')
                        rateStart = True
                        rateBlinks = Blinks - blinksTemp
                        rate = float(rateBlinks) / rateTime
                        rateCount = rateCount + 1


                        if min>rateBlinks:
                            min=rateBlinks
                        if max<rateBlinks:
                            max=rateBlinks
                        ratenumber = ratenumber +1
                        average = (Blinks) /ratenumber
                        blinksRate = rate/ratenumber
                        blinkRateArray.append(blinksRate)
                        standardDeviation = np.std(blinkRateArray)
                        print "SD: "
                        print standardDeviation

                        print "*************************************************"
                        print "Blinking Rate: ", rateBlinks, "s Per ", rateTime, " Seconds."
                        print "Total rate: ", rate, "per rate time."
                        rateString = "Blinking Rate: " + str(rateBlinks) + " Per " + str(rateTime) + " Seconds."
                        totalRateString = "Incrementing average : " + str(average) + " per rate time."
                        StandardDeviationString = "Standard Deviation  : " + str(standardDeviation)

                        patientLog.write(str(rateCount))
                        patientLog.write("\n")
                        patientLog.write(str(rateString))
                        patientLog.write("\n")
                        patientLog.write(str(totalRateString))
                        patientLog.write("\n")
                        patientLog.write(str(StandardDeviationString))
                        patientLog.write("\n")
                        patientLog.close()
                        if rate < 0.1:
                            alert()

                    if blinkDetected == True:
                        if start == True:
                            start = False
                            tStart = time.time()
                        tEnd = time.time()
                        total = tEnd - tStart
                        if total > blinkDetectionThreshold:
                            start = True
                            blinkDetected = False
                    ret, frame = cap.read()
                    rett, newframe = cap.read()
                    if ret:
                        gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        # gray = cv2.equalizeHist(gray2)
                        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                        gray = clahe.apply(gray2)
                        faces = face_cascade.detectMultiScale(
                            gray,
                            scaleFactor=1.3,
                            minNeighbors=5,
                            minSize=(50, 50)
                        )

                        for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            roi_gray = gray[y:y + h, x:x + w]
                            roi_color = frame[y:y + h, x:x + w]
                            eyes = eye_cascade.detectMultiScale(
                                roi_gray,
                                scaleFactor=1.2,
                                minNeighbors=5,
                                minSize=(15, 15),
                                maxSize=(80, 80)
                            )
                        try:
                            eyes
                        except NameError:
                            print "well, no eyes are detected!"
                        else:
                            ii = 0
                            for (ex, ey, ew, eh) in eyes:
                                if ii < 1 and ey < (h * .33) and (total > blinkDetectionThreshold) and oneEyeDetected == False:
                                    
                                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
                                  
                                    patientTimeLog = open("patientBlinkTime.txt", 'a')
                                    print "#########################Blink Detected##############################"
                                    print >> patientTimeLog, 'Blink Detected'
                                    print >> patientTimeLog, 'Blink Time: ', strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    patientTimeLog.close()
                                    blinkDetected = True
                                    Blinks = Blinks + 1
                                    print Blinks
                                    blinkCountResultLabel.config(text = str(Blinks))
                                    tempForDecimials = round(max, 3)
                                    blinkMaxResultLabel.config(text = str(tempForDecimials))
                                    tempForDecimials = round(min, 3)
                                    blinkMinResultLabel.config(text = str(tempForDecimials))
                                    tempForDecimials = round(average, 3)
                                    blinkAvgResultLabel.config(text = str(tempForDecimials))
                                    tempForDecimials = round(standardDeviation, 3)
                                    blinkRateResultLabel.config(text= str(tempForDecimials))
                                    if standardDeviation<=0.06:
                                         blinkstateShape.config(text=str(">90%"))
                                    if standardDeviation > 0.08 and standardDeviation <=0.1:
                                        blinkstateShape.config(text=str("<80%"))
                                    if standardDeviation > 0.1 and standardDeviation <= 0.15:
                                        blinkstateShape.config(text=str("<60%"),bg = "yellow")
                                    if standardDeviation > 0.15 and standardDeviation <= 0.2:
                                        blinkstateShape.config(text=str("<50%"), bg = "yellow")
                                    if standardDeviation > 0.2 and standardDeviation <= 0.3:
                                        blinkstateShape.config(text=str("<40%"), bg="red")
                                    if standardDeviation >0.3:
                                        blinkstateShape.config(text=str("<30%"), bg="red")

                                    cv2.putText(frame, 'Blinked!', (10, 30), font, 1, (255, 0, 0), 2)
                                    blinkMaxResultLabel.config(text = str(max))
                                    blinkMinResultLabel.config(text = str(min))
                                    blinkAvgResultLabel.config(text = str(average))
                                    oneEyeDetected = True
                                    print "ex:", ex
                                    print "ew:", ew
                                    print "ey:", ey
                                    print "eh:", eh
                                    print "x:", x
                                    print "w:", w
                                    print "y:", y
                                    print "h:", h
                                    xs = [ex, ew, ey, eh]
                                    print xs
                                    img = gray[y: y + h, x: x + w]  # its img[y: y + h, x: x + w]
                                    ii = ii + 1

                                    print "Start: ", start
                                    print "Total: ", total

                            oneEyeDetected = False


                            
                    cv2.putText(frame, 'Press Esc to end the experiment!', (10, 460), font, 1, (255, 255, 255), 2)

                    cv2.imshow("Faces found", frame)
                    cv2.imshow("Blink found", img)
                    k = cv2.waitKey(10) & 0xff
                    if k == 27:
                        print "SD: "
                        print standardDeviation
                        print blinkRateArray
                        cv2.destroyWindow("Faces found")
                        cv2.destroyWindow("Blink found")
                        break
                return
        blinkstateLabel = tk.Label(self, text="Test Result:")
        blinkstateLabel.grid(row=0, column=0)

        blinkstateShape = tk.Label(self, text="None", bg="green", width=40, height=3, fg="white",
                                   font=(None, 15))
        blinkstateShape.grid(row=1, column=0)


        blinkstateLabel = tk.Label(self, text="Focus percentage:")
        blinkstateLabel.grid(row=0, column=0)

        blinkstateShape = tk.Label(self, text="Eyes Are Openned", bg="green", width=40, height=3, fg="white",
                                   font=(None, 15))
        blinkstateShape.grid(row=1, column=0)

        blinkRateLabel = tk.Label(self, text="Blinking Rate Standard Deviation")
        blinkRateLabel.grid(row=0, column=1, sticky="w", ipadx=10)

        blinkRateResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkRateResultLabel.grid(row=1, column=1, sticky="w", ipadx=10)


        blinkCountLabel = tk.Label(self, text="Blink Count:")
        blinkCountLabel.grid(row=3, column=1, sticky="w", ipadx=10)

        blinkCountResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkCountResultLabel.grid(row=4, column=1, ipadx=10)

        blinkAvgLabel = tk.Label(self, text="Blink Average:")
        blinkAvgLabel.grid(row=3, column=0, sticky="w")

        blinkAvgResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkAvgResultLabel.grid(row=4, column=0)

        blinkMaxLabel = tk.Label(self, text="Blink Max:")
        blinkMaxLabel.grid(row=5, column=0, sticky="w")

        blinkMaxResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkMaxResultLabel.grid(row=6, column=0)

        blinkMinLabel = tk.Label(self, text="Blink Min:")
        blinkMinLabel.grid(row=5, column=1, sticky="w", ipadx=10)

        blinkMinResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkMinResultLabel.grid(row=6, column=1, ipadx=10)

        startButton = tk.Button(self, text="Start/Stop", bg="blue",command=looping)
        startButton.grid(row=7, column=0, sticky="w", padx=150)

        pauseButton = tk.Button(self, text="Pause/Resume", bg="blue")
        pauseButton.grid(row=7, column=0, sticky="E", padx=130)

        reesetButton = tk.Button(self, text="Reset", bg="blue")
        reesetButton.grid(row=7, column=1, sticky="w", padx=10)

        configButton = tk.Button(self, text="Config", bg="blue", command=lambda: controller.show_frame("PageOne"))
        configButton.grid(row=7, column=1, sticky="E")

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        '''GUI FIRST PAGE'''
        label_1 = tk.Label(self, text="Training", font=TITLE_FONT)
        label_1.config(font=("Courier", 34))
        label_1.grid(row=1, sticky="W")
        blinkstateLabel = tk.Label(self, text="Blink State:")
        blinkstateLabel.grid(row=3, column=0)

        blinkstateShape = tk.Label(self, text="Eyes Are Openned", bg="green", width=40, height=3, fg="white",
                                   font=(None, 15))
        blinkstateShape.grid(row=4, column=0)

        blinkRateLabel = tk.Label(self, text="Blinking Rate per Time Unit")
        blinkRateLabel.grid(row=3, column=1, sticky="w", ipadx=10)

        blinkRateResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkRateResultLabel.grid(row=4, column=1, sticky="w", ipadx=10)

        blinkRateResultRateLabel = tk.Label(self, text="/Min", font=(None, 15))
        blinkRateResultRateLabel.grid(row=4, column=1, sticky="E")

        blinkCountLabel = tk.Label(self, text="Blink Count:")
        blinkCountLabel.grid(row=6, column=1, sticky="w", ipadx=10)

        blinkCountResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkCountResultLabel.grid(row=7, column=1, ipadx=10)

        blinkAvgLabel = tk.Label(self, text="State:")
        blinkAvgLabel.grid(row=6, column=0, sticky="w")

        blinkAvgResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkAvgResultLabel.grid(row=7, column=0)

        blinkMinLabel = tk.Label(self, text="Blink Min:")
        blinkMinLabel.grid(row=8, column=1, sticky="w", ipadx=10)

        blinkMinResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkMinResultLabel.grid(row=9, column=1, ipadx=10)

        blinkMinLabel = tk.Label(self, text="Focus Avg:")
        blinkMinLabel.grid(row=10, column=1, sticky="w", ipadx=10)

        blinkMinResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkMinResultLabel.grid(row=11, column=1, ipadx=10)

        blinkMinLabel = tk.Label(self, text="Drowsiness Avg:")
        blinkMinLabel.grid(row=12, column=1, sticky="w", ipadx=10)

        blinkMinResultLabel = tk.Label(self, text="X", font=(None, 15))
        blinkMinResultLabel.grid(row=13, column=1, ipadx=10)

        startButton = tk.Button(self, text="Start/Stop")
        startButton.grid(row=15, column=0, sticky="we")

        pauseButton = tk.Button(self, text="Pause/Resume")
        pauseButton.grid(row=15, column=1, sticky="we")

        reesetButton = tk.Button(self, text="Reset")
        reesetButton.grid(row=15, column=2, sticky="we")

        configButton = tk.Button(self, text="Config", command=lambda: controller.show_frame("PageOne"))
        configButton.grid(row=15, column=3, sticky="we")

if __name__ == "__main__":
    app = AdhdGUI()
    app.mainloop()
