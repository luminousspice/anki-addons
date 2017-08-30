# -*- coding: utf-8 -*-
# 1min Interval Report: an Anki addon reports totals and ratio of 1min interval
# in review log for each deck.
# Version: 0.1.0
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2016-2017 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt import mw
from aqt.utils import showText
from aqt.qt import *

#Interval value: 1min = -60, 10min = -600, 1day = 1
IVL = -60
#Session Type: 0=lrn, 1=rev, 2=relrn, 3=cram
TYPE = 0


def onemin_ivls_list(dids):
    """Retrieve lists of 1min ivl in revlog for each deck."""
    ivlslist = []
    for d in dids:
        cids = mw.col.db.list("select id from cards where did = ?", d)
        counter = 0
        ratio = 0
        clist = []
        csize = 0
        lcounter = 0
        lratio = 0
        llist = []
        lsize = 0
        for x in cids:
            clist = mw.col.db.list("""
select lastivl from revlog where cid = ? order by id desc
""", x)
            counter += clist.count(IVL)
            csize += len(clist)
            llist = mw.col.db.list("""
select lastivl from revlog where type = ? and cid = ? order by id desc
""", TYPE, x)
            lcounter += llist.count(IVL)
            lsize += len(llist)
        if csize:
            ratio = counter * 100 / csize
        if lsize:
            lratio = lcounter * 100 / lsize
        deck = mw.col.decks.get(d)
        ivlslist.append([deck['name'], counter, ratio, lratio])
    ivlslist = sorted(ivlslist, key=lambda x: x[0])
    return ivlslist


def display_result(ilist):
    """Format and Display the report on a showText window."""
    r = "1min Interval Report:\n\n"
    r += "Deck\tCount\t% Total\t% in Learn\n"
    for l in ilist:
        r += "%s\t%d\t%0.1f\t%0.1f\n" % (l[0], l[1], l[2], l[3])
    showText(r)


def onemin_ivls():
    """Display totals and ratio of 1min ivl in revlog for each deck."""
    dids = mw.col.decks.allIds()
    ivls = onemin_ivls_list(dids)
    display_result(ivls)


action = QAction("1min Interval Report", mw)
action.triggered.connect(onemin_ivls)
mw.form.menuTools.addAction(action)
