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

## @package Ahnonay
# Ahnonay's Age-wide module.
# @date June 2003: Creation.

from Plasma import *
from PlasmaNetConstants import *
from PlasmaTypes import *

from xPsnlVaultSDL import *

## The pages that must be paged in for each sphere.
kSpheres = {
    1: ("Sphere01BuildingInterior", "MaintRoom01", "ahnySphere01"),
    2: ("MaintRoom02", "ahnySphere02"),
    3: ("MaintRoom03", "ahnySphere03"),
    4: ("Vortex", "Hub", "MaintRoom04", "EngineerHut", "ahnySphere04")
}

## The pages corresponding to each of the four spheres.
kSpherePages = {
    "Ahnonay_District_ahnySphere01", "Ahnonay_ahnySphere01",
    "Ahnonay_District_ahnySphere02", "Ahnonay_ahnySphere02",
    "Ahnonay_District_ahnySphere03", "Ahnonay_ahnySphere03",
    "Ahnonay_District_ahnySphere04", "Ahnonay_ahnySphere04"
}


## Ahnonay's responder.
# Manages the paging in and out of the various spheres.
class Ahnonay(ptResponder):

    id = 5399
    version = 1

    ## Initialize Ahnonay's responder.
    def __init__(self):

        PtDebugPrint(u"Ahnonay: Version {}.".format(self.version))
        ptResponder.__init__(self)

    ## Called by Plasma when the Age state has been fully received.
    # Determines where the player is supposed to link to.
    def OnServerInitComplete(self):

        # Initialize age data.
        ageInfo = ptAgeVault().getAgeInfo()
        guid = ageInfo.getAgeInstanceGuid()
        linkID = None
        locked = None
        volatile = None
        spawn = None
        owner = None

        # Get the player's Age settings.
        ageStruct = ptAgeInfoStruct()
        ageStruct.setAgeFilename("Personal")
        ageLinkNode = ptVault().getOwnedAgeLink(ageStruct)
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
                            linkID = chron
                            PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Link Chron already exists: {}.".format(linkID.getValue()), level=kDebugDumpLevel)
                        elif chron and chron.getName() == "AhnonayLocked":
                            locked = chron
                            PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Locked Chron already exists: {}.".format(locked.getValue()), level=kDebugDumpLevel)
                        elif chron and chron.getName() == "AhnonayVolatile":
                            volatile = chron
                            PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Volatile Chron already exists: {}.".format(volatile.getValue()), level=kDebugDumpLevel)
                        elif chron and chron.getName() == "AhnonaySpawnPoints":
                            spawn = chron
                            PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Spawn Chron already exists: {}.".format(spawn.getValue()), level=kDebugDumpLevel)
                        elif chron and chron.getName() == "AhnonayOwner":
                            owner = chron
                    break

        # Determine the player's status.
        myID = str(PtGetClientIDFromAvatarKey(PtGetLocalAvatar().getKey()))
        if not owner:
            PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Player is not the Age owner and doesn't have his own Ahnonay.", level=kDebugDumpLevel)
        elif owner.getValue() == myID:
            # Setup the Age Vault if this is the owner's first visit.
            if not linkID:
                PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Link Chron not found, creating.", level=kDebugDumpLevel)
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName("AhnonayLink")
                newNode.chronicleSetValue(guid)
                ageDataFolder.addNode(newNode)
            if not locked:
                PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Locked Chron not found, creating.", level=kDebugDumpLevel)
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName("AhnonayLocked")
                newNode.chronicleSetValue("1")
                ageDataFolder.addNode(newNode)
            if not volatile:
                PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Volatile Chron not found, creating.", level=kDebugDumpLevel)
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName("AhnonayVolatile")
                newNode.chronicleSetValue("0")
                ageDataFolder.addNode(newNode)
            if not spawn:
                PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Spawn Chron not found, creating.", level=kDebugDumpLevel)
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName("AhnonaySpawnPoints")
                newNode.chronicleSetValue("Default,LinkInPointDefault")
                ageDataFolder.addNode(newNode)
            if volatile and volatile.getValue() == "1" and linkID and guid != linkID.getValue():
                PtDebugPrint(u"Ahnonay.OnServerInitComplete(): New instance of Ahnonay; setting new vars.",
                             level=kDebugDumpLevel)
                linkid.setValue(guid)
                locked.setValue("1")
                volatile.setValue("0")
                spawn.setValue("Default,LinkInPointDefault")
        else:
            PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Player is not the Age owner, but he has his own Ahnonay.",
                         level=kDebugDumpLevel)

        # Set the current sphere.
        ageSDL = PtGetAgeSDL()
        sphere = ageSDL["ahnyCurrentSphere"][0]
        if sphere > 4:
            sphere = 1
            ageSDL["ahnyCurrentSphere"] = (1,)

        # Determine the appropriate sphere for the player.
        link = ptNetLinkingMgr().getCurrAgeLink()
        spawnPoint = link.getSpawnPoint()
        spTitle = spawnPoint.getTitle()
        spName = spawnPoint.getName()
        if spTitle == "SCSavePoint":
            if spName == "SaveClothPoint7" or spName == "SaveClothPoint8":
                PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Linking player to hub or hut.", level=kDebugDumpLevel)
                newSphere = 4
            else:
                offset = str(ageSDL["ahnyCurrentOffset"][0])
                PtDebugPrint(u"Ahnonay.OnServerInitComplete(): Sphere0{} loaded with offset: {}.".format(sphere, offset), level=kDebugDumpLevel)
                newSphere = (int(sphere) - int(offset)) % 4 or 4
        else:
            newSphere = sphere

        # Page in the appropriate sphere.
        for page in kSpheres[newSphere]:
            PtPageInNode(page)

    ## Called by Plasma when a page has been loaded.
    # Warps the player to the appropriate sphere.
    def OnPageLoad(self, what, who):

        PtDebugPrint(u"Ahnonay.OnPageLoad(): what={}; who={}.".format(what, who), level=kDebugDumpLevel)

        # Find out if a sphere page is being loaded; if so warp the avatar to it.
        if what != kLoaded or who not in kSpherePages:
            return
        ageSDL = PtGetAgeSDL()
        sphere = str(ageSDL["ahnyCurrentSphere"][0])
        offset = str(ageSDL["ahnyCurrentOffset"][0])
        PtDebugPrint(u"Ahnonay.OnPageLoad(): Sphere0{} loaded with offset: {}.".format(sphere, offset), level=kDebugDumpLevel)

        # Get the spawn point.
        link = ptNetLinkingMgr().getCurrAgeLink()
        spawnPoint = link.getSpawnPoint()
        spTitle = spawnPoint.getTitle()
        spName = spawnPoint.getName()

        # Warp the avatar to the spawn point's location.
        if spTitle == "SCSavePoint":
            if spName == "SaveClothPoint7" or spName == "SaveClothPoint8":
                PtDebugPrint(u"Ahnonay.OnPageLoad(): Linking player to hub or hut.", level=kDebugDumpLevel)
                newSphere = 4
            else:
                newSphere = (int(sphere) - int(offset)) % 4 or 4
            spawnPoint = spName + str(newSphere)
            PtGetLocalAvatar().physics.warpObj(PtFindSceneobject(spawnPoint, "Ahnonay").getKey())
        else:
            defaultLink = "LinkInPointSphere0%s" % (sphere)
            PtGetLocalAvatar().physics.warpObj(PtFindSceneobject(defaultLink, "Ahnonay").getKey())

    ## Called by Plasma on receipt of a backdoor message.
    # Used to set the current sphere SDL.
    def OnBackdoorMsg(self, target, param):

        ageSDL = PtGetAgeSDL()
        if target == "sphere" and self.sceneobject.isLocallyOwned():
            ageSDL["ahnyCurrentSphere"] = (int(param),)
