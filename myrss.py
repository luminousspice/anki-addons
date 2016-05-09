# -*- coding: utf-8 -*-

import feedparser
from aqt import mw
from aqt.qt import *

URL = "http://www.merriam-webster.com/wotd/feed/rss2"
tags = "MW"
TITLE = "Words"
MODEL = "words"

def buildCard():
    # MAKE DECK
    deck  = mw.col.decks.get(mw.col.decks.id(TITLE))
    model = mw.col.models.byName(MODEL)

    # ASSIGN MODEL TO DECK
    mw.col.decks.select(deck['id'])
    mw.col.decks.get(deck)['mid'] = model['id']
    mw.col.decks.save(deck)

    # ASSIGN DECK TO MODEL
    mw.col.models.setCurrent(model)
    mw.col.models.current()['did'] = deck['id']
    mw.col.models.save(model)

    response = feedparser.parse(URL)

    for entry in response.entries:
        term['question']  = entry.summary
        term['answer'] = entry.title
        term['url'] = entry.link
        card = mw.col.newNote()
        if not term['question'] is None:
            card['Front']   = u''.join(unicode(i) for i in term['question'])
        if not term['answer'] is None:
            card['Back']    = u''.join(unicode(i) for i in term['answer'])

        card['Note'] = u''.join(unicode(i) for i in term['url'])
        card.tags = filter(None, tags)
        mw.col.addNote(card)

    mw.col.reset()
    mw.reset()

# create a new menu item, "test"
action = QAction("Build Card", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), buildCard)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
