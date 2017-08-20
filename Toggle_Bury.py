# -*- coding: utf-8 -*-
# Toggle Bury: an Anki add-on adds a toggle button to bury cards in the Card
# Browser.
# Version: 0.0.1
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2017 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt.qt import *
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from aqt.forms.browser import Ui_Dialog
from aqt.browser import Browser, BrowserToolbar
from anki.sched import Scheduler
from anki.utils import ids2str, intTime
from aqt.utils import shortcut
from anki.hooks import wrap, addHook

def my_setupMenus(self):
    self.buryCut1 = QShortcut(QKeySequence("Ctrl+-"), self)
    self.buryCut1.activated.connect(self.onBury)

addHook("browser.setupMenus", my_setupMenus)

def my_draw(self):
    mark = self.browser.isMarked()
    pause = self.browser.isSuspended()
    bury = self.browser.isBuried()
    def borderImg(link, icon, on, title, tooltip=None):
        if on:
            fmt = '''\
<a class=hitem title="%s" href="%s">\
<img valign=bottom style='border: 1px solid #aaa;;height: 16px; width: 16px;' src="qrc:/icons/%s.png"> %s</a>'''
        else:
            fmt = '''\
<a class=hitem title="%s" href="%s"><img style="padding: 1px;height: 16px; width: 16px;" valign=bottom src="qrc:/icons/%s.png"> %s</a>'''
        return fmt % (tooltip or title, link, icon, title)
    right = "<div>"
    right += borderImg("add", "add16", False, _("Add"),
                   shortcut(_("Add Note (Ctrl+E)")))
    right += borderImg("info", "info", False, _("Info"),
                   shortcut(_("Card Info (Ctrl+Shift+I)")))
    right += borderImg("mark", "star16", mark, _("Mark"),
                   shortcut(_("Mark Note (Ctrl+K)")))
    right += borderImg("pause", "pause16", pause, _("Suspend"),
                   shortcut(_("Suspend Card (Ctrl+J)")))
    right += borderImg("bury", "media-playback-stop", bury, _("Bury"),
                   shortcut(_("Bury (Ctrl+-)")))
    right += borderImg("setDeck", "deck16", False, _("Change Deck"),
                       shortcut(_("Move To Deck (Ctrl+D)")))
    right += borderImg("addtag", "addtag16", False, _("Add Tags"),
                   shortcut(_("Bulk Add Tags (Ctrl+Shift+T)")))
    right += borderImg("deletetag", "deletetag16", False,
                       _("Remove Tags"), shortcut(_(
                           "Bulk Remove Tags (Ctrl+Alt+T)")))
    right += borderImg("delete", "delete16", False, _("Delete"))
    right += "</div>"
    self.web.page().currentFrame().setScrollBarPolicy(
        Qt.Horizontal, Qt.ScrollBarAlwaysOff)
    self.web.stdHtml(self._body % (
        "", #<span style='display:inline-block; width: 100px;'></span>",
        #self._centerLinks(),
        right, ""), self._css + """
#header { font-weight: normal; }
a { margin-right: 1em; }
.hitem { overflow: hidden; white-space: nowrap;}
""")

def my_linkHandler(self, l):
    org_linkHandler(self, l)
    if l == "bury":
        self.browser.onBury()

BrowserToolbar.draw = my_draw
org_linkHandler = BrowserToolbar._linkHandler
BrowserToolbar._linkHandler = my_linkHandler

def isBuried(self):
    return not not (self.card and self.card.queue == -2)

def onBury(self, bur=None):
    if bur is None:
        bur = not self.isBuried()
    self.editor.saveNow()
    c = self.selectedCards()
    if bur:
        self.col.sched.buryCards(c)
    else:
        self.col.sched.unburiedCards(c)
    self.model.reset()
    self.mw.requireReset()

def unburiedCards(self, ids):
    "Unburied cards."
    self.col.log(ids)
    self.col.db.execute(
        "update cards set queue=type,mod=?,usn=? "
        "where queue = -2 and id in "+ ids2str(ids),
        intTime(), self.col.usn())

Browser.isBuried = isBuried
Browser.onBury = onBury
Scheduler.unburiedCards = unburiedCards
