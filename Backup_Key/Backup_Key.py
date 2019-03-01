# -*- coding: utf-8 -*-
# Backup Key: an Anki add-on adds a shortcut to save a backup file
# from the deck list on the main window.
# GitHub: https://github.com/luminousspice/anki-addons/
# Version: 0.1.0
#
# Copyright: 2019 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt import mw
from aqt.qt import *
from aqt.utils import showWarning, tooltip


def backup_collection(self):
    """ Backup the collection after optimizing and checking the db. """
    if not mw.col:
        return
    label = _("Backing Up...")
    mw.progress.start(label=label, immediate=True)
    corrupt = False
    try:
        mw.maybeOptimize()
    except:
        corrupt = True
    try:
        mw.col.close()
    except:
        corrupt = True
    if corrupt:
        showWarning(_("Your collection file appears to be corrupt. \
This can happen when the file is copied or moved while Anki is open, or \
when the collection is stored on a network or cloud drive. If problems \
persist after restarting your computer, please open an automatic backup \
from the profile screen."))
    else:
        mw.backup()
        mw.col.reopen()
    mw.progress.finish()
    if not corrupt:
        tooltip(_("Backed up."))


action = QAction(mw)
action.setText(_("Save Backup"))
action.setShortcut(_("Ctrl+S"))
action.triggered.connect(backup_collection)
mw.form.menuCol.addSeparator()
mw.form.menuCol.addAction(action)
