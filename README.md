# Project Bundler Utility

Project Bundler is a simple yet powerful desktop application built with Python and Tkinter. It is designed to scan a project directory (or multiple directories), consolidate all its text-based source code into a single `.txt` file, and include a file structure tree. This is incredibly useful for sharing projects, submitting assignments, or feeding code into Large Language Models (LLMs) for analysis or review.

![Project Bundler App Screenshot](v1.3_Add_Subfolders_Feature/image.png)
*(Screenshot of v1.3)*

## Why Use Project Bundler?

-   **Easy Sharing:** Package an entire codebase into a single, easy-to-share text file.
-   **Code Reviews:** Provide a complete code snapshot for peer or AI-driven reviews without needing to zip the project.
-   **LLM-Friendly Context:** Easily copy-paste an entire project's context into models like ChatGPT, Claude, or Gemini for debugging, explanation, or refactoring.
-   **Archiving:** Create a simple, human-readable archive of a project at a specific point in time.

---

## Features

This repository tracks the evolution of the application through several versions:

### Version 1.0: Initial Release
-   Basic GUI to select a single project folder.
-   Bundles all files into a single `.txt` file.
-   Automatically generates a file structure tree at the top of the bundle.
-   Ignores common unnecessary files and folders (e.g., `.git`, `__pycache__`, `node_modules`).

### Version 1.2: UI and Performance Upgrade
-   **Multi-Folder Selection:** Select and manage a list of multiple project folders to bundle together.
-   **UI Responsiveness:** The bundling process now runs on a separate thread, preventing the "Not Responding" issue with large projects.
-   **Progress Bar:** A real-time progress bar shows the status of the bundling process.
-   **Robust Folder Management:** Add or remove folders from the queue before bundling.

### Version 1.3: Enhanced Usability
-   **"Add Subfolders" Feature:** A powerful new feature to quickly add multiple projects.
    -   Select a parent directory (e.g., `C:\MyProjects`).
    -   The app displays a list of all immediate subfolders.
    -   Use `Ctrl+Click` or `Shift+Click` to multi-select the desired project folders to add to the main list.

---

## How to Use the Application

### Using the Pre-built Executable (`.exe`)

The easiest way to use the app is to run the pre-built executable.

1.  Navigate to the **Releases** section of this GitHub repository.
2.  Download the `.zip` file for the latest version (e.g., `ProjectBundler_v1.3.zip`).
3.  Unzip the file.
4.  Run `ProjectBundler.exe`.

### Running from Source

If you have Python installed, you can run the application directly from the source code.

**Prerequisites:**
-   Python 3.9+

**Steps:**

1.  Clone or download this repository.
    ```bash
    git clone https://github.com/your-username/Project-Bundler-App.git
    cd Project-Bundler-App
    ```

2.  Navigate to the folder of the version you want to run. For example:
    ```bash
    cd v1.3_Add_Subfolders_Feature
    ```

3.  Run the main GUI script:
    ```bash
    python bundle_gui.py
    ```

---

## How to Build the Executable from Source

If you want to modify the code and build your own `.exe` file, you will need `PyInstaller`.

**Prerequisites:**
-   Python 3.9+
-   PyInstaller

**Steps:**

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Navigate to the project directory (e.g., `v1.3_Add_Subfolders_Feature`).

3.  Run the PyInstaller command using the included `.spec` file. The `.spec` file contains all the necessary build configurations, including the application icon.
    ```bash
    pyinstaller ProjectBundler.spec
    ```
    *Note: If the `pyinstaller` command is not found, you may need to use `python -m pyinstaller ...` or troubleshoot your system's PATH.*

4.  The final executable will be located in the newly created `dist/` directory.

---

## Project Structure Overview

The application is built around a main GUI script (`bundle_gui.py`) which handles both the user interface and the core bundling logic.

-   **`bundle_gui.py`**: The main Tkinter application code. It defines the UI layout, event handlers (button clicks), and manages the threading for the bundling process.
-   **`ProjectBundler.spec`**: The configuration file for PyInstaller. It specifies the entry point script, the name of the output executable, data files, and the application icon.
-   **`app_icon.ico`**: The icon file used for the application window and the final `.exe`.
-   **`image.png`**: A screenshot of the application used in the README.

This project was created with passion by Yaswanth Kumar.
