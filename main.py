import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
from tkinter import messagebox

# Class
class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")

        # Customization
        self.root.geometry("750x750")
        # Trying to insert an ico
        try:
            self.root.iconbitmap("folder.ico")
        except tk.TclError:
            print("We couldn't load the ico image, let's use the default one")
        
        """self.root.resizable(False, False) if u want it"""

        # Stacks for undo and redo operations
        self.undo_stack = []
        self.redo_stack = []
        # Menu
        menu_bar = tk.Menu(root)
        self.root.config(menu=menu_bar)
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=menu_file)

        # Addin' its commands
        menu_file.add_command(label="Open", command=self.open_file)
        menu_file.add_command(label="Save", command=self.save_file)
        menu_file.add_command(label="Delete", command=self.delete_file)
        menu_file.add_command(label="New", command=self.new_file)

        # Adding Undo and Redo to the menu bar
        menu_edit = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=menu_edit)

        # It's commands
        menu_edit.add_command(label="Undo", command=self.undo)
        menu_edit.add_command(label="Redo", command=self.redo)
        
        # Menu (Context one)
        menu_contx = tk.Menu(root, tearoff=0)
        menu_contx.add_command(label="Copy", command=self.copy)
        menu_contx.add_command(label="Cut", command=self.cut)
        menu_contx.add_command(label="Paste", command=self.paste)
        
        # Event
        def show_menu_contx(event):
            menu_contx.tk_popup(event.x_root, event.y_root)
        
        self.root.bind("<Button-3>", show_menu_contx)        

        # Graphical user interface
        self.text_area = ScrolledText(root, wrap='word', undo=False, padx=15, pady=10, font = ("Times New Roman", 14, "italic"))
        self.text_area.pack(expand=True, fill='both') # Only if resizable is desactivated

        # Event to detect changes in the text
        self.text_area.bind("<KeyRelease>", self.on_text_change)

        # Save the initial state of the text area
        self.save_state()
    
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
        
    def cut(self):
        self.text_area.event_generate("<<Cut>>")
        
    def paste(self):
        self.text_area.event_generate("<<Paste>>")   
        
    def delete_file(self):
        """
        Delete a selected file from the file system.
        """
        file_to_delete = askopenfilename()
        if file_to_delete:
            try:
                os.remove(file_to_delete)
                tk.messagebox.showinfo("Success", "File deleted successfully.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {e}")
        
    def new_file(self):
        """
        Clear the text area to create a new file.
        """
        self.text_area.delete("1.0", tk.END)
        file_opened = askopenfilename()
        if file_opened:
            self.text_area.delete(1.0, "end")
            with open(file_opened, 'r') as file:
                self.text_area.insert(1.0, "end")
    
    def open_file(self, *args):
        file_opened = askopenfilename()
        if file_opened:
            self.text_area.delete(1.0, "end")
            with open(file_opened, 'r') as file:
                self.text_area.insert(1.0, file.read())
    
    def save_file(self):
        file_selected = asksaveasfilename()
        if file_selected:
            self.text_area.delete(1.0, "end")
            with open(file_selected, 'r') as file:
                self.text_area.insert(1.0, file.read())
    
    def save_state(self):
        """
        Save the current state of the text area to the undo stack.
        Clear the redo stack whenever a new state is saved.
        """
        current_text = self.text_area.get("1.0", tk.END)
        if not self.undo_stack or self.undo_stack[-1] != current_text:
            self.undo_stack.append(current_text)
            self.redo_stack.clear()  # Clear redo stack when a new state is saved

    def on_text_change(self, event):
        """
        Detect changes in the text area and save the state.
        Ignore non-character keys like Shift, Ctrl, etc.
        """
        if event.keysym not in ["Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"]:
            self.save_state()

    def undo(self):
        """
        Perform the undo operation by reverting to the previous state.
        Move the current state to the redo stack.
        """
        if len(self.undo_stack) > 1:
            current_text = self.undo_stack.pop()  # Remove the current state
            self.redo_stack.append(current_text)  # Save it to the redo stack
            previous_text = self.undo_stack[-1]  # Get the previous state
            self.replace_text(previous_text)  # Replace the text area content

    def redo(self):
        """
        Perform the redo operation by restoring the next state.
        Move the restored state back to the undo stack.
        """
        if self.redo_stack:
            next_text = self.redo_stack.pop()  # Get the next state
            self.undo_stack.append(next_text)  # Save it to the undo stack
            self.replace_text(next_text)  # Replace the text area content

    def replace_text(self, text):
        """
        Replace the content of the text area with the given text.
        """
        self.text_area.delete("1.0", tk.END)  # Clear the text area
        self.text_area.insert(tk.END, text)  # Insert the new text


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()