# -*- coding: utf-8 -*-
# Another Retreat:
# an Anki addon sets the next interval at lapse to the last succeed interval.
# Version: 0.3.1
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2016 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

import time
import random
from heapq import heappush

try:
    from PyQt5 import QtWidgets
except ImportError:
    from PyQt4 import QtGui

from anki.sched import Scheduler
from aqt.deckconf import DeckConf
from aqt.forms import dconf
from anki.hooks import wrap


def newAnswerLrnCard(self, card, ease):
    # ease 1=no, 2=yes, 3=remove
    conf = self._lrnConf(card)
    if card.odid and not card.wasNew:
        type = 3
    elif card.type == 2:
        type = 2
    else:
        type = 0
    leaving = False
    # lrnCount was decremented once when card was fetched
    lastLeft = card.left
    # immediate graduate?
    if ease == 3:
        self._rescheduleAsRev(card, conf, True)
        leaving = True
    # graduation time?
    elif ease == 2 and (card.left%1000)-1 <= 0:
        self._rescheduleAsRev(card, conf, False)
        leaving = True
    else:
        # one step towards graduation
        if ease == 2:
            # decrement real left count and recalculate left today
            left = (card.left % 1000) - 1
            card.left = self._leftToday(conf['delays'], left)*1000 + left
        # failed
        else:
            card.left = self._startingLeft(card)
            resched = self._resched(card)
            if 'mult' in conf and resched:
                # review that's lapsed
                card.ivl = withdrawLapseIvl(self, card, conf)
            else:
                # new card; no ivl adjustment
                pass
            if resched and card.odid:
                card.odue = self.today + 1
        delay = self._delayForGrade(conf, card.left)
        if card.due < time.time():
            # not collapsed; add some randomness
            delay *= random.uniform(1, 1.25)
        card.due = int(time.time() + delay)
        # due today?
        if card.due < self.dayCutoff:
            self.lrnCount += card.left // 1000
            # if the queue is not empty and there's nothing else to do, make
            # sure we don't put it at the head of the queue and end up showing
            # it twice in a row
            card.queue = 1
            if self._lrnQueue and not self.revCount and not self.newCount:
                smallestDue = self._lrnQueue[0][0]
                card.due = max(card.due, smallestDue+1)
            heappush(self._lrnQueue, (card.due, card.id))
        else:
            # the card is due in one or more days, so we need to use the
            # day learn queue
            ahead = ((card.due - self.dayCutoff) // 86400) + 1
            card.due = self.today + ahead
            card.queue = 3
    self._logLrn(card, ease, conf, leaving, type, lastLeft)


def withdrawLapseIvl(self, card, conf):
    """Return the previous succeed ivl from revlog."""
    dconf = self.col.decks.confForDid(card.did)
    if dconf.get('anotherRetreat'):
        ivls = self.col.db.list("""
select ivl from revlog where cid = ? and ivl > 0 order by id desc
""", card.id)
        if ivls:
            backward_ivls = [x for x in ivls if x < ivls[0]]
            if backward_ivls:
                return max(conf['minInt'], backward_ivls[0])
    return max(conf['minInt'], int(card.ivl*conf['mult']))


def setupUi(self, Dialog):
    """Add an option for Another Retreat at lapse section on Deckconf dialog."""
    try:
        self.anotherRetreat = QtWidgets.QCheckBox(self.tab_2)
    except NameError:
        self.anotherRetreat = QtGui.QCheckBox(self.tab_2)
    self.anotherRetreat.setText(_("Activate Another Retreat Addon"))
    self.gridLayout_2.addWidget(self.anotherRetreat, 5, 0, 1, 3)


def load_conf(self):
    """Get the option for Another Retreat."""
    self.conf = self.mw.col.decks.confForDid(self.deck['id'])
    c = self.conf
    f = self.form
    f.anotherRetreat.setChecked(c.get("anotherRetreat", False))


def save_conf(self):
    """Save the option for Another Retreat."""
    self.conf['anotherRetreat'] = self.form.anotherRetreat.isChecked()


Scheduler._nextLapseIvl = withdrawLapseIvl
Scheduler._answerLrnCard = newAnswerLrnCard
dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setupUi)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
