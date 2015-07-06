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
Module: ahnyLinkBookGUIPopup
Age: global
Date: November, 2002
Author: Doug McBride
Shows the linking book GUI with the appropriate linking panel. 

# March 2003
This script now also provides the GUI for books taken off of the Personal Age Bookshelf. There are a few
differences between books on pedestals vs. books on the psnlBookshelf:
- The "Share Book" decal on the book itself is never available on a book from the psnlBookshelf
- Turned corners, indicating more pages in the book, are only available in books in the psnlBookshelf

# April 29, 2003
Major change over to using ptBook instead of LinkBooksGUI dialog
First phase - keep hi level structure, only replace the bring up of books
"""

from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import xLinkingBookDefs

# Define the attributes that will be entered in Max.
actClickableBook = ptAttribActivator(1, "Actvtr: Clickable small book")
SeekBehavior = ptAttribBehavior(2, "Smart seek before GUI (optional)")
respLinkResponder = ptAttribResponder(3, "Rspndr: Link out")
TargetAge = ptAttribString(4, "Name of Linking Panel", "Teledahn")

actBookshelf = ptAttribActivator(5, "Bookshelf (Only used in PsnlAge)")  # Leave blank unless it's a Personal Age Bookshelf
shareRegion = ptAttribActivator(6, "region in which the sharer must remain")
shareBookSeek = ptAttribBehavior(7, "smart seek & use book for share acceptance")  # Different, because the offerer's client links the offeree in this case

IsDRCStamped = ptAttribBoolean(10, "DRC Stamp", default=1)

respLinkSphere01 = ptAttribResponder(11, "sphere 01 resp")
respLinkSphere02 = ptAttribResponder(12, "sphere 02 resp")
respLinkSphere03 = ptAttribResponder(13, "sphere 03 resp")
respLinkSphere04 = ptAttribResponder(14, "sphere 04 resp")

kGrsnTeamBook = 99


class ahnyLinkBookGUIPopup(ptModifier):
    """
        The Linking Book GUI Popup python code.
    """
    
    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5343
        self.version = 27
        minor = 4
        PtDebugPrint("ahnyLinkBookGUIPopup: v{}.{}".format(self.version, minor), level=kWarningLevel)
        
        self.localAvatar = None
        self.linkingBook = None
        self.noReenableBook = False

    def OnServerInitComplete(self):
        # Only in the personal age should actBookshelf be anything, so this should only happen in the personal age
        if actBookshelf:
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags("CurrentPage", 1, 1)
            ageSDL.sendToClients("CurrentPage")

    def OnNotify(self, state, id, events):
        # If it's the share region, we only care if the offerer is LEAVING the
        # region, since he had to be inside it to trigger the clickable for the
        # book anyway. Is it a clickable book on a pedestal?
        if id == actClickableBook.id and PtFindAvatar(events) == PtGetLocalAvatar():
            actClickableBook.disable()
            PtToggleAvatarClickability(False)
            self.localAvatar = PtFindAvatar(events)
            SeekBehavior.run(self.localAvatar)

        # Is it the seek behavior because we clicked on a book ourself?    
        elif id == SeekBehavior.id and PtFindAvatar(events) == PtGetLocalAvatar():
            PtDebugPrint("ahnyLinkBookGUIPopup.OnNotify(): events = {}".format(events), level=kDebugDumpLevel)
            for event in events:
                # Smart seek completed. Exit multistage, and show GUI.
                if event[0] == kMultiStageEvent and event[2] == kEnterStage:
                    SeekBehavior.gotoStage(self.localAvatar, -1)
                    PtDebugPrint("ahnyLinkBookGUIPopup.OnNotify(): Attempting to draw link panel GUI.", level=kWarningLevel)
                    self.ShowBookNoTreasure()
        
        else:
            for event in events:
                # Is it from the OpenBook? (we only have one book to worry about)
                if event[0] == PtEventType.kBook:
                    PtDebugPrint("ahnyLinkBookGUIPopup.OnNotify(): BookNotify event={}, id={}".format(event[1], event[2]), level=kDebugDumpLevel)
                    if event[1] == PtBookEventTypes.kNotifyImageLink:
                        if event[2] >= xLinkingBookDefs.kFirstLinkPanelID or event[2] == xLinkingBookDefs.kBookMarkID:
                            PtDebugPrint("ahnyLinkBookGUIPopup.OnNotify(): Book, hit linking panel {}.".format(event[2]), level=kWarningLevel)
                            self.HideBook(True)
                            respLinkSphere01.run(self.key, avatar=PtGetLocalAvatar(), netPropagate=0)
        
                    elif event[1] == PtBookEventTypes.kNotifyShow:
                        PtDebugPrint("ahnyLinkBookGUIPopup.OnNotify(): Book, NotifyShow", level=kDebugDumpLevel)
                        # Re-allow KI and BB
                        PtSendKIMessage(kEnableKIandBB, 0)

                    elif event[1] == PtBookEventTypes.kNotifyHide:
                        PtDebugPrint("ahnyLinkBookGUIPopup.OnNotify(): Book, NotifyHide", level=kDebugDumpLevel)
                        PtToggleAvatarClickability(True)
        
                        if not self.noReenableBook:
                            actClickableBook.enable()
                
                    elif event[1] == PtBookEventTypes.kNotifyCheckUnchecked:
                        PtDebugPrint("ahnyLinkBookGUIPopup.OnNotify(): Book, NotifyCheckUncheck", level=kDebugDumpLevel)

    def ShowBookNoTreasure(self):
        try:
            params = xLinkingBookDefs.xAgeLinkingBooks["Ahnonay"]

            sharable, width, height, stampdef, bookdef = params[:5]
            if len(params) == 6:
                gui = params[5]
            elif len(params) == 5:
                gui = "BkBook"
            else:
                return

            PtDebugPrint("ahnyLinkBookGUIPopup.ShowBookNoTreasure(): bookdef = {}".format(bookdef), level=kDebugDumpLevel)
            PtSendKIMessage(kDisableKIandBB, 0)
            self.linkingBook = ptBook(bookdef, self.key)
            self.linkingBook.setSize(width, height)
            self.linkingBook.setGUI(gui)
            self.linkingBook.show(1)

        except LookupError:
            PtDebugPrint("ahnyLinkBookGUIPopup.ShowBookNoTreasure(): Could not find Ahnonay's linking panel.", level=kErrorLevel)

    def HideBook(self, isLinking=False):
        self.noReenableBook = isLinking
        
        PtToggleAvatarClickability(True)  # Enable me as clickable
        if self.linkingBook:
            self.linkingBook.hide()

    def OnTimer(self, id):
        if id == kGrsnTeamBook:
            PtDebugPrint("ahnyLinkBookGUIPopup.OnTimer(): Got timer callback. Removing popup for a grsn team book.", level=kDebugDumpLevel)
            self.linkingBook.hide()
