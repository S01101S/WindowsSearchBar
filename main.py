import customtkinter as tk
import keyboard
import os 
import subprocess
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
from PIL import Image

class SearchBarApp:

    def __init__(self):

        self.appPaths = {
            "spotify": "spotify", 
            "vscode": r"C:\Users\fujitsu\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "minecraft": r"C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe",
            "download": r"C:\Users\fujitsu\Downloads",
            "settings": "ms-settings:",
            "bluetooth": "ms-settings:bluetooth",
            "network": "ms-settings:network-status",
            "wifi": "ms-settings:network-wifi",
            "display": "ms-settings:display",
            "sound": "ms-settings:sound",
            "windows update": "ms-settings:windowsupdate",
            "apps": "ms-settings:appsfeatures",
            "power and sleep": "ms-settings:powersleep",
            "personalisation": "ms-settings:personalization",
            "wiztree": r"C:\Program Files\WizTree\WizTree64.exe"
        }


        self.iconPath = {
            "vscode": "Icons/vscodeIcon.png",
            "brave": "Icons/braveIcon.png",
            "google": "Icons/googleIcon.png",
            "discord": "Icons/discordIcon.png",
            "steam": "Icons/steamIcon.png",
            "spotify": "Icons/spotifyIcon.png",
            "minecraft": "Icons/minecraftIcon.png",
            "backup": "Icons/backupIcon.png",
            "settings": "Icons/settingIcon.png",
            "bluetooth": "Icons/settingIcon.png",
            "network": "Icons/settingIcon.png",
            "wifi": "Icons/settingIcon.png",
            "display": "Icons/settingIcon.png",
            "sound": "Icons/settingIcon.png",
            "windows update": "Icons/settingIcon.png",
            "apps": "Icons/settingIcon.png",
            "power and sleep": "Icons/settingIcon.png",
            "shutdown": "Icons/settingIcon.png",
            "power off": "Icons/settingIcon.png",
            "restart": "Icons/settingIcon.png",
            "reboot": "Icons/settingIcon.png",
            "abort shutdown": "Icons/settingIcon.png"
        }

        self.spotifyClientId = '09ed8cf13660402a89cec458587dff1f'
        self.spotifyClientSecret = '8762c215354640eb8c8016aa41eeb8ac'
        self.spotifyRedirectURI = 'http://127.0.0.1:8080/callback'

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.spotifyClientId,
            client_secret=self.spotifyClientSecret,
            redirect_uri=self.spotifyRedirectURI,
            scope="user-modify-playback-state user-read-playback-state playlist-read-private"
        ))

        self.isHidden = False 

        tk.set_appearance_mode("dark")
        self.app = tk.CTk()
        self.setupFrame() 
        self.initApps()
        self.bindKeys()


    def setupFrame(self):
        
        self.app.geometry("600x100")
        self.app.title("Launcher")
        self.app.overrideredirect(True)

        windowWidth = 600
        windowHeight = 400

        screenWidth = self.app.winfo_screenwidth()
        screenHeight = self.app.winfo_screenheight()

        xCoord = int((screenWidth / 2) - (windowWidth / 2))
        yCoord = int(screenHeight * 0.1)

        self.app.geometry(f"{windowWidth}x{windowHeight}+{xCoord}+{yCoord}")

        transparentColor = "#000001"
        self.app.configure(fg_color=transparentColor)
        self.app.wm_attributes("-transparentcolor", transparentColor)

        self.searchBar = tk.CTkEntry(self.app, width=500, height=50, corner_radius=20, placeholder_text="Search...", fg_color="#2b2b2b", border_color="#565b5e", border_width=2, text_color="white")
        self.searchBar.pack(pady=25)

        self.resultsFrame = tk.CTkFrame(self.app, fg_color="transparent")
        self.resultsFrame.pack(pady=0)
        self.isHidden = False


    def initApps(self):

        startMenu = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs")
        systemMenu = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
        desktopMenu = os.path.join(os.environ["USERPROFILE"], r"Desktop")
        publicDesktopMenu = r"C:\Users\Public\Desktop"
        documentsFolder = os.path.join(os.environ["USERPROFILE"], "Documents")  
        cvFolder = os.path.join(os.environ["USERPROFILE"], r"Documents\CV")
        personalProjects = r"C:\PersonalProjects"
    
        directories = [startMenu, systemMenu, desktopMenu, publicDesktopMenu, documentsFolder, cvFolder, personalProjects]

        bannedSearches = ["uninstall", "setup", "update", "recovery", "administrative tools", "gh-pages", "__main__", "cli -"]
        allowedExtensions = (".lnk", ".exe", ".png", ".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".mp4", ".mp3", ".wav", ".avi", ".mkv", ".flv", ".mov", ".wmv", ".zip", ".rar", ".py", ".cs", ".css", ".html", ".js", ".c", ".blend")
    
        for i in directories:
    
            try:
                for root, dirs, files in os.walk(i):
    
    
                    bannedFolders = ["node_modules", "venv", "env", ".git", "__pycache__", "bin", "obj", "build", "dist", ".idea", ".vscode", "gh-pages", "site-packages", "lib", "scripts", "_internal", "icons"]
                    dirs[:] = [x for x in dirs if x.lower() not in bannedFolders]
    
                    for folder in dirs:
    
                        folderName = folder.lower()
    
                        isAppBanned = False 
    
                        for j in bannedSearches:
    
                            if(j in folderName):
                                isAppBanned = True 
    
                        if(isAppBanned == False and folderName not in self.appPaths):
                            self.appPaths[folderName] = os.path.join(root, folder) 
    
                            
    
                    for file in files:
                        if(file.endswith(allowedExtensions)):
    
                            app, extension = os.path.splitext(file)
                        
                            if(extension.lower() in [".lnk", ".exe"]):
                                appName = app.lower()
                            else: 
                                parentFolder = os.path.basename(root).lower()
                                appName = f"{parentFolder} - {file.lower()}"
    
                            isAppBanned = False 
    
                            for j in bannedSearches:
                                if(j in appName):
                                    isAppBanned = True 
    
                            if(isAppBanned == False and appName not in self.appPaths):
                                self.appPaths[appName] = os.path.join(root, file)
            except Exception:
                pass



    def launchApp(self, appName):

        filePath = self.appPaths[appName]
        
        name, extension = os.path.splitext(filePath)
    
        codingExtension = [".py", ".cs", ".css", ".html", ".js", ".c", ".cpp"]
    
        try: 
            if(extension.lower() in codingExtension):
                subprocess.Popen(f'code "{filePath}"', shell=True)
            else: 
                os.startfile(filePath)
        except FileNotFoundError:
            subprocess.Popen(f'start "{self.appPaths[appName]}"', shell=True)
        except Exception as e:
            print(f"Error: {e}")        
    
        self.searchBar.delete(0, tk.END)
    
        for i in self.resultsFrame.winfo_children():
            i.destroy()
    
    
        self.app.withdraw()
        self.isHidden = True 



    def spaceKey(self,event):

        searchQuery = self.searchBar.get().lower().strip()

        googleSearchQuery = searchQuery[1:].strip()

        if(searchQuery[0] == "?"):
        
            webbrowser.open(f"https://www.google.com/search?q={googleSearchQuery}")

            self.searchBar.delete(0, tk.END) 
            self.isHidden = True
            self.app.withdraw()
            return

        if(searchQuery.startswith("sp artist ")):

            artistName = searchQuery[10:].strip()

            self.playSpotifyArtist(artistName)

            self.searchBar.delete(0, tk.END)
            self.isHidden = True 
            self.app.withdraw()
            return

        if(searchQuery in ['sp play', 'sp pause', 'sp next', 'sp previous', 'sp skip']):
        
            spotifyAction = searchQuery.split()[-1]

            self.handleSpotifyAction(spotifyAction)

            self.searchBar.delete(0, tk.END)
            self.isHidden = True
            self.app.withdraw()
            return

        if(searchQuery.startswith("sp song ")):

            songName = searchQuery[8:].strip()

            self.handleSpotifySong(songName)

            self.searchBar.delete(0, tk.END)
            self.isHidden = True 
            self.app.withdraw()
            return

        if(searchQuery.startswith("sp ")):

            playlistName = searchQuery[3:].strip()

            self.playSpotifyPlaylist(playlistName)

            self.searchBar.delete(0, tk.END)
            self.isHidden = True 
            self.app.withdraw()
            return

        if(searchQuery.startswith("yt ")):

            youtubeQuery = searchQuery[3:].strip().replace(" ", "+")
            youtubeURL = f"https://www.youtube.com/results?search_query={youtubeQuery}" 

            bravePath = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

            try:
                subprocess.Popen([bravePath, youtubeURL])
            except FileNotFoundError:
                webbrowser.open(youtubeURL)

            self.searchBar.delete(0, tk.END)
            self.isHidden = True 
            self.app.withdraw() 
            return

        if(searchQuery in ["shutdown", "power off"]):
            subprocess.call(["shutdown", "-s", "-t", "1"])
            self.searchBar.delete(0, tk.END)
            self.isHidden = True 
            self.app.withdraw()
            return 

        if(searchQuery in ["restart", "reboot"]):
            subprocess.call(["shutdown", "-r", "-t", "1"])
            self.searchBar.delete(0, tk.END)
            self.isHidden = True 
            self.app.withdraw()
            return 

        if(searchQuery == "abort shutdown"):
            subprocess.call(["shutdown", "-a"])
            self.searchBar.delete(0, tk.END)
            self.isHidden = True 
            self.app.withdraw()
            return

        if(searchQuery in self.appPaths):

            self.launchApp(searchQuery)
            
        else:

            for i in self.appPaths:

                if(searchQuery in i):
                    self.launchApp(i)
                    break



    def toggleSearchBar(self):

        if(self.isHidden):
            self.app.deiconify()
            self.app.attributes("-topmost", True)
            self.app.after(50, self.searchBar.focus_force)
            self.isHidden = False 
        else:
            self.app.withdraw()
            self.isHidden = True


    def emptyClick(self, event):

        if(str(self.app.focus_get()) == "None"):
            self.app.withdraw()
            self.isHidden = True 




    def resultFrameSearches(self, event):


        if(event.keysym == "Return"):
            return 
        
        searchQuery = self.searchBar.get().lower().strip()


        for i in self.resultsFrame.winfo_children():
            i.destroy()

        if(searchQuery == ""):
            return 

        if(searchQuery[0] == "?"):
            return



        if(re.match(r'^[0-9+\-*/(). %]+$', searchQuery)):
                
            try:

                ans = str(eval(searchQuery))

                resultRowFrame = tk.CTkFrame(self.resultsFrame, width=500, height=35, fg_color="#2b2b2b")
                resultRowFrame.pack(pady=2, fill="x")
                resultRowFrame.pack_propagate(False)

                name = tk.CTkLabel(resultRowFrame, text=ans, text_color="white", font=("Arial", 16, "bold"), anchor="w")
                name.pack(side="left", padx=10)

                return
                
            except Exception as e: 
                return
                

    
        matchingItems = 0


        for i in self.appPaths:

            if(searchQuery in i):

                resultRowFrame = tk.CTkFrame(self.resultsFrame, width=500, height=35, fg_color="#2b2b2b")
                resultRowFrame.pack(pady=2, fill="x")
                resultRowFrame.pack_propagate(False) 

                        
                iconToLoad = self.iconPath["backup"] 

                for y in self.iconPath:

                    if(y in i):
                        iconToLoad = self.iconPath[y]
                        break 

                appIcon = tk.CTkImage(light_image=Image.open(iconToLoad), size=(24, 24))

                iconLabel = tk.CTkLabel(resultRowFrame, text="", image=appIcon)
                iconLabel.pack(side="left", padx=(10, 5))

                name = tk.CTkLabel(resultRowFrame, text=i, text_color="white", anchor="w")
                name.pack(side="left", padx=10)

                displayPath = self.appPaths[i]
                if(len(displayPath) > 40):
                    displayPath = "...." + displayPath[-37:]

                path = tk.CTkLabel(resultRowFrame, text=displayPath, text_color="gray50", anchor="e")
                path.pack(side="right", padx=10)

                for x in (resultRowFrame, name, path):

                    x.bind("<Button-1>", lambda event, name=i: self.launchApp(name))
                    x.bind("<Enter>", lambda event, frame=resultRowFrame: frame.configure(fg_color="#565b5e"))
                    x.bind("<Leave>", lambda event, frame=resultRowFrame: frame.configure(fg_color="#2b2b2b"))



                matchingItems += 1
                if(matchingItems >= 7):
                    break



    def bindKeys(self):

        self.searchBar.bind("<KeyRelease>", self.resultFrameSearches)
        keyboard.add_hotkey('ctrl+shift+space', self.toggleSearchBar, suppress=True)
        self.searchBar.bind("<Return>", self.spaceKey)
        self.app.bind("<FocusOut>", self.emptyClick)


    def run(self):

        self.app.mainloop()



    def playSpotifyPlaylist(self, playlistName):

        try:
            playlistResult = self.sp.current_user_playlists(limit=50)
            playlistURI = None 


            for i in playlistResult['items']:

                if(i['name'].lower() == playlistName.lower()):
                    playlistURI = i['uri']
                    break

            if(playlistURI):

                devices = self.sp.devices()

                if(not devices['devices']):
                    print("Error spotify is not open")
                    return 

                targetDevice = devices['devices'][0]['id']

                self.sp.start_playback(device_id=targetDevice, context_uri=playlistURI)
                                
            else:
                print(f"Error could not find '{playlistName}' in your library.")
                
        except Exception as e:
            print(f"Error {e}")


    def playSpotifyArtist(self, artistName):

        try:

            artistResult = self.sp.search(q=artistName, type="artist", limit=1)

            if(artistResult['artists']['items']):

                artistURI = artistResult['artists']['items'][0]['uri']

            if(artistURI):

                devices = self.sp.devices()

                if(not devices['devices']):
                    print("Error spotify is not open")
                    return 

                targetDevice = devices['devices'][0]['id']

                self.sp.start_playback(device_id=targetDevice, context_uri=artistURI)

            else:
                print("Could not find artist")
        except Exception as e:
            print(f"Error {e}")    


    def handleSpotifyAction(self, action):

        try:
            devices = self.sp.devices()

            if(not devices['devices']):
                print("Error spotify is not open")
                return 

            targetDevice = devices['devices'][0]['id']

            if(action == "play"):
                self.sp.start_playback(device_id=targetDevice)
            elif(action == "pause"):
                self.sp.pause_playback(device_id=targetDevice)
            elif(action == "skip" or action == "next"):
                self.sp.next_track(device_id=targetDevice)
            elif(action == "previous"):
                self.sp.previous_track(device_id=targetDevice)


        except Exception as e:
            print(f"Error {e}")

    def handleSpotifySong(self, songName):

        try:

            trackQuery = f"track:{songName}"

            songResult = self.sp.search(q=trackQuery, type="track", limit=1)

            if(songResult['tracks']['items']):

                songURI = songResult['tracks']['items'][0]['uri']

                devices = self.sp.devices()

                if(not devices['devices']):
                    print("Error spotify is not open")
                    return 

                targetDevice = devices['devices'][0]['id']

                self.sp.start_playback(device_id=targetDevice, uris=[songURI])

            else:
                print("Error")

        except Exception as e:
            print(f"Error {e}")

if(__name__ == "__main__"):
    searchBarLauncher = SearchBarApp()
    searchBarLauncher.run()