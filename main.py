from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QListWidget, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox
import os
from PIL import Image, ImageEnhance

workdir = ''

class ImageProcessor():
    def __init__(self, pic, filename):
        self.filename = filename
        self.path = os.path.join(workdir, filename)
        self.pic = Image.open(self.path)
    def loadImage(self):
        self.pic = Image.open(self.path)
    def showImage(self):
        lb_pic.hide()
        pixmappic = QPixmap(self.path)
        w, h = lb_pic.width(), lb_pic.height()
        pixmappic = pixmappic.scaled(w, h, Qt.KeepAspectRatio)
        lb_pic.setPixmap(pixmappic)
        lb_pic.show()
    def do_l(self):
        self.pic = self.pic.transpose(Image.ROTATE_90)
        self.saveImage()
    def do_r(self):
        self.pic = self.pic.transpose(Image.ROTATE_270)
        self.saveImage()
    def do_mr(self):
        self.pic = self.pic.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
    def do_shs(self):
        self.pic = ImageEnhance.Sharpness(self.pic)
        self.saveImage()
    def do_bw(self):
        self.pic = self.pic.convert('L')
        self.saveImage()
    def saveImage(self):
        path = os.path.join(workdir, 'Modified')
        if not(os.path.exists(path)) or os.path.isdir(path):
            os.mkdir(path)
        self.path = os.path.join(path, self.filename)
        self.pic.save(self.filename)
        self.showImage()

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter():
    files = list()
    filenames = os.listdir(workdir)
    extensions = ['.gif', '.jpg', '.jpeg', '.bmp', '.png']
    for filename in filenames:
        for extension in extensions:
            if filename.endswith(extension) == True:
                files.append(filename)
    return files

def showFilenamesList():
    filelist.clear()
    chooseWorkdir()
    filenames = filter()
    for filename in filenames:
        filelist.addItem(filename)

def showChosenImage():
    filename = ''
    for i in filelist.selectedItems():
        filename = i.text()
    global image
    image = ImageProcessor(None, filename)
    image.loadImage()
    image.showImage()

def do_bw():
    image.do_bw()
def do_l():
    image.do_l()
def do_r():
    image.do_r()
def do_mr():
    image.do_mr()
def do_shs():
    image.do_shs()

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')

#objects
fileb = QPushButton('Папка')
filelist = QListWidget()
lb_pic = QLabel('КАРТИНКА')
left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
sharpness = QPushButton('Резкость')
grayscale = QPushButton('Ч/Б')

#layout
layout1 = QVBoxLayout()
layout2 = QVBoxLayout()
layout3 = QHBoxLayout()
layout4 = QHBoxLayout()

#compilation
layout1.addWidget(fileb)
layout1.addWidget(filelist)
layout4.addLayout(layout1)
layout3.addWidget(left)
layout3.addWidget(right)
layout3.addWidget(mirror)
layout3.addWidget(sharpness)
layout3.addWidget(grayscale)
layout2.addWidget(lb_pic)
layout2.addLayout(layout3)
layout4.addLayout(layout2)

fileb.clicked.connect(showFilenamesList)
left.clicked.connect(do_l)
right.clicked.connect(do_r)
mirror.clicked.connect(do_mr)
sharpness.clicked.connect(do_shs)
grayscale.clicked.connect(do_bw)
filelist.itemClicked.connect(showChosenImage)
main_win.setLayout(layout4)
main_win.show()
app.exec_()