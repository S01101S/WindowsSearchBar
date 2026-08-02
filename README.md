# Custom Windows Search Bar 

| Contents |
| -------- | 
| [About](#About-the-Project) |
| [Features](#features) |
| [Tech Stack](#tech-stack) |
| [Commands](#commands) | 
| [Setup](#setup) |



## About the Project
A lightweight Windows productivity launcher built in Python. It is designed as a faster and highly extensible alternative to the native Windows search bar, this tool allows users to launch local applications, manage clipboard history, control Spotify playback and execute system commands.


## Features 
- **App & File Launching:** Indexes standard Windows directories (Desktop, Start Menu, Documents) to instantly launch `.exe` applications, `.py` scripts, `.blend` files and standard documents. Includes icons for recognised software.
- **Clipboard Manager:** Runs a background monitor to capture clipboard history, storing the last 5 copied strings in a double-ended queue for instant retrieval and re-copying.
- **Spotify**: Full playback control directly from the search bar. 
    - Play, pause, skip and rewind.
    - Search and instantly play specific tracks, artists or personal playlists.
- **Chromium App Integration:** Web searches and YouTube queries automatically launch in a dedicated borderless application using standard browsers (Brave, Google or Edge).
- **Calculator:** Instantly parses and calculates mathematical expressions directly in the results frame as you type.
- **System Power Commands:** Native OS-level commands to shutdown, restart, or abort shutdown.

## Tech Stack
- **Language:** Python 3
- **GUI:** CustomTkinter 
- **API:** Spotipy (Spotify Web API), webbrowser 
- **System Integration:** os, subprocess, pyperclip, keyboard


## Commands 

Trigger the search bar in Windows using the global hotkey: `Ctrl + Shift + Space`.

| Command Syntax        | Action                                                                  | 
| --------------------- | ----------------------------------------------------------------------- | 
| clip                  | Displays the last 5 copied text items. Click to copy back to clipboard. |
| ? <query>             | Performs a standard Google web search.                                  | 
| yt <query>            | Opens a borderless YouTube app window with the search results.          | 
| sp play / sp pause    | Controls active Spotify playback.                                       | 
| sp next / sp previous | Skips to the next or previous song                                      |
| sp song <name>        | Searches Spotify for a song and instantly plays the top result.         |
| sp artist <name>      | Searchesf for an artist and begins playback.                            |
| sp <playlist name>    | searches your personal Spotify library and plays a matching playlist    |
| shutdown / reboot     | Executes a windows power command (with a 1 seconds delay).              |



## Setup


### 1. Clone the Repository 

```bash 
git clone https://github.com/S01101S/WindowsSearchBar.git
cd WindowsSearchBar
```

### 2. Install Dependencies
```
pip install customtkinter keyboard spotipy python-dotenv pyperclip Pillow
```

### 3. Spotify API Configuration 
To use the Spotify features you must have your own developer key.
1. Go to Spotify Developer Dashboard and create an app.
2. Set your redirect URI to `http://127.0.0.1:8080/callback`
3. Create a `.env` file in the root directory of this project and add your keys:

``` Code
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8080
```

### 4. Running the App
Run the script through your IDE or terminal 
``` bash
python main.py
```

**Creating a Standalone Executable:** Once you have tested the script in your IDE or terminal you can use PyInstaller to compile the project into a standalone .exe file. This integrates the launcher directly into your system, meaning you can run it as a standard Windows application without needing to open your IDE or execute the code each time.

NOTE: When creating an .exe using PyInstaller make sure to copy the icons folder and paste it inside the dist folder.
NOTE: Please update the appPaths in the code to make your systems configurations to launch applications correctly.

### License 
[MIT](LICENSE)