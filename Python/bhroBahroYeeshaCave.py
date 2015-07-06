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
Module: bhroBahroYeeshaCave.py
Age: BahroCave
Date: June 2003
Author: Adam Van Ornum
Controls the bahro cave side of the bahro pole stuff
"""

from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import xRandom
from xPsnlVaultSDL import *
import copy

# Max attributes
respTeledahnWedge = ptAttribResponder(1, "Tldn wedge resp")
respGarrisonWedge = ptAttribResponder(2, "Grsn wedge resp")
respGardenWedge = ptAttribResponder(3, "Grdn wedge resp")
respKadishWedge = ptAttribResponder(4, "Kdsh wedge resp")

soTeledahnPoleCollider = ptAttribSceneobject(5, "Tldn pole collider")
soGarrisonPoleCollider = ptAttribSceneobject(6, "Grsn pole collider")
soGardenPoleCollider = ptAttribSceneobject(7, "Grdn pole collider")
soKadishPoleCollider = ptAttribSceneobject(8, "Kdsh pole collider")

respTeledahnPoleRemove = ptAttribResponder(9, "Tldn remove pole resp", ["Remove", "PutBack", "Reject"])
respGarrisonPoleRemove = ptAttribResponder(10, "Grsn remove pole resp", ["Remove", "PutBack", "Reject"])
respGardenPoleRemove = ptAttribResponder(11, "Grdn remove pole resp", ["Remove", "PutBack", "Reject"])
respKadishPoleRemove = ptAttribResponder(12, "Kdsh remove pole resp", ["Remove", "PutBack", "Reject"])

respTeledahnJCDisable = ptAttribResponder(13, "Tldn JC disable resp")
respGarrisonJCDisable = ptAttribResponder(14, "Grsn JC disable resp")
respGardenJCDisable = ptAttribResponder(15, "Grdn JC disable resp")
respKadishJCDisable = ptAttribResponder(16, "Kdsh JC disable resp")

clickTeledahnJC = ptAttribActivator(17, "Tldn JC clickable")
clickGarrisonJC = ptAttribActivator(18, "Grsn JC clickable")
clickGardenJC = ptAttribActivator(19, "Grdn JC clickable")
clickKadishJC = ptAttribActivator(20, "Kdsh JC clickable")

respTeledahnSolutionSymbols = ptAttribResponder(21, "Tldn solution symbols", ["0", "1", "2", "3", "4", "5", "6"])
respGarrisonSolutionSymbols = ptAttribResponder(22, "Grsn solution symbols", ["0", "1", "2", "3", "4", "5", "6"])
respGardenSolutionSymbols = ptAttribResponder(23, "Grdn solution symbols", ["0", "1", "2", "3", "4", "5", "6"])
respKadishSolutionSymbols = ptAttribResponder(24, "Kdsh solution symbols", ["0", "1", "2", "3", "4", "5", "6"])

clickTeledahnYS = ptAttribActivator(25, "Tldn YS clickable")
clickGarrisonYS = ptAttribActivator(26, "Grsn YS clickable")
clickGardenYS = ptAttribActivator(27, "Grdn YS clickable")
clickKadishYS = ptAttribActivator(28, "Kdsh YS clickable")

respTeledahnYS = ptAttribResponder(29, "Tldn yeesha speech")
respGarrisonYS = ptAttribResponder(30, "Grsn yeesha speech")
respGardenYS = ptAttribResponder(31, "Grdn yeesha speech")
respKadishYS = ptAttribResponder(32, "Kdsh yeesha speech")

respTeledahnJCOneShot = ptAttribResponder(33, "Tldn JC one shot resp")
respGarrisonJCOneShot = ptAttribResponder(34, "Grsn JC one shot resp")
respGardenJCOneShot = ptAttribResponder(35, "Grdn JC one shot resp")
respKadishJCOneShot = ptAttribResponder(36, "Kdsh JC one shot resp")

respTeledahnYSOneShot = ptAttribResponder(37, "Tldn YS one shot resp", ["trigger", "glowstart", "glowend"])
respGarrisonYSOneShot = ptAttribResponder(38, "Grsn YS one shot resp", ["trigger", "glowstart", "glowend"])
respGardenYSOneShot = ptAttribResponder(39, "Grdn YS one shot resp", ["trigger", "glowstart", "glowend"])
respKadishYSOneShot = ptAttribResponder(40, "Kdsh YS one shot resp", ["trigger", "glowstart", "glowend"])

respSequentialYS = ptAttribResponder(41, "Sequential yeesha speeches", ["1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b"])

rgnLinkOut = ptAttribActivator(42, "Link out region")
respLinkOut = ptAttribResponder(43, "Link out responder", ["starfield", "cavern"])

respStarCavern = ptAttribResponder(44, "Starfield/cavern vis", ["StarVis", "CavernVis"])

respKillSpeeches = ptAttribResponder(45, "Kill yeesha speeches", ["a", "age", "b"])

respBahroScream = ptAttribResponder(46, "Bahro scream")

rgnCaveJump = ptAttribActivator(47, "Cave jump region")

kWriteTimestamps = 8

# Bahro pole SDL variable states
#   0: Initial state, no pole, hydrant up, sheath up, clicking hand changes to state 1
#      Anim sheath down
#   1: No pole, hydrant up, sheath down, clicking hand causes full glow
#   2: After book has been used, No pole, hydrant up, sheath up, clicking hand causes progress glow
#   3: Animate the hydrant down and proceed to state 4
#   4: All cloths have been found and pole was sent to psnl age, pole is there, hydrant down, clicking hand does nothing
#   5: Anim all hydrants up and proceed to state 6
#   6: All poles in psnl age, pole is there, hydrant up, clicking hand plays full glow
#   7: Anim fissure stuff
#   8: Pole returned, no pole, hydrant up, clicking hand plays full glow
#   9: Selfish person unreturned pole, no pole, hydrant up, clicking hand plays full glow


class bhroBahroYeeshaCave(ptModifier):
    """Bahro pole state control script."""

    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5315
        self.version = 6
        PtDebugPrint("bhroBahroYeeshaCave: v{}".format(self.version), level=kWarningLevel)

        self.ageFrom = ""
        self.AgePlaying = ""
        self.currentYS = "zz"
        self.IsStarfield = True
        self.SpeechRespReset = True
        self.varMap = {"YeeshaSymbolTouched": 0, "SolutionSymbol": 1, "YeeshaSpeech": 2}

        self.ageDict = {
            "Teledahn": {
                "State": 0,
                "SDL": "psnlBahroWedge04",
                "WedgeAnim": respTeledahnWedge,
                "PoleCollider": soTeledahnPoleCollider,
                "JCDisable": respTeledahnJCDisable,
                "JCClickable": clickTeledahnJC,
                "SolutionSymbols": respTeledahnSolutionSymbols,
                "YSClickable": clickTeledahnYS,
                "YeeshaSpeech": respTeledahnYS,
                "PoleRemove": respTeledahnPoleRemove,
                "OneShotYS": respTeledahnYSOneShot,
                "OneShotJC": respTeledahnJCOneShot
            },
            "Garrison": {
                "State": 0,
                "SDL": "psnlBahroWedge01",
                "WedgeAnim": respGarrisonWedge,
                "PoleCollider": soGarrisonPoleCollider,
                "JCDisable": respGarrisonJCDisable,
                "JCClickable": clickGarrisonJC,
                "SolutionSymbols": respGarrisonSolutionSymbols,
                "YSClickable": clickGarrisonYS,
                "YeeshaSpeech": respGarrisonYS,
                "PoleRemove": respGarrisonPoleRemove,
                "OneShotYS": respGarrisonYSOneShot,
                "OneShotJC": respGarrisonJCOneShot
            },
            "Garden": {
                "State": 0,
                "SDL": "psnlBahroWedge02",
                "WedgeAnim": respGardenWedge,
                "PoleCollider": soGardenPoleCollider,
                "JCDisable": respGardenJCDisable,
                "JCClickable": clickGardenJC,
                "SolutionSymbols": respGardenSolutionSymbols,
                "YSClickable": clickGardenYS,
                "YeeshaSpeech": respGardenYS,
                "PoleRemove": respGardenPoleRemove,
                "OneShotYS": respGardenYSOneShot,
                "OneShotJC": respGardenJCOneShot
            },
            "Kadish": {
                "State": 0,
                "SDL": "psnlBahroWedge03",
                "WedgeAnim": respKadishWedge,
                "PoleCollider": soKadishPoleCollider,
                "JCDisable": respKadishJCDisable,
                "JCClickable": clickKadishJC,
                "SolutionSymbols": respKadishSolutionSymbols,
                "YSClickable": clickKadishYS,
                "YeeshaSpeech": respKadishYS,
                "PoleRemove": respKadishPoleRemove,
                "OneShotYS": respKadishYSOneShot,
                "OneShotJC": respKadishJCOneShot
            }
        }

    def OnFirstUpdate(self):
        PtDebugPrint("bhroBahroYeeshaCave.OnFirstUpdate(): Everything ok so far.", level=kDebugDumpLevel)
        xRandom.seed()
        xRandom.setmaxseries(1)

        PtSendKIMessage(kDisableYeeshaBook, 0)

        vault = ptVault()
        entry = vault.findChronicleEntry("BahroCave")
        if entry is None:
            PtDebugPrint("bhroBahroYeeshaCave.OnFirstUpdate(): Did not find BahroCave chronicle, creating.", level=kWarningLevel)
            vault.addChronicleEntry("BahroCave", 0, "0")

    def OnServerInitComplete(self):
        self.ageFrom = PtGetPrevAgeName()
        if not self.ageFrom:
            self.ageFrom = "Garrison"
        PtDebugPrint("bhroBahroYeeshaCave.OnServerInitComplete(): Came from: {}.".format(self.ageFrom), level=kDebugDumpLevel)

        # Check if a cleft Yeesha imager solution has already been created, otherwise create it
        if not self.CheckForSolution():
            PtDebugPrint("bhroBahroYeeshaCave.OnServerInitComplete(): No solution found, attempting to create.", level=kDebugDumpLevel)
            self.CreateSolution()

        self.UpdatePoleStates()
        self.UpdateToState2()

        # check and see if the yeesha speech variable has been set yet
        autostart = False
        self.UseYeeshaSpeech = self.GetAgeVariable(self.ageFrom, "YeeshaSpeech")
        PtDebugPrint("bhroBahroYeeshaCave.UseYeeshaSpeech = {}".format(self.UseYeeshaSpeech), level=kDebugDumpLevel)
        if self.UseYeeshaSpeech is not None:
            if int(self.UseYeeshaSpeech) == 0:
                self.UseYeeshaSpeech = self.GetNumYSSet() + 1
                if self.GetAutoStartLevel() < self.UseYeeshaSpeech:
                    autostart = True
                    self.IncrementAutoStartLevel()
                PtDebugPrint("bhroBahroYeeshaCave.GetAutoStartLevel = {}".format(self.GetAutoStartLevel()), level=kDebugDumpLevel)

        PtDebugPrint("bhroBahroYeeshaCave.OnServerInitComplete(): autostart = {}".format(autostart), level=kDebugDumpLevel)

        journeyComplete = False
        sdl = xPsnlVaultSDL()
        if sdl["CleftVisited"][0]:
            journeyComplete = True

        # Process stuff for each age
        starCavernRun = False
        for ageName, age in self.ageDict.items():
            currentState = age["State"]
            PtDebugPrint("bhroBahroYeeshaCave.OnServerInitComplete(): Current state for {}: {}".format(ageName, currentState), level=kDebugDumpLevel)
            
            # If the age is not the one that I'm from then run the responder to make it back off
            if age != self.ageFrom and currentState < 8:
                age["WedgeAnim"].run(self.key, fastforward=1)

            if not starCavernRun and currentState > 5:
                respStarCavern.run(self.key, state="CavernVis", fastforward=1)
                starCavernRun = True
                self.IsStarfield = False

            # cCheck the current state to see if the pole is here or not
            if currentState in (4, 5, 6, 9):
                self.DisablePole(age, 1)

            # Check the current state to see if the journey symbol should show up or not
            if currentState == 4 or (currentState > 6 and not journeyComplete):
                age["JCDisable"].run(self.key, fastforward=1)

            # Display the appropriate solution symbol
            val = self.GetAgeVariable(ageName, "SolutionSymbol")
            age["SolutionSymbols"].run(self.key, state=val, fastforward=1)

        if not starCavernRun:
            respStarCavern.run(self.key, state="StarVis", fastforward=1)

        if autostart:
            PtAtTimeCallback(self.key, 3, 1)

    def OnNotify(self, state, id, events):
        PtDebugPrint("bhroBahroYeeshaCave.OnNotify(): id={}".format(id), level=kDebugDumpLevel)

        if not state:
            return

        # Notify from JC click
        for ageName, age in self.ageDict.items():
            if id == age["JCClickable"].id:
                self.JCClickHandle(ageName)
                break
            elif id == age["YSClickable"].id:
                self.YSClickHandle(ageName)
                break
            elif id == age["OneShotJC"].id:
                self.PostJCOneShot(ageName)
                break
            elif id == age["OneShotYS"].id:
                self.PostYSOneShot(ageName)
                break
            elif id == age["YeeshaSpeech"].id:
                self.SpeechRespReset = True
                self.PlayYeeshaSpeech(ageName)
                break
            elif id == age["PoleRemove"].id:
                self.PostPoleRemove(ageName)
                break
        else:
            # Notify from sequential speech series
            if id == respSequentialYS.id:
                self.SpeechRespReset = True
                self.PlayYeeshaSpeech(self.ageFrom)

            # Notify hitting link region
            elif id == rgnLinkOut.id:
                self.LinkOut()

            # Notify from cave jump force 3rd person region
            elif id == rgnCaveJump.id:
                cam = ptCamera()
                cam.undoFirstPerson()
                cam.disableFirstPersonOverride()
                PtDebugPrint("bhroBahroYeeshaCave.OnNotify(): Undid first person and disabled override.", level=kDebugDumpLevel)
    
    def OnTimer(self, id):
        PtDebugPrint("bhroBahroYeeshaCave.OnTimer(): id={}".format(id), level=kDebugDumpLevel)
        if id == 1:
            self.PostYSOneShot(self.ageFrom, 1)

        elif id == 2:
            cam = ptCamera()
            cam.enableFirstPersonOverride()

    def UpdatePoleStates(self):
        psnlSDL = xPsnlVaultSDL()
        sdllist = psnlSDL.BatchGet(["{}PoleState".format(a) for a in self.ageDict])
        for ageName, age in self.ageDict.items():
            age["State"] = sdllist[ageName + "PoleState"]

    def SetState(self, age, state):
        if isinstance(state, int):
            psnlSDL = xPsnlVaultSDL()
            psnlSDL[age + "PoleState"] = (state,)

    def GetAgeNode(self, age):
        vault = ptVault()
        chron = vault.findChronicleEntry("BahroCave")
        ageChronRefList = chron.getChildNodeRefList()

        for ageChron in ageChronRefList:
            ageChild = ageChron.getChild()
            ageChild = ageChild.upcastToChronicleNode()
            if ageChild.chronicleGetName() == age:
                return ageChild
        return None

    def GetAgeVariable(self, age, variable):
        node = self.GetAgeNode(age)

        if node is not None:
            varlist = node.chronicleGetValue().split(",")
            return varlist[self.varMap[variable]]
        else:
            return None

    def SetAgeVariable(self, age, variable, value):
        node = self.GetAgeNode(age)

        if node is not None:
            varlist = node.chronicleGetValue().split(",")
            while len(varlist) < len(self.varMap):
                varlist.append("0")
            varlist[self.varMap[variable]] = str(value)
            varstr = ""
            for var in range(len(varlist) - 1):
                varstr += (varlist[var] + ",")
            varstr += varlist[-1]
            
            node.chronicleSetValue(varstr)
            node.save()
        else:
            raise RuntimeError("Could not find chronicle variable to set")

    def AreListsEquiv(self, list1, list2):
        if list1[0] in list2 and len(list1) == len(list2):
            # rearrange list
            list2Copy = copy.copy(list2)
            while list2Copy[0] != list1[0]:
                list2Copy.append(list2Copy.pop(0))

            # check if all values match up now
            for i in range(4):
                if list2Copy[i] != list1[i]:
                    return False
            return True
        
        return False

    def CheckForSolution(self):
        return self.GetAgeVariable("Teledahn", "SolutionSymbol") is not None

    def CreateSolution(self):
        solutionlist = [3, 2, 5, 0]
        cleftSolList = [3, 2, 5, 0]

        while self.AreListsEquiv(solutionlist, cleftSolList):
            solutionlist = []
            while len(solutionlist) < 4:
                newint = xRandom.randint(0, 6)
                if newint not in solutionlist:
                    solutionlist.append(newint)

        vault = ptVault()
        entry = vault.findChronicleEntry("BahroCave")
        if entry is not None:
            for v, ageName in enumerate(self.ageDict):
                newnode = ptVaultChronicleNode(0)
                newnode.chronicleSetName(ageName)
                newnode.chronicleSetValue("0," + str(solutionlist[v]) + ",0")
                entry.addNode(newnode)

    def DisablePole(self, age, fforward=0):
        self.ageDict[age]["PoleRemove"].run(self.key, state="Remove", fastforward=fforward)
        self.ageDict[age]["PoleCollider"].value.physics.suppress(1)
        if not fforward:
            vault = ptVault()
            if vault is not None:  # Is the Vault online?
                psnlSDL = vault.getPsnlAgeSDL()
                if psnlSDL:
                    ypageSDL = psnlSDL.findVar("YeeshaPage25")
                    if ypageSDL:
                        size, state = divmod(ypageSDL.getInt(), 10)
                        PtDebugPrint("bhroBahroYeeshaCave.DisablePole(): YeeshaPage25={}".format(state), level=kDebugDumpLevel)
                        if state == 1:
                            PtDebugPrint("bhroBahroYeeshaCave.DisablePole(): Sending the pole and YeeshaPage25 is on! Will do the age's wedge...", level=kWarningLevel)
                            self.DoWedge()

    def EnablePole(self, age, fforward=0):
        self.ageDict[age]["PoleRemove"].run(self.key, state="PutBack", fastforward=fforward)
        self.ageDict[age]["PoleCollider"].value.physics.suppress(0)

    def JCClickHandle(self, age):
        cam = ptCamera()
        cam.undoFirstPerson()
        cam.disableFirstPersonOverride()
        PtAtTimeCallback(self.key, 5, 2)

        avatar = PtGetLocalAvatar()
        self.ageDict[age]["OneShotJC"].run(self.key, avatar=avatar)

    def YSClickHandle(self, age):
        avatar = PtGetLocalAvatar()
        self.ageDict[age]["OneShotYS"].run(self.key, avatar=avatar, state="trigger")

    def PostPoleRemove(self, age):
        self.ageDict[age]["JCClickable"].enable()

    def PostJCOneShot(self, age):
        vault = ptVault()
        if vault is not None:  # Is the Vault online?
            psnlSDL = vault.getPsnlAgeSDL()
            if psnlSDL:
                ypageSDL = psnlSDL.findVar("YeeshaPage25")
                if ypageSDL:
                    size, state = divmod(ypageSDL.getInt(), 10)
                    PtDebugPrint("bhroBahroYeeshaCave.PostJCOneShot(): YeeshaPage25={}".format(state), level=kDebugDumpLevel)
                    if state != 1:
                        PtDebugPrint("bhroBahroYeeshaCave.PostJCOneShot(): Can't send pole to Relto, YeeshaPage25 is off! Returning the pole...", level=kWarningLevel)
                        self.ageDict[age]["JCClickable"].disable()
                        self.ageDict[age]["PoleRemove"].run(self.key, state="Reject")
                        return
                    
        self.UpdatePoleStates()

        state = self.ageDict[age]["State"]

        PtDebugPrint("bhroBahroYeeshaCave.PostJCOneShot(): Current {} state: {}".format(age, state), level=kDebugDumpLevel)
        self.ageDict[age]["JCClickable"].disable()

        if state == 2:
            self.DisablePole(age)
            self.SetState(age, 3)
        elif state == 3:
            self.EnablePole(age)
            self.SetState(age, 2)
        elif state == 6:
            self.EnablePole(age)
            self.SetState(age, 7)
        elif state == 7:
            self.DisablePole(age)
            self.SetState(age, 6)
        elif state == 8:
            polesInPsnl = 1
            for ageName, age in self.ageDict.items():
                if age["State"] == 9:
                    polesInPsnl += 1
            if polesInPsnl == 1:
                PtDebugPrint("bhroBahroYeeshaCave.PostJCOneShot(): Playing Bahro Cave bahro scream", level=kWarningLevel)
                respBahroScream.run(self.key)
            self.DisablePole(age)
            self.SetState(age, 9)
        elif state == 9:
            self.EnablePole(age)
            self.SetState(age, 8)

    def PostYSOneShot(self, age, autotriggered=0):
        if self.AgePlaying != age:
            self.ageDict[age]["OneShotYS"].run(self.key, state="glowstart")
            
        prevage = self.AgePlaying
        self.AgePlaying = age
        
        if self.currentYS != "zz":
            PtDebugPrint("bhroBahroYeeshaCave.PostYSOneShot(): Killing speech {}.".format(self.currentYS), level=kDebugDumpLevel)
            respKillSpeeches.run(self.key, state=self.currentYS)
            self.currentYS = "zz"
            self.ageDict[prevage]["OneShotYS"].run(self.key, state="glowend")
            if prevage == age:
                self.AgePlaying = ""
                return

        if not int(self.GetAgeVariable(age, "YeeshaSymbolTouched")) and not autotriggered:
            PtDebugPrint("bhroBahroYeeshaCave.PostYSOneShot(): First time touching the symbol.", level=kWarningLevel)
            self.SetAgeVariable(age, "YeeshaSymbolTouched", 1)

        self.PlayYeeshaSpeech(age)

    def PlayYeeshaSpeech(self, age):
        if not self.SpeechRespReset or self.AgePlaying == "":
            return
        
        if age != self.AgePlaying:
            age = self.AgePlaying
        
        speech = self.GetAgeVariable(age, "YeeshaSpeech")
        if int(speech) == 0:
            speech = str(self.UseYeeshaSpeech)
        
        if self.currentYS == "a":
            self.currentYS = "age"
        elif self.currentYS == "age":
            self.currentYS = "b"
        elif self.currentYS == "b":
            self.currentYS = "zz"
            self.AgePlaying = ""
        else:
            self.currentYS = "a"

        if self.currentYS == "age":
            PtDebugPrint("bhroBahroYeeshaCave.PlayYeeshaSpeech(): Playing 'ge' YeeshaSpeech for: ".format(age), level=kDebugDumpLevel)
            self.ageDict[age]["YeeshaSpeech"].run(self.key)
            self.SpeechRespReset = False
        elif self.currentYS != "zz":
            PtDebugPrint("bhroBahroYeeshaCave.PlayYeeshaSpeech(): Playing 'sequential' YeeshaSpeech...", level=kDebugDumpLevel)
            PtDebugPrint("bhroBahroYeeshaCave.PlayYeeshaSpeech(): speech={}".format(speech), level=kDebugDumpLevel)
            PtDebugPrint("bhroBahroYeeshaCave.currentYS={}".format(self.currentYS), level=kDebugDumpLevel)
            state = speech + self.currentYS
            PtDebugPrint("bhroBahroYeeshaCave.PlayYeeshaSpeech(): state={}".format(state), level=kDebugDumpLevel)
            respSequentialYS.run(self.key, state)
            self.SpeechRespReset = False
        else:
            self.ageDict[age]["OneShotYS"].run(self.key, state="glowend")

    def GetNumYSSet(self):
        num = 0
        for age in self.ageDict:
            if int(self.GetAgeVariable(age, "YeeshaSpeech")):
                num += 1
        return num

    def LinkOut(self):
        polesInPsnl = 0
        updateAgeList = []

        psnlSDL = xPsnlVaultSDL()
        for age in self.ageDict:
            agevar = age + "PoleState"
            sdlval = psnlSDL[agevar][0]
            if sdlval == 4 and age != self.ageFrom:
                polesInPsnl += 1
                updateAgeList.append((agevar, (5,)))
            elif sdlval == 3 and age == self.ageFrom:
                if int(self.GetAgeVariable(self.ageFrom, "YeeshaSpeech")) == 0:
                    self.SetAgeVariable(self.ageFrom, "YeeshaSpeech", self.UseYeeshaSpeech)

        if polesInPsnl == 3 and psnlSDL[self.ageFrom + "PoleState"][0] == 3:
            psnlSDL.BatchSet(updateAgeList)

        if self.IsStarfield:
            respLinkOut.run(self.key, state="starfield")
        else:
            respLinkOut.run(self.key, state="cavern")

    def DoWedge(self):
        psnlSDL = xPsnlVaultSDL()

        if self.ageFrom in self.ageDict:
            sdlName = self.ageDict[self.ageFrom]["SDL"]
        else:
            PtDebugPrint("bhroBahroYeeshaCave.DoWedge(): Didn't recognize previous age name, no wedge will be set.", level=kErrorLevel)
            return

        sdlVal = psnlSDL[sdlName][0]
        if not sdlVal:
            PtDebugPrint("bhroBahroYeeshaCave.DoWedge(): Previous age was {}, turning wedge SDL of {} to On".format(self.ageFrom, sdlName), level=kDebugDumpLevel)
            psnlSDL[sdlName] = (1,)

    def SetCurrentState(self, age, state):
        ageSDL = xPsnlVaultSDL()
        ageSDL[age + "PoleState"] = (state, )

    def UpdateToState2(self):
        vault = ptVault()
        myAges = vault.getAgesIOwnFolder()
        myAges = myAges.getChildNodeRefList()
        for ageInfo in myAges:
            link = ageInfo.getChild()
            link = link.upcastToAgeLinkNode()
            info = link.getAgeInfo()
            if not info:
                continue
            ageName = info.getAgeFilename()
            spawnPoints = link.getSpawnPoints()

            if ageName == "Gira":
                ageName = "Garden"

            if ageName in self.ageDict:
                for spawnPoint in spawnPoints:
                    if spawnPoint.getName() == "LinkInPointDefault":
                        if self.ageDict[ageName]["State"] == 1:
                            self.SetCurrentState(ageName, 2)
                        break
        self.UpdatePoleStates()

    def GetAutoStartLevel(self):
        vault = ptVault()
        bc = vault.findChronicleEntry("BahroCave")
        if bc is not None:
            val = bc.chronicleGetValue()
            if val == "":
                return 0
            else:
                return int(val)
        else:
            return 0

    def IncrementAutoStartLevel(self):
        vault = ptVault()
        bc = vault.findChronicleEntry("BahroCave")
        if bc is not None:
            val = bc.chronicleGetValue()
            if val == "":
                val = 0
            else:
                val = int(val)
            bc.chronicleSetValue(str(val + 1))
            bc.save()
            PtDebugPrint("bhroBahroYeeshaCave.IncrementAutoStartLevel(): Setting BC chron={}.".format(str(val + 1)), level=kDebugDumpLevel)
        else:
            PtDebugPrint("bhroBahroYeeshaCave.IncrementAutoStartLevel(): No BC chron found.", level=kDebugDumpLevel)

    def OnBackdoorMsg(self, target, param):
        if target == "kill":
            respKillSpeeches.run(self.key, state=param)
            self.currentYS = "b"

        elif target == "wedgetoggle":
            vault = ptVault()
            myAges = vault.getAgesIOwnFolder()
            myAges = myAges.getChildNodeRefList()
            for ageInfo in myAges:
                link = ageInfo.getChild()
                link = link.upcastToAgeLinkNode()
                info = link.getAgeInfo()
                if not info:
                    continue
                ageName = info.getAgeFilename()

            if param == "Gira":
                param = "Garden"
            if param in self.ageDict:
                sdlName = self.ageDict[param]["SDL"]
            else:
                PtDebugPrint("bhroBahroYeeshaCave.OnBackdoorMsg(): Incorrect age specified, no wedge will be set.", level=kErrorLevel)
                return

            psnlSDL = xPsnlVaultSDL(ageName == "Personal")
            sdlVal = psnlSDL[sdlName][0]
            PtDebugPrint("bhroBahroYeeshaCave.OnBackdoorMsg(): Previous age was {}, turning wedge SDL of {} to {}".format(param, sdlName, "OFF" if sdlVal else "ON"), level=kDebugDumpLevel)
