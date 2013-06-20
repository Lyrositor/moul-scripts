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

## @package ahnyMaintRoom.py
# Ahnonay's maintenance room code.
# @date April 2004: Creation.

from Plasma import *
from PlasmaTypes import *

from xPsnlVaultSDL import *

# Define the attributes that will be entered in Max.
SphereNum = ptAttribInt(1, "Sphere #")
ActAdvanceSwitch = ptAttribActivator(2, "Clk: advance spheres switch")
RespAdvanceBeh = ptAttribResponder(3, "Resp: advance spheres beh")
RespAdvanceUse = ptAttribResponder(4, "Resp: advance spheres use", ("down0", "up", "down1", "down2", "down3"))
RespHubDoor = ptAttribResponder(5, "Resp: hub door (sphere 4 only!)", ("close", "open"))


## The responder for the maintenance room.
# Manages the state of the rooms according to the sphere rotation.
class ahnyMaintRoom(ptResponder):

    id = 5581
    version = 2

    ## Initialize the maintenance room responder.
    def __init__(self):

        PtDebugPrint(u"ahnyMaintRoom: Version {}.".format(self.version))
        ptResponder.__init__(self)
        self.boolHubDoor = False
        self.actingAvatar = None
        self.diffSphere = 0

    ## Called by Plasma on receipt of the first plEvalMsg.
    # Sets the state of the maintenance room.
    def OnFirstUpdate(self):

        ageSDL = PtGetAgeSDL()
        if not ageSDL:  # This should never happen, but we don't trust eap.
            PtDebugPrint(u"ahnyMaintRoom.OnFirstUpdate(): Cannot find the Ahnonay Age SDL.", level=kErrorLevel)
            return

        ageSDL.setFlags("ahnyHubDoor", 1, 1)
        ageSDL.sendToClients("ahnyHubDoor")
        ageSDL.setNotify(self.key, "ahnyHubDoor", 0.0)
        
        ageSDL.setFlags("ahnyImagerSphere", 1, 1)
        ageSDL.sendToClients("ahnyImagerSphere")
        ageSDL.setNotify(self.key, "ahnyImagerSphere", 0.0)

        ageSDL.setFlags("ahnyCurrentSphere", 1, 1)
        ageSDL.sendToClients("ahnyCurrentSphere")
        ageSDL.setNotify(self.key, "ahnyCurrentSphere", 0.0)
        
        self.boolHubDoor = ageSDL["ahnyHubDoor"][0]
        sphere = ageSDL["ahnyCurrentSphere"][0]
        ageSDL["ahnyImagerSphere"] = (sphere,)

        if SphereNum.value == 4:
            if sphere == 4 and not self.boolHubDoor:
                self.boolHubDoor = True
                ageSDL["ahnyHubDoor"] = (1,)
            elif self.boolHubDoor:
                self.boolHubDoor = False
                ageSDL["ahnyHubDoor"] = (0,)
            RespHubDoor.run(self.key, state="open" if sphere == 4 else "close", fastforward=1)
            RespAdvanceUse.run(self.key, state="down0", fastforward=1)
        elif SphereNum.value not in {1, 2, 3}:
            PtDebugPrint(u"ahnyMaintRoom.OnFirstUpdate(): Invalid sphere number set in component. Disabling clickable.", level=kErrorLevel)
            ActAdvanceSwitch.disableActivator()

        self._SetSphereDifference()

    ## Called by Plasma when a timer is over.
    # Used to manage the state of the door.
    def OnTimer(self, ID):

        ageSDL = PtGetAgeSDL()
        if ID == 1:
            PtAtTimeCallback(self.key, 0, 2)
            if self.actingAvatar == PtGetLocalAvatar():
                ageSDL["ahnyCurrentSphere"] = (SphereNum.value,)
                PtDebugPrint(u"ahnyMaintRoom.OnTimer(): Advanced from sphere {} to sphere {} with maintenance button.".format(ageSDL["ahnyCurrentSphere"][0], SphereNum.value))
                if SphereNum.value == 4:
                    ageSDL["ahnyImagerSphere"] = (SphereNum.value,)
                    self.boolHubDoor = ageSDL["ahnyHubDoor"][0]
                    if self.boolHubDoor and ageSDL["ahnyCurrentSphere"][0] != 4:
                        PtDebugPrint(u"ahnyMaintRoom.OnTimer(): Door is open and the player isn't going to sphere 4, so closing it.")
                        ageSDL["ahnyHubDoor"] = (0,)
                    elif not self.boolHubDoor and ageSDL["ahnyCurrentSphere"][0] == 4:
                        PtDebugPrint(u"ahnyMaintRoom.OnTimer(): Door is not open and we're going to sphere 4, so opening it.")

        elif ID == 2:
            ActAdvanceSwitch.enableActivator()
            if SphereNum.value == 4:
                ageSDL["ahnyHubDoor"] = (1,)

    ## Called by Plasma when an SDL notify is received.
    # Used to toggle the door SDL setting.
    def OnSDLNotify(self, varName, sdlName, playerID, tag):

        if SphereNum.value == 4:
            ageSDL = PtGetAgeSDL()
            if varName == "ahnyHubDoor":
                self.boolHubDoor = ageSDL["ahnyHubDoor"][0]
                RespHubDoor.run(self.key, state="open" if self.boolHubDoor else "close")
            elif VARname == "ahnyCurrentSphere":
                self.boolHubDoor = ageSDL["ahnyHubDoor"][0]
                if self.boolHubDoor and ageSDL["ahnyCurrentSphere"][0] != 4:
                    PtDebugPrint(u"ahnyMaintRoom.OnSDLNotify(): Door is open and the player isn't going to sphere 4, so closing it.")
                    ageSDL["ahnyHubDoor"] = (0,)
                elif not self.boolHubDoor and ageSDL["ahnyCurrentSphere"][0] == 4:
                    PtDebugPrint(u"ahnyMaintRoom.OnSDLNotify(): Door is not open and we're going to sphere 4, so opening it.")
                    PtAtTimeCallback(self.key, 7, 2)
        if varName == "ahnyCurrentSphere":
            self._SetSphereDifference()

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Handles the effects of rotated spheres.
    def OnNotify(self, state, ID, events):

        if ID == ActAdvanceSwitch.id and state:
            self.actingAvatar = PtFindAvatar(events)
            RespAdvanceBeh.run(self.key, avatar=PtFindAvatar(events))
        
        elif ID == RespAdvanceBeh.id:
            RespAdvanceUse.run(self.key, state="up")

        elif ID == RespAdvanceUse.id:
            if self.diffSphere == 0:
                RespAdvanceUse.run(self.key, state="down0")
                self._SetSphereDifference()
            else:
                if self.diffSphere == 1:
                    RespAdvanceUse.run(self.key, state="down1")
                    PtAtTimeCallback(self.key, 7, 1)
                elif self.diffSphere == 2:
                    RespAdvanceUse.run(self.key, state="down2")
                    PtAtTimeCallback(self.key, 14, 1)
                elif self.diffSphere == 3:
                    RespAdvanceUse.run(self.key, state="down3")
                    PtAtTimeCallback(self.key, 21, 1)
                else:
                    PtDebugPrint(u"ahnyMaintRoom.OnNotify(): Impossible sphere advancement number: {}!".format(self.diffSphere), level=kErrorLevel)

    ## Sets the difference between the active sphere and the current sphere.
    # The active sphere is the sphere that will next be loaded, while the
    # current sphere is the one the player is in right then.
    def _SetSphereDifference(self):

        ageSDL = PtGetAgeSDL()
        activeSphere = ageSDL["ahnyCurrentSphere"][0]
        currentSphere = SphereNum.value
        self.diffSphere = (activeSphere - currentSphere) % 4
        PtDebugPrint(u"ahnyMaintRoom.SetSphereDifference(): Setting sphere difference to {}.".format(self.diffSphere))
