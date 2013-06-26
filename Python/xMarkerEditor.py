# xMarkerEditor
# Handles all the marker editing stuff.

from Plasma import *
from PlasmaGame import *
from PlasmaGameConstants import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *

import yaml

def GetEditor():

    editor = {
        "client" : None, 
        "downloading" : False, 
        "downloading_id" : None,
        "uploading" : False,
        "uploadedGame" : False,
        "uploadedGamesMarkers" : 0,
        "uploadedGamesMarkersTotal" : 0,
        "node" : None,
        "game" : {
            "name" : None, 
            "guid" : None,
            "creator" : None, 
            "markers" : []
        }
    }
    return editor

def ListGames(self):

    file = open("Games/List.txt", "w")
    file.write("List of marker games\n--------------------\n")
    for id, game in enumerate(GetList()):
        file.write(str(id) + ": \"" + game.getGameName() + "\"\n")
    file.close()
    self.DisplayStatusMessage("A list of your games has been saved in \"Games/List.txt\".")

def DownloadGame(self, params=None):

    games = GetList()
    try:
        game = games[id]
        name = PtGetLocalPlayer().getPlayerName()
        guid = game.getGameGuid()
        self.editor["downloading"] = True
        self.editor["downloading_id"] = id
        self.editor["game"]["name"] = game.getGameName()
        self.editor["game"]["guid"] = guid
        PtCreateMarkerGame(self.key, PtMarkerGameTypes.kMarkerGameQuest, templateId = guid)
        filename = ""
        for c in name:
            if c.isalnum():
                filename += c
        self.DisplayStatusMessage("Your game has been downloaded as \"Games/" + filename + "." + str(id) + ".txt\"")
    except IndexError:
        self.DisplayStatusMessage("There is no such marker game.")

def GetList():

    games = []
    journals = ptVault().getAgeJournalsFolder()
    agefolderRefs = journals.getChildNodeRefList()
    for agefolderRef in agefolderRefs:
        agefolder = agefolderRef.getChild()
        if agefolder.getType() == PtVaultNodeTypes.kFolderNode:
            agefolder = agefolder.upcastToFolderNode()
            subs = agefolder.getChildNodeRefList()
            for sub in subs:
                sub = sub.getChild()
                if sub.getType() == PtVaultNodeTypes.kMarkerGameNode:
                    game = sub.upcastToMarkerGameNode()
                    games.append(game)
    return games

def UploadGame(self, params=None):

    try:
        file = open("Games/" + params, "r")
        content = file.read()
        file.close()
        try:
            self.editor["game"] = yaml.load(content)
            try:
                guid = self.editor["game"]["guid"]
                valid = False
                for game in GetList():
                    if game.getGameGuid() == guid:
                        valid = True
                        self.editor["node"] = game
                if not valid:
                    self.DisplayStatusMessage("Invalid GUID.")
                    return
                # We are editing an existing game.
                try:
                    if isinstance(self.editor["game"]["markers"], list) == False:
                        self.DisplayStatusMessage("The file is not a valid Marker Game file: invalid parameters.")
                        return
                    for marker in self.editor["game"]["markers"]:
                        try:
                            if not isinstance(marker["text"], unicode) or not isinstance(marker["age"], unicode) or not isinstance(marker["coords"], list) or len(marker["coords"]) != 3:
                                self.DisplayStatusMessage("The file is not a valid Marker Game file: incorrect markers.")
                                return
                            for coord in marker["coords"]:
                                if isinstance(coord, float) == False:
                                    self.DisplayStatusMessage("The file is not a valid Marker Game file: incorrect marker coordinates.")
                                    return
                        except KeyError:
                            self.DisplayStatusMessage("The file is not a valid Marker Game file: incorrect markers.")
                            return
                        if len(marker["text"]) >= 128:
                            self.DisplayStatusMessage("The file is not a valid Marker Game file: marker description too long.")
                            return
                except KeyError:
                    self.DisplayStatusMessage("The file is not a valid Marker Game file: missing parameters.")
                    return
                try:
                    if len(self.editor["game"]["name"]) >= 128:
                        self.DisplayStatusMessage("The file is not a valid Marker Game file: name too long.")
                        return
                except KeyError:
                    pass
                self.editor["uploading"] = True
                PtCreateMarkerGame(self.key, PtMarkerGameTypes.kMarkerGameQuest, self.editor["game"]["name"], templateId = guid)
            except KeyError:
                # We are creating a new game.
                try:
                    if isinstance(self.editor["game"]["name"], unicode) == False or isinstance(self.editor["game"]["markers"], list) == False or isinstance(self.editor["game"]["creator"], unicode) == False:
                        self.DisplayStatusMessage("The file is not a valid Marker Game file: invalid parameters.")
                        return
                    for marker in self.editor["game"]["markers"]:
                        try:
                            if isinstance(marker["text"], unicode) == False or isinstance(marker["age"], unicode) == False or isinstance(marker["coords"], list) == False or len(marker["coords"]) != 3:
                                self.DisplayStatusMessage("The file is not a valid Marker Game file: incorrect markers.")
                                return
                            for coord in marker["coords"]:
                                if isinstance(coord, float) == False:
                                    self.DisplayStatusMessage("The file is not a valid Marker Game file: incorrect marker coordinates.")
                                    return
                        except KeyError:
                            self.DisplayStatusMessage("The file is not a valid Marker Game file: incorrect markers.")
                            return
                        if len(marker["text"]) >= 128:
                            self.DisplayStatusMessage("The file is not a valid Marker Game file: marker description too long.")
                            return
                except KeyError:
                    self.DisplayStatusMessage("The file is not a valid Marker Game file: missing parameters.")
                    return
                if len(self.editor["game"]["name"]) >= 128:
                    self.DisplayStatusMessage("The file is not a valid Marker Game file: name too long.")
                    return
                self.editor["uploading"] = True
                PtCreateMarkerGame(self.key, PtMarkerGameTypes.kMarkerGameQuest, self.editor["game"]["name"])
        except ValueError:
            self.DisplayStatusMessage("The file is not a valid Marker Game file: incorrect format.")
            return   
    except IOError:
        self.DisplayStatusMessage("Could not open file.")
        return