# -*- coding: utf-8 -*-
# Frozen Card:
# an Anki add-on adds a deck option to deactivate Anki algorithm to keep
# cards new in the decks
# Version: 0.0.1
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2017 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

try:
    from PyQt5 import QtWidgets
except ImportError:
    from PyQt4 import QtGui

from anki.sched import Scheduler
from aqt.deckconf import DeckConf
from aqt.forms import dconf
from anki.hooks import wrap


def myAnswerCard(self, card, ease):
    dconf = self.col.decks.confForDid(card.did)
    if dconf.get('frozenCard'):
        freezeCard(self, card, ease)
    else:
        orgAnswerCard(self, card, ease)


def freezeCard(self, card, ease):
    """Freeze cards and push back them to the new queue."""
    self.col.log()
    assert ease >= 1 and ease <= 4
    cids = []
    cids.append(card.id)
    Scheduler.forgetCards(self, cids)


def setupUi(self, Dialog):
    """Add an option for Frozen Card section on Deckconf dialog."""
    try:
        self.frozenCard = QtWidgets.QCheckBox(self.tab)
    except NameError:
        self.frozenCard = QtGui.QCheckBox(self.tab)
    self.frozenCard.setText(_("Deactivate Anki algorithm (Frozen Card)"))
    self.gridLayout.addWidget(self.frozenCard, 7, 0, 1, 3)


def load_conf(self):
    """Get the option for Frozen Card."""
    self.conf = self.mw.col.decks.confForDid(self.deck['id'])
    c = self.conf
    f = self.form
    f.frozenCard.setChecked(c.get("frozenCard", False))


def save_conf(self):
    """Save the option for Frozen Card."""
    self.conf['frozenCard'] = self.form.frozenCard.isChecked()


orgAnswerCard = Scheduler.answerCard
Scheduler.answerCard = myAnswerCard
dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setupUi)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
