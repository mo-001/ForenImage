#Masters Disserattion Project - u5580118
#Effectiveness of Picture Forensic Tools
#The following is a tool that will provide the following features:

#MODULES
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
from viewer import Viewer

class ForenImage(Tk):
    """
    This class is used for generating the image forensic tool, by inheriting the Tk/window object from Tkinter. This is done so that it is easier to build new objects 
    that integrate into the window, rather than having to make references back to the window.
    """
    def __init__(self):
        """
        Initial method to construct the rest of the class
        """
        super().__init__()
        self.filepath = StringVar()
        self.filepaths = StringVar()
        self.path_error = StringVar()
        self.location = StringVar()
        self.md5_text = StringVar()
        self.md5_text.set("MD5 Hash Digest: ")
        self.sha1_text = StringVar()
        self.sha1_text.set("SHA1 Hash Digest: ")
        self.image = None
        self.init_root()
    
    def run():
        self.title = "ForenImage"
        self.mainloop()
    
    def init_root(self):
        """
        Initializes the top level window and subsequent tabs
        """
        self.init_main()
        self.init_tabs()
    def init_main(self):
        """
        Initializes the main elements within the window
        """
        self.image_label = Canvas(self, width=300, height=300)
        self.image_label.pack()
        self.left_frame = Frame()
        self.left_frame.pack()
        #upload label initialization
        upload_label = Label(self, textvariable=self.filepath)
        upload_label.pack()
        upload_batch_label = Label(self, textvariable=self.filepaths)
        upload_label.pack()
        #error label init
        error_label = Label(self, textvariable=self.path_error)
        #batch upload 
        batch_upload_button = Button(text="Batch Upload", command=self.action_batch_upload_button)
        batch_upload_button.pack()
        upload_button = Button(text="Browse", command=self.action_upload_button)
        upload_button.pack()
        error_label.pack()


    
    def init_tabs(self):
        """
        Initializes the tabs for the image analysis

        """
        tabsControl = Notebook(self, width=500, height=300)
        tabsControl.add(self.init_metadata_tab(), text="Metadata")
        tabsControl.add(self.init_ela_tab(), text="Analysis")
        tabsControl.add(self.init_edges_tab(), text="Edges Detection")
        tabsControl.add(self.init_strings_tab(), text="String Data")
        tabsControl.add(self.init_hex_tab(), text="Hex Data")
        tabsControl.add(self.init_location_tab(tabsControl), text="Location")
        tabsControl.add(self.init_digest_tab(), text="Digest")
        tabsControl.add(self.init_steg_tab(), text="Steganography")
        tabsControl.pack()
        return tabsControl
    
    def init_metadata_tab(self):
        """ 
        Initializes the metadata tab
        """
        metadata_tab = ttk.Frame()
        self.metadata_listbox = Listbox(metadata_tab, height=300, width=300)
        self.metadata_listbox.pack()
        return metadata_tab
    
    def init_ela_tab(self):
            """ 
            Initializes the ELA tab
            """
            ela_tab = ttk.Frame()
            self.ela_label = Canvas(ela_tab, width=300, height=300)
            self.ela_label.pack()
            return ela_tab
    def init_edges_tab(self):
        """ 
        Initializes the edge detection tab
        """
        edges_tab= ttk.Frame()
        self.edge_label = Canvas(edges_tab, width=300, height=300)
        self.edge_label.pack()
        return edges_tab
    def init_strings_tab(self):
        """ 
        Initializes the string extraction tab
        """
        string_tab = ttk.Frame()
        string_tab.pack()
        string_frame = Frame(string_tab)
        string_frame.pack()
        self.string_label = Text(string_tab, width=150)
        self.string_label.pack()
        save_strings = Button(string_frame, text="Save", command=self.action_save_strings)
        save_strings.pack()
        return string_tab
    
    def init_hex_tab(self):
        """ 
        Initializes the hex viewer tab
        """
        hex_tab = ttk.Frame()
        hex_frame = Frame(hex_tab, width=100, height=100)
        hex_frame.pack()
        self.hex_label = Text(hex_tab,  width=100, height=100)
        self.hex_label.pack()
        save_hex = Button(hex_frame,text="Save", command=self.action_save_hex)
        save_hex.pack()
        return hex_tab
    def init_location_tab(self, tabsControl):
        """ 
        Initializes the location tab
        """
        self.location_tab = tkintermapview.TkinterMapView(tabsControl)
        return self.location_tab
    
    def init_digest_tab(self):
        """ 
        Initializes the digest tab
        """
        digest_tab = ttk.Frame()
        self.md5_text = StringVar()
        self.sha1_text = StringVar()
        md5_label = Label(digest_tab, textvariable=self.md5_text)
        sha1_label = Label(digest_tab, textvariable=self.sha1_text)
        md5_label.pack()
        sha1_label.pack()
        return digest_tab
    def init_steg_tab(self):
        """ 
        Initializes the steganography tab
        """
        self.viewer = Viewer(self)
        self.steg_tab = self.viewer
        return self.steg_tab

    def process_metadata(self,listbox):
        """ 
        Processes metadata 
        :listbox - listbox reference to input data into
        """
        listbox.delete(0, END)
        with ExifToolHelper() as et:
            for d in et.get_metadata(self.filepath.get()):
                for i in range(len(list(d.items()))):
                    listbox.insert(i, list(d.items())[i])
            location_data = et.get_tags(self.filepath.get(), ["EXIF:GPSLatitude","EXIF:GPSLongitude"])
            self.location.set(str(location_data[0].get("EXIF:GPSLatitude")) + "," + str(location_data[0].get("EXIF:GPSLongitude")))
   
    def process_ela(self,filepath):
        """ 
        Processes image to produce ELA image
        :filepath - filepath to open
        """
        image = Image.open(filepath)
        temp_path = "temp_ela.jpg"
        image.save(temp_path, "JPEG", quality=quality)
        compressed_image = Image.open(temp_path)

        ela_image = ImageChops.difference(image, compressed_image)
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0/max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        return ela_image
    
    def calculate_ela(self,  quality=90):
        """ 
            Calculates ELA of image
        """
        image = Image.open(self.filepath.get())
        temp_path = "temp_ela.jpg"
        image.save(temp_path, "JPEG", quality=quality)
        compressed_image = Image.open(temp_path)

        ela_image = ImageChops.difference(image, compressed_image)
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0/max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        return ela_image
    def detect_edges(self):
        """
            Detects edges 
            Returns:
            :edge_image - edge image 
        """
        image = Image.open(self.filepath.get())
        edge_image = image.filter(ImageFilter.FIND_EDGES)
        return edge_image
    def process_strings(self,filepath):
        """ 
            Processes image to extract strings 
            :filepath - filepath to open
        """
        self.string_label.delete('1.0', END)
        strings_str = ""
        if self.filepath:
            with open(self.filepath.get(), 'rb') as image:
                data = image.read()
                strings = re.findall(b'[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};\'"\\|,.<>\/? ]{4,}', data)
                strings = [s.decode('utf-8', 'ignore') for s in strings]
                strings_str = "\n".join(strings)
        self.string_label.insert(END, strings_str)
        return strings_str
    
    def process_hex(self,filepath):
        """ 
        Processes image to produce hexadecimal conversion
        :filepath - filepath to open
        """
        hex_data = ""
        if self.filepath.get():
            with open(self.filepath.get(), 'rb') as image:
                data = image.read(1024)  # Read the first 1024 bytes for demonstration
                hex_data = binascii.hexlify(data).decode('utf-8')
                hex_str = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))
        self.hex_label.insert(END, hex_str)
        return hex_data
    def locate_coords(self):
        """
            Locates and returns the GPS coordinates via EXIFTool
            If not, returns a default location
        """
        with ExifToolHelper() as et:
            location_data = et.get_tags(self.filepath.get(), ["EXIF:GPSLatitude","EXIF:GPSLongitude"])
            location = str(location_data[0].get("EXIF:GPSLatitude")) + "," + str(location_data[0].get("EXIF:GPSLongitude"))
            try:
                lat, long = location.split(",")[0], location.split(",")[1]
                return float(long), float(lat)
            except:
                return 1.0,1.0

    def create_map(self, lat, long):
        """
            Creates the map widget given co-ordinates
        """
        self.location_tab.set_position(float(long), float(lat))
    
    def hash_file(self, filepath):
        """ 
        Processes image to produce a hash with MD5 and SHA1
        :filepath - filepath to open
        """
        BUFF_SIZE = 65536
        with open(filepath, 'rb') as file:
            md5 = hashlib.md5(file.read())
            sha1 = hashlib.sha1(file.read())
            return md5, sha1
    
    def detect_steganography(self):
        """ 
        Processes image to detect steganography
        :filepath - filepath to open
        """
        orig = Image.open(self.filepath.get())
        thumb = orig.copy()
        print(self.viewer.image)
        if not self.viewer.image:
            self.steg_tab.run(self.filepath.get())
            print(self.viewer.image)
        else:
            self.viewer.pack_forget()
            self.steg_tab.run(self.filepath.get())
   

    def action_upload_button(self): 
        """ 
        Parses a single file to be used within the forensics tool
        :filepath - filepath to open
        """
        filename = filedialog.askopenfile()
        if self.validate_image(filename.name):
            self.path_error.set("")
            self.filepath.set(filename.name)
            self.show_image(Image.open(filename.name), self.image_label)
            self.process_metadata(self.metadata_listbox)
            if self.is_jpg(filename.name):
                self.show_image(self.calculate_ela(), self.ela_label)
                self.show_image(self.detect_edges(), self.edge_label)
            self.process_strings(self.filepath.get())
            self.process_hex(self.filepath.get())
            
            lat, long = self.locate_coords()
            self.create_map(lat, long)

            md5_value, sha1_value = self.hash_file(filename.name)
            self.md5_text.set("MD5 Hash: {0}".format(md5_value.hexdigest()))
            self.sha1_text.set("SHA1 Hash: {0}".format(sha1_value.hexdigest()))

            self.detect_steganography()
            


        else:
            self.path_error.set("Please input a png, bmp, or jpg file")
   
    def show_image(self, imagefile, label):
        """
            Shows an image
        """
        self.image = ImageTk.PhotoImage(imagefile.resize((300,300), Image.Resampling.NEAREST))
        label.create_image(0,0, image=self.image, anchor=NW, tags="IMG")
        label.image = self.image
    
    def action_batch_upload_button(self):
        """ 
        Parses multiple files to be used within the forensics tool
        """
        files = filedialog.askopenfilenames(title="Choose a file")
        if self.validate_files(files) == False:
            self.path_error.set("Some files are not of either .jpg, .png, or .bmp. Please upload one of the prior formats.")
        else:
            for i in range(len(files)):
                self.files_box.insert(i, files[i])
            self.left_frame.pack(side="left")
            self.files_box.bind("<<ListboxSelect>>", self.on_filesbox_select)
            self.files_box.pack(side=LEFT)
      
    def action_save_hex(self, filepath):
        """ 
            Saves altered hex data
            :filepath - filepath to open
        """
        file_clean = self.filepath.get().split(".")
        with open(file_clean, 'w') as file:
            content = self.hex_label.get("1.0", END)
            file.write(content)

    
    def action_save_strings(self, filepath):
        """ 
        Saves altered string data of image
        :filepath - filepath to open
        """
        with open(self.filepath.get(), 'w') as file:
            content = self.string_label.get("1.0", END)
            file.write(content)

    
    def on_filesbox_select(self,event):
        """
            Runs processing when a filepath in the listbox is selected
            Args:
            :event - on selecting the listbox
        """
        selection = event.widget.curselection()
        if selection:
            name = event.widget.get(selection[0])
            self.filepath.set(name)
            self.show_image(Image.open(name), self.image_label)
            self.process_metadata(self.metadata_listbox)
            
    def validate_image(self, name):
        """
            Validates a file to ensure it is of the 3 image formats covered in this tool
        """
        new_name = name.split("/")[-1].lower().split('.')[1]
        if((new_name != "jpg") and (new_name != "png") and (new_name != "bmp")):
            return False
        return True
    def is_jpg(self, filename):
        extension = filename.split("/")[-1].lower().split('.')[1]
        if(extension != "jpg"):
            return False
        return True

    
    
    
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
app = ForenImage()
app.mainloop()