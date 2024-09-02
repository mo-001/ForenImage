from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import filedialog as tkFileDialog
from tkinter import simpledialog as tkSimpleDialog
import tkintermapview
from PIL import ImageTk, Image, ImageChops, ImageEnhance, ImageFilter
from exiftool import ExifToolHelper
import re
import binascii
import numpy
import hashlib
import sys 
import os

class Viewer(Frame):
    def __init__(self, master, image=None):
        super().__init__(height=100, width=100)
        self.master = master
        self.image = image
        self.filepath = None
    
    def run(self, filepath):
        print(self.filepath)
        if self.filepath != filepath and self.filepath != None:
            self.lblImage.destroy()
            self.views.destroy()
        self.filepath = filepath
        self.image = Image.open(filepath).resize((300,300), Image.Resampling.NEAREST)
        self.original = self.image
        self.genViews()
        self.currentView = StringVar(self)
        self.currentView.set('Original')
        options = list(self.filters.keys())
        options.sort()
        self.views = OptionMenu(self, self.currentView,
                *options, command=self.applyFilter)
        self.views.pack()

        self.tkImage = ImageTk.PhotoImage(self.image)
        self.lblImage = Label(master=self, image=self.tkImage)
        self.lblImage.bind('<Button-1>', self.displayInfos)
        self.lblImage.bind('<Button-3>', self.save)
        self.lblImage.image = self.tkImage
        self.lblImage.pack()

        self.status = StringVar()
        self.lblStatus = Label(textvariable=self.status, justify='right')
        self.lblStatus.pack()
    def displayInfos(self, event):
        """
        Displays the coordinates in the status bar
        """
        x = int((event.x-0.1)/args.scalefactor)
        y = int((event.y-0.1)/args.scalefactor)
        pixel = orig.getpixel((x, y))
        self.setStatus("Coordinates : (%s:%s) - Pixel value : %s" %
                (x, y, str(pixel)))

    def setStatus(self, text):
        """
        Changes the text in the status bar
        """
        self.status.set(text)

    def save(self, event):
        """
        Saves the filtered image to a file
        """
        options = {'filetypes':[('PNG','.png'),('GIF','.gif')]}
        outfile = tkFileDialog.asksaveasfilename(**options)
        if outfile == '':
            return
        else:
            self.image.save(outfile)
            return

    def genViews(self):
        """
        Generates filters based on the source image
        """
        self.filters = {}
        for plug in viewPlugins:
            self.filters.update({plug.name:viewPlugins.index(plug)})

    def applyFilter(self, view):
        """
        Applies a filter to the image
        """
        view = self.filters[self.currentView.get()]
        plugin = viewPlugins[view]
        if plugin.parameters:
            for param in list(plugin.parameters.keys()):
                a = tkSimpleDialog.askinteger(
                        'Question', plugin.parameters[param])
                if a is not None:
                    setattr(viewPlugins[view], param, a)
        self.image = viewPlugins[view].process(self.original)

        self.showImage(self.currentView.get(), self.image)
        self.setStatus("")
        return

    def showImage(self, title, image):
        """
        Updates the image in the window
        """
        self.tkImage = ImageTk.PhotoImage(image)
        self.lblImage.configure(image=self.tkImage)
        self.lblImage.image = self.tkImage



viewPlugins = []
plugins = []
commandPlugins = []
def loadPlugins():
    sys.path.insert(0,'plugins/')
    plugs = []
    for filename in os.listdir('plugins/'):
        name, ext = os.path.splitext(filename)
        if ext.endswith(".py"):
            plugs.append(__import__(name))
    for plug in plugs:
        plugin = plug.register()
        plugin.mode = "visual"
        viewPlugins.append(plugin)
        plugins.append(plugin)
loadPlugins()