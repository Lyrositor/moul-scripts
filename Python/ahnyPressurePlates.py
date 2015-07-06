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
Module: ahnyPressurePlates
Age: Ahnonay
Date: April, 2007
Author: Derek Odell
Ahnonay Quab control
"""

from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import xLinkingBookDefs

# Define the attributes that will be entered in Max.
zones = ptAttribActivator(1, "act: Zone Detectors")
respClockLights = ptAttribResponderList(2, "resp: Clock Lights", statelist=["on", "off"], byObject=1)
zoneObjects = ptAttribSceneobjectList(3, "obj: Zones")
SDLOccupied = ptAttribString(4, "str: SDL Occupied Zones")
SDLTrees = ptAttribString(5, "str: SDL Trees (optional)")
bookClickable = ptAttribActivator(6, "act: Book Clickable")
SeekBehavior = ptAttribBehavior(7, "beh: Smart Seek To Book")
Sphere = ptAttribDropDownList(8, "Which Sphere?", ("Sphere01", "Sphere02", "Sphere03", "Sphere04"))
respLinkResponder = ptAttribResponder(9, "resp: Link To Cathedral")
respSphereRotate = ptAttribResponder(10, "resp: Sphere Rotation SFX")

kTreeToZoneKey = (1, 3, 4, 5, 8, 9, 10, 12, 13, 15, 16, 18, 21, 22, 24)


class ahnyPressurePlates(ptModifier):

    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5947
        self.version = 1
        PtDebugPrint("ahnyPressurePlates: v{}".format(self.version), level=kWarningLevel)

        self.linkingBook = None
        self.localAvatar = None
        self.objZoneList = []
        self.respLightList = []

    def OnFirstUpdate(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            PtDebugPrint("ahnyPressurePlates.OnFirstUpdate(): Cannot find the Ahnonay Age SDL.", level=kErrorLevel)
            ageSDL[SDLOccupied.value] = (0,)*25

        ageSDL.setFlags("ahnyCurrentSphere", 1, 1)
        ageSDL.sendToClients("ahnyCurrentSphere")
        ageSDL.setNotify(self.key, "ahnyCurrentSphere", 0.0)

        ageSDL.setFlags(SDLOccupied.value, 1, 1)
        ageSDL.sendToClients(SDLOccupied.value)
        ageSDL.setNotify(self.key, SDLOccupied.value, 0.0)

        if not len(PtGetPlayerList()):
            ageSDL[SDLOccupied.value] = (0,)*25

        for light in respClockLights.value:
            thisLight = light.getName()
            self.respLightList.append(thisLight)

        for zone in zoneObjects.value:
            thisZone = zone.getName()
            self.objZoneList.append(thisZone)

        if self.respLightList:
            for idx, occupants in enumerate(ageSDL[SDLOccupied.value]):
                if occupants:
                    respClockLights.run(self.key, state="on", objectName=self.respLightList[idx])
        if Sphere.value == "Sphere02":
            try:
                ageSDL[SDLTrees.value][0]
            except:
                PtDebugPrint("ahnyPressurePlates.OnFirstUpdate(): Cannot find the Ahnonay Age SDL.", level=kErrorLevel)
                ageSDL[SDLTrees.value] = (1,)*15

            ageSDL.setFlags(SDLTrees.value, 1, 1)
            ageSDL.sendToClients(SDLTrees.value)
            ageSDL.setNotify(self.key, SDLTrees.value, 0.0)

            occupiedZones = list(ageSDL[SDLOccupied.value])
            occupiedTrees = list(ageSDL[SDLTrees.value])
            for index in kTreeToZoneKey:
                if occupiedZones[index] == 0 and occupiedTrees[kTreeToZoneKey.index(index)] == 1:
                    respClockLights.run(self.key, state="on", objectName=self.respLightList[index], netForce=1)
            ageSDL[SDLOccupied.value] = tuple(occupiedZones)

    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if VARname == "ahnyCurrentSphere" and respSphereRotate.value != []:
            PtDebugPrint("ahnyPressurePlates.OnSDLNotify(): Playing audio SFX.", level=kDebugDumpLevel)
            respSphereRotate.run(self.key)

    def OnNotify(self, state, id, events):
        ageSDL = PtGetAgeSDL()

        if id == zones.id:
            for event in events:
                if (event[0] == kCollisionEvent) and self.sceneobject.isLocallyOwned():
                    region = event[3]
                    regName = region.getName()
                    for zone in zoneObjects.value:
                        zoneName = zone.getName()
                        if zoneName == regName:
                            index = self.objZoneList.index(zoneName)
                            occupiedZones = list(ageSDL[SDLOccupied.value])
                            if event[1] == 1:  # We are entering
                                if occupiedZones[index] != 255:  # Avoid overflow
                                    occupiedZones[index] += 1
                                if self.respLightList != [] and occupiedZones[index] == 1:  # If we are now equal to one run the responder
                                    respClockLights.run(self.key, state="on", objectName=self.respLightList[index], netForce=1)
                                PtDebugPrint("ahnyPressurePlates.OnNotify(): {} - enter {}".format(occupiedZones, index), level=kDebugDumpLevel)
                            else:  # This should be exiting
                                if occupiedZones[index] != 0:  # Only subtract if we are not zero don't want to overflow
                                    occupiedZones[index] -= 1
                                if Sphere.value == "Sphere02" and index in kTreeToZoneKey:
                                    if (not ageSDL[SDLTrees.value][kTreeToZoneKey.index(index)]) and occupiedZones[index] == 0:
                                        if self.respLightList:
                                            respClockLights.run(self.key, state="off", objectName=self.respLightList[index], netForce=1)
                                else:

                                    if self.respLightList != [] and occupiedZones[index] == 0:
                                        respClockLights.run(self.key, state="off", objectName=self.respLightList[index], netForce=1)
                                PtDebugPrint("ahnyPressurePlates.OnNotify(): {} - exit {}".format(occupiedZones, index), level=kDebugDumpLevel)
                            ageSDL[SDLOccupied.value] = tuple(occupiedZones)

        # Is it a clickable book on a pedestal?
        elif id == bookClickable.id and PtFindAvatar(events) == PtGetLocalAvatar() and state:
            PtToggleAvatarClickability(False)
            bookClickable.disable()
            self.localAvatar = PtFindAvatar(events)
            SeekBehavior.run(self.localAvatar)

        # Is it the seek behavior because we clicked on a book ourself?
        elif id == SeekBehavior.id and PtFindAvatar(events) == PtGetLocalAvatar():
            for event in events:
                # Smart seek completed. Exit multistage, and show GUI.
                if event[0] == kMultiStageEvent and event[2] == kEnterStage:
                    SeekBehavior.gotoStage(self.localAvatar, -1)
                    self.ShowBook()

        else:
            for event in events:
                # Is it from the OpenBook? (we only have one book to worry about)
                if event[0] == PtEventType.kBook:
                    PtDebugPrint("ahnyPressurePlates.OnNotify(): BookNotify event={}, id={}".format(event[1], event[2]), level=kDebugDumpLevel)
                    if event[1] == PtBookEventTypes.kNotifyImageLink:
                        if event[2] >= xLinkingBookDefs.kFirstLinkPanelID or event[2] == xLinkingBookDefs.kBookMarkID:
                            PtDebugPrint("ahnyPressurePlates.OnNotify(): Book, hit linking panel {}.".format(event[2]), level=kDebugDumpLevel)
                            self.HideBook()

                            if self.RegionsEmpty():
                                PtDebugPrint("ahnyPressurePlates.OnNotify(): Sphere rotating.", level=kWarningLevel)
                                currentSphere = ageSDL["ahnyCurrentSphere"][0]
                                if currentSphere == 3 or currentSphere == 4:
                                    ageSDL["ahnyCurrentSphere"] = (1,)
                                else:
                                    ageSDL["ahnyCurrentSphere"] = ((currentSphere + 1),)
                            else:
                                PtDebugPrint("ahnyPressurePlates.OnNotify(): Sphere staying put", level=kWarningLevel)

                            respLinkResponder.run(self.key, avatar=PtGetLocalAvatar(), netPropagate=0)

                    elif event[1] == PtBookEventTypes.kNotifyShow:
                        PtDebugPrint("ahnyPressurePlates.OnNotify(): Book, NotifyShow", level=kDebugDumpLevel)
                        PtSendKIMessage(kEnableKIandBB, 0)

                    elif event[1] == PtBookEventTypes.kNotifyHide:
                        PtDebugPrint("ahnyPressurePlates.OnNotify(): Book, NotifyHide", level=kDebugDumpLevel)
                        PtToggleAvatarClickability(True)
                        bookClickable.enable()

    def RegionsEmpty(self):
        ageSDL = PtGetAgeSDL()
        occupantList = list(ageSDL[SDLOccupied.value])

        if Sphere.value == "Sphere01":
            quabs = ageSDL["ahnyQuabs"][0]
            if quabs:
                PtDebugPrint("ahnyPressurePlates.RegionsEmpty(): Not all quabs kicked off.", level=kDebugDumpLevel)
                return False
        elif Sphere.value == "Sphere02":
            treeList = list(ageSDL[SDLTrees.value])
            for tree in treeList:
                if tree:
                    PtDebugPrint("ahnyPressurePlates.RegionsEmpty(): Not all trees knocked over.", level=kDebugDumpLevel)
                    return False

        for zone in occupantList[1:]:
            if zone:
                PtDebugPrint("ahnyPressurePlates.RegionsEmpty(): Some zones still occupied.", level=kDebugDumpLevel)
                return False

        if occupantList[0] == 1:
            return True

        PtDebugPrint("ahnyPressurePlates.RegionsEmpty(): Book zone still occupied.", level=kDebugDumpLevel)
        return False

    def ShowBook(self):
        try:
            params = xLinkingBookDefs.xAgeLinkingBooks["AhnonayCathedral"]

            sharable, width, height, stampdef, bookdef = params[:5]
            if len(params) == 6:
                gui = params[5]
            elif len(params) == 5:
                gui = "BkBook"
            else:
                return

            PtSendKIMessage(kDisableKIandBB, 0)
            bookdef = bookdef.replace("%s", "")
            self.linkingBook = ptBook(bookdef, self.key)
            self.linkingBook.setSize(width, height)
            self.linkingBook.setGUI(gui)
            self.linkingBook.show(1)

        except LookupError:
            PtDebugPrint("ahnyPressurePlates.ShowBook(): Could not find age AhnonayCathedral's linking panel.", level=kErrorLevel)

    def HideBook(self):
        PtToggleAvatarClickability(True)  # enable me as clickable
        if self.linkingBook:
            self.linkingBook.hide()
