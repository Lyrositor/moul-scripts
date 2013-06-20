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

## @package ahnyIslandHut
# The module for the control tower island in Ahnonay.
# @date June 2003: Creation.

from Plasma import *
from PlasmaTypes import *

from xPsnlVaultSDL import *

# Define the attributes that will be entered in Max.
ActRotateSwitch = ptAttribActivator(1, "Clk: rotate spheres")
RespRotateSwitch = ptAttribResponder(2, "Resp: rotate spheres switch")
SDLWaterCurrent = ptAttribString(3, "SDL: water current")
ActWaterCurrent = ptAttribActivator(4,"Clk: water current")
RespCurrentValve = ptAttribResponder(5, "Resp: water current valve", ("on", "off"))
WaterCurrent1 = ptAttribSwimCurrent(6, "Water current 1")
WaterCurrent2 = ptAttribSwimCurrent(7, "Water current 2")
WaterCurrent3 = ptAttribSwimCurrent(8, "Water current 3")
WaterCurrent4 = ptAttribSwimCurrent(9, "Water current 4")
RespCurrentChange = ptAttribResponder(10, "Resp: change the water current", ("on", "off"))
RespRotateSpheres = ptAttribResponder(11, "Resp: rotate the spheres")
SDLHutDoor = ptAttribString(12, "SDL: hut door")
ActHutDoor = ptAttribActivator(13, "Clk: hut door switch")
RespHutDoorBeh = ptAttribResponder(14, "Resp: hut door switch", ("open", "close"))
RespHutDoor = ptAttribResponder(15, "Resp: hut door", ("open", "close"))

## A list of the water current attributes.
kCurrents = (WaterCurrent1, WaterCurrent2, WaterCurrent3, WaterCurrent4)


## The responder for the island hut in Ahnonay.
# Controls the water current and the state of the door.
class ahnyIslandHut(ptResponder):

    id = 5580
    version = 1

    ## Initialize the island hut responder.
    # Defines the island's state variables.
    def __init__(self):

        PtDebugPrint(u"ahnyIslandHut: Version {}.".format(self.version))
        ptResponder.__init__(self)
        self.boolCurrent = False
        self.boolHutDoor = False
        self.actingAvatar = None
        self.actingAvatarDoor = None

    ## Called by Plasma on receipt of the first plEvalMsg.
    # Sets the state of the hut and the current according to the Age's SDL.
    def OnFirstUpdate(self):

        ageSDL = PtGetAgeSDL()
        if not ageSDL:
            PtDebugPrint(u"ahnyIslandHut.OnFirstUpdate(): Cannot find Ahnonay's Age SDL.", level=kErrorLevel)
            ageSDL[SDLWaterCurrent.value] = (0,)
            ageSDL[SDLHutDoor.value] = (0,)

        ageSDL.setFlags(SDLWaterCurrent.value, 1, 1)
        ageSDL.setFlags(SDLHutDoor.value, 1, 1)
        ageSDL.sendToClients(SDLWaterCurrent.value)
        ageSDL.sendToClients(SDLHutDoor.value)
        ageSDL.setNotify(self.key, SDLWaterCurrent.value, 0.0)
        ageSDL.setNotify(self.key, SDLHutDoor.value, 0.0)

        self.boolCurrent = ageSDL[SDLWaterCurrent.value][0]
        self.boolHutDoor = ageSDL[SDLHutDoor.value][0]

        # Enable or disable current.
        RespCurrentChange.run(self.key, state="on" if self.boolCurrent else "off", fastforward=1)
        PtDebugPrint(u"ahnyIslandHut.OnFirstUpdate(): {}abling current.".format("En" if self.boolCurrent else "Dis"))
        if self.boolCurrent:
            for c in kCurrents: c.current.enable()
        else:
            for c in kCurrents: c.current.disable()

        # Open or close the door.
        RespHutDoor.run(self.key, state="open" if self.boolHutDoor else "close", fastforward=1)

    ## Called by Plasma when an SDL notify is received.
    # Used to toggle current and door SDL settings.
    def OnSDLNotify(self, varName, sdlName, playerID, tag):

        ageSDL = PtGetAgeSDL()

        if varName == SDLWaterCurrent.value:
            self.boolCurrent = ageSDL[SDLWaterCurrent.value][0]
            RespCurrentChange.run(self.key, state="on" if self.boolCurrent else "off")
        elif varName == SDLHutDoor.value:
            self.boolHutDoor = ageSDL[SDLHutDoor.value][0]
            RespHutDoor.run(self.key, state="open" if self.boolHutDoor else "close")

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Used to toggle current and door settings visibly.
    def OnNotify(self, state, ID, events):

        ageSDL = PtGetAgeSDL() 

        if ID == ActWaterCurrent.id and state:
            self.actingAvatar = PtFindAvatar(events)
            RespCurrentValve.run(self.key, state="off" if self.boolCurrent else "on", avatar=PtFindAvatar(events))

        elif ID == RespCurrentValve.id and self.actingAvatar == PtGetLocalAvatar():
            ageSDL[SDLWaterCurrent.value] = (int(not self.boolCurrent),)

        elif ID == RespCurrentChange.id:
            for current in kCurrents:
                PtDebugPrint(u"ahnyIslandHut.OnNotify(): {}abling current.".format("En" if self.boolCurrent else "Dis"))
                if self.boolCurrent:
                    current.enable()
                else:
                    current.disable()

        elif ID == ActHutDoor.id and state:
            self.actingAvatarDoor = PtFindAvatar(events)
            RespHutDoorBeh.run(self.key, state="close" if self.boolHutDoor else "open", avatar=PtFindAvatar(events))

        elif ID == RespHutDoorBeh.id and self.actingAvatarDoor == PtGetLocalAvatar():
            ageSDL[SDLHutDoor.value] = (int(not self.boolHutDoor),)
