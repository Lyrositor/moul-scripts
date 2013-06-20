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

## @package ahnyKadishDoor
# The module for the door to Kadish's secret hut.
# @author Chris Doyle
# @date April 2004: Creation.

from Plasma import *
from PlasmaControlKeys import kKeyExitMode, kKeyMoveBackward, kKeyRotateLeft, kKeyRotateRight
from PlasmaTypes import *
from PlasmaKITypes import *

# Define the attributes that will be entered in Max.
SDLDoor = ptAttribString(1, "SDL: door")
ActConsole = ptAttribActivator(2, "Clk: console")
RespConsole = ptAttribResponder(3, "Resp: console", ("enter", "exit"))
MltStgSeek = ptAttribBehavior(4, "Smart seek before puzzle")
ActButtons = ptAttribActivatorList(5, "Clk: list of 8 buttons")
RespButtons = ptAttribResponderList(6, "Resp: list of 8 buttons", byObject=1)
RespDoor = ptAttribResponder(7, "Resp: door ops", ("close", "open"))
ObjButtons = ptAttribSceneobjectList(8, "Objects: list of 8 buttons")

## The correct button combination for Kadish's door.
kSolutionList = (3, 2, 1, 4, 8, 5, 6, 7)

## The responder for Kadish's door in Ahnonay.
# Provides all the wiring for the door to Kadish's engineer hut.
class ahnyKadishDoor(ptResponder):

    id = 5600
    version = 3

    ## Initialize the door responder.
    # Defines the door's state variables.
    def __init__(self):

        PtDebugPrint(u"ahnyKadishDoor: Version {}.".format(self.version))
        ptResponder.__init__(self)
        self.boolDoor = False
        self.btnNum = 0
        self.respList = []
        self.objList = []
        self.currentList = [0, 0, 0, 0, 0, 0, 0, 0]
        self.actingAvatar = None

    ## Called by Plasma on receipt of the first plEvalMsg.
    # Populates the responder and object lists.
    def OnFirstUpdate(self):

        self.respList = [r.getName() for r in RespButtons.value]
        PtDebugPrint(u"ahnyKadishDoor.OnFirstUpdate(): respList={}.".format(self.respList), level=kDebugDumpLevel)
        self.objList = [o.getName() for o in ObjButtons.value]
        PtDebugPrint(u"ahnyKadishDoor.OnFirstUpdate(): objList={}.".format(self.objList), level=kDebugDumpLevel)

        PtAtTimeCallback(self.key, 0, 1)

    ## Called by Plasma when an SDL notify is received.
    # Used to toggle the door SDL settings.
    def OnSDLNotify(self, varName, sdlName, playerID, tag):

        ageSDL = PtGetAgeSDL()
        if varName == SDLDoor.value:
            self.boolDoor = ageSDL[SDLDoor.value][0]
            RespDoor.run(self.key, state="open" if self.boolDoor else "close")

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Processes door and puzzle-related notifications.
    def OnNotify(self, state, ID, events):

        if ID == ActConsole.id and state:
            self.actingAvatar = PtFindAvatar(events)
            if self.actingAvatar == PtGetLocalAvatar():
                PtDebugPrint(u"ahnyKadishDoor.OnNotify(): Switching to console close-up.", level=kDebugDumpLevel)
                ActConsole.disableActivator()
                PtEnableControlKeyEvents(self.key)
                MltStgSeek.run(self.actingAvatar)

        elif ID == MltStgSeek.id and self.actingAvatar == PtGetLocalAvatar():
            for event in events:
                # Is smart seek completed?
                if event[0] == kMultiStageEvent and event[2] == kEnterStage:
                    # Exit multistage and show GUI.
                    MltStgSeek.gotoStage(self.actingAvatar, -1) 
                    PtDebugPrint(u"ahnyKadishDoor.OnNotify(): Entering puzzle view mode now that seek is done.", level=kDebugDumpLevel)
                    self.actingAvatar.draw.disable()
                    cam = ptCamera()
                    cam.disableFirstPersonOverride()
                    cam.undoFirstPerson()
                    RespConsole.run(self.key, state="enter")
                    PtAtTimeCallback(self.key, 0.5, 2)

        elif ID == ActButtons.id and state:
            PtDebugPrint(u"ahnyKadishDoor.OnNotify(): Disabling 8 button clickables.", level=kDebugDumpLevel)
            for i, btn in enumerate(ActButtons.value):
                ActButtons.value[i].disable()
            for event in events:
                if event[0] == kPickedEvent:
                    btnName = event[3].getName()
                    for i, obj in enumerate(self.objList):
                        if obj == btnName:
                            self.btnNum = i
                            break
                    PtDebugPrint(u"ahnyKadishDoor.OnNotify(): btnBum={}".format(self.btnNum + 1), level=kDebugDumpLevel)
                    RespButtons.run(self.key, objectName=self.respList[self.btnNum])

        elif ID == RespButtons.id and self.actingAvatar == PtGetLocalAvatar():
            PtDebugPrint(u"ahnyKadishDoor.OnNotify(): Checking buttons.")

            ageSDL = PtGetAgeSDL()
            self.currentList.append(self.btnNum + 1)
            while len(self.currentList) > len(kSolutionList):
                del self.currentList[0]
            PtDebugPrint(u"ahnyKadishDoor.OnNotify(): Solution list: {}.".format(kSolutionList))
            PtDebugPrint(u"ahnyKadishDoor.OnNotify(): Current list: {}.".format(self.currentList))

            if any(kSolutionList == self.currentList[i:] + self.currentList[:i] for i in xrange(len(self.currentList))):
                PtDebugPrint(u"ahnyKadishDoor.OnNotify(): Opening door.")
                self._ExitConsole()
                ageSDL[SDLDoor.value] = (1,)
            else:
                if self.boolDoor:
                    self._ExitConsole()
                    ageSDL[SDLDoor.value] = (0,)
                else:
                    for i, btn in enumerate(ActButtons.value):
                        ActButtons.value[i].enable()

    ## Called by Plasma when the control key state is changed.
    # Used to exit the console with the movement keys.
    def OnControlKeyEvent(self, controlKey, activeFlag):

        if controlKey in [kKeyExitMode, kKeyMoveBackward, kKeyRotateLeft, kKeyRotateRight]:
            self._ExitConsole()

    ## Called by Plasma when a timer is over.
    # Used to handle the various door and button timer events.
    def OnTimer(self, ID):

        if ID == 1:
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(SDLDoor.value, 1, 1)
            ageSDL.sendToClients(SDLDoor.value)
            ageSDL.setNotify(self.key, SDLDoor.value, 0.0)
            try:
                ageSDL = PtGetAgeSDL()
            except:
                PtDebugPrint(u"ahnyKadishDoor.OnTimer(): Cannot find AhnySphere04's Age SDL.", level=kErrorLevel)
                ageSDL[SDLDoor.value] = (0,)
            self.boolDoor = ageSDL[SDLDoor.value][0]
            RespDoor.run(self.key, state="open" if self.boolDoor else "close", fastforward=1)

        elif ID == 2:
            PtDebugPrint(u"ahnyKadishDoor.onTimer(): Re-enabling 8 button clickables.", level=kDebugDumpLevel)
            for i, btn in enumerate(ActButtons.value):
                ActButtons.value[i].enable()

        elif ID == 3:
            PtDebugPrint(u"ahnyKadishDoor.onTimer(): Re-enabling the console's clickable.", level=kDebugDumpLevel)
            ActConsole.enableActivator()

    ## Disengage and exit the console.
    # This returns the player to his normal view mode.
    def _ExitConsole(self):

        for i, btn in enumerate(ActButtons.value):
            ActButtons.value[i].disable()
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        PtDisableControlKeyEvents(self.key)
        RespConsole.run(self.key, state="exit")
        avatar = PtGetLocalAvatar()
        avatar.draw.enable()
        PtAtTimeCallback(self.key, 0.5, 3)
