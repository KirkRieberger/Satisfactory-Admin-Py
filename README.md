# Satisfactory Admin Py
## A web app to manage Satisfactory Dedicated Servers
THIS REPO IS A WORK IN PROGRESS! ONLY RUDIMENTARY FUNCTIONALITY EXISTS!

This project aims to implement most* of the Satisfactory Dedicated Server API functions in an easy-to-use interface.

## TODO:
#### Lightweight Query API
- [x] Server State
- [x] Change List
- [x] Flags
- [x] Substate Change List
- [x] Server Name

#### HTTPS API
##### Basic Functionality
- [x] VerifyAuthenticationToken
- [x] QueryServerState
##### Modify Server Options
- [x] GetServerOptions
- [ ] ApplyServerOptions
- [x] GetAdvancedGameSettings
- [ ] ApplyAdvancedGameSettings
- [ ] RenameServer
##### New Server Tasks
- [ ] ClaimServer
- [ ] SetClientPassword
- [ ] SetAdminPassword
##### Save/Session Management
- [ ] SetAutoLoadSessionName
- [ ] CreateNewGame
- [ ] SaveGame
- [ ] DeleteSaveFile
- [ ] DeleteSaveSession
- [ ] EnumerateSessions
- [ ] LoadGame
- [ ] UploadSaveGame
- [ ] DownloadSaveGame
##### Miscellaneous
- [ ] RunCommand
- [ ] Shutdown

#### User Interface
- [x] Basic Layout
- [ ] Dashboard Tab
- [ ] Settings Tab
- [ ] Save Management Tab
- [ ] Console Tab