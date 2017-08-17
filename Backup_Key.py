# -*- coding: utf-8 -*-
# Copyright: 2017 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#
# Backup Key: an Anki add-on adds a shortcut to save a backup file
# from the deck list on the main window.
# GitHub: https://github.com/luminousspice/anki-addons/

from aqt import mw
from aqt.qt import *

action = QAction(mw)
action.setText(_("Save Backup"))
action.setShortcut(_("Ctrl+S"))
action.triggered.connect(mw.backup)
mw.form.menuCol.addSeparator()
mw.form.menuCol.addAction(action)
