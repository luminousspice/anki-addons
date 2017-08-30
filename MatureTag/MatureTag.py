# -*- coding: utf-8 -*-
# Copyright: 2014-2016 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#
# Mature Tag: an Anki addon automatically adds a tag on your mature cards after the review.
# GitHub: https://github.com/luminousspice/anki-addons/

from anki.hooks import wrap
from anki.sched import Scheduler

# Threshold interval for tagging
threshold = 21
# Tag string for mature note
MatureTag = u"Mature"

def matureCheck(self, card, ease):
    f = card.note()
    if (card.ivl >= threshold):
        f.addTag(MatureTag)
    else:
        f.delTag(MatureTag)
    f.flush()
    return True

Scheduler.answerCard = wrap(Scheduler.answerCard, matureCheck)
