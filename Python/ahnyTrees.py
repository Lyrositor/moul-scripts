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
Module: ahnyTrees
Age: Ahnonay
Date: April, 2007
Author: Derek Odell
Ahnonay Quab control
"""

from Plasma import *
from PlasmaTypes import *

# Define the attributes that will be entered in Max.
rgnTrees = ptAttribActivator(1, "act: Tree Detector")
respTreeAnims = ptAttribResponderList(2, "resp: Tree Anims", byObject=1)
objTrees = ptAttribSceneobjectList(3, "obj: Tree Meshs")
SDLTrees = ptAttribString(4, "str: SDL Trees (optional)")


class ahnyTrees(ptModifier):

    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5948
        self.version = 1
        PtDebugPrint("ahnyTrees: v{}".format(self.version), level=kWarningLevel)

        self.respTreeAnimsList = []
        self.objTreeList = []

    def OnFirstUpdate(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            PtDebugPrint("ahnyTrees.OnFirstUpdate(): Cannot find the Ahnonay Age SDL.", level=kErrorLevel)
            ageSDL[SDLTrees.value] = (1,)*15

        ageSDL.setFlags(SDLTrees.value, 1, 1)
        ageSDL.sendToClients(SDLTrees.value)
        ageSDL.setNotify(self.key, SDLTrees.value, 0.0)

        for responder in respTreeAnims.value:
            self.respTreeAnimsList.append(responder.getName())

        for obj in objTrees.value:
            self.objTreeList.append(obj.getName())

        ageSDL = PtGetAgeSDL()
        for idx, visible in enumerate(ageSDL[SDLTrees.value]):
            if not visible:
                respTreeAnims.run(self.key, objectName=self.respTreeAnimsList[idx], fastforward=1)

    def OnNotify(self, state, id, events):
        PtDebugPrint("ahnyTrees.OnNotify(): state={} id={} events={}".format(state, id, events), level=kDebugDumpLevel)

        ageSDL = PtGetAgeSDL()
        if id == rgnTrees.id:
            for event in events:
                if event[0] == kCollisionEvent and self.sceneobject.isLocallyOwned():
                    region = event[3]
                    regName = region.getName()
                    for object in self.objTreeList:
                        if object == regName:
                            treeSDL = list(ageSDL[SDLTrees.value])
                            index = self.objTreeList.index(object)
                            if treeSDL[index]:
                                respTreeAnims.run(self.key, objectName=self.respTreeAnimsList[index], netForce=1)
                                treeSDL[index] = 0
                                ageSDL[SDLTrees.value] = tuple(treeSDL)
                                PtDebugPrint("ahnyTrees.OnNotify(): Tree knocked down.", level=kWarningLevel)
