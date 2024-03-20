import tkinter as tk
from tkinter import scrolledtext
import functions

class GUI:
    def __init__(self, master):
        self.master = master
        self.window_setup()
        self.files = None
    
    def window_setup(self):
        self.master.title("Product Image Preparer")
        self.directory_selection()
        self.function_pane()
        self.status_pane()
        self.make_changes_pane()


    #Part 0
    # row 0, column 0 
    def directory_selection(self):
        self.directory_selection_container = tk.Frame(self.master)
        self.directory_selection_container.grid(row=0, column=0)

        self.select_image_directory = tk.Button(self.master, text="Select Image Folder", command=self.get_files)
        self.select_image_directory.grid(row=0, column=0)
        
    #Part 2
    # row 1 column 1
    def status_pane(self):
        self.status_container = tk.Frame(self.master)
        self.status_container.grid(row=1, column=1)
        self.status_text= scrolledtext.ScrolledText(self.status_container,width=40, height=10)
        self.status_text.grid(row=0, column=0)

        return

    # row 1, column 0
    def function_pane(self):
        self.function_container = tk.Frame(self.master)  # Create a frame to contain the functions
        self.function_container.grid(row=1, column=0) 

        self.compress_images_pane()
        self.image_border_pane()
        self.watermark_image_pane()
        return

    def compress_images_pane(self):
        self.compress_images_container = tk.Frame(self.function_container)
        self.compress_images_label = tk.Label(self.compress_images_container, text="Image Compression")
        self.scale = tk.Scale(self.compress_images_container, from_=0, to=100, orient=tk.HORIZONTAL, command=self.compress_files)
        self.compress_images_label.grid(row=0, column=0)
        self.scale.grid(row=1, column=0)

        self.compress_images_container.grid(row=0, column=0)

    def image_border_pane(self):
        # Define a list of options
        
        self.image_border_container = tk.Frame(self.function_container)
        self.image_border_label= tk.Label(self.image_border_container, text="Image Border")
        options = ["red","blue","green","yellow","white","black","cyan","magenta","brown","orange","pink","violet","navy","teal","olive","maroon","gray"]
        
        # Create a StringVar to store the selected option
        self.selected_option = tk.StringVar()
        self.selected_option.set(options[0])  # Set the default selected option
        
        # Create the dropdown menu
        self.dropdown_menu = tk.OptionMenu(self.image_border_container, self.border_files, *options)
        self.dropdown_menu.grid(row=0, column=0)

        # Bind a function to handle menu selection
        #self.selected_option.trace("w", self.select_color)
        self.image_border_label.grid(row=1, column=0)

        self.image_border_container.grid(row=1, column=0)
    def watermark_image_pane(self):
        self.watermark_image_container= tk.Frame(self.function_container)
        self.watermark_image_pane= tk.Label(self.watermark_image_container, text="Watermark Image")
        self.watermark_image_pane.grid(row=2, column=1)
    
        self.watermark_image_container.grid(row=2, column=0)
    
    #Part 3
    # row 2 column 0
    def make_changes_pane(self):
        self.changes_pane_container = tk.Frame(self.master)
        self.changes_pane_container.grid(row=2, column=1)
        self.make_changes_button = tk.Button(self.changes_pane_container, text="Apply Image Changes", command=self.apply_changes)
        self.make_changes_button.grid(row=0, column=0)
        
        return

    def apply_changes(self):
        self.compress_files(self.files)
        self.status_text.insert(tk.END, "\nCompression Complete")
        self.border_files()
        self.status_text.insert(tk.END, "\nBorders Complete")
        #self.watermark_path = functions.get_watermark()
        #self.watermark_files(self.watermark_path)
        #self.status_text.insert(tk.END, "\nWatermark Complete")


    def get_files(self):
        self.files =  functions.get_files()
        self.status_text.insert(tk.END, "\n".join(self.files))

    def compress_files(self, value):
        functions.compress_files(self.files, value)
    
    def border_files(self, *args):
        functions.add_border(self.files, self.selected_option.get())

    def watermark_files(self, watermark_path):
        functions.add_watermark(self.files, watermark_path)


def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()