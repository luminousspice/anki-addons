# -*- coding: utf-8 -*-
# Stainless Ease:
# an Anki addon allows lapse to reduce Ease Factor only at leeches.
# Version: 0.0.1
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2019 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

try:
    from PyQt5 import QtWidgets
except ImportError:
    from PyQt4 import QtGui

from anki.sched import Scheduler
from aqt import mw
from aqt.deckconf import DeckConf
from aqt.forms import dconf
from anki.hooks import addHook, wrap


# Reduce Ease Factor by 20% at the leech.
CUT = 200


def preserve_ease(self, card,  _old):
    card.lastfactor = card.factor
    ret =  _old(self, card)
    dconf = self.col.decks.confForDid(card.did)
    conf = self._lapseConf(card)
    if dconf.get('stainlessEase') and not self._checkLeech(card, conf):
        card.factor = card.lastfactor
    return ret


def reduce_ease(card):
    """Reduce ease factor."""
    dconf = mw.col.decks.confForDid(card.did)
    if dconf.get('stainlessEase'):
        card.factor = max(1300, card.lastfactor-CUT)


def setupUi(self, Dialog):
    """Add an option for Stainless Ease at Lapse section on Deckconf dialog."""
    try:
        self.stainlessEase = QtWidgets.QCheckBox(self.tab_2)
    except NameError:
        self.stainlessEase = QtGui.QCheckBox(self.tab_2)
    self.stainlessEase.setText(_("Stainless Ease"))
    self.gridLayout_2.addWidget(self.stainlessEase, 7, 0, 1, 3)


def load_conf(self):
    """Get the option for Stainless Ease."""
    self.conf = self.mw.col.decks.confForDid(self.deck['id'])
    c = self.conf
    f = self.form
    f.stainlessEase.setChecked(c.get("stainlessEase", False))


def save_conf(self):
    """Save the option for Stainless Ease."""
    self.conf['stainlessEase'] = self.form.stainlessEase.isChecked()


addHook("leech", reduce_ease)
Scheduler._rescheduleLapse = wrap(Scheduler._rescheduleLapse, preserve_ease, 'around')
dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setupUi)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
