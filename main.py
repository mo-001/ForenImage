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
from PIL import ImageTk, Image, ImageChops, ImageEnhance, ImageFilter
from exiftool import ExifToolHelper

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

    
    
    
    
    
app = ForenImage()
app.mainloop()