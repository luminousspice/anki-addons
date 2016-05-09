# -*- coding: utf-8 -*-

import BeautifulSoup
import urllib2
from aqt import mw
from aqt.qt import *

URL = "http://www.merriam-webster.com/wotd/feed/rss2"
DECK = "Words"
MODEL = "words"
tags = ["MW"]

def buildCard():
    # get deck and model
    deck  = mw.col.decks.get(mw.col.decks.id(DECK))
    model = mw.col.models.byName(MODEL)

    # assign model to deck
    mw.col.decks.select(deck['id'])
    mw.col.decks.get(deck)['mid'] = model['id']
    mw.col.decks.save(deck)

    # assign deck to model
    mw.col.models.setCurrent(model)
    mw.col.models.current()['did'] = deck['id']
    mw.col.models.save(model)

    # retrieve rss
    data = urllib2.urlopen(URL)
    doc = BeautifulSoup.BeautifulStoneSoup(data, selfClosingTags=['link'])

    if not doc.find('entry') is None:
        items = doc.findAll('entry')
    elif not doc.find('item') is None:
        items = doc.findAll('item')
    else:
        return

    # iterate notes
    for item in items:
        note = mw.col.newNote()
        note['Front'] = item.title.string
        if not item.summary is None:
            note['Back'] = item.summary.string
        elif not item.description is None:
            note['Back'] = item.description.string
        if not item.link.string is None:
            note['id'] = item.link.string
        elif not item.link['href'] is None:
            note['id'] = item.link['href']
        else:
            note['id'] = item.id.string
        note.tags = filter(None, tags)
        if note.dupeOrEmpty():
            continue
        mw.col.addNote(note)

    mw.col.reset()
    mw.reset()

# create a new menu item
action = QAction("Feed to Anki", mw)
mw.connect(action, SIGNAL("triggered()"), buildCard)
mw.form.menuTools.addAction(action)
