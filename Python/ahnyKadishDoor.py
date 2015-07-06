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
Module: ahnyKadishDoor.py
Age: Ahnonay Sphere 4
Date: April 2004
Author: Chris Doyle
wiring for Kadish's engineer hut door
"""

from Plasma import *
from PlasmaTypes import *
import copy
import PlasmaControlKeys

# Define the attributes that will be entered in Max.
SDLDoor = ptAttribString(1, "SDL: door")
ActConsole = ptAttribActivator(2, "clk: console")
RespConsole = ptAttribResponder(3, "resp: console", ["enter", "exit"])
MltStgSeek = ptAttribBehavior(4, "Smart seek before puzzle")
ActButtons = ptAttribActivatorList(5, "clk: list of 8 buttons")
RespButtons = ptAttribResponderList(6, "resp: list of 8 buttons", byObject=1)
RespDoor = ptAttribResponder(7, "resp: door ops", ["close", "open"])
ObjButtons = ptAttribSceneobjectList(8, "objects: list of 8 buttons")

kSolutionList = (3, 2, 1, 4, 8, 5, 6, 7)


class ahnyKadishDoor(ptResponder):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5600
        self.version = 3
        PtDebugPrint("ahnyKadishDoor: v{}".format(self.version), level=kWarningLevel)

        self.boolDoor = 0
        self.btnNum = 0
        self.btnList = []
        self.respList = []
        self.objList = []
        self.solutionNum = 8
        self.currentList = [0]*8
        self.actingAvatar = None

    def OnFirstUpdate(self):
        for button in ActButtons.value:
            self.btnList.append(button.getName())
        PtDebugPrint("ahnyKadishDoor.btnList = {}".format(self.btnList), level=kDebugDumpLevel)
        for resp in RespButtons.value:
            self.respList.append(resp.getName())
        PtDebugPrint("ahnyKadishDoor.respList = {}".format(self.respList), level=kDebugDumpLevel)
        for obj in ObjButtons.value:
            self.objList.append(obj.getName())
        PtDebugPrint("ahnyKadishDoor.objList = {}".format(self.objList), level=kDebugDumpLevel)

        PtAtTimeCallback(self.key, 0, 1)

    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        if VARname == SDLDoor.value:
            self.boolDoor = ageSDL[SDLDoor.value][0]
            RespDoor.run(self.key, state="open" if self.boolDoor else "close")

    def OnNotify(self, state, id, events):
        if id == ActConsole.id and state:
            self.actingAvatar = PtFindAvatar(events)
            if self.actingAvatar == PtGetLocalAvatar():
                PtDebugPrint("ahnyKadishDoor.OnNotify(): Switching to console close up.", level=kWarningLevel)
                ActConsole.disableActivator()
                PtEnableControlKeyEvents(self.key)
                MltStgSeek.run(self.actingAvatar)
        
        if id == MltStgSeek.id and self.actingAvatar == PtGetLocalAvatar():
            for event in events:
                # Smart seek completed. Exit multistage, and show GUI.
                if event[0] == kMultiStageEvent and event[2] == kEnterStage:
                    MltStgSeek.gotoStage(self.actingAvatar, -1) 
                    PtDebugPrint("ahnyKadishDoor.OnNotify(): Entering puzzle view mode now that seek is done.", level=kWarningLevel)
                    self.actingAvatar.draw.disable()
                    # Disable First Person Camera
                    cam = ptCamera()
                    cam.disableFirstPersonOverride()
                    cam.undoFirstPerson()
                    RespConsole.run(self.key, state="enter")
                    PtAtTimeCallback(self.key, 0.5, 2)
        
        if id == ActButtons.id and state:
            PtDebugPrint("ahnyKadishDoor.OnNotify(): Disabling 8 button clickables.", level=kWarningLevel)
            for btn in ActButtons.value:
                btn.disable()
            for event in events:
                if event[0] == kPickedEvent:
                    xEvent = event[3]
                    btnName = xEvent.getName()
                    for i, obj in enumerate(self.objList):
                        if obj == btnName:
                            self.btnNum = i
                            break
                        else:
                            i += 1
                    
                    PtDebugPrint("ahnyKadishDoor.btnNum = {}".format(self.btnNum+1), level=kWarningLevel)
                    RespButtons.run(self.key, objectName=self.respList[self.btnNum])
        
        if id == RespButtons.id and self.actingAvatar == PtGetLocalAvatar():
            self.CheckButtons()

    def CheckButtons(self):
        ageSDL = PtGetAgeSDL()
        
        self.currentList.append(self.btnNum + 1)
        while len(self.currentList) > len(kSolutionList):
            del self.currentList[0]
        
        PtDebugPrint("ahnyKadishDoor.CheckButtons(): Solution = {}".format(kSolutionList))
        PtDebugPrint("ahnyKadishDoor.CheckButtons(): Current  = {}".format(self.currentList))
        
        if self.AreListsEquiv(kSolutionList, self.currentList):
            PtDebugPrint("ahnyKadishDoor.CheckButtons(): Open!", level=kWarningLevel)
            self.ExitConsole()
            ageSDL[SDLDoor.value] = (1,)
        else:
            if self.boolDoor:
                self.ExitConsole()
                ageSDL[SDLDoor.value] = (0,)
            else:
                for btn in ActButtons.value:
                    btn.enable()

    def AreListsEquiv(self, list1, list2):
        if list1[0] in list2:
            # Rearrange list
            list2Copy = copy.copy(list2)
            while list2Copy[0] != list1[0]:
                list2Copy.append(list2Copy.pop(0))

            # Check if all values match up now
            for i in range(self.solutionNum):
                if list2Copy[i] != list1[i]:
                    return False

            return True
        return False

    def OnControlKeyEvent(self, controlKey, activeFlag):
        if controlKey in (PlasmaControlKeys.kKeyExitMode, PlasmaControlKeys.kKeyMoveBackward, PlasmaControlKeys.kKeyRotateLeft, PlasmaControlKeys.kKeyRotateRight):
            self.ExitConsole()

    def ExitConsole(self):
        PtDebugPrint("ahnyKadishDoor.ExitConsole(): Disengage and exit the console.", level=kDebugDumpLevel)
        for btn in ActButtons.value:
            btn.disable()

        # Re-enable first person
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        PtDisableControlKeyEvents(self.key)
        RespConsole.run(self.key, state="exit")
        avatar = PtGetLocalAvatar()
        avatar.draw.enable()
        PtAtTimeCallback(self.key, 0.5, 3)

    def OnTimer(self, id):
        if id == 1:
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(SDLDoor.value, 1, 1)
            ageSDL.sendToClients(SDLDoor.value)
            ageSDL.setNotify(self.key, SDLDoor.value, 0.0)
            try:
                ageSDL = PtGetAgeSDL()
            except:
                PtDebugPrint("ahnyKadishDoor.OnTimer(): Cannot find AhnySphere04 age SDL.", level=kErrorLevel)
                ageSDL[SDLDoor.value] = (0,)
            self.boolDoor = ageSDL[SDLDoor.value][0]
            RespDoor.run(self.key, state="open" if self.boolDoor else "close", fastforward=1)
        
        elif id == 2:
            PtDebugPrint("ahnyKadishDoor.OnTimer(): Re-enabling 8 button clickables.", level=kWarningLevel)
            for btn in ActButtons.value:
                btn.enable()
        
        elif id == 3:
            PtDebugPrint("ahnyKadishDoor.OnTimer(): Re-enabling the console's clickable.", level=kWarningLevel)
            ActConsole.enableActivator()
