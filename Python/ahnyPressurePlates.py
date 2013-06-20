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

## @package ahnyPressurePlates
# The controls for the pressure plates in Ahnonay.
# @author Derek Odell
# @date April 2007: Creation.

from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *

import xLinkingBookDefs
import xRandom

# Define the attributes that will be entered in Max.
Zones = ptAttribActivator(1, "Act: Zone Detectors")
RespClockLights = ptAttribResponderList(2, "Resp: Clock Lights", ("on", "off"), True)
ZoneObjects = ptAttribSceneobjectList(3, "Obj: Zones")
SDLOccupied = ptAttribString(4, "Str: SDL Occupied Zones")
SDLTrees = ptAttribString(5, "Str: SDL Trees (optional)")
BookClickable = ptAttribActivator(6, "Act: Book Clickable")
SeekBehavior = ptAttribBehavior(7, "Beh: Smart Seek To Book")
Sphere = ptAttribDropDownList(8, "Which Sphere?", ("Sphere01", "Sphere02", "Sphere03", "Sphere04"))
RespLinkResponder = ptAttribResponder(9, "Resp: Link To Cathedral")
RespSphereRotate = ptAttribResponder(10, "Resp: Sphere Rotation SFX")

## Establishes the correspondence between the crystal trees and the pressure
# plates they rest on.
kTreeToZoneKey = (1, 3, 4, 5, 8, 9, 10, 12, 13, 15, 16, 18, 21, 22, 24)


## The modifier for the Ahnonay pressure plates.
# Handles everything tied to the pressure plates.
class ahnyPressurePlates(ptModifier):

    id = 5947
    version = 1

    ## Initialize the pressure plates modifier.
    def __init__(self):

        PtDebugPrint(u"ahnyPressurePlates: Version {}.".format(self.version))
        ptModifier.__init__(self)
        self.respLightList = []
        self.objZoneList = []
        self.gLinkingBook = None

    ## Called by Plasma on receipt of the first plEvalMsg.
    # Sets the initial state of the Age's pressure plates.
    def OnFirstUpdate(self):

        ageSDL = PtGetAgeSDL()
        if not ageSDL:
            PtDebugPrint(u"ahnyPressurePlates.OnFirstUpdate(): Cannot find the Ahnonay Age SDL.", level=kErrorLevel)
            return
        try:
            ageSDL[SDLOccupied.value][0]
        except:
            ageSDL[SDLOccupied.value] = tuple([0] * 25)

        ageSDL.setFlags("ahnyCurrentSphere", 1, 1)
        ageSDL.sendToClients("ahnyCurrentSphere")
        ageSDL.setNotify(self.key, "ahnyCurrentSphere", 0.0)

        ageSDL.setFlags(SDLOccupied.value, 1, 1)
        ageSDL.sendToClients(SDLOccupied.value)
        ageSDL.setNotify(self.key, SDLOccupied.value, 0.0)

        if not PtGetPlayerList():
            ageSDL[SDLOccupied.value] = tuple([0] * 25)

        self.respLightList = [l.getName() for l in RespClockLights.value]
        self.objZoneList = [z.getName() for z in ZoneObjects.value]

        if self.respLightList:
            for i, occupants in enumerate(ageSDL[SDLOccupied.value]):
                if occupants:
                    RespClockLights.run(self.key, state="on", objectName=self.respLightList[i])

        if Sphere.value == "Sphere02":
            try:
                ageSDL[SDLTrees.value][0]
            except:
                PtDebugPrint(u"ahnyPressurePlates.OnFirstUpdate(): Cannot find the Ahnonay Age SDL.", level=kErrorLevel)
                ageSDL[SDLTrees.value] = tuple([1] * 15)

            ageSDL.setFlags(SDLTrees.value, 1, 1)
            ageSDL.sendToClients(SDLTrees.value)
            ageSDL.setNotify(self.key, SDLTrees.value, 0.0)

            occupiedZones = ageSDL[SDLOccupied.value]
            occupiedTrees = ageSDL[SDLTrees.value]
            for index in kTreeToZoneKey:
                if occupiedZones[index] == 0 and occupiedTrees[kTreeToZoneKey.index(index)] == 1:
                    RespClockLights.run(self.key, state="on", objectName=self.respLightList[index], netForce=1)
            ageSDL[SDLOccupied.value] = occupiedZones

    ## Called by Plasma when an SDL notify is received.
    # Used to play the rotating sphere SFX.
    def OnSDLNotify(self, varName, sdlName, playerID, tag):

        if varName == "ahnyCurrentSphere" and RespSphereRotate.value:
            PtDebugPrint(u"ahnyPressurePlates.OnSDLNotify(): Playing sphere rotation SFX.")
            RespSphereRotate.run(self.key)

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Handles the linking book, as well as entering and leaving regions.
    def OnNotify(self, state, ID, events):

        ageSDL = PtGetAgeSDL()
        if ID == Zones.id:
            for event in events:
                if event[0] == kCollisionEvent and self.sceneobject.isLocallyOwned():
                    region = event[3]
                    regName = region.getName()
                    for zone in ZoneObjects.value:
                        zoneName = zone.getName()
                        if zoneName == regName:
                            index = self.objZoneList.index(zoneName)
                            occupiedZones = list(ageSDL[SDLOccupied.value])
                            # Is the player entering?
                            if event[1] == 1:
                                if occupiedZones[index] < 255:  # Avoid overflow.
                                    occupiedZones[index] += 1
                                # If equal to one, run the responder.
                                if self.respLightList and occupiedZones[index] == 1:
                                    RespClockLights.run(self.key, state="on", objectName=self.respLightList[index], netForce=1)
                                PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Entering {:02d}. Occupied zones: {}.".format(index, occupiedZones))
                            # Otherwise, the player is exiting.
                            else:
                                if occupiedZones[index] > 0: # Avoid overflow.
                                    occupiedZones[index] -= 1
                                if Sphere.value == "Sphere02" and index in kTreeToZoneKey:
                                    if not ageSDL[SDLTrees.value][kTreeToZoneKey.index(index)] and occupiedZones[index] == 0 and self.respLightList:
                                        RespClockLights.run(self.key, state="off", objectName=self.respLightList[index], netForce=1)
                                elif self.respLightList and occupiedZones[index] == 0:
                                    RespClockLights.run(self.key, state="off", objectName=self.respLightList[index], netForce=1)
                                PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Exiting {:02d}. Occupied zones: {}.".format(index, occupiedZones))
                            ageSDL[SDLOccupied.value] = tuple(occupiedZones)

        # Is it a clickable book on a pedestal?
        elif ID == BookClickable.id and PtFindAvatar(events) == PtGetLocalAvatar() and state:
            PtToggleAvatarClickability(False)
            BookClickable.disable()
            SeekBehavior.run(PtFindAvatar(events))

        # Is it the seek behavior because we clicked on a book ourself?    
        elif ID == SeekBehavior.id and PtFindAvatar(events) == PtGetLocalAvatar():
            for event in events:
                # Is smart seek completed?
                if event[0] == kMultiStageEvent and event[2] == kEnterStage:
                    # Exit multistage, and show GUI.
                    SeekBehavior.gotoStage(PtGetLocalAvatar(), -1) 
                    try:
                        params = xLinkingBookDefs.xAgeLinkingBooks["AhnonayCathedral"]
                        if len(params) == 6:
                            sharable, width, height, stampdef, bookdef, gui = params
                        elif len(params) == 5:
                            sharable, width, height, stampdef, bookdef = params
                            gui = "BkBook"
                        else:
                            continue

                        PtSendKIMessage(kDisableKIandBB, 0)
                        bookdef = bookdef.replace("%s", "")
                        self.gLinkingBook = ptBook(bookdef, self.key)
                        self.gLinkingBook.setSize(width, height)
                        self.gLinkingBook.setGUI(gui)
                        self.gLinkingBook.show(True)
                    except LookupError:
                        PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Could not find Age AhnonayCathedral's linking panel.", level=kErrorLevel)

        else:
            for event in events:
                # Since there's only one book to worry about, is it from the open book?
                if event[0] == PtEventType.kBook:
                    PtDebugPrint(u"ahnyPressurePlates.OnNotify(): BookNotify event={0[1]}, id={0[2]}.".format(event), level=kDebugDumpLevel)
                    if event[1] == PtBookEventTypes.kNotifyImageLink:
                        if event[2] >= xLinkingBookDefs.kFirstLinkPanelID or event[2] == xLinkingBookDefs.kBookMarkID:
                            PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Linking Book panel {} hit.".format(event[2]))
                            PtToggleAvatarClickability(True)  # Enable player as clickable.
                            if self.gLinkingBook:
                                self.gLinkingBook.hide()
                            PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Occupied value: {}.".format(ageSDL[SDLOccupied.value]))
                            if self._AreRegionsEmpty():
                                PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Sphere is rotating.")
                                currentSphere = ageSDL["ahnyCurrentSphere"][0]
                                if currentSphere in {3, 4}:
                                    ageSDL["ahnyCurrentSphere"] = (1,)
                                else:
                                    ageSDL["ahnyCurrentSphere"] = ((currentSphere + 1),)
                            else:
                                PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Sphere is staying put.")

                            RespLinkResponder.run(self.key, avatar=PtGetLocalAvatar(), netPropagate=False)
                    elif event[1] == PtBookEventTypes.kNotifyShow:
                        PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Book: NotifyShow.")
                        PtSendKIMessage(kEnableKIandBB, 0)

                    elif event[1] == PtBookEventTypes.kNotifyHide:
                        PtDebugPrint(u"ahnyPressurePlates.OnNotify(): Book: NotifyHide.")
                        PtToggleAvatarClickability(True)
                        BookClickable.enable()

    ## Checks if all regions are empty.
    # On Sphere01, it checks for quabs; on Sphere02, it checks for trees. On
    # all spheres, it checks for other people.
    def _AreRegionsEmpty(self):

        ageSDL = PtGetAgeSDL()
        occupantList = ageSDL[SDLOccupied.value]
        if any(occupantList[1:]):
            PtDebugPrint(u"ahnyPressurePlates._AreRegionsEmpty(): Some zones are still occupied.")
            return False
        elif Sphere.value == "Sphere01" and ageSDL["ahnyQuabs"][0]:
            PtDebugPrint(u"ahnyPressurePlates._AreRegionsEmpty(): Not all quabs were kicked off.")
            return False
        elif Sphere.value == "Sphere02":
            treeList = ageSDL[SDLTrees.value]
            if any(treeList):
                PtDebugPrint(u"ahnyPressurePlates._AreRegionsEmpty(): Not all quabs were knocked over.")
                return False
        elif occupantList[0] != 1:
            PtDebugPrint(u"ahnyPressurePlates._AreRegionsEmpty(): Book zone still occupied.")
            return False
        return True
