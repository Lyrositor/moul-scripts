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

## @package ahnyVogondolaRideV2
# Controls Kadisha's vogondola ride in Ahnonay.
# @author Adam Van Ornum
# @author Chris Purvis
# @date April 2004: Creation.

from Plasma import *
from PlasmaTypes import *

# Define the attributes that will be entered in Max.
GroupSelector = ptAttribDropDownList(1, "Group Selector", ("Hub", "Eng Hut", "Vogondola", "Vogondola Throttle", "Vogondola Reverse", "Call buttons"))

ActHubChairClick = ptAttribActivator(2, "Hub chair clickable")
BehHubChairClimb = ptAttribBehavior(3, "Hub chair climb beh")
RespHubChairLower = ptAttribNamedResponder(4, "Hub chair lower resp", ("lower", "raise"), netForce=1)

ActVogEjectFront = ptAttribActivator(5, "Vog eject front click")
ActVogEjectRear = ptAttribActivator(6, "Vog eject rear click")

ActVogThrottleF = ptAttribActivator(7, "Vog throttle forward click")
ActVogThrottleB = ptAttribActivator(8, "Vog throttle back click")
ActVogThrottleRevF = ptAttribActivator(9, "Vog throttle rev forward click")
ActVogThrottleRevB = ptAttribActivator(10, "Vog throttle rev back click")

ActVogDirection = ptAttribActivator(11, "Vog direction click")
ActVogDirectionRev = ptAttribActivator(12, "Vog direction rev click")

RespVogChairLower = ptAttribResponder(13, "Vog chair lower resp")
RespVogRotate = ptAttribResponder(14, "Vog rotate resp", ("back", "front"))
RespVogThrottle = ptAttribResponder(15, "Vog throttle resp", ("start", "stop"))
RespVogThrottleRev = ptAttribResponder(16, "Vog throttle rev resp", ("start", "stop"))
RespVogEjectHub = ptAttribResponder(17, "Vog eject hub resp", ("norotate", "rotate", "oneshot"), netForce=1)
RespVogEjectEngHut = ptAttribResponder(18, "Vog eject eng hut resp", ("norotate", "rotate", "oneshot"), netForce=1)

SoVogDummy = ptAttribSceneobject(19, "Vog avatar dummy")
SoVogSubworld = ptAttribSceneobject(20, "Vog subworld")

ActEngHutChairClick = ptAttribActivator(21, "Eng Hut chair clickable")
BehEngHutChairClimb = ptAttribBehavior(22, "Eng Hut chair climb beh")
RespEngHutChairLower = ptAttribNamedResponder(23, "Eng Hut chair lower resp", ("lower", "raise"), netForce=1)

ActTubeEndFromHub = ptAttribActivator(24, "Tube end from hub act")
ActTubeEndFromEngHut = ptAttribActivator(25, "Tube end from eng hut act")
ActSailEndToEngHut = ptAttribActivator(26, "Sail end to eng hut act")
ActSailEndToHub = ptAttribActivator(27, "Sail end to hub act")
ActHubRideEnd = ptAttribActivator(28, "Hub ride end act")
ActEngHutRideEnd = ptAttribActivator(29, "Eng hut ride end act")

RespVogRideStart = ptAttribResponder(30, "Vog ride start resp")
RespVogRideStop = ptAttribResponder(31, "Vog ride stop resp")
RespVogRideStartRev = ptAttribResponder(32, "Vog ride start rev resp")
RespVogRideStopRev = ptAttribResponder(33, "Vog ride stop rev resp")

RespVogRideReset = ptAttribResponder(38, "Vog ride reset resp", ("hub", "eng hut"))

SoEjectPointHub = ptAttribSceneobject(39, "eject point hub")
SoEjectPointEngHut = ptAttribSceneobject(40, "eject point eng hut")

ActCallButtonHub = ptAttribNamedActivator(41, "Hub vog call button")
ActCallButtonEngHut = ptAttribNamedActivator(42, "Eng hut vog call button")
RespHubCallbutton = ptAttribNamedResponder(43, "Hub call button resp")
RespEngHutCallbutton = ptAttribNamedResponder(44, "Eng hut call button resp")

RespSounds = ptAttribResponder(45, "Sound responder", ("hubtubeout", "hubtubein", "sailtohub", "sailtohut", "huttubeout", "huttubein", "stop"))

ActStopVogSoundForward = ptAttribActivator(46, "Vog snd stop forward act")
ActStopVogSoundBackward = ptAttribActivator(47, "Vog snd stop backward act")

ActHubChairClick.setVisInfo(1, ["Hub"])
BehHubChairClimb.setVisInfo(1, ["Hub"])
RespHubChairLower.setVisInfo(1, ["Hub"])
ActVogEjectFront.setVisInfo(1, ["Vogondola"])
ActVogEjectRear.setVisInfo(1, ["Vogondola"])

ActVogThrottleF.setVisInfo(1, ["Vogondola Throttle"])
ActVogThrottleB.setVisInfo(1, ["Vogondola Throttle"])
ActVogThrottleRevF.setVisInfo(1, ["Vogondola Throttle"])
ActVogThrottleRevB.setVisInfo(1, ["Vogondola Throttle"])
RespVogThrottle.setVisInfo(1, ["Vogondola Throttle"])
RespVogThrottleRev.setVisInfo(1, ["Vogondola Throttle"])

ActVogDirection.setVisInfo(1, ["Vogondola Reverse"])
ActVogDirectionRev.setVisInfo(1, ["Vogondola Reverse"])
RespVogRotate.setVisInfo(1, ["Vogondola Reverse"])

RespVogChairLower.setVisInfo(1, ["Vogondola"])
RespVogEjectHub.setVisInfo(1, ["Vogondola"])
RespVogEjectEngHut.setVisInfo(1, ["Vogondola"])
SoVogDummy.setVisInfo(1, ["Vogondola"])
SoVogSubworld.setVisInfo(1, ["Vogondola"])

ActEngHutChairClick.setVisInfo(1, ["Eng Hut"])
BehEngHutChairClimb.setVisInfo(1, ["Eng Hut"])
RespEngHutChairLower.setVisInfo(1, ["Eng Hut"])

ActTubeEndFromHub.setVisInfo(1, ["Vogondola"])
ActTubeEndFromEngHut.setVisInfo(1, ["Vogondola"])
ActSailEndToEngHut.setVisInfo(1, ["Vogondola"])
ActSailEndToHub.setVisInfo(1, ["Vogondola"])
ActHubRideEnd.setVisInfo(1, ["Vogondola"])
ActEngHutRideEnd.setVisInfo(1, ["Vogondola"])

RespVogRideStart.setVisInfo(1, ["Vogondola"])
RespVogRideStop.setVisInfo(1, ["Vogondola"])
RespVogRideStartRev.setVisInfo(1, ["Vogondola"])
RespVogRideStopRev.setVisInfo(1, ["Vogondola"])

ActCallButtonHub.setVisInfo(1, ["Call buttons"])
ActCallButtonEngHut.setVisInfo(1, ["Call buttons"])
RespHubCallbutton.setVisInfo(1, ["Call buttons"])
RespEngHutCallbutton.setVisInfo(1, ["Call buttons"])

RespVogRideReset.setVisInfo(1, ["Vogondola"])

SoEjectPointHub.setVisInfo(1, ["Vogondola"])
SoEjectPointEngHut.setVisInfo(1, ["Vogondola"])
RespSounds.setVisInfo(1, ["Vogondola"])

ActStopVogSoundForward.setVisInfo(1, ["Vogondola"])
ActStopVogSoundBackward.setVisInfo(1, ["Vogondola"])

## Disable the players' controls for the Vogondola.
def DisableVogControls(enabledControlList):

    disableControlList = (
        ActVogEjectFront, ActVogEjectRear, ActVogThrottleF, ActVogThrottleB,
        ActVogThrottleRevF, ActVogThrottleRevB, ActVogDirection,
        ActVogDirectionRev
    )

    if enabledControlList:
        for control in disableControlList:
            if control in enabledControlList:
                control.enable()
            else:
                control.disable()

## Toggles whether or not the vogondola is occupied.
# If occupant evaluates to True, it disables the access points; otherwise it
# enables them all.
def VogondolaIsOccupied(occupant):

    if occupant:
        PtDebugPrint(u"ahnyVogondolaRideV2.VogondolaIsOccupied(): Someone got in the Vogondola, disabling all access points.")
        ActHubChairClick.disable()
        ActEngHutChairClick.disable()
        ActCallButtonHub.disable()
        ActCallButtonEngHut.disable()
    else:
        PtDebugPrint(u"ahnyVogondolaRideV2.VogondolaIsOccupied(): Someone got out of the Vogondola, enabling all access points.")
        sdl = PtGetAgeSDL()
        vogLoc = sdl["ahnyVogLocation"][0]
        if vogLoc == 0:
            PtDebugPrint(u"ahnyVogondolaRideV2.VogondolaIsOccupied(): Hub Chair enabled.")
            ActHubChairClick.enable()
        elif vogLoc == 2:
            PtDebugPrint(u"ahnyVogondolaRideV2.VogondolaIsOccupied(): Hut Chair enabled.")
            ActEngHutChairClick.enable()

# Brains: determine what happens at the various stages.


## The brain for the Vogondola when in the hub.
class InHubBrain:

    name = "In Hub Brain"

    ## Initialize the brain.
    # Disables the necessary enabled controls.
    def __init__(self, parent):

        PtDebugPrint(u"ahnyVogondolaRideV2: Initializing {}.".format(self.name))
        self.parent = parent

        PtDisableMovementKeys()

        enabledControlList = [ActVogEjectFront, ActVogEjectRear, ActVogThrottleB]
        if self.parent.direction == 1:
            enabledControlList.append(ActVogDirection)
        elif self.parent.direction == -1:
            enabledControlList.append(ActVogDirectionRev)
        DisableVogControls(enabledControlList)

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Handles the various events that can occur.
    def OnNotify(self, state, ID, events):

        if ID == ActHubChairClick.id and state:
            PtDebugPrint(u"ahnyVogondolaRideV2.InHubBrain.OnNotify(): Hub Chair clicked, disable it.")
            ActHubChairClick.disable()
            avatar = PtFindAvatar(events)
            BehHubChairClimb.run(avatar)

        elif ID == BehHubChairClimb.id:
            for event in events:
                if event[0] == kMultiStageEvent and event[1] == 0 and event[2] == kEnterStage:
                    RespHubChairLower.run(self.parent.key, events=events, state="lower")
                    PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): {} finished smart-seek.".format(self.name))
                    
                elif event[0] == kMultiStageEvent and event[1] == 0 and event[2] == kAdvanceNextStage:
                    avatar = PtGetLocalAvatar()
                    avatar.avatar.enterSubWorld(SoVogSubworld.value)
                    avatar.physics.warpObj(SoVogDummy.value.getKey())
                    PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): {} pinned avatar.".format(self.name))
                    RespVogChairLower.run(self.parent.key, events=events)
                    
        elif ID == ActVogDirection.id and state:
            self.parent.direction = -1
            ActVogDirection.disable()
            ActVogThrottleB.disable()
            RespVogRotate.run(self.parent.key, state="back")
            ActVogDirectionRev.enable()

        elif ID == ActVogDirectionRev.id and state:
            self.parent.direction = 1
            ActVogDirectionRev.disable()
            RespVogRotate.run(self.parent.key, state="front")
            ActVogThrottleB.enable()
            ActVogDirection.enable()

        elif ID in (ActVogEjectFront.id, ActVogEjectRear.id) and state:
            DisableVogControls(None)
            RespVogEjectHub.run(self.parent.key, state="norotate" if ID == ActVogEjectFront.id else "rotate")
            sdl = PtGetAgeSDL()
            sdl["ahnyVogLocation"] = (0,)

        elif ID == ActVogThrottleB.id and state:
            DisableVogControls(None)
            RespVogRideStart.run(self.parent.key)

        elif ID == RespVogRideStart.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Running RespSounds (state: hubtubeout; location: Hub Brain RespVogRideStart).", level=kDebugDumpLevel)
            RespSounds.run(self.parent.key, state="hubtubeout")

        elif ID == ActTubeEndFromHub.id:
            RespVogRideStop.run(self.parent.key)
            self.parent.currentBrain = HubSailTubeTransitionBrain(self.parent)
            self.parent.direction = 1

        elif ID == RespVogEjectHub.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Ejecting from Vogondola at Hub. Removing brain.")
            avatar = PtGetLocalAvatar()
            RespHubChairLower.run(self.parent.key, avatar=avatar, state="raise")
            avatar.avatar.exitSubWorld()
            avatar.physics.warpObj(SoEjectPointHub.value.getKey())
            RespVogEjectHub.run(self.parent.key, avatar=avatar, state="oneshot")
            self.parent.currentBrain = None
            PtEnableMovementKeys()


## The brain for the Vogondola's Hub transition tube.
class HubSailTubeTransitionBrain:

    name = "Hub Sail Tube Transition Brain"

    ## Initialize the brain.
    # Disables the necessary enabled controls.
    def __init__(self, parent):

        PtDebugPrint(u"ahnyVogondolaRideV2: Initializing {}.".format(self.name))
        self.parent = parent

        enabledControlList = [ActVogThrottleB, ActVogThrottleRevB]
        if self.parent.direction == 1:
            enabledControlList.append(ActVogDirection)
        elif self.parent.direction == -1:
            enabledControlList.append(ActVogDirectionRev)
        DisableVogControls(enabledControlList)

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Handles the various events that can occur.
    def OnNotify(self, state, ID, events):

        if ID == ActVogDirection.id and state:
            ActVogDirection.disable()
            ActVogThrottleB.disable()
            self.parent.direction = -1
            RespVogRotate.run(self.parent.key, state="back")
            ActVogThrottleRevB.enable()
            ActVogDirectionRev.enable()

        elif ID == ActVogDirectionRev.id and state:
            ActVogDirectionRev.disable()
            ActVogThrottleRevB.disable()
            self.parent.direction = 1
            RespVogRotate.run(self.parent.key, state="front")
            ActVogThrottleB.enable()
            ActVogDirection.enable()

        elif ID == ActVogThrottleB.id and state:
            RespVogRideStart.run(self.parent.key)
            self.parent.currentBrain = SailingBrain(self.parent)
            self.parent.direction = 1

        elif ID == ActVogThrottleRevB.id and state:
            DisableVogControls(None)
            RespVogRideStartRev.run(self.parent.key)

        elif ID == RespVogRideStartRev.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Running RespSounds (state: hubtubein; location: Hub Transition RespVogRideStartRev).", level=kDebugDumpLevel)
            RespSounds.run(self.parent.key, state="hubtubein")

        elif ID == ActHubRideEnd.id:
            RespVogThrottle.run(self.parent.key, state="stop")
            self.parent.currentBrain = InHubBrain(self.parent)


## The brain for the Vogondola's sailing.
class SailingBrain:

    name = "Sailing Brain"

    ## Initialize the brain.
    # Disables the necessary enabled controls.
    def __init__(self, parent):

        PtDebugPrint(u"ahnyVogondolaRideV2: Initializing {}.".format(self.name))
        self.parent = parent

        enabledControlList = None
        if self.parent.direction == 1:
            enabledControlList = (ActVogThrottleF,)
        elif self.parent.direction == -1:
            enabledControlList = (ActVogThrottleRevF,)
        DisableVogControls(enabledControlList)

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Handles the various events that can occur.
    def OnNotify(self, state, ID, events):

        if (ID == ActVogThrottleF.id or ID == ActVogThrottleRevF.id) and state:
            RespVogRideStop.run(self.parent.key)
            enabledControlList = None
            
            if self.parent.direction == 1:
                enabledControlList = (ActVogThrottleB, ActVogDirection)
            elif self.parent.direction == -1:
                enabledControlList = (ActVogThrottleRevB, ActVogDirectionRev)

            DisableVogControls(enabledControlList)

        elif ID == RespVogRideStop.id or ID == RespVogRideStopRev.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Stopping Vogondola ride.")
            RespSounds.run(self.parent.key, state="stop")

        elif ID == ActVogDirection.id and state:
            ActVogDirection.disable()
            ActVogThrottleB.disable()
            self.parent.direction = -1
            RespVogRotate.run(self.parent.key, state="back")
            ActVogThrottleRevB.enable()
            ActVogDirectionRev.enable()

        elif ID == ActVogDirectionRev.id and state:
            ActVogDirectionRev.disable()
            ActVogThrottleRevB.disable()
            self.parent.direction = 1
            RespVogRotate.run(self.parent.key, state="front")
            ActVogThrottleB.enable()
            ActVogDirection.enable()

        elif ID == ActVogThrottleB.id and state:
            DisableVogControls((ActVogThrottleF,))
            RespVogRideStart.run(self.parent.key)

        elif ID == ActVogThrottleRevB.id and state:
            DisableVogControls((ActVogThrottleRevF,))
            RespVogRideStartRev.run(self.parent.key)

        elif ID == RespVogRideStart.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Running RespSounds (state: sailtohut; location: Sail Brain RespVogRideStart).", level=kDebugDumpLevel)
            RespSounds.run(self.parent.key, state="sailtohut")

        elif ID == RespVogRideStartRev.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Running RespSounds (state: sailtohub; location: Sail Brain RespVogRideStartRev).", level=kDebugDumpLevel)
            RespSounds.run(self.parent.key, state="sailtohub")

        elif ID == ActSailEndToEngHut.id and self.parent.direction == 1:
            RespVogRideStop.run(self.parent.key)
            self.parent.currentBrain = EngHutSailTubeTransitionBrain(self.parent)

        elif ID == ActSailEndToHub.id and self.parent.direction == -1:
            RespVogRideStop.run(self.parent.key)
            self.parent.currentBrain = HubSailTubeTransitionBrain(self.parent)


## The brain for the Vogondola's Hut transition tube.
class EngHutSailTubeTransitionBrain:

    name = "Eng Hut Sail Tube Transition Brain"

    ## Initialize the brain.
    # Disables the necessary enabled controls.
    def __init__(self, parent):

        PtDebugPrint(u"ahnyVogondolaRideV2: Initializing {}.".format(self.name))
        self.parent = parent

        enabledControlList = [ActVogThrottleB, ActVogThrottleRevB]
        if self.parent.direction == 1:
            enabledControlList.append(ActVogDirection)
        elif self.parent.direction == -1:
            enabledControlList.append(ActVogDirectionRev)
        DisableVogControls(enabledControlList)

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Handles the various events that can occur.
    def OnNotify(self, state, ID, events):

        if ID == ActVogDirection.id and state:
            ActVogDirection.disable()
            ActVogThrottleB.disable()
            self.parent.direction = -1
            RespVogRotate.run(self.parent.key, state="back")
            ActVogThrottleRevB.enable()
            ActVogDirectionRev.enable()

        elif ID == ActVogDirectionRev.id and state:
            ActVogDirectionRev.disable()
            ActVogThrottleRevB.disable()
            self.parent.direction = 1
            RespVogRotate.run(self.parent.key, state="front")
            ActVogThrottleB.enable()
            ActVogDirection.enable()

        elif ID == ActVogThrottleRevB.id and state:
            RespVogRideStartRev.run(self.parent.key)
            self.parent.currentBrain = SailingBrain(self.parent)
            self.parent.direction = -1

        elif ID == ActVogThrottleB.id and state:
            DisableVogControls(None)
            RespVogRideStart.run(self.parent.key)

        elif ID == RespVogRideStart.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Running RespSounds (state: huttubein; location: Sail Brain RespVogRideStart).", level=kDebugDumpLevel)
            RespSounds.run(self.parent.key, state="huttubein")

        elif ID == ActEngHutRideEnd.id:
            RespVogThrottle.run(self.parent.key, state="stop")
            self.parent.currentBrain = InEngHutBrain(self.parent)


## The brain for the Vogondola when in the hut.
class InEngHutBrain:

    name = "In Eng Hut Brain"

    ## Initialize the brain.
    # Disables the necessary enabled controls.
    def __init__(self, parent):

        PtDebugPrint(u"ahnyVogondolaRideV2: Initializing {}.".format(self.name))
        self.parent = parent

        PtDisableMovementKeys()

        enabledControlList = [ActVogEjectFront, ActVogEjectRear, ActVogThrottleRevB]
        if self.parent.direction == 1:
            enabledControlList.append(ActVogDirection)
        elif self.parent.direction == -1:
            enabledControlList.append(ActVogDirectionRev)
        DisableVogControls(enabledControlList)

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Handles the various events that can occur.
    def OnNotify(self, state, ID, events):

        if ID == ActEngHutChairClick.id and state:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Hut Chair clicked, disable it.")
            ActEngHutChairClick.disable()
            avatar = PtFindAvatar(events)
            BehEngHutChairClimb.run(avatar)

        elif ID == BehEngHutChairClimb.id:
            for event in events:
                if event[0] == kMultiStageEvent and event[1] == 0 and event[2] == kEnterStage:
                    RespEngHutChairLower.run(self.parent.key, events=events, state="lower")
                    PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): {} finished smart-seek.".format(self.name))
                    
                elif event[0] == kMultiStageEvent and event[1] == 0 and event[2] == kAdvanceNextStage:
                    avatar = PtGetLocalAvatar()
                    avatar.avatar.enterSubWorld(SoVogSubworld.value)
                    avatar.physics.warpObj(SoVogDummy.value.getKey())
                    PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): {} pinned avatar.".format(self.name))
                    RespVogChairLower.run(self.parent.key, events=events)
                    
        elif ID == ActVogDirection.id and state:
            ActVogDirection.disable()
            self.parent.direction = -1
            RespVogRotate.run(self.parent.key, state="back")
            ActVogThrottleRevB.enable()
            ActVogDirectionRev.enable()

        elif ID == ActVogDirectionRev.id and state:
            ActVogDirectionRev.disable()
            ActVogThrottleRevB.disable()
            self.parent.direction = 1
            RespVogRotate.run(self.parent.key, state="front")
            ActVogDirection.enable()

        elif ID == ActVogEjectFront.id and state:
            DisableVogControls(None)
            RespVogEjectEngHut.run(self.parent.key, state="norotate")
            sdl = PtGetAgeSDL()
            sdl["ahnyVogLocation"] = (2,)

        elif ID == ActVogEjectRear.id and state:
            DisableVogControls(None)
            RespVogEjectEngHut.run(self.parent.key, state="rotate")
            sdl = PtGetAgeSDL()
            sdl["ahnyVogLocation"] = (2,)

        elif ID == ActVogThrottleRevB.id and state:
            DisableVogControls(None)
            RespVogRideStartRev.run(self.parent.key)

        elif ID == RespVogRideStartRev.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Running RespSounds (state: huttubeout; location: Sail Brain RespVogRideStartRev).", level=kDebugDumpLevel)
            RespSounds.run(self.parent.key, state="huttubeout")

        elif ID == ActTubeEndFromEngHut.id:
            RespVogRideStop.run(self.parent.key)
            self.parent.currentBrain = EngHutSailTubeTransitionBrain(self.parent)
            self.parent.direction = -1

        elif ID == RespVogEjectEngHut.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Ejecting from Vogondola at HuT. Removing brain.")
            avatar = PtGetLocalAvatar()
            RespEngHutChairLower.run(self.parent.key, avatar=avatar, state="raise")
            avatar.avatar.exitSubWorld()
            avatar.physics.warpObj(SoEjectPointEngHut.value.getKey())
            RespVogEjectEngHut.run(self.parent.key, avatar=avatar, state="oneshot")
            self.parent.currentBrain = None
            PtEnableMovementKeys()


## The responder for Ahnonay's Vogondola ride.
# Controls the Vogondola's behavior.
class ahnyVogondolaRideV2(ptResponder):

    id = 5338
    version = 2

    ## Initialize the responder.
    def __init__(self):

        PtDebugPrint(u"ahnyVogondolaRideV2: Version {}.".format(self.version))
        ptResponder.__init__(self)
        self.currentBrain = None
        self.direction = 1
        self.occupant = None
        self.throttle = 0

    ## Called by Plasma on receipt of the first plEvalMsg.
    # Sets up the Vogondola's default state from SDL settings.
    def OnFirstUpdate(self):

        ageSDL = PtGetAgeSDL()
        if not ageSDL:  # This should never happen, but we don't trust eap.
            PtDebugPrint(u"ahnyVogondolaRideV2.OnFirstUpdate(): Cannot find Ahnonay's Age SDL.", level=kErrorLevel)
            return

        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags("ahnyVogLocation", 1, 1)
        ageSDL.sendToClients("ahnyVogLocation")
        ageSDL.setNotify(self.key, "ahnyVogLocation", 0.0)
        
        ageSDL.setFlags("ahnyVogOccupant", 1, 1)
        ageSDL.sendToClients("ahnyVogOccupant")
        ageSDL.setNotify(self.key, "ahnyVogOccupant", 0.0)
        
        # First update, all buttons disabled.
        ActCallButtonHub.disable()
        ActCallButtonEngHut.disable()
        ActHubChairClick.disable()
        ActEngHutChairClick.disable()
        
        if ageSDL["ahnyVogOccupant"][0]:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnFirstUpdate(): {} is in the Vogondola.".format(ageSDL["ahnyVogOccupant"][0]))
            self.occupant = ageSDL["ahnyVogOccupant"][0]
        else:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnFirstUpdate(): Vogondola is empty.")
            PtAtTimeCallback(self.key, 0, 1)

    ## Called by Plasma when a timer is over.
    # Enables buttons or raises the chair.
    def OnTimer(self, ID):

        if ID == 1:
            sdl = PtGetAgeSDL()
            vogLoc = sdl["ahnyVogLocation"][0]

            # vogLoc: 0 = hub, 1 = in between, 2 = engineer hut.
            if vogLoc == 0:
                PtDebugPrint(u"ahnyVogondolaRideV2.OnTimer(): Hut Call and Hub Chair enabled.")
                ActCallButtonEngHut.enable()
                ActHubChairClick.enable()

            elif vogLoc == 1:
                PtDebugPrint(u"ahnyVogondolaRideV2.OnTimer(): Hut Call and Hub Call enabled.")
                ActCallButtonEngHut.enable()
                ActCallButtonHub.enable()
                RespHubChairLower.run(self.key, state="lower", fastforward=1)

            elif vogLoc == 2:
                PtDebugPrint(u"ahnyVogondolaRideV2.OnTimer(): Hut Chair and Hub Call enabled.")
                ActCallButtonHub.enable()
                ActEngHutChairClick.enable()
                RespEngHutChairLower.run(self.key, state="raise", fastforward=1)
                RespHubChairLower.run(self.key, state="lower", fastforward=1)
                RespVogRideStart.run(self.key, fastforward=1)
                RespVogThrottle.run(self.key, state="stop", fastforward=1)

        elif ID == 2:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnTimer(): Raising chair in Hub.")
            RespHubChairLower.run(self.key, state="raise")

        elif ID == 3:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnTimer(): Raising chair in Hut.")
            RespEngHutChairLower.run(self.key, state="raise")


    ## Called by Plasma when an avatar is paged into the Age.
    # Checks whether the buttons should be enabled.
    def AvatarPage(self, avObj, pageIn, lastOut):

        if not pageIn and self.occupant:
            avID = PtGetClientIDFromAvatarKey(avObj.getKey())
            if avID == PtGetClientIDFromAvatarKey(self.occupant.getKey()):
                PtDebugPrint(u"ahnyVogondolaRideV2.AvatarPage(): Vogondola rider left; enabling call buttons.")
                ActCallButtonHub.enable()
                ActCallButtonEngHut.enable()
                sdl = PtGetAgeSDL()
                sdl["ahnyVogOccupant"] = (0,)
                self.occupant = None

    ## Called by Plasma on receipt of a plNotifyMsg.
    # Manages the Vogondola behavior.
    def OnNotify(self, state, ID, events):

        PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Notify state = {}, ID = {}.".format(state, ID), level=kDebugDumpLevel)
        
        if ID == ActHubChairClick.id and state:
            sdl = PtGetAgeSDL()
            sdl["ahnyVogLocation"] = (1,)
            sdl["ahnyVogOccupant"] = (PtFindAvatar(events).getKey(),)
            self.occupant = PtFindAvatar(events)
            VogondolaIsOccupied(True)

            if PtFindAvatar(events) == PtGetLocalAvatar():
                cam = ptCamera()
                cam.undoFirstPerson()
                cam.disableFirstPersonOverride()
                RespVogRideReset.run(self.key, state="hub", fastforward=1)
                self.direction = 1
                self.currentBrain = InHubBrain(self)
                self.currentBrain.OnNotify(state, ID, events)

        elif ID == ActEngHutChairClick.id and state:
            sdl = PtGetAgeSDL()
            sdl["ahnyVogLocation"] = (1,)
            sdl["ahnyVogOccupant"] = (PtFindAvatar(events).getKey(),)
            self.occupant = PtFindAvatar(events)
            VogondolaIsOccupied(True)

            if PtFindAvatar(events) == PtGetLocalAvatar():
                cam = ptCamera()
                cam.undoFirstPerson()
                cam.disableFirstPersonOverride()
                RespVogRideReset.run(self.key, state="eng hut", fastforward=1)
                self.direction = 1
                self.currentBrain = InEngHutBrain(self)
                self.currentBrain.OnNotify(state, ID, events)

        elif ID == ActCallButtonHub.id and state:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Call button for Hub clicked.")
            VogondolaIsOccupied(True)
            RespHubCallbutton.run(self.key, events=events)
            sdl = PtGetAgeSDL()
            if sdl["ahnyVogLocation"][0] == 2:
                RespEngHutChairLower.run(self.key, state="lower")
            sdl["ahnyVogLocation"] = (0,)

        elif ID == RespHubCallbutton.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Call button for Hub returned.")
            PtAtTimeCallback(self.key, 5, 2)

        elif ID == ActCallButtonEngHut.id and state:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Call button for Hut clicked.")
            VogondolaIsOccupied(True)
            RespEngHutCallbutton.run(self.key, events=events)
            sdl = PtGetAgeSDL()
            if sdl["ahnyVogLocation"][0] == 0:
                RespHubChairLower.run(self.key, state="lower")
            sdl["ahnyVogLocation"] = (2,)

        elif ID == RespEngHutCallbutton.id:
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Call button for Hut returned.")
            PtAtTimeCallback(self.key, 5, 3)

        elif ID == RespHubChairLower.id and self.currentBrain == None:
            if self.occupant == PtGetLocalAvatar():
                PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Hub Chair came up and was enabled.")
                ActHubChairClick.enable()
                cam = ptCamera()
                cam.enableFirstPersonOverride()
            else:
                VogondolaIsOccupied(False)

            sdl = PtGetAgeSDL()
            sdl["ahnyVogOccupant"] = (0,)
            self.occupant = None
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Hub Chair came up and Hut Call was enabled.")
            ActCallButtonEngHut.enable()
            
        elif ID == RespEngHutChairLower.id and self.currentBrain == None:
            if self.occupant == PtGetLocalAvatar():
                PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Hut Chair came up and was enabled.")
                ActEngHutChairClick.enable()
                cam = ptCamera()
                cam.enableFirstPersonOverride()
            else:
                VogondolaIsOccupied(False)
            
            sdl = PtGetAgeSDL()
            sdl["ahnyVogOccupant"] = (0,)
            self.occupant = None
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Hut Chair came up and Hub Call was enabled.")
            ActCallButtonHub.enable()

        elif (ID == ActStopVogSoundForward.id or ID == ActStopVogSoundBackward.id) and state:
            ActStopVogSoundForward.disable()
            ActStopVogSoundBackward.disable()
            PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Running RespSounds (state: stop; location: Anim Event Det).", level=kDebugDumpLevel)
            RespSounds.run(self.key, state="stop")

        else:
            if self.currentBrain:
                # Passing event on to sub-brain.
                self.currentBrain.OnNotify(state, ID, events)

    ## Called by Plasma on receipt of a backdoor message.
    # Used to debug the state of the Vogondola.
    def OnBackdoorMsg(self, target, param):

        if target == "vog":
            if param == "currentbrain":
                PtDebugPrint(u"ahnyVogondolaRideV2.OnNotify(): Vogondola Current Brain = {}.".format(None if not self.currentBrain else self.currentBrain.name))
