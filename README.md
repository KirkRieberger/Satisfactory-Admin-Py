# Satisfactory Admin Py
## A web app to manage Satisfactory Dedicated Servers
> [!IMPORTANT]
> This repo is a work in progress! Only rudimentary functionality exists!

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
- [x] RenameServer
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
- [ ] Initial Server Claim / Config
- [ ] Dashboard Tab
- [x] Settings Tab
- [ ] Save Management Tab
- [ ] Console Tab

#### Other
- [ ] "No Cert" function to control "verify=False" flag in requests.post() (Should be True by default)
- [ ] Local header override for content-type (multipart, etc). Assume application/json in most circumstances
- [ ] Login modal, "claim server" option
    Claim Server button -> Enter IP/Port -> On success, replace auth token -> name server, set pswds
