# -*- coding: utf-8 -*-
# 1min Interval Counter: an Anki addon reports totals of 1min interval
# in review log for each deck.
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2016 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt import mw
from aqt.utils import showText
from aqt.qt import *


def onemin_ivls():
    """Display totals of 1min ivl in revlog for each deck."""
    list = []
    r = "1min Interval count in review log for each deck\n\n"
    dids = mw.col.decks.allIds()
    for d in dids:
        cids = mw.col.db.list("select id from cards where did = ?", d)
        counter = 0
        for x in cids:
            counter += mw.col.db.scalar("select count() from revlog where lastivl = -60 and cid = ? order by id desc", x)
        deck  = mw.col.decks.get(d)
        list.append([deck['name'],counter])
    list = sorted(list,key=lambda x:x[0])
    for l in list:
        r += str(l[0])+": \t"+str(l[1])+"\n"
    showText(r)


action = QAction("1min Interval Report", mw)
mw.connect(action, SIGNAL("triggered()"), onemin_ivls)
mw.form.menuTools.addAction(action)