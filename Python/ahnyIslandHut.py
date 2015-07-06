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
Module: ahnyIslandHut.py
Age: Ahnonay
Date: June 2003
"""

from Plasma import *
from PlasmaTypes import *

# Define the attributes that will be entered in Max.
ActRotateSwitch = ptAttribActivator(1, "clk: rotate spheres")
RespRotateSwitch = ptAttribResponder(2, "resp: rotate spheres switch")
SDLWaterCurrent = ptAttribString(3, "SDL: water current")
ActWaterCurrent = ptAttribActivator(4, "clk: water current")
RespCurrentValve = ptAttribResponder(5, "resp: water current valve", ["on", "off"])
WaterCurrent1 = ptAttribSwimCurrent(6, "water current 1")
WaterCurrent2 = ptAttribSwimCurrent(7, "water current 2")
WaterCurrent3 = ptAttribSwimCurrent(8, "water current 3")
WaterCurrent4 = ptAttribSwimCurrent(9, "water current 4")
RespCurrentChange = ptAttribResponder(10, "resp: change the water current", ["on", "off"])
RespRotateSpheres = ptAttribResponder(11, "resp: rotate the spheres")
SDLHutDoor = ptAttribString(12, "SDL: hut door")
ActHutDoor = ptAttribActivator(13, "clk: hut door switch")
RespHutDoorBeh = ptAttribResponder(14, "resp: hut door switch", ["open", "close"])
RespHutDoor = ptAttribResponder(15, "resp: hut door", ["open", "close"])


class ahnyIslandHut(ptResponder):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5580
        self.version = 1
        PtDebugPrint("ahnyIslandHut: v{}".format(self.version), level=kWarningLevel)

        self.boolCurrent = 0
        self.boolHutDoor = 0
        self.actingAvatar = None
        self.actingAvatarDoor = None

    def OnFirstUpdate(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            PtDebugPrint("ahnyIslandHut.OnFirstUpdate(): Cannot find the Ahnonay Age SDL.", level=kErrorLevel)
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

        if self.boolCurrent:
            RespCurrentChange.run(self.key, state="on", fastforward=1)
            PtDebugPrint("ahnyIslandHut.OnFirstUpdate(): Will now enable current.", level=kWarningLevel)
            WaterCurrent1.current.enable()
            WaterCurrent2.current.enable()
            WaterCurrent3.current.enable()
            WaterCurrent4.current.enable()
        else:
            RespCurrentChange.run(self.key, state="off", fastforward=1)
            PtDebugPrint("ahnyIslandHut.OnFirstUpdate(): Will now disable current.", level=kWarningLevel)
            WaterCurrent1.current.disable()
            WaterCurrent2.current.disable()
            WaterCurrent3.current.disable()
            WaterCurrent4.current.disable()

        RespHutDoor.run(self.key, state="open" if self.boolHutDoor else "close", fastforward=1)

    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()

        if VARname == SDLWaterCurrent.value:
            self.boolCurrent = ageSDL[SDLWaterCurrent.value][0]
            RespCurrentChange.run(self.key, state="on" if self.boolCurrent else "off")

        elif VARname == SDLHutDoor.value:
            self.boolHutDoor = ageSDL[SDLHutDoor.value][0]
            RespHutDoor.run(self.key, state="open" if self.boolHutDoor else "close")

    def OnNotify(self, state, id, events):
        ageSDL = PtGetAgeSDL()

        if id == ActWaterCurrent.id and state:
            self.activeAvatar = PtFindAvatar(events)
            RespCurrentChange.run(self.key, state="off" if self.boolCurrent else "on", avatar=self.activeAvatar)

        elif id == RespCurrentValve.id and self.activeAvatar == PtGetLocalAvatar():
            ageSDL[SDLWaterCurrent.value] = (int(not self.boolCurrent),)

        elif id == RespCurrentChange.id:
            if self.boolCurrent:
                PtDebugPrint("ahnyIslandHut.OnNotify(): Will now enable current.", level=kWarningLevel)
                WaterCurrent1.current.enable()
                WaterCurrent2.current.enable()
                WaterCurrent3.current.enable()
                WaterCurrent4.current.enable()
            else:
                PtDebugPrint("ahnyIslandHut.OnNotify(): Will now disable current.", level=kWarningLevel)
                WaterCurrent1.current.disable()
                WaterCurrent2.current.disable()
                WaterCurrent3.current.disable()
                WaterCurrent4.current.disable()

        elif id == ActHutDoor.id and state:
            self.actingAvatarDoor = PtFindAvatar(events)
            RespHutDoorBeh.run(self.key, state="close" if self.boolHutDoor else "open", avatar=self.actingAvatarDoor)

        elif id == RespHutDoorBeh.id and self.actingAvatarDoor == PtGetLocalAvatar():
            ageSDL[SDLHutDoor.value] = (int(not self.boolHutDoor),)
