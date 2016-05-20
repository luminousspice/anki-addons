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
select ivl from revlog where cid = ? and ivl > 0 order by id desc
""", card.id)
    if ivls:
        backward_ivls = [x for x in ivls if 0 < x < ivls[0]]
        if backward_ivls:
            return max(conf['minInt'], backward_ivls[0])

    return conf['minInt']

Scheduler._nextLapseIvl = withdrawLapseIvl
