import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import queue

# ==============================================================================
# CORE BUNDLING LOGIC (Moved into the class to access GUI elements)
# ==============================================================================
# This logic will now be part of the app class to easily update the GUI.

# ==============================================================================
# GUI APPLICATION CLASS (Completely Overhauled)
# ==============================================================================

class ProjectBundlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Bundler v1.2")
        self.root.geometry("600x450")
        self.root.minsize(500, 350)

        # --- Main Frame ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Folder Selection Frame ---
        folder_frame = ttk.LabelFrame(main_frame, text="Project Folders to Bundle", padding="10")
        folder_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # --- Listbox to show selected folders ---
        self.folder_listbox = tk.Listbox(folder_frame, selectmode=tk.EXTENDED)
        self.folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Scrollbar for the listbox ---
        scrollbar = ttk.Scrollbar(folder_frame, orient=tk.VERTICAL, command=self.folder_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.folder_listbox.config(yscrollcommand=scrollbar.set)

        # --- Folder management buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.add_button = ttk.Button(button_frame, text="Add Folder...", command=self.add_folder)
        self.add_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.remove_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_folder)
        self.remove_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # --- Bundling and Progress Frame ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)

        self.bundle_button = ttk.Button(action_frame, text="Create Project Bundle...", command=self.start_bundling, state="disabled")
        self.bundle_button.pack(fill=tk.X, pady=(0, 5))

        # --- Progress Bar ---
        self.progress = ttk.Progressbar(action_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(5, 0))

        # --- Status Label ---
        self.status_label = ttk.Label(main_frame, text="Add folders to begin.", relief="sunken", anchor='w', padding=5)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5,0))

        # --- Menu ---
        self.create_menu()
        
        # Queue for thread communication
        self.queue = queue.Queue()
        self.root.after(100, self.process_queue)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About...", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

    def show_about_dialog(self):
        messagebox.showinfo(
            "About Project Bundler",
            "Project Bundler v1.2\n\nThis application was created with passion by Yaswanth Kumar."
        )

    def add_folder(self):
        path = filedialog.askdirectory(title="Select a Project Folder")
        if path:
            # Avoid adding duplicates
            if path not in self.folder_listbox.get(0, tk.END):
                self.folder_listbox.insert(tk.END, path)
                self.update_ui_state()

    def remove_folder(self):
        selected_indices = self.folder_listbox.curselection()
        # Iterate backwards to safely delete items from the list
        for i in reversed(selected_indices):
            self.folder_listbox.delete(i)
        self.update_ui_state()

    def update_ui_state(self):
        if self.folder_listbox.size() > 0:
            self.bundle_button.config(state="normal")
            self.status_label.config(text=f"{self.folder_listbox.size()} folder(s) selected. Ready to bundle.")
        else:
            self.bundle_button.config(state="disabled")
            self.status_label.config(text="Add folders to begin.")

    def set_controls_state(self, state):
        """Enable or disable main controls."""
        self.bundle_button.config(state=state)
        self.add_button.config(state=state)
        self.remove_button.config(state=state)
        # Disable listbox interaction during bundling
        listbox_state = "normal" if state == "normal" else "disabled"
        self.folder_listbox.config(state=listbox_state)

    def process_queue(self):
        """Process messages from the worker thread."""
        try:
            while True:
                msg = self.queue.get_nowait()
                msg_type = msg.get("type")
                if msg_type == "progress":
                    self.progress['value'] = msg["value"]
                    self.status_label.config(text=msg.get("text", ""))
                elif msg_type == "max_progress":
                    self.progress['maximum'] = msg["value"]
                elif msg_type == "reset_progress":
                    self.progress['value'] = 0
                    self.status_label.config(text="Starting bundle...")
                elif msg_type == "done":
                    self.set_controls_state("normal")
                    messagebox.showinfo("Success", f"Project successfully bundled!\n\nSaved to:\n{msg['path']}")
                    self.status_label.config(text="Done. Add or remove folders to bundle again.")
                elif msg_type == "error":
                    self.set_controls_state("normal")
                    messagebox.showerror("Error", f"An error occurred during bundling:\n\n{msg['error']}")
                    self.status_label.config(text="An error occurred.")
        except queue.Empty:
            pass  # No more messages.
        finally:
            self.root.after(100, self.process_queue) # Check again after 100ms

    def start_bundling(self):
        folders_to_bundle = self.folder_listbox.get(0, tk.END)
        if not folders_to_bundle:
            messagebox.showerror("Error", "No folders selected. Please add a folder first.")
            return

        default_filename = f"{os.path.basename(folders_to_bundle[0])}_bundle.txt"
        save_path = filedialog.asksaveasfilename(
            title="Save Bundle As", initialfile=default_filename,
            defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not save_path:
            self.status_label.config(text="Save operation cancelled.")
            return

        self.set_controls_state("disabled")
        self.queue.put({"type": "reset_progress"})

        # Run bundling in a separate thread
        thread = threading.Thread(
            target=self.bundle_project_threaded,
            args=(folders_to_bundle, save_path),
            daemon=True
        )
        thread.start()
        
    def bundle_project_threaded(self, project_dirs, output_file_path):
        """This function runs in a separate thread."""
        try:
            all_files_to_bundle = []
            
            # --- First pass: Collect all file paths to calculate total for progress bar ---
            self.queue.put({"type": "progress", "value": 0, "text": "Scanning files..."})
            for project_dir in project_dirs:
                ignore_list = {'.git', '.vscode', 'node_modules', 'dist', 'build', '__pycache__', '.DS_Store', '*.log', '*.pyc', os.path.basename(output_file_path)}
                for root, dirs, files in os.walk(project_dir, topdown=True):
                    dirs[:] = [d for d in dirs if d not in ignore_list]
                    for file in files:
                        if file not in ignore_list:
                            full_path = os.path.join(root, file)
                            all_files_to_bundle.append((project_dir, full_path))
            
            self.queue.put({"type": "max_progress", "value": len(all_files_to_bundle)})

            # --- Second pass: Write to the output file ---
            with open(output_file_path, 'w', encoding='utf-8') as f:
                # Bundle Header
                f.write("=" * 15 + " PROJECT BUNDLE " + "=" * 15 + "\n")
                f.write(f"Bundled {len(project_dirs)} project(s).\n\n")

                processed_count = 0
                for project_dir in project_dirs:
                    project_name = os.path.basename(project_dir)
                    f.write(f"PROJECT BUNDLE: {project_name}\n" + "=" * 40 + "\n\n")
                    
                    # Filter files for the current project
                    project_files = [path for proj, path in all_files_to_bundle if proj == project_dir]
                    
                    # Generate File Structure
                    relative_paths = [os.path.relpath(p, project_dir) for p in project_files]
                    relative_paths.sort()
                    
                    tree_structure = self.build_file_tree(relative_paths)
                    tree_lines = self.generate_tree_lines(tree_structure)
                    
                    f.write("File Structure:\n" + "-" * 20 + "\n" + f"{project_name}/\n")
                    for line in tree_lines: f.write(line + "\n")
                    
                    # Write File Contents
                    f.write("\n\n" + "File Contents:\n" + "-" * 20 + "\n\n")
                    for rel_path in relative_paths:
                        full_path = os.path.join(project_dir, rel_path)
                        display_path = rel_path.replace(os.sep, '/')
                        
                        # Update progress
                        processed_count += 1
                        status_text = f"Bundling: {display_path}"
                        self.queue.put({"type": "progress", "value": processed_count, "text": status_text})
                        
                        f.write(f"--- File: {display_path} ---\n\n")
                        try:
                            with open(full_path, 'r', encoding='utf-8', errors='ignore') as content_file:
                                f.write(content_file.read())
                        except Exception as e:
                            f.write(f"*** ERROR: Could not read file. Reason: {e} ***")
                        f.write("\n\n" + "=" * 40 + "\n\n")

            self.queue.put({"type": "done", "path": output_file_path})

        except Exception as e:
            self.queue.put({"type": "error", "error": str(e)})

    # --- Tree generation helper functions (unchanged) ---
    def build_file_tree(self, file_paths):
        tree = {}
        for path in file_paths:
            parts = path.split(os.sep)
            current_level = tree
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        return tree

    def generate_tree_lines(self, tree_dict, prefix=""):
        lines = []
        items = sorted(tree_dict.keys(), key=lambda k: (not bool(tree_dict[k]), k.lower()))
        for i, name in enumerate(items):
            is_last = i == (len(items) - 1)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{name}")
            if tree_dict[name]:
                new_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(self.generate_tree_lines(tree_dict[name], new_prefix))
        return lines

# --- Main execution block (No changes here) ---
if __name__ == "__main__":
    app_root = tk.Tk()
    app = ProjectBundlerApp(app_root)
    app_root.mainloop()
