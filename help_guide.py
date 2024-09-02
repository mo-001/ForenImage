import tkinter as tk

class ForenImageHelpGuide(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window settings
        self.title("ForenImage Help Guide")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Function descriptions
        self.function_descriptions = [
            ("Steganography Detection", "Analyzes images for hidden data or messages using algorithms to detect concealed steganographic content embedded within the image."),
            ("Hash Digest", "Computes a unique hash value to verify image integrity and detect any unauthorized modifications or tampering."),
            ("Metadata Extraction", "Extracts metadata such as camera settings, date, and GPS coordinates embedded within the image for detailed analysis."),
            ("Locational Information", "Retrieves GPS coordinates from an image's metadata to identify the geographic location where the image was captured."),
            ("Error Level Analysis", "Analyzes compression errors in JPEG images to detect areas of manipulation or inconsistencies in the image data."),
            ("Edge Detection", "Identifies and highlights the boundaries of objects within an image to analyze shapes and detect tampering."),
            ("Copy-Move Detection", "Detects duplicated regions within an image, which can indicate image forgery or manipulation through cloning."),
            ("Hex Viewer", "Displays the hexadecimal representation of image data, allowing for a detailed examination of its binary structure."),
            ("String Extraction", "Extracts text strings hidden within image files, revealing any embedded messages or suspicious content."),
            ("Image Manipulation", "Provides tools to enhance images via blurring, sharpening, or computing luminance gradient.")
        ]

        
        # Current page tracker
        self.current_page = 0
        
        # Setup UI components
        self.create_widgets()
        self.update_page()
    
    def create_widgets(self):
        # Title label for the function name
        self.title_label = tk.Label(self, text="", font=("Helvetica", 16, "bold"), wraplength=380)
        self.title_label.pack(pady=10)
        
        # Description label for the function details
        self.description_label = tk.Label(self, text="", wraplength=380, justify="left")
        self.description_label.pack(pady=10)
        
        # Navigation buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side="bottom", pady=20)
        
        self.left_button = tk.Button(button_frame, text="←", command=self.go_left, state="disabled", width=10)
        self.left_button.pack(side="left", padx=20)
        
        self.right_button = tk.Button(button_frame, text="→", command=self.go_right, width=10)
        self.right_button.pack(side="right", padx=20)
    
    def update_page(self):
        # Update the title and description based on the current page
        title, description = self.function_descriptions[self.current_page]
        self.title_label.config(text=title)
        self.description_label.config(text=description)
        
        # Enable/disable buttons based on the page
        self.left_button.config(state="normal" if self.current_page > 0 else "disabled")
        self.right_button.config(state="normal" if self.current_page < len(self.function_descriptions) - 1 else "disabled")
    
    def go_left(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()
    
    def go_right(self):
        if self.current_page < len(self.function_descriptions) - 1:
            self.current_page += 1
            self.update_page()
    def run():
        app = ForenImageHelpGuide()
        app.mainloop()

# Create an instance of the help guide and run the main loop
if __name__ == "__main__":
    app = ForenImageHelpGuide()
    app.mainloop()
