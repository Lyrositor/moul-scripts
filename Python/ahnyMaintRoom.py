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
Module: ahnyMaintRoom.py
Age: Ahnonay Spheres 1-4
Date: April 2004
"""

from Plasma import *
from PlasmaTypes import *

# Define the attributes that will be entered in Max.
SphereNum = ptAttribInt(1, "sphere #")
ActAdvanceSwitch = ptAttribActivator(2, "clk: advance spheres switch")
RespAdvanceBeh = ptAttribResponder(3, "resp: advance spheres beh")
RespAdvanceUse = ptAttribResponder(4, "resp: advance spheres use", ["down0", "up", "down1", "down2", "down3"])
RespHubDoor = ptAttribResponder(5, "resp: hub door (sphere 4 only!)", ["close", "open"])


class ahnyMaintRoom(ptResponder):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5581
        self.version = 2
        PtDebugPrint("ahnyMaintRoom: v{}".format(self.version), level=kWarningLevel)

        self.actingAvatar = None
        self.boolHubDoor = 0
        self.diffsphere = 0

    def OnFirstUpdate(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            PtDebugPrint("ahnyMaintRoom.OnFirstUpdate(): Cannot find the Ahnonay Age SDL.", level=kErrorLevel)
        
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
            if sphere == 4:
                if not self.boolHubDoor:
                    self.boolHubDoor = 1
                    ageSDL["ahnyHubDoor"] = (1,)
                RespHubDoor.run(self.key, state="open", fastforward=1)
            else:
                if self.boolHubDoor:
                    self.boolHubDoor = 0
                    ageSDL["ahnyHubDoor"] = (0,)
                RespHubDoor.run(self.key, state="close", fastforward=1)
            RespAdvanceUse.run(self.key, state="down0", fastforward=1)
        else:
            if SphereNum.value != 1 and SphereNum.value != 2 and SphereNum.value != 3:
                PtDebugPrint("ahnyMaintRoom.OnFirstUpdate(): Invalid sphere# set in component. Disabling clickable.", level=kErrorLevel)
                ActAdvanceSwitch.disableActivator()
        
        self.SphereDifference()

    def OnTimer(self, id):
        if id == 1:
            PtAtTimeCallback(self.key, 0, 2)
            if self.actingAvatar == PtGetLocalAvatar():
                ageSDL = PtGetAgeSDL()
                ageSDL["ahnyCurrentSphere"] = (SphereNum.value,)
                PtDebugPrint("ahnyMaintRoom.OnTimer(): Advanced from sphere {} with maintainence button".format(ageSDL["ahnyCurrentSphere"][0]), level=kWarningLevel)
                PtDebugPrint("ahnyMaintRoom.OnTimer(): Sphere {} will now be the active sphere".format(SphereNum.value), level=kWarningLevel)
                if SphereNum.value == 4:
                    ageSDL["ahnyImagerSphere"] = (SphereNum.value,)
                    self.boolHubDoor = ageSDL["ahnyHubDoor"][0]
                    if self.boolHubDoor and ageSDL["ahnyCurrentSphere"][0] != 4:
                        PtDebugPrint("ahnyMaintRoom.OnTimer(): Door is open and we're not going to Sphere 4, so close it.", level=kWarningLevel)
                        ageSDL["ahnyHubDoor"] = (0,)
                    elif not self.boolHubDoor and ageSDL["ahnyCurrentSphere"][0] == 4:
                        PtDebugPrint("ahnyMaintRoom.OnTimer(): Door is not open and we're going to Sphere 4, so open it.", level=kWarningLevel)
        
        elif id == 2:
            ActAdvanceSwitch.enableActivator()
            if SphereNum.value == 4:
                ageSDL = PtGetAgeSDL()
                ageSDL["ahnyHubDoor"] = (1,)

    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if SphereNum.value == 4:
            ageSDL = PtGetAgeSDL()
            if VARname == "ahnyHubDoor":
                self.boolHubDoor = ageSDL["ahnyHubDoor"][0]
                RespHubDoor.run(self.key, state="open" if self.boolHubDoor else "close")
            elif VARname == "ahnyCurrentSphere":
                self.boolHubDoor = ageSDL["ahnyHubDoor"][0]
                if self.boolHubDoor and ageSDL["ahnyCurrentSphere"][0] != 4:
                    PtDebugPrint("ahnyMaintRoom.OnSDLNotify(): Door is open and we're not going to Sphere 4, so close it.", level=kWarningLevel)
                    ageSDL["ahnyHubDoor"] = (0,)
                elif not self.boolHubDoor and ageSDL["ahnyCurrentSphere"][0] == 4:
                    PtDebugPrint("ahnyMaintRoom.OnSDLNotify(): Door is not open and we're going to Sphere 4, so open it.", level=kWarningLevel)
                    PtAtTimeCallback(self.key, 7, 2)
        
        if VARname == "ahnyCurrentSphere":
            self.SphereDifference()

    def OnNotify(self, state, id, events):
        if id == ActAdvanceSwitch.id and state:
            self.actingAvatar = PtFindAvatar(events)
            RespAdvanceBeh.run(self.key, avatar=self.actingAvatar)
        
        elif id == RespAdvanceBeh.id:
            RespAdvanceUse.run(self.key, state="up")
        
        elif id == RespAdvanceUse.id:
            if self.diffsphere == 0:
                RespAdvanceUse.run(self.key, state="down0")
                self.SphereDifference()
            else:
                if self.diffsphere == 1:
                    RespAdvanceUse.run(self.key, state="down1")
                    PtAtTimeCallback(self.key, 7, 1)
                elif self.diffsphere == 2:
                    RespAdvanceUse.run(self.key, state="down2")
                    PtAtTimeCallback(self.key, 14, 1)
                elif self.diffsphere == 3:
                    RespAdvanceUse.run(self.key, state="down3")
                    PtAtTimeCallback(self.key, 21, 1)
                else:
                    PtDebugPrint("ahnyMaintRoom.OnNotify(): Sphere advancement# not possible??", level=kErrorLevel)

    def SphereDifference(self):
        ageSDL = PtGetAgeSDL()
        activeSphere = ageSDL["ahnyCurrentSphere"][0]
        currentSphere = SphereNum.value
        self.diffsphere = (activeSphere - currentSphere) % 4
        PtDebugPrint("ahnyMaintRoom.SphereDifference(): Setting sphere difference for Maint Room switch to {}.".format(self.diffsphere), level=kWarningLevel)
