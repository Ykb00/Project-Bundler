import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

# ==============================================================================
# CORE BUNDLING LOGIC (No changes here)
# ==============================================================================

def build_file_tree(file_paths):
    tree = {}
    for path in file_paths:
        parts = path.split(os.sep)
        current_level = tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
    return tree

def generate_tree_lines(tree_dict, prefix=""):
    lines = []
    items = sorted(tree_dict.keys(), key=lambda k: (not bool(tree_dict[k]), k.lower()))
    for i, name in enumerate(items):
        is_last = i == (len(items) - 1)
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{name}")
        if tree_dict[name]:
            new_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(generate_tree_lines(tree_dict[name], new_prefix))
    return lines

def perform_bundling(project_dir, output_file_path):
    ignore_list = {'.git', '.vscode', 'node_modules', 'dist', 'build', '__pycache__', '.DS_Store', '*.log', '*.pyc', os.path.basename(output_file_path)}
    all_file_paths = []
    for root, dirs, files in os.walk(project_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in ignore_list]
        for file in files:
            if file not in ignore_list:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, project_dir)
                all_file_paths.append(relative_path)
    all_file_paths.sort()
    tree_structure = build_file_tree(all_file_paths)
    tree_lines = generate_tree_lines(tree_structure)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(f"PROJECT BUNDLE: {os.path.basename(project_dir)}\n" + "=" * 40 + "\n\n")
        f.write("File Structure:\n" + "-" * 20 + "\n" + f"{os.path.basename(project_dir)}/\n")
        for line in tree_lines: f.write(line + "\n")
        f.write("\n" * 2 + "File Contents:\n" + "-" * 20 + "\n\n")
        for relative_path in all_file_paths:
            full_path = os.path.join(project_dir, relative_path)
            display_path = relative_path.replace(os.sep, '/')
            f.write(f"--- File: {display_path} ---\n\n")
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as content_file:
                    f.write(content_file.read())
            except Exception as e:
                f.write(f"*** ERROR: Could not read file. Reason: {e} ***")
            f.write("\n\n" + "=" * 40 + "\n\n")

# ==============================================================================
# GUI APPLICATION CLASS (Updated with Menu and About Dialog)
# ==============================================================================

class ProjectBundlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Bundler")
        self.root.geometry("500x200") # Increased height slightly for the menu
        self.root.minsize(450, 180)

        # --- NEW: Create the main menu bar ---
        self.create_menu()

        self.folder_path = tk.StringVar()
        self.root.columnconfigure(1, weight=1)
        
        # --- Widgets ---
        ttk.Label(root, text="Project Folder:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.path_label = ttk.Label(root, textvariable=self.folder_path, relief="sunken", padding=(5, 2))
        self.path_label.grid(row=0, column=1, padx=5, pady=10, sticky='ew')
        ttk.Button(root, text="Browse...", command=self.select_folder).grid(row=0, column=2, padx=10, pady=10)
        
        self.bundle_button = ttk.Button(root, text="Create Project Bundle...", command=self.bundle_project, state="disabled")
        self.bundle_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')
        
        self.status_label = ttk.Label(root, text="Please select a folder to begin.", relief="sunken")
        self.status_label.grid(row=2, column=0, columnspan=3, padx=0, pady=5, sticky='sew')
        self.root.rowconfigure(2, weight=1)

    # --- NEW: Method to create the entire menu system ---
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About...", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

    # --- NEW: Method to display the "About" dialog window ---
    def show_about_dialog(self):
        # Create a Toplevel window (a new window on top of the main one)
        about_window = tk.Toplevel(self.root)
        about_window.title("About Project Bundler")
        about_window.geometry("350x200")
        about_window.resizable(False, False)
        about_window.transient(self.root) # Keep it on top of the main window
        about_window.grab_set()           # Modal behavior: user can't interact with main window

        # --- !! CUSTOMIZE THIS TEXT !! ---
        created_by_text = "This application was created with passion by\nYaswanth Kumar"
        # --- !! ---------------------- !! ---
        
        # Add widgets to the "About" window
        ttk.Label(about_window, text="Project Bundler", font=("Segoe UI", 16, "bold")).pack(pady=(15, 0))
        ttk.Label(about_window, text="Version 1.1").pack()
        ttk.Separator(about_window, orient='horizontal').pack(fill='x', padx=20, pady=10)
        ttk.Label(about_window, text=created_by_text, justify='center').pack(pady=5)
        ttk.Button(about_window, text="OK", command=about_window.destroy).pack(pady=15)

    def select_folder(self):
        path = filedialog.askdirectory(title="Select a Project Folder")
        if path:
            self.folder_path.set(path)
            self.bundle_button.config(state="normal")
            self.status_label.config(text=f"Ready to bundle: {os.path.basename(path)}")

    def bundle_project(self):
        source_dir = self.folder_path.get()
        if not source_dir:
            messagebox.showerror("Error", "No folder selected. Please browse for a folder first.")
            return

        default_filename = f"{os.path.basename(source_dir)}_bundle.txt"
        save_path = filedialog.asksaveasfilename(
            title="Save Bundle As", initialfile=default_filename,
            defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not save_path:
            self.status_label.config(text="Save operation cancelled.")
            return

        try:
            self.status_label.config(text="Bundling... Please wait.")
            self.root.update_idletasks()
            perform_bundling(source_dir, save_path)
            messagebox.showinfo("Success", f"Project successfully bundled!\n\nSaved to:\n{save_path}")
            self.status_label.config(text="Done. Select another folder to begin again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during bundling:\n\n{e}")
            self.status_label.config(text="An error occurred.")

# --- Main execution block (No changes here) ---
if __name__ == "__main__":
    app_root = tk.Tk()
    app = ProjectBundlerApp(app_root)
    app_root.mainloop()
