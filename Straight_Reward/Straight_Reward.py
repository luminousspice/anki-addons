# -*- coding: utf-8 -*-
# Straight Reward:
# an Anki addon increases Ease Factor at every 5 straight success
# ("Good" rating in review).
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
from aqt.deckconf import DeckConf
from aqt.forms import dconf
from anki.hooks import wrap
from aqt.utils import tooltip


# Reward at every 5 strait success
STRAIT = 5
# Increase +15% to Ease Factor as reward
REWARD = 150
# Praise with the reward.
PRAISE = " Straight Success! <br>Ease Factor gained a %d %% : " %(REWARD/10)


def rescheduleRevReward(self, card, ease):
    """Increase ease factor as reward for straight"""
    dconf = self.col.decks.confForDid(card.did)
    if dconf.get('straitReward'):
        count = checkStrait(self, card, ease)
        if ease == 3 and count > 0 and count % STRAIT == STRAIT - 1:
            card.factor = max(1300, card.factor+REWARD)
            tooltip(str(count+1) + PRAISE + str(card.factor/10))


def checkStraight(self, card, conf):
    """Return the latest straight eases from revlog."""
    eases = self.col.db.list("""
select ease from revlog where cid = ? order by id desc
""", card.id)
    if eases:
        strait = [i for i, x in enumerate(eases) if x <> 3]
        if strait:
            return strait[0]
        else:
            return len(eases)


def setupUi(self, Dialog):
    """Add an option for Straight Reward at Review section on Deckconf dialog."""
    try:
        self.straightReward = QtWidgets.QCheckBox(self.tab_3)
    except NameError:
        self.straightReward = QtGui.QCheckBox(self.tab_3)
    self.straightReward.setText(_("Straight Reward"))
    self.gridLayout_3.addWidget(self.straightReward, 7, 0, 1, 3)


def load_conf(self):
    """Get the option for Straight Reward."""
    self.conf = self.mw.col.decks.confForDid(self.deck['id'])
    c = self.conf
    f = self.form
    f.straightReward.setChecked(c.get("straightReward", False))


def save_conf(self):
    """Save the option for Straight Reward."""
    self.conf['straightReward'] = self.form.straightReward.isChecked()


Scheduler._rescheduleRev = wrap(Scheduler._rescheduleRev, rescheduleRevReward)
dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setupUi)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
