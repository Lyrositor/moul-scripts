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

## @package ahnyKadishHut
## The module for Kadish's secret hut.
# @author Chris Doyle
# @date April 2004: Creation.

from Plasma import *
from PlasmaTypes import *

# Define the attributes that will be entered in Max.
SDLWindows = ptAttribString(1, "SDL: windows")
ActWindows = ptAttribActivator(2, "Clk: windows")
RespWindowsBeh = ptAttribResponder(3, "Resp: windows oneshot")
RespWindows = ptAttribResponder(4, "Resp: windows use", ("close", "open"))


## The responder for Kadish's Hut in Ahnonay.
# Provides the wiring for items inside Kadish's hut.
class ahnyKadishHut(ptResponder):

    id = 5610
    version = 4

    ## Initialize the hut responder.
    # Sets windows to closed by default.
    def __init__(self):

        PtDebugPrint(u"ahnyKadishHut: Version {}.".format(self.version))
        ptResponder.__init__(self)
        self.boolWindows = False

    ## Called by Plasma on receipt of the first plEvalMsg.
    # Determines the current state of the windows in the hut.
    def OnFirstUpdate(self):

        ageSDL = PtGetAgeSDL()
        if not ageSDL:  # This should never happen, but we don't trust eap.
            PtDebugPrint(u"ahnyKadishHut.OnFirstUpdate(): Cannot find AhnySphere04's Age SDL.", level=kErrorLevel)
            return

        ageSDL.setFlags(SDLWindows.value, 1, 1)
        ageSDL.sendToClients(SDLWindows.value)
        ageSDL.setNotify(self.key, SDLWindows.value, 0.0)

        self.boolWindows = ageSDL[SDLWindows.value][0]

        PtDebugPrint(u"ahnyKadishHut.OnFirstUpdate(): Windows are {}.".format("open" if self.boolWindows else "closed"))
        RespWindows.run(self.key, state="open" if self.boolWindows else "close", fastforward=1)

    ## Called by Plasma when an SDL notify is received.
    # Used to toggle the windows settings.
    def OnSDLNotify(self, varName, sdlName, playerID, tag):

        if varName == SDLWindows.value:
            ageSDL = PtGetAgeSDL()
            self.boolWindows = ageSDL[SDLWindows.value][0]
            PtDebugPrint(u"ahnyKadishHut.OnFirstUpdate(): Windows will now {}.".format("open" if self.boolWindows else "close"))
            RespWindows.run(self.key, state="open" if self.boolWindows else "close")

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Toggles the windows' settings.
    def OnNotify(self, state, ID, events):

        if ID == ActWindows.id and state:
            RespWindowsBeh.run(self.key, avatar=PtFindAvatar(events))

        elif ID == RespWindowsBeh.id:
            ageSDL = PtGetAgeSDL()
            ageSDL[SDLWindows.value] = (int(not self.boolWindows),)
