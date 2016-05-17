# -*- coding: utf-8 -*-
# Another Retreat:
# an Anki addon sets the next interval at lapse to the last succeed interval.
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2016 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from anki.sched import Scheduler


def withdrawLapseIvl(self, card, conf):
    ''' Return the latest lastivl from revlog.'''
    lastIvl = self.col.db.scalar("""
select lastivl from revlog where cid = ? order by id desc""", card.id)
    return max(conf['minInt'], lastIvl)

Scheduler._nextLapseIvl = withdrawLapseIvl
