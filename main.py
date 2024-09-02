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
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledFrame
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
from help_guide import ForenImageHelpGuide
from tktooltip import ToolTip
import cv2

#APP
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
        self.menu = self.init_menu()
        self.init_main()
        self.init_style()
        self.init_tabs()
        self.config(menu=self.menu)
    
    def init_style(self):
        """
        Initializes the accessibility styles for buttons
        """
        self.style = Style(theme='darkly')
        self = self.style.master
        
    

    def init_main(self):
        """
        Initializes the main elements within the window
        """
        self.image_label = Canvas(self, width=300, height=300)
        self.image_label.pack()
        self.left_frame = ttk.Frame()
        self.left_frame.pack()
        self.files_box = self.init_files_box(self.left_frame)
        #upload label initialization
        upload_label = Label(self, textvariable=self.filepath)
        upload_label.pack()
        upload_batch_label = Label(self, textvariable=self.filepaths)
        upload_label.pack()
        #error label init
        error_label = Label(self, textvariable=self.path_error)
        #generate copy move
        self.init_copy_move()
        #batch upload 
        batch_upload_button = Button(style="Access.TButton",text="Batch Upload", command=self.action_batch_upload_button)
        batch_upload_button.pack()
        #tooltip for batch upload
        ToolTip(batch_upload_button, msg="You can upload multiple files of .bmp, .png and .jpg format here.")
        upload_button = ttk.Button(style="Access.TButton",text="Browse", command=self.action_upload_button)
        upload_button.pack()
        error_label.pack()
        #tool tip for single upload
        ToolTip(upload_button, msg="You can upload a single file of .bmp, .png and .jpg format here.")

    def init_menu(self):
        """
        Initializes the menu
        """
        menu_bar = Menu(self)
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        return menu_bar
    
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
        tabsControl.add(self.init_image_tab(), text="Image Manipulation")
        tabsControl.pack()
        return tabsControl
    def init_files_box(self, frame):
        """ 
        Initializes the files listbox
        """
        files_box = Listbox(frame, width=50, height=50)
        return files_box
    
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
    
    def init_copy_move(self):
        """ 
        Initializes the copymove label
        """
        self.copy_move_text = StringVar()
        copy_move_label = Label(self, textvariable=self.copy_move_text)
        copy_move_label.pack()
    
    def init_image_tab(self):
        """
          Initializes image tab
        """
        image_frame = ScrolledFrame()
        self.luminence_label = Label(image_frame, text="Luminence Gradient: ")
        self.luminence_label.pack()
        self.equalizer_label = Label(image_frame)
        self.equalizer_label.pack()
        self.sharpen_image_label = Label(image_frame)
        self.sharpen_image_label.pack()
        self.blur_image_label = Label(image_frame)
        self.blur_image_label.pack()
        return image_frame.container

    

    def process_metadata(self,listbox):
        """ 
        Processes metadata 
        :listbox - listbox reference to input data into
        """
        #wipe listbox so we don't get extra data
        listbox.delete(0, END)
        with ExifToolHelper() as et:
            #get metadata
            for d in et.get_metadata(self.filepath.get()):
                for i in range(len(list(d.items()))):
                    #insert metadata
                    listbox.insert(i, list(d.items())[i])
   
    
    def calculate_ela(self,  quality=90):
        """ 
            Calculates ELA of image
        """
        #get image
        image = Image.open(self.filepath.get())
        #temp save so that it doesn't affect original and compress
        temp_path = "temp_ela.jpg"
        image.save(temp_path, "JPEG", quality=quality)
        compressed_image = Image.open(temp_path)
        #get difference
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
        #use filter to create edges
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
            #read hex data
            with open(self.filepath.get(), 'rb') as image:
                data = image.read(1024)  # Read the first 1024 bytes for demonstration
                hex_data = binascii.hexlify(data).decode('utf-8')
                hex_str = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))
        #put into widget
        self.hex_label.insert(END, hex_str)
        return hex_data
    def locate_coords(self):
        """
            Locates and returns the GPS coordinates via EXIFTool
            If not, returns a default location
        """
        #use exiftool to extract
        with ExifToolHelper() as et:
            #get location via exif
            location_data = et.get_tags(self.filepath.get(), ["EXIF:GPSLatitude","EXIF:GPSLongitude"])
            location = str(location_data[0].get("EXIF:GPSLatitude")) + "," + str(location_data[0].get("EXIF:GPSLongitude"))
            #try to split - ensures that no faliure state
            try:
                lat, long = location.split(",")[0], location.split(",")[1]
                return float(long), float(lat)
            #otherwise return a default location
            except:
                return 1.0,1.0

    def create_map(self, lat, long):
        """
            Creates the map widget given co-ordinates
        """
        #create the map at the location tab
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
        #check for if image already exists
        if not self.viewer.image:
            self.steg_tab.run(self.filepath.get())
            print(self.viewer.image)
        #else destroy current view
        else:
            self.viewer.pack_forget()
            self.steg_tab.run(self.filepath.get())
    
    def process_copymove(self, filepath):
        """ 
        Processes image to detect copy move
        :filepath - filepath to open
        """
        #open image
        image = Image.open(filepath).convert('L')
        image_data = numpy.array(image)
        shift = False
        #calculate shift in similarity
        for y_shift in range(1,30):
            for x_shift in range(1, 30):
                shift_data = numpy.roll(image_data, (y_shift, x_shift), axis=(0,1))
                similarity = numpy.mean(image_data == shift_data)
                if similarity > 0.95:
                    shift = True
                    break
        if shift:
            self.copy_move_text.set("Copy Move Detected")
        else:
            self.copy_move_text.set("Copy Move Not Detected")

    def process_image_manip(self):
        """
            Processes image manipulation
        """
        self.luminence_label.config(text=self.compute_luminance(self.filepath.get()))
        equimage = ImageTk.PhotoImage(Image.fromarray(self.equalize_image(self.filepath.get())).resize((300,300), Image.Resampling.NEAREST))
        self.equalizer_label.config(image=equimage)
        self.equalizer_label.image = equimage
        sharpimage = ImageTk.PhotoImage(Image.fromarray(self.sharpen_image(self.filepath.get())).resize((300,300), Image.Resampling.NEAREST))
        self.sharpen_image_label.config(image=sharpimage)
        self.sharpen_image_label.image = sharpimage
        blurimage = ImageTk.PhotoImage(Image.fromarray(self.blur_image(self.filepath.get())).resize((300,300), Image.Resampling.NEAREST))
        self.blur_image_label.config(image=blurimage)
        self.blur_image_label.image = blurimage 
    def blur_image(self, image_path, kernel_size=5):
        """
        Applies Gaussian blur to an image to reduce noise.

        Args:
        - image_path: str, path to the input image file
        - kernel_size: int, size of the Gaussian kernel

        Returns:
        - blurred_image: 2D numpy array representing the blurred image
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to load.")
        # Apply Gaussian blur
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred_image
    
    def sharpen_image(self, image_path):
        """
        Sharpens an image to enhance its details.

        :filename: str, path to the input image file

        -sharpened_image: 2D numpy array representing the sharpened image
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to load.")
        
        # Define sharpening kernel
        kernel = numpy.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])
        
        # Apply the kernel to the image
        sharpened_image = cv2.filter2D(image, -1, kernel)
        
        return sharpened_image
        
    def compute_luminance(self, image_path):
        """
        Computes the luminance gradient of an image using Sobel filters.

        :image_path: str, path to the input image file

        -gradient_magnitude: 2D numpy array representing the gradient magnitude
        """
        # Load image in grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError("Image not found or unable to load.")
        # Compute Sobel gradients
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        # Compute gradient magnitude
        gradient_magnitude = numpy.sqrt(sobel_x**2 + sobel_y**2)
        # Normalize gradient magnitude for better visualization
        gradient_magnitude = (gradient_magnitude / gradient_magnitude.max()) * 255
        return gradient_magnitude.astype(numpy.uint8)
        
    def equalize_image(self, image_path):
        """
        Applies histogram equalization to improve the contrast of a grayscale image.

        :image_path: str, path to the input image file

        
        -equalized_image: 2D numpy array representing the equalized image
        """
        # Load image in grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            raise ValueError("Image not found or unable to load.")
        
        # Apply histogram equalization
        equalized_image = cv2.equalizeHist(image)
        
        return equalized_image

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
            # self.process_copymove()
            self.process_image_manip()



        else:
            self.path_error.set("Please input a png, bmp, or jpg file")
   
    def show_image(self, imagefile, label):
        """
            Shows an image
        """
        self.image = ImageTk.PhotoImage(imagefile.resize((300,300), Image.Resampling.NEAREST))
        label.create_image(0,0, image=self.image, anchor=NW, tags="IMG")
        label.image = self.image
    def show_help(self):
        """
        Initializes the help window
        """
        app = ForenImageHelpGuide()
        app.mainloop()
    def action_batch_upload_button(self):
        """ 
        Parses multiple files to be used within the forensics tool
        """
        files = filedialog.askopenfilenames(title="Choose a file")
        if self.validate_files(files) == False:
            self.path_error.set("Some files are not of either .jpg, .png, or .bmp. Please upload one of the prior formats.")
        else:
            if(not len(files) == 0):
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
        with open("temp_{}".format(self.filepath.get()), 'w') as file:
            content = self.hex_label.get("1.0", END)
            file.write(content)

    
    def action_save_strings(self, filepath):
        """ 
        Saves altered string data of image
        :filepath - filepath to open
        """
        with open("temp_{}".format(self.filepath.get()), 'w') as file:
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
            self.process_strings(self.filepath.get())
            self.process_hex(self.filepath.get())
            if self.is_jpg(name):
                self.show_image(self.calculate_ela(), self.ela_label)
                self.show_image(self.detect_edges(), self.edge_label)
            # else:
                #lock tabs
            lat, long = self.locate_coords()
            self.create_map(lat, long)
            md5_value, sha1_value = self.hash_file(name)
            self.md5_text.set("MD5 Hash: {0}".format(md5_value.hexdigest()))
            self.sha1_text.set("SHA1 Hash: {0}".format(sha1_value.hexdigest()))
            self.detect_steganography()
            # self.process_copymove()
            self.process_image_manip()

    def validate_files(self, files):
        """
            Validates a list of files
        """
        for name in files:
            if self.validate_image(name) == False:
                return False
                break
        return True
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