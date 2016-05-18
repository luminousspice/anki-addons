# -*- coding: utf-8 -*-
# Another Retreat:
# an Anki addon sets the next interval at lapse to the last succeed interval.
# Version: 0.1.1
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2016 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from anki.sched import Scheduler


def withdrawLapseIvl(self, card, conf):
    ''' Return the latest lastivl from revlog.'''
    lastIvls = self.col.db.list("""
select lastivl from revlog where cid = ? and type = 1 order by id desc""", card.id)
    d = [x for x in lastIvls if x < card.ivl]
    return max(conf['minInt'], d[0])

Scheduler._nextLapseIvl = withdrawLapseIvl
