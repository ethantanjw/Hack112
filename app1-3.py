from tkinter import *
from tkinter import filedialog
from fer import FER
import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from songGenerator import *
import requests
from io import BytesIO
from facialemotionrecog import *
import webbrowser

# Class structure: https://stackoverflow.com/questions/69079608/how-to-make-multiple-pages-in-tkinter-gui-app
class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x400")
        self.mainPage()
        
    def uploadPicture(self):
        # Create an import button: https://stackoverflow.com/questions/50123315/how-do-i-create-an-import-file-button-with-tkinter
        self.filename = filedialog.askopenfilename()
        self.test_image_one = plt.imread(self.filename)
        self.filenameSplit = self.filename.split('/')
        label130 = tk.Label(text="Uploaded.",font = "Arial 12")
        label130.pack(side = BOTTOM)

    def mainPage(self):
        for i in self.master.winfo_children():
            i.destroy()
        title = tk.Label(text="\n\n\nSpotitector",font = "Arial 35")
        title.pack(side = TOP)
        title = tk.Label(text="\n\nPlay a song based on your detected emotion.",font = "Arial 20")
        title.pack(side = TOP)
        spacing = tk.Label(text="\n\n\n")
        spacing.pack(side =BOTTOM)
        viewPic = ttk.Button(text="View Your Picture", command=self.viewPicture)
        viewPic.pack(side = BOTTOM, expand = False)
        chooseFile = ttk.Button(root, text="Choose File", command=self.uploadPicture)
        scanFace = ttk.Button(text="Scan Your Face", command=self.afterScanPage)
        chooseFile.pack(side =BOTTOM)
        scanFace.pack(side = BOTTOM, expand = False)

    def afterScanPage(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.emotion = fer.scanFace()
        self.emotion = self.emotion[0].lower() + self.emotion[1:]
        goBack = ttk.Button(text="Go Back", command=self.mainPage)
        goBack.pack(side = TOP,expand = True)
        analyzed = tk.Label(text="Scan completed.")
        analyzed.pack(side="top", fill="both")
        getSong = ttk.Button(text="Get Your Song", command=self.showEmoScan)
        getSong.pack(side = TOP,expand = True)
        
    def showEmoScan(self):
        for i in self.master.winfo_children():
            i.destroy()
        spacing = tk.Label(text="\n\n\n\n")
        spacing.pack(side =TOP)
        analyzedEmo = tk.Label(text=f"Analyzed. \n\nYou are feeling {self.emotion}.",font='Arial 20')
        analyzedEmo.pack(side="top", fill="both")
        self.songstuff = sg.getSong(self.emotion)
        spacing = tk.Label(text="\n\n\n\n")
        spacing.pack(side = TOP)
        # Album cover
        self.artistImage = self.songstuff['art']
        response = requests.get(self.artistImage)
        img_data = response.content 
        img = Image.open(BytesIO(img_data))
        resize = img.resize((200,200))
        # https://stackoverflow.com/questions/13148975/tkinter-label-does-not-show-image
        bar = Frame(root)
        bar.pack(side=TOP)
        icon = ImageTk.PhotoImage(resize)
        icon_size = Label(bar)
        icon_size.image = icon
        icon_size.configure(image=icon)
        icon_size.pack(side=TOP)
        trackInfo = tk.Label(text=f"Track: {self.songstuff['artists']} - {self.songstuff['name']}")
        trackInfo.pack(side=TOP, fill="both")
        playSong = Button(text='Play Song', command =self.redirect)
        playSong.pack(side = BOTTOM, expand = True)
        spacing = tk.Label(text="\n\n\n\n")
        spacing.pack(side =BOTTOM)

    def viewPicture(self):
        for i in self.master.winfo_children():
            i.destroy()
        spacing = tk.Label(text="\n\n\n")
        spacing.pack(side =TOP)
        goBack = ttk.Button(text="Go Back", command=self.mainPage)
        goBack.pack()
        spacing = tk.Label(text="\n\n\n")
        spacing.pack(side =TOP)
        # Display album cover: https://stackoverflow.com/questions/13148975/tkinter-label-does-not-show-image
        bar = Frame(root)
        bar.pack(side=TOP)
        image = Image.open(self.filenameSplit[-1])
        resize = image.resize((600,400))
        icon = ImageTk.PhotoImage(resize)
        icon_size = Label(bar)
        icon_size.image = icon
        icon_size.configure(image=icon)
        icon_size.pack(side=TOP)
        spacing = tk.Label(text="\n\n\n")
        spacing.pack(side =BOTTOM)
        submitPic = Button(root, text='Submit', command =self.analyzeEmoImp)
        submitPic.pack(side =BOTTOM)
        confirmSub = tk.Label(text="Submit Picture?")
        confirmSub.pack(side=BOTTOM, fill="both", expand=True)

    def analyzeEmoImp(self):
        for i in self.master.winfo_children():
            i.destroy()
        # Emotion analyzer: https://gist.github.com/rjrahul24/e0e44edee1ebfe67e10b4c5f64855d1c
        self.emo_detector = FER(mtcnn=True)
        self.captured_emotions = self.emo_detector.detect_emotions(self.test_image_one)
        # plt.imshow(self.test_image_one)
        self.dominant_emotion, self.emotion_score = self.emo_detector.top_emotion(self.test_image_one)
        self.convertedEmotionScore = self.emotion_score * 100
        label1 = tk.Label(text=f"Analyzed {self.filenameSplit[-1]}\n\nYou are {self.convertedEmotionScore}% {self.dominant_emotion}")
        label1.pack(side="top", fill="both", expand=True)
        # Display album cover: https://stackoverflow.com/questions/13148975/tkinter-label-does-not-show-image
        self.songstuff = sg.getSong(self.dominant_emotion)
        bar = Frame(root)
        bar.pack(side=TOP)
        albCover = self.songstuff['art']
        response = requests.get(albCover)
        # Open image from URL: https://stackoverflow.com/questions/58583230/open-image-from-requests-response-content
        img_data = response.content 
        img = Image.open(BytesIO(img_data))
        resize = img.resize((200,200))
        icon = ImageTk.PhotoImage(resize)
        icon_size = Label(bar)
        icon_size.image = icon
        icon_size.configure(image=icon)
        icon_size.pack(side=TOP)
        showTrack = tk.Label(text=f"Track: {self.songstuff['artists']} - {self.songstuff['name']}")
        showTrack.pack(side=BOTTOM, fill="both", expand=True)
        pressPlay = Button(root, text='Play Song', command =self.redirect)
        pressPlay.pack(side = BOTTOM)

    def redirect(self):
        webbrowser.open(self.songstuff['url'])


sg = SongGenerator()
sg.assignSongs()
fer = EmotionRecognition()
root = Tk()
app(root)
root.title("Spotitector")
root.geometry('800x1000')
root.mainloop()



