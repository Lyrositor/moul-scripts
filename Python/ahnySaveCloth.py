# -*- coding: utf-8 -*-
""" *==LICENSE==*

CyanWorlds.com Engine - MMOG client, server and tools
Copyright (C) 2011  Cyan Worlds, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Additional permissions under GNU GPL version 3 section 7

If you modify this Program, or any covered work, by linking or
combining it with any of RAD Game Tools Bink SDK, Autodesk 3ds Max SDK,
NVIDIA PhysX SDK, Microsoft DirectX SDK, OpenSSL library, Independent
JPEG Group JPEG library, Microsoft Windows Media SDK, or Apple QuickTime SDK
(or a modified version of those libraries),
containing parts covered by the terms of the Bink SDK EULA, 3ds Max EULA,
PhysX SDK EULA, DirectX SDK EULA, OpenSSL and SSLeay licenses, IJG
JPEG Library README, Windows Media SDK EULA, or QuickTime SDK EULA, the
licensors of this Program grant you additional
permission to convey the resulting work. Corresponding Source for a
non-source form of such a combination shall include the source code for
the parts of OpenSSL and IJG JPEG Library used as well as that of the covered
work.

You can contact Cyan Worlds, Inc. by email legal@cyan.com
 or by snail mail at:
      Cyan Worlds, Inc.
      14617 N Newport Hwy
      Mead, WA   99021

 *==LICENSE==* """

## @package ahnySaveCloth
# The controls for the Path of the Shell save cloths.
# @author Adam Van Ornum
# @date January 2004

from Plasma import *
from PlasmaTypes import *

# Define the attributes that will be entered in Max.
Activator = ptAttribActivator(1,"Activator: Cloth Clickable")
OneShotResp = ptAttribResponder(2, "Resp: One Shot")
ClothID  = ptAttribString(3, "Save cloth ID")


## Modifier for Ahnonay save cloths.
# Manages all the save cloths.
class ahnySaveCloth(ptModifier):

    id = 5424
    version = 1

    ## Initialize the save cloths modifier.
    def __init__(self):

        PtDebugPrint(u"ahnySaveCloth: Version {}.".format(self.version))
        ptModifier.__init__(self)
        self.avatar = None
        self.link = None
        self.whereAmI = 0
        self.gotSC = 0
        self.sdlSC = ""

    ## Called by Plasma on receipt of the first plEvalMsg.
    # Gets the setting for the save cloth.
    def OnFirstUpdate(self):

        ageStruct = ptAgeInfoStruct()
        ageStruct.setAgeFilename("Personal")

        vault = ptVault()
        ageLinkNode = vault.getOwnedAgeLink(ageStruct)
        if ageLinkNode:
            ageInfoNode = ageLinkNode.getAgeInfo()
            ageInfoChildren = ageInfoNode.getChildNodeRefList()
            for ageInfoChildRef in ageInfoChildren:
                ageInfoChild = ageInfoChildRef.getChild()
                folder = ageInfoChild.upcastToFolderNode()
                if folder and folder.folderGetName() == "AgeData":
                    ageDataFolder = folder
                    ageDataChildren = folder.getChildNodeRefList()
                    for ageDataChildRef in ageDataChildren:
                        ageDataChild = ageDataChildRef.getChild()
                        chron = ageDataChild.upcastToChronicleNode()
                        if chron and chron.getName() == "AhnonayLink":
                            self.link = chron.getValue()
                            break
                    break

        ageVault = ptAgeVault()
        ageInfo = ageVault.getAgeInfo()
        guid = ageInfo.getAgeInstanceGuid()
        ageSDL = PtGetAgeSDL()

        if guid == self.link:
            sphere = ageSDL["ahnyCurrentSphere"][0]
            
            linkMgr = ptNetLinkingMgr()
            curLink = linkMgr.getCurrAgeLink()
            spawnPoint = curLink.getSpawnPoint()

            spTitle = spawnPoint.getTitle()
            spName = spawnPoint.getName()

            if spTitle == "SCSavePoint":
                if spName == "SaveClothPoint7" or spName == "SaveClothPoint8":
                    PtDebugPrint(u"ahnySaveCloth.OnFirstUpdate(): Linking to hub or hut.")
                    self.whereAmI = 4
                else:
                    PtDebugPrint(u"ahnySaveCloth.OnFirstUpdate(): Sphere 0{} loaded with offset: {}.".format(sphere, offset))
                    offset = str(ageSDL["ahnyCurrentOffset"][0])
                    self.whereAmI = (int(sphere) - int(offset)) % 4
                    if self.whereAmI == 0:
                        self.whereAmI = 4
            else:
                self.whereAmI = sphere
            PtDebugPrint(u"ahnySaveCloth.OnFirstUpdate(): I am Age owner in {}.".format(self.whereAmI))

        # SaveCloth SDL stuff, for use with PotS symbols.
        self.sdlSC = "ahnyGotSaveCloth" + ClothID.value
        try:
            ageSDL.setFlags(self.sdlSC, 1, 1)
            ageSDL.sendToClients(self.sdlSC)
            ageSDL.setNotify(self.key, self.sdlSC, 0.0)
            self.gotSC = ageSDL[self.sdlSC][0]
            PtDebugPrint("ahnySaveCloth.OnFirstUpdate(): Found SDL: {}, which = {}.".format(self.sdlSC, self.gotSC))
        except:
            PtDebugPrint("ahnySaveCloth.OnFirstUpdate(): Couldn't find SDL {}, defaulting to 0.".format(self.sdlSC), level=kErrorLevel)

        ageSDL.setFlags("ahnyCurrentSphere", 1, 1)
        ageSDL.sendToClients("ahnyCurrentSphere")
        ageSDL.setNotify(self.key, "ahnyCurrentSphere", 0.0)

        ageSDL.setFlags("ahnyCurrentOffset", 1, 1)
        ageSDL.sendToClients("ahnyCurrentOffset")
        ageSDL.setNotify(self.key, "ahnyCurrentOffset", 0.0)

    ## Called by Plasma when an SDL notify is received.
    # Gets the Ahnonay save cloths that have been obtained.
    def OnSDLNotify(self, varName, sdlName, playerID, tag):

        if varName != self.sdlSC:
            return
        ageSDL = PtGetAgeSDL()
        self.gotSC = ageSDL[self.sdlSC][0]

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Used to handle cloths being pressed.
    def OnNotify(self, state, ID, events):

        if not state:
            return

        if ID == Activator.id:
            self.avatar = PtFindAvatar(events)
            OneShotResp.run(self.key, avatar=PtFindAvatar(events))

        elif ID == OneShotResp.id and self.avatar == PtGetLocalAvatar():
            ageVault = ptAgeVault()
            ageInfo = ageVault.getAgeInfo()
            guid = ageInfo.getAgeInstanceGuid()

            if guid == self.link:
                PtDebugPrint(u"ahnySaveCloth.OnNotify(): Player is the Age owner; setting spawn point.")
                
                ageSDL = PtGetAgeSDL()
                sphere = ageSDL["ahnyCurrentSphere"][0]
                offset = (sphere - self.whereAmI) % 4
                PtDebugPrint(u"ahnySaveCloth.OnNotify(): Offset = {}.".format(offset))
                ageSDL["ahnyCurrentOffset"] = (offset,)

                spawn = None

                ageStruct = ptAgeInfoStruct()
                ageStruct.setAgeFilename("Personal")

                vault = ptVault()
                ageLinkNode = vault.getOwnedAgeLink(ageStruct)
                if ageLinkNode:
                    ageInfoNode = ageLinkNode.getAgeInfo()
                    ageInfoChildren = ageInfoNode.getChildNodeRefList()
                    for ageInfoChildRef in ageInfoChildren:
                        ageInfoChild = ageInfoChildRef.getChild()
                        folder = ageInfoChild.upcastToFolderNode()
                        if folder and folder.folderGetName() == "AgeData":
                            ageDataFolder = folder
                            ageDataChildren = folder.getChildNodeRefList()
                            for ageDataChildRef in ageDataChildren:
                                ageDataChild = ageDataChildRef.getChild()
                                chron = ageDataChild.upcastToChronicleNode()
                                if chron and chron.getName() == "AhnonaySpawnPoints":
                                    spawn = chron.getValue().split(";")
                                    newSpawn = "{};SCSavePoint,SaveClothPoint{}".format(spawn[0], ClothID.value)
                                    PtDebugPrint(u"ahnySaveCloth.OnNotify(): New spawn = {}.".format(newSpawn))
                                    chron.setValue(newSpawn) 
                                    if not self.gotSC:
                                        ageSDL[self.sdlSC] = (1,)
                                    return
                PtDebugPrint(u"ahnySaveCloth.OnNotify(): Couldn't find chronicle node.", level=kErrorLevel)

            else:
                PtDebugPrint(u"ahnySaveCloth.OnNotify(): Player is not the Age owner, cannot do anything.")
        else:
            PtDebugPrint(u"ahnySaveCloth.OnNotify(): Error trying to access the Vault.", level=kErrorLevel)
