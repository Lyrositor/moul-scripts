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
Module: bhroBahroPOTS
Age: LiveBahroCaves
Date: May 2007
Author: Chris Doyle, shameless plagarized off of Derek Odell's bhroBahroPod.py script
POTS Bahro Cave
"""

from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from xPsnlVaultSDL import *

clkErcana = ptAttribActivator(1, "clk: Ercana symbol")
clkAhnonay = ptAttribActivator(2, "clk: Ahnonay symbol")
respWedges = ptAttribResponder(3, "resp: Ground Wedges", ["Ercana", "Ahnonay"])
respErcanaRing = ptAttribResponder(4, "resp: Ercana Floating Ring")
respAhnonayRing = ptAttribResponder(5, "resp: Ahnonay Floating Ring")

kAges = {
    clkErcana.id: [12, "Ercana", respErcanaRing],
    clkAhnonay.id: [13, "Ahnonay", respAhnonayRing]
}


class bhroBahroPOTS(ptResponder):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 8816
        self.version = 1
        PtDebugPrint("bhroBahroPOTS: v{}".format(self.version), level=kWarningLevel)

    def OnFirstUpdate(self):
        PtSendKIMessage(kDisableYeeshaBook, 0)

    def OnServerInitComplete(self):
        # If the age is not the one that I'm from then run the responder to make it back off
        ageFrom = PtGetPrevAgeName()
        PtDebugPrint("bhroBahroPOTS.OnServerInitComplete(): Came from {}, running opposite responder state".format(ageFrom), level=kWarningLevel)
        if ageFrom == "Ercana":
            respWedges.run(self.key, state="Ahnonay", fastforward=1)
        elif ageFrom == "Ahnonay":
            respWedges.run(self.key, state="Ercana", fastforward=1)

        psnlSDL = xPsnlVaultSDL()
        for id, age in kAges.items():
            if psnlSDL["psnlBahroWedge{:02}".format(age[0])][0]:
                PtDebugPrint("bhroBahroPOTS.OnServerInitComplete(): You have the {} wedge, no need to display it.".format(age[1]), level=kWarningLevel)
                age[2].run(self.key, fastforward=1)

    def OnNotify(self, state, id, events):
        if id in kAges and state:
            psnlSDL = xPsnlVaultSDL()
            PtDebugPrint("bhroBahroPod.OnNotify(): Clicked {} symbol.".format(kAges[id][1]), level=kWarningLevel)
            kAges[id][2].run(self.key, avatar=PtFindAvatar(events))
            sdlVal = psnlSDL["psnlBahroWedge{:02}".format(kAges[id][0])][0]
            if not sdlVal:
                PtDebugPrint("bhroBahroPod.OnNotify(): Turning {} wedge SDL to On".format(kAges[id][1]), level=kWarningLevel)
                psnlSDL["psnlBahroWedge{:02}".format(kAges[id][0])] = (1,)
