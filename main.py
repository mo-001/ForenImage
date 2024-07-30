#Masters Disserattion Project - u5580118
#Effectiveness of Picture Forensic Tools
#The following is a tool that will provide the following features:

#MODULES
from tkinter import *
from tkinter.ttk import *

class ForenImage(Tk):
    """
    This class is used for generating the image forensic tool, by inheriting the Tk/window object from Tkinter. This is done so that it is easier to build new objects 
    that integrate into the window, rather than having to make references back to the window.
    """
    def __init__(self):
        """
        Initial method to construct the rest of the class
        """
        super().__init__(height=100, width=100)
        self.filepath = StringVar()
    
    def run():
        self.title = "ForenImage"
        self.mainloop()
    
    def init_root(self):
        """
        Initializes the top level window and subsequent tabs
        """
        self.init_main()
        self.init_tabs()
        self.config(menu=self.menu)
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


    
    def init_tabs(self):
        """
        Initializes the tabs for the image analysis

        """
        tabsControl = Notebook(self, width=500, height=300)
        tabsControl.add(self.init_steg_tab(), text="Steganography")
        tabsControl.add(self.init_metadata_tab(), text="Metadata")
        tabsControl.add(self.init_ela_tab(), text="Analysis")
        tabsControl.add(self.init_strings_tab(), text="String Data")
        tabsControl.add(self.init_hex_tab(), text="Hex Data")
        tabsControl.add(self.init_edges_tab(), text="Edges Detection")
        tabsControl.add(self.init_location_tab(tabsControl), text="Location")
        tabsControl.add(self.init_digest_tab(), text="Digest")
        tabsControl.pack()
        return tabsControl
    
app = ForenImage()
app.mainloop()