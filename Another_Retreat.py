# -*- coding: utf-8 -*-
# Another Retreat:
# an Anki addon sets the next interval at lapse to the last succeed interval.
# Version: 0.1.2
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2016 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from anki.sched import Scheduler


def withdrawLapseIvl(self, card, conf):
    ''' Return the latest lastivl from revlog.'''
    ivls = self.col.db.list("""
select ivl from revlog where cid = ? order by id desc
""", card.id)
    lastIvls = self.col.db.list("""
select lastivl from revlog where cid = ? and type = 1 order by id desc
""", card.id)
    civls = [x for x in ivls if x > 0]
    d = [x for x in lastIvls if x < civls[0]]
    if d:
        return max(conf['minInt'], d[0])
    else:
        return conf['minInt']

Scheduler._nextLapseIvl = withdrawLapseIvl
