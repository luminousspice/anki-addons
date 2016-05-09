# -*- coding: utf-8 -*-

import urllib2
from aqt import mw, utils
from aqt.qt import *
from anki.lang import ngettext
from BeautifulSoup import BeautifulStoneSoup

URL = "http://www.merriam-webster.com/wotd/feed/rss2"
MODEL = u"words"
DECK = u"Word of the Day"
tags = [u"MW",u"wotd"]

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
    doc = BeautifulStoneSoup(data, selfClosingTags=['link'], convertEntities=BeautifulStoneSoup.ALL_ENTITIES)

    if not doc.find('item') is None:
        items = doc.findAll('item')
        feed = "rss"
    elif not doc.find('entry') is None:
        items = doc.findAll('entry')
        feed = "atom"
    else:
        return

    # iterate notes
    dups = 0
    adds = 0
    log = ""
    for item in items:
        note = mw.col.newNote()
        note['Front'] = item.title.string
        nounique = note.dupeOrEmpty()
        if nounique:
            if nounique == 2:
                log += "%s \n" % note['Front']
            continue
        if feed == "rss":
            if not item.link.string is None:
                note['Link'] = item.link.string
            if not item.description is None:
                note['Back'] = item.description.string
        if feed == "atom":
            if not item.link['href'] is None:
                note['Link'] = item.link['href']
            if not item.summary is None:
                note['Back'] = item.summary.string
        note.tags = filter(None, tags)
        mw.col.addNote(note)
        adds += 1

    mw.col.reset()
    mw.reset()

    #show result
    msg = ngettext("%d note added", "%d notes added", adds) % adds
    msg += "\n"
    if len(log) > 0:
        msg += _("duplicate") + ":\n"
        msg += log
    utils.showText(msg)

# create a new menu item
action = QAction("Feed to Anki", mw)
mw.connect(action, SIGNAL("triggered()"), buildCard)
mw.form.menuTools.addAction(action)
