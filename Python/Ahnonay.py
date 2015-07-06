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
Module: Ahnonay.py
Age: Ahnonay
Date: June 2003
"""

from Plasma import *
from PlasmaTypes import *

kSpherePages = {"Ahnonay_District_ahnySphere01",
                "Ahnonay_District_ahnySphere02",
                "Ahnonay_District_ahnySphere03",
                "Ahnonay_District_ahnySphere04",
                "Ahnonay_ahnySphere01",
                "Ahnonay_ahnySphere02",
                "Ahnonay_ahnySphere03",
                "Ahnonay_ahnySphere04"}


class Ahnonay(ptResponder):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5399
        self.version = 1
        PtDebugPrint("Ahnonay: v{}".format(self.version), level=kWarningLevel)

    def OnServerInitComplete(self):
        agevault = ptAgeVault()
        ageinfo = agevault.getAgeInfo()
        guid = ageinfo.getAgeInstanceGuid()
        linkid = None
        locked = None
        volatile = None
        spawn = None
        owner = None
        myID = str(PtGetClientIDFromAvatarKey(PtGetLocalAvatar().getKey()))

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
                            linkid = chron
                            PtDebugPrint("Ahnonay.OnServerInitComplete(): Link Chron already exists: {}".format(linkid.getValue()), level=kDebugDumpLevel)
                        elif chron and chron.getName() == "AhnonayLocked":
                            locked = chron
                            PtDebugPrint("Ahnonay.OnServerInitComplete(): Locked Chron already exists: {}".format(locked.getValue()), level=kDebugDumpLevel)
                        elif chron and chron.getName() == "AhnonayVolatile":
                            volatile = chron
                            PtDebugPrint("Ahnonay.OnServerInitComplete(): Volatile Chron already exists: {}".format(volatile.getValue()), level=kDebugDumpLevel)
                        elif chron and chron.getName() == "AhnonaySpawnPoints":
                            spawn = chron
                            PtDebugPrint("Ahnonay.OnServerInitComplete(): Spawn Chron already exists: {}".format(spawn.getValue()), level=kDebugDumpLevel)
                        elif chron and chron.getName() == "AhnonayOwner":
                            owner = chron
                    break

        if owner is None:
            PtDebugPrint("I am not the age owner, and I don't have my own Ahnonay", level=kWarningLevel)
            
        elif owner.getValue() == myID:
            if linkid is None:
                PtDebugPrint("Ahnonay.OnServerInitComplete(): Link Chron not found, creating", level=kWarningLevel)
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName("AhnonayLink")
                newNode.chronicleSetValue(guid)
                ageDataFolder.addNode(newNode)

            if locked is None:
                PtDebugPrint("Ahnonay.OnServerInitComplete(): Locked Chron not found, creating", level=kWarningLevel)
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName("AhnonayLocked")
                newNode.chronicleSetValue("1")
                ageDataFolder.addNode(newNode)

            if volatile is None:
                PtDebugPrint("Ahnonay.OnServerInitComplete(): Volatile Chron not found, creating", level=kWarningLevel)
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName("AhnonayVolatile")
                newNode.chronicleSetValue("0")
                ageDataFolder.addNode(newNode)

            if spawn is None:
                PtDebugPrint("Ahnonay.OnServerInitComplete(): Spawn Chron not found, creating", level=kWarningLevel)
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName("AhnonaySpawnPoints")
                newNode.chronicleSetValue("Default,LinkInPointDefault")
                ageDataFolder.addNode(newNode)

            if volatile and linkid:
                if volatile.getValue() == "1" and guid != linkid.getValue():
                    PtDebugPrint("Ahnonay.OnServerInitComplete(): In a new instance of Ahnonay so setting new vars", level=kWarningLevel)
                    linkid.setValue(guid)
                    locked.setValue("1")
                    volatile.setValue("0")
                    spawn.setValue("Default,LinkInPointDefault")
        else:
            PtDebugPrint("I am not the age owner, but I do have my own Ahnonay", level=kWarningLevel)

        ageSDL = PtGetAgeSDL()
        sphere = ageSDL["ahnyCurrentSphere"][0]
        
        if sphere > 4:
            sphere = 1
            ageSDL["ahnyCurrentSphere"] = (1,)
        
        linkmgr = ptNetLinkingMgr()
        link = linkmgr.getCurrAgeLink()
        spawnPoint = link.getSpawnPoint()

        spTitle = spawnPoint.getTitle()
        spName = spawnPoint.getName()

        if spTitle == "SCSavePoint":
            if spName == "SaveClothPoint7" or spName == "SaveClothPoint8":
                PtDebugPrint("Ahnonay.OnServerInitComplete(): Linking to hub or hut.", level=kWarningLevel)
                newSphere = 4
            else:
                offset = ageSDL["ahnyCurrentOffset"][0]
                PtDebugPrint("Ahnonay.OnPageLoad(): Sphere0{} loaded with offset: {}".format(sphere, offset), level=kWarningLevel)
                newSphere = (sphere - offset) % 4
                if newSphere == 0:
                    newSphere = 4
        else:
            newSphere = sphere
            
        if newSphere == 1:
            PtPageInNode("Sphere01BuildingInterior")
            PtPageInNode("MaintRoom01")
            PtPageInNode("ahnySphere01")
        elif newSphere == 2:
            PtPageInNode("MaintRoom02")
            PtPageInNode("ahnySphere02")
        elif newSphere == 3:
            PtPageInNode("MaintRoom03")
            PtPageInNode("ahnySphere03")
        elif newSphere == 4:
            PtPageInNode("Vortex")
            PtPageInNode("Hub")
            PtPageInNode("MaintRoom04")
            PtPageInNode("EngineerHut")
            PtPageInNode("ahnySphere04")

    def OnPageLoad(self, what, who):
        PtDebugPrint("Ahnonay.OnPageLoad(): what={} who={}".format(what, who), level=kDebugDumpLevel)

        if what == kLoaded:
            if who in kSpherePages: 
                ageSDL = PtGetAgeSDL()
                sphere = ageSDL["ahnyCurrentSphere"][0]
                offset = ageSDL["ahnyCurrentOffset"][0]
                PtDebugPrint("Ahnonay.OnPageLoad(): Sphere0{} loaded with offset: {}".format(sphere, offset), level=kWarningLevel)
                
                linkmgr = ptNetLinkingMgr()
                link = linkmgr.getCurrAgeLink()
                spawnPoint = link.getSpawnPoint()

                spTitle = spawnPoint.getTitle()
                spName = spawnPoint.getName()

                if spTitle == "SCSavePoint":
                    if spName == "SaveClothPoint7" or spName == "SaveClothPoint8":
                        PtDebugPrint("Ahnonay.OnPageLoad(): Linking to hub or hut.", level=kWarningLevel)
                        newSphere = 4
                    else:
                        newSphere = (sphere - offset) % 4
                        if newSphere == 0:
                            newSphere = 4
                    spawnPoint = spName + str(newSphere)
                    PtGetLocalAvatar().physics.warpObj(PtFindSceneobject(spawnPoint, "Ahnonay").getKey())
                else:
                    defaultLink = "LinkInPointSphere0{}".format(sphere)
                    PtGetLocalAvatar().physics.warpObj(PtFindSceneobject(defaultLink, "Ahnonay").getKey())

    def OnBackdoorMsg(self, target, param):
        ageSDL = PtGetAgeSDL()
        if target == "sphere":
            if self.sceneobject.isLocallyOwned():
                ageSDL["ahnyCurrentSphere"] = (int(param),)
