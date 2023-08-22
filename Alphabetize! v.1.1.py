import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class AlphabetizeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alphabetize! v1.1")
        self.destination_folder = tk.StringVar()

        ttk.Label(root, text="Target Folder:").pack(pady=10)
        self.target_frame = ttk.Frame(root)
        self.target_frame.pack(pady=5)
        
        target_entry = ttk.Entry(self.target_frame, textvariable=self.destination_folder)
        target_entry.pack(side=tk.LEFT)
        
        ttk.Button(self.target_frame, text="Select Folder", command=self.select_folder).pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Alphabetize!", command=self.alphabetize_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Undo", command=self.undo_files).pack(side=tk.LEFT, padx=5)
        
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)
        
        # Home Tab
        home_tab = ttk.Frame(notebook)
        notebook.add(home_tab, text='Home')
        
        help_text = tk.Text(home_tab, wrap=tk.WORD, padx=10, pady=10)
        help_text.insert(tk.END, "Welcome to Alphabetize! v1.1\n\n", "center bold")
        help_text.insert(tk.END, "TO USE:\n", "center")
        help_text.insert(tk.END, "Choose a target folder with the 'Select Folder' button and press 'Alphabetize!'\n\nThe Alphabetize! function will move the target folder's contents into Alphabetized! sub-folders with a '#' folder for contents starting with numbers.\n\n", "center")
        help_text.insert(tk.END, "NOTES:\n", "center")
        help_text.insert(tk.END, "1. Folders within the target folder will be moved without altering their contents.\n\n2. The 'Undo' function will only delete empty sub-folders named '#' or 'A'-'Z' upon completion.")
        help_text.tag_configure("center", justify="center")
        help_text.tag_configure("bold", font=("Helvetica", 12, "bold"))
        help_text.config(state=tk.DISABLED)
        help_text.pack(fill='both', expand=True)
    
    def select_folder(self):
        self.destination_folder.set(filedialog.askdirectory())
    
    def alphabetize_files(self):
        dest_folder = self.destination_folder.get()
        if not dest_folder:
            messagebox.showerror("Error", "Please select a target directory.")
            return
        
        for filename in os.listdir(dest_folder):
            if filename != os.path.basename(__file__):
                first_char = filename[0]
                if first_char.isdigit():
                    subfolder_path = os.path.join(dest_folder, "#")
                else:
                    first_char = first_char.upper()
                    if first_char.isalpha() and 'A' <= first_char <= 'Z':
                        subfolder_path = os.path.join(dest_folder, first_char)
                    else:
                        continue

                os.makedirs(subfolder_path, exist_ok=True)
                item_path = os.path.join(dest_folder, filename)
                if os.path.isdir(item_path):
                    shutil.move(item_path, subfolder_path)
                else:
                    shutil.move(item_path, os.path.join(subfolder_path, filename))
        
        messagebox.showinfo("Operation Complete", "The target folder's contents have been Alphabetized!")

    def undo_files(self):
        dest_folder = self.destination_folder.get()
        if not dest_folder:
            messagebox.showerror("Error", "Please select a target folder.")
            return
        
        for root, dirs, files in os.walk(dest_folder, topdown=False):
            for dir_name in dirs[:]:
                if dir_name == "#" or (len(dir_name) == 1 and dir_name.isalpha()):
                    dir_path = os.path.join(root, dir_name)
                    for filename in os.listdir(dir_path):
                        shutil.move(os.path.join(dir_path, filename), os.path.join(dest_folder, filename))
                    os.rmdir(dir_path)
                
                    dirs.remove(dir_name)
        
            for filename in files:
                shutil.move(os.path.join(root, filename), os.path.join(dest_folder, filename))
        
        messagebox.showinfo("Operation Complete", "Alphabetize! undone. Empty sub-folders have been deleted.")

def main():
    root = tk.Tk()
    app = AlphabetizeApp(root)
    root.geometry("500x430")
    root.mainloop()

if __name__ == "__main__":
    main()
