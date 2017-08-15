# -*- coding: utf-8 -*-
# Japanese Help Launcher:
# an Anki addon adds an menu item to launch Anki help document in Japanese.
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2016-2017 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

u"""
このアドオンはメニューに日本語マニュアルを呼び出す項目を追加します。
ショートカットキーは Shift+F1 です。OS X は fn+Shift+F1 の場合があります。
日本語マニュアルの URL が変わったら DOCURL の値を変更してください。
"""

from aqt import mw, utils
from aqt.qt import *
from anki.lang import _


DOCURL = "http://wikiwiki.jp/rage2050/"


def launch_doc():
    utils.openLink(DOCURL)


# create a new menu item
action = QAction(_(u"日本語マニュアル"), mw)
action.setShortcut("Shift+F1")
mw.connect(action, SIGNAL("triggered()"), launch_doc)
mw.form.menuHelp.addAction(action)
