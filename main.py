import tkinter as tk

# Class
class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor with Undo/Redo")

        # Stacks for undo and redo operations
        self.undo_stack = []
        self.redo_stack = []

        # Customization
        self.root.geometry("750x750")
        self.root.resizable(False, False)

        # Graphical user interface
        self.text_area = tk.Text(root, wrap=tk.WORD, undo=False, font = ("Times New Roman", 14, "italic"))
        self.text_area.pack(expand=True, fill='both')

        # Buttons for undo and redo
        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Undo", command=self.undo).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Redo", command=self.redo).pack(side=tk.LEFT)

        # Event to detect changes in the text
        self.text_area.bind("<KeyRelease>", self.on_text_change)

        # Save the initial state of the text area
        self.save_state()

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