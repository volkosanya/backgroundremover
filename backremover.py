from PIL import Image
from rembg import remove
import os
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def remove_background(input_path):
    try:
        # Open the input image
        input_image = Image.open(input_path) 

        # Remove the background
        output_image = remove(input_image) 

        # Construct the output file path
        output_path = os.path.splitext(input_path)[0] + '_no_bg.png' #create new filename for the output image
        
        # Save the output image
        output_image.save(output_path)

        print(f"Saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error: {e}")
        return None
    

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title('Background Removal Tool')
        self.geometry('400x200')
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop)
        
        self.label = tk.Label(self, text="Drag and drop an image file here", padx=10, pady=10)
        self.label.pack(expand=True, fill=tk.BOTH)

        self.file_path_label = tk.Label(self, text="", padx=10, pady=10)
        self.file_path_label.pack(expand=True, fill=tk.BOTH)

        self.status_label = tk.Label(self, text="", padx=10, pady=10)
        self.status_label.pack(expand=True, fill=tk.BOTH)

    def drop(self, event):
        # Reset the counters at the start of a new drop event
        self.total_files = 0
        self.processed_files = 0

        file_paths = self.parse_drop_files(event.data)
        self.total_files = len(file_paths)

        self.update_status()

        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.file_path_label.config(text=f"File: {file_path}")
                self.status_label.config(text=f"[{self.processed_files}/{self.total_files}] Processing...")
                self.update()
                self.process_file(file_path)
            else:
                self.file_path_label.config(text="")
                self.status_label.config(text="Invalid file. Please drop a valid image file.")
                self.update()

        self.update_status(final=True)
    
    def parse_drop_files(self, data):
        # Remove curly braces and split by space
        files = data.strip("{}").split()
        return files

    def process_file(self, file_path):
        result = remove_background(file_path)
        self.processed_files += 1
        if result:
            self.file_path_label.config(text=f"Saved: {result}")
        else:
            self.file_path_label.config(text="Error processing the file")
        self.update_status()

    def update_status(self, final=False):
        if final:
            self.status_label.config(text=f"Done! [{self.processed_files}/{self.total_files}]", fg="green")
        else:
            self.status_label.config(text=f"[{self.processed_files}/{self.total_files}] Processing...")

if __name__ == "__main__":
    app = App()
    app.mainloop()
