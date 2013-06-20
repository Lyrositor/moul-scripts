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

## @package ahnyTrees
# The controls for the trees in misty Ahnonay.
# @author Derek Odell
# @date April 2007: Creation.

from Plasma import *
from PlasmaTypes import *

# Define the attributes that will be entered in Max.
RgnTrees = ptAttribActivator(1, "Act: Tree Detector")
RespTreeAnims = ptAttribResponderList(2, "Resp: Tree Anims", byObject=1)
ObjTrees = ptAttribSceneobjectList(3, "Obj: Tree Meshs")
SDLTrees = ptAttribString(4, "Str: SDL Trees (optional)")


## The modifier for the Ahnonay crystal trees.
# Controls the trees presence or absence.
class ahnyTrees(ptModifier):

    id = 5948
    version = 1

    ## Initialize the modifier for the trees.
    def __init__(self):

        PtDebugPrint(u"ahnyTrees: Version {}.".format(self.version))
        ptModifier.__init__(self)
        self.respTreeAnimsList = []
        self.objTreeList = []

    ## Called by Plasma on receipt of the first plEvalMsg.
    # Sets up the trees' initial position.
    def OnFirstUpdate(self):

        ageSDL = PtGetAgeSDL()
        if not ageSDL:  # This should never happen, but we don't trust eap.
            PtDebugPrint(u"ahnyTrees.OnFirstUpdate(): Cannot find Ahnonay's Age SDL.", level=kErrorLevel)
            return
        try:
            ageSDL[SDLTrees.value][0]
        except:
            ageSDL[SDLTrees.value] = tuple([1] * 15)

        ageSDL.setFlags(SDLTrees.value, 1, 1)
        ageSDL.sendToClients(SDLTrees.value)
        ageSDL.setNotify(self.key, SDLTrees.value, 0.0)

        self.respTreeAnimsList = [r.getName() for r in RespTreeAnims.value]
        self.objTreeList = [o.getName() for o in ObjTrees.value]

        for idx, visible in enumerate(ageSDL[SDLTrees.value]):
            if not visible:
                RespTreeAnims.run(self.key, objectName=self.respTreeAnimsList[idx], fastforward=1)

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Used to remove trees when the player walks into them.
    def OnNotify(self, state, ID, events):

        if ID == RgnTrees.id:
            for event in events:
                if event[0] == kCollisionEvent and self.sceneobject.isLocallyOwned() :
                    region = event[3]
                    regName = region.getName()
                    for obj in self.objTreeList:
                        if obj == regName:
                            ageSDL = PtGetAgeSDL()
                            treeSDL = list(ageSDL[SDLTrees.value])
                            index = self.objTreeList.index(obj)
                            if treeSDL[index]:
                                RespTreeAnims.run(self.key, objectName=self.respTreeAnimsList[index], netForce=1)
                                treeSDL[index] = 0
                                ageSDL[SDLTrees.value] = tuple(treeSDL)
                                PtDebugPrint(u"ahnyTrees.OnNotify(): Tree {} knocked down.".format(index))
