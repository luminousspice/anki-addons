# -*- coding: utf-8 -*-
# Copyright: 2016 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#
# Find Matures: an Anki addon adds a tag to find mature cards on the left pane of Card Browser.
# GitHub: https://github.com/luminousspice/anki-addons/

from aqt.qt import *
from aqt.browser import Browser

def mySystemTagTree(self, root):
    origSystemTagTree(self, root)
    matureTag(self, root)

def matureTag(self, root):
    root = self.CallbackItem(
        root, _("Mature"), lambda c="prop:ivl>20": self.setFilter(c))
    root.setIcon(0, QIcon(":/icons/view-pim-news.png"))

origSystemTagTree = Browser._systemTagTree
Browser._systemTagTree = mySystemTagTree