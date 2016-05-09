# -*- coding: utf-8 -*-

from aqt import mw
import BeautifulSoup
import urllib
from aqt.qt import *

URL = "http://www.merriam-webster.com/wotd/feed/rss2"
tags = ["MW"]
DECK = "Words"
MODEL = "words"

def buildCard():
    # MAKE DECK
    deck  = mw.col.decks.get(mw.col.decks.id(DECK))
    model = mw.col.models.byName(MODEL)

    # ASSIGN MODEL TO DECK
    mw.col.decks.select(deck['id'])
    mw.col.decks.get(deck)['mid'] = model['id']
    mw.col.decks.save(deck)

    # ASSIGN DECK TO MODEL
    mw.col.models.setCurrent(model)
    mw.col.models.current()['did'] = deck['id']
    mw.col.models.save(model)

    data = urllib.urlopen(URL)
    doc = BeautifulSoup.BeautifulStoneSoup(data, selfClosingTags=['link'])

    for item in doc.findAll('entry'):
        note = mw.col.newNote()
        if not item.title is None:
            note['Front']   = u''.join(unicode(i) for i in item.title.string)
        if not item.summary is None:
            note['Back']    = u''.join(unicode(i) for i in item.summary.string)

        note['id'] = u''.join(unicode(i) for i in item.link['href'])
        note.tags = filter(None, tags)
        if note.dupeOrEmpty():
            continue
        mw.col.addNote(card)

    mw.col.reset()
    mw.reset()

# create a new menu item, "test"
action = QAction("Build Card", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), buildCard)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
