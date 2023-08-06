import os
from tkinter import filedialog

data = b""

def OpenOriginalFile():
    global data
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select original file", filetypes=(("jpg file", "*.jpg"),("png file", "*.png"), ("mp4 file", "*.mp4")))
    originalFile = open(filename, "rb")
    data = originalFile.read()
    originalFile.close()

def OpenFileToHide():
    global data
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open file to hide", filetypes=(("jpg file", "*.jpg"),("png file", "*.png"), ("mp4 file", "*.mp4")))
    fileToHide = open(filename, "rb")
    dataToHide = fileToHide.read()
    fileToHide.close()
    data += dataToHide

def SaveModifiedFile():
    global data
    filename = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open file to hide", filetypes=(("jpg file", "*.jpg"),("png file", "*.png"), ("mp4 file", "*.mp4")))
    modifiedFile = open(filename, "wb")
    modifiedFile.write(data)
    modifiedFile.close()

def ExtractHiddenData():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open manipulated file", filetypes=(("jpg file", "*.jpg"),("png file", "*.png"), ("mp4 file", "*.mp4")))
    manipulatedFile = open(filename, "rb")
    data = manipulatedFile.read(16)
    fileType = GetFileType(data)
    if fileType == "jpg":
        JPG_original(filename)
    elif fileType == "png":
        PNG_original(filename)
    elif fileType == "mp42":
        MP42_original(filename)
    elif fileType == "mp4":
        MP4_original(filename)
    manipulatedFile.close()

def HiddenJPG(_filename):
    manipulatedFile = open(_filename, "rb")
    data = manipulatedFile.read()
    offset = data.index(bytes.fromhex("ffd9"))
    manipulatedFile.seek(offset+2)
    secretData = manipulatedFile.read()
    manipulatedFile.close()
    secretFile = open(os.getcwd()+"/extractedSecret.jpg", "wb")
    secretFile.write(secretData)
    secretFile.close()

def HiddenPNG(_filename):
    manipulatedFile = open(_filename, "rb")
    data = manipulatedFile.read()
    offset = data.index(bytes.fromhex("49454e44ae426082"))
    manipulatedFile.seek(offset+8)
    secretData = manipulatedFile.read()
    manipulatedFile.close()
    secretFile = open(os.getcwd()+"/extractedSecret.png", "wb")
    secretFile.write(secretData)
    secretFile.close()

def HiddenMP42(_filename):
    manipulatedFile = open(_filename, "rb")
    data = manipulatedFile.read()
    offset = data.index(b"ftypmp42")
    manipulatedFile.seek(offset-4)
    secretData = manipulatedFile.read()
    manipulatedFile.close()
    secretFile = open(os.getcwd()+"/extractedSecret.mp4", "wb")
    secretFile.write(secretData)
    secretFile.close()

def HiddenMP4(_filename):
    manipulatedFile = open(_filename, "rb")
    data = manipulatedFile.read()
    offset = data.index(b"ftypisom")
    manipulatedFile.seek(offset-4)
    secretData = manipulatedFile.read()
    manipulatedFile.close()
    secretFile = open(os.getcwd()+"/extractedSecret.mp4", "wb")
    secretFile.write(secretData)
    secretFile.close()

def JPG_original(_filename):
    manipulatedFile = open(_filename, "rb")
    data = manipulatedFile.read()
    offset = data.index(bytes.fromhex("ffd9"))
    manipulatedFile.seek(offset+2)
    newData = manipulatedFile.read()
    if "ffd8ffe0" in newData.hex():
        HiddenJPG(_filename)
    elif "89504e470d0a1a0a" in newData.hex():
        HiddenPNG(_filename)
    elif b"ftypmp42" in newData:
        HiddenMP42(_filename)
    elif b"ftypisom" in newData:
        HiddenMP4(_filename)

def PNG_original(_filename):
    manipulatedFile = open(_filename, "rb")
    data = manipulatedFile.read()
    offset = data.index(bytes.fromhex("ffd9"))
    manipulatedFile.seek(offset+2)
    newData = manipulatedFile.read()
    if "ffd8ffe0" in newData.hex():
        HiddenJPG(_filename)
    elif "89504e470d0a1a0a" in newData.hex():
        HiddenPNG(_filename)
    elif b"ftypmp42" in newData:
        HiddenMP42(_filename)
    elif b"ftypisom" in newData:
        HiddenMP4(_filename)

def MP42_original(_filename):
    manipulatedFile = open(_filename, "rb")
    data = manipulatedFile.read()
    offset = data.index(bytes.fromhex("ffd9"))
    manipulatedFile.seek(offset+2)
    newData = manipulatedFile.read()
    if "ffd8ffe0" in newData.hex():
        HiddenJPG(_filename)
    elif "89504e470d0a1a0a" in newData.hex():
        HiddenPNG(_filename)
    elif b"ftypmp42" in newData:
        HiddenMP42(_filename)
    elif b"ftypisom" in newData:
        HiddenMP4(_filename)

def MP4_original(_filename):
    manipulatedFile = open(_filename, "rb")
    data = manipulatedFile.read()
    offset = data.index(bytes.fromhex("ffd9"))
    manipulatedFile.seek(offset+2)
    newData = manipulatedFile.read()
    if "ffd8ffe0" in newData.hex():
        HiddenJPG(_filename)
    elif "89504e470d0a1a0a" in newData.hex():
        HiddenPNG(_filename)
    elif b"ftypmp42" in newData:
        HiddenMP42(_filename)
    elif b"ftypisom" in newData:
        HiddenMP4(_filename)

def GetFileType(data):
    if "ffd8ffe0" in data.hex(): return "jpg"
    if "8950" in data.hex(): return "png"
    if b"ftypmp42" in data.hex(): return "mp42"
    if b"ftypisom" in data.hex(): return "mp4"
