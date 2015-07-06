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
"""
Module: ahnySaveCloth
Age: Most post-prime ages
Date: January 2004
Author: Adam Van Ornum
Sets a save point
"""

from Plasma import *
from PlasmaTypes import *

# Define the attributes that will be entered in Max.
Activator = ptAttribActivator(1, "Activator: Cloth Clickable")
OneShotResp = ptAttribResponder(2, "Resp: One Shot")
clothID = ptAttribString(3, "save cloth ID")


class ahnySaveCloth(ptModifier):

    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5424
        self.version = 1
        PtDebugPrint("ahnySaveCloth: v.".format(self.version), level=kWarningLevel)

        self.avatar = None
        self.gotSC = 0
        self.sdlSC = ""
        self.link = None
        self.whereAmI = 0

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
                    ageDataChildren = folder.getChildNodeRefList()
                    for ageDataChildRef in ageDataChildren:
                        ageDataChild = ageDataChildRef.getChild()
                        chron = ageDataChild.upcastToChronicleNode()
                        if chron and chron.getName() == "AhnonayLink":
                            self.link = chron.getValue()

        ageSDL = PtGetAgeSDL()
        agevault = ptAgeVault()
        ageinfo = agevault.getAgeInfo()
        guid = ageinfo.getAgeInstanceGuid()

        if guid == self.link:
            sphere = ageSDL["ahnyCurrentSphere"][0]
            
            linkmgr = ptNetLinkingMgr()
            curLink = linkmgr.getCurrAgeLink()
            spawnPoint = curLink.getSpawnPoint()

            spTitle = spawnPoint.getTitle()
            spName = spawnPoint.getName()

            if spTitle == "SCSavePoint":
                if spName == "SaveClothPoint7" or spName == "SaveClothPoint8":
                    PtDebugPrint("ahnySaveCloth.OnFirstUpdate(): Linking to hub or hut.", level=kWarningLevel)
                    self.whereAmI = 4
                else:
                    offset = str(ageSDL["ahnyCurrentOffset"][0])
                    PtDebugPrint("ahnySaveCloth.OnFirstUpdate(): Sphere0{} loaded with offset: {}.".format(sphere, offset), level=kWarningLevel)
                    self.whereAmI = (sphere - offset) % 4
                    if self.whereAmI == 0:
                        self.whereAmI = 4
            else:
                self.whereAmI = sphere
            PtDebugPrint("ahnySaveCloth.OnFirstUpdate(): I am age owner in {}.".format(self.whereAmI), level=kWarningLevel)

        # SaveCloth SDL stuff, for use with POTS symbols
        self.sdlSC = "ahnyGotSaveCloth" + clothID.value
        try:
            ageSDL.setFlags(self.sdlSC, 1, 1)
            ageSDL.sendToClients(self.sdlSC)
            ageSDL.setNotify(self.key, self.sdlSC, 0.0)
            self.gotSC = ageSDL[self.sdlSC][0]
            PtDebugPrint("ahnySaveCloth.OnFirstUpdate(): Found SDL: {}, which = {}.".format(self.sdlSC, self.gotSC), level=kDebugDumpLevel)
        except:
            PtDebugPrint("ahnySaveCloth.OnFirstUpdate(): Couldn't find SDL: {}, defaulting to 0".format(self.sdlSC), level=kErrorLevel)

        ageSDL.setFlags("ahnyCurrentSphere", 1, 1)
        ageSDL.sendToClients("ahnyCurrentSphere")
        ageSDL.setNotify(self.key, "ahnyCurrentSphere", 0.0)

        ageSDL.setFlags("ahnyCurrentOffset", 1, 1)
        ageSDL.sendToClients("ahnyCurrentOffset")
        ageSDL.setNotify(self.key, "ahnyCurrentOffset", 0.0)

    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if VARname != self.sdlSC:
            return
        ageSDL = PtGetAgeSDL()
        PtDebugPrint("ahnySaveCloth.OnSDLNotify(): VARname: {}, SDLname: {}, tag: {}, value: {}".format(VARname, SDLname, tag, ageSDL[self.sdlSC][0]), level=kDebugDumpLevel)
        self.gotSC = ageSDL[self.sdlSC][0]

    def OnNotify(self, state, id, events):
        if not state:
            return

        if id == Activator.id:
            self.avatar = PtFindAvatar(events)
            OneShotResp.run(self.key, avatar=self.avatar)  # Run the oneshot

        elif id == OneShotResp.id and self.avatar == PtGetLocalAvatar():
            agevault = ptAgeVault()
            ageinfo = agevault.getAgeInfo()
            guid = ageinfo.getAgeInstanceGuid()

            if guid == self.link:
                PtDebugPrint("ahnySaveCloth.OnNotify(): I'm the age owner, setting spawnpoint.", level=kDebugDumpLevel)

                ageSDL = PtGetAgeSDL()
                sphere = ageSDL["ahnyCurrentSphere"][0]
                offset = (sphere - self.whereAmI) % 4
                PtDebugPrint("ahnySaveCloth.OnNotify(): Offset = {}".format(offset), level=kDebugDumpLevel)
                ageSDL["ahnyCurrentOffset"] = (offset,)

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
                            ageDataChildren = folder.getChildNodeRefList()
                            for ageDataChildRef in ageDataChildren:
                                ageDataChild = ageDataChildRef.getChild()
                                chron = ageDataChild.upcastToChronicleNode()
                                if chron and chron.getName() == "AhnonaySpawnPoints":
                                    spawn = chron.getValue().split(";")
                                    newSpawn = "{};SCSavePoint,SaveClothPoint{}".format(spawn[0], clothID.value)
                                    chron.setValue(newSpawn)
                                    if not self.gotSC:
                                        ageSDL = PtGetAgeSDL()
                                        ageSDL[self.sdlSC] = (1,)
                                    return

                PtDebugPrint("ahnySaveCloth.OnNotify(): Couldn't find chron node.", level=kErrorLevel)
            else:
                PtDebugPrint("ahnySaveCloth.OnNotify(): I'm not the age owner, so I don't do anything.", level=kDebugDumpLevel)
        else:
            PtDebugPrint("ahnySaveCloth.OnNotify(): Error trying to access the Vault.", level=kErrorLevel)
