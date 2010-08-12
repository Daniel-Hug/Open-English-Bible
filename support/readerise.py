# -*- coding: utf-8 -*-
#

import os
import parseUsfm

class DummyFile(object):
    def close(self):
        pass
    def write(self, str):
        pass

class ReaderPrinter(object):
    def __init__(self, outputDir):
        self.outputDir = outputDir
        self.f = DummyFile()
        self.cb = u''    # Current Book
        self.cc = u'001'    # Current Chapter
        self.cv = u'001'    # Currrent Verse
        self.indentFlag = False
 
    def write(self, unicodeString):
        self.f.write(unicodeString.encode('utf-8'))

    def writeIndent(self, level):
        if level == 0:
            self.indentFlag = False
            self.write(u'<br /><br />')
            return 
        if not self.indentFlag:
            self.indentFlag = True
            self.write(u'<br />')
        self.write(u'<br />')
        self.write(u'&nbsp;&nbsp;&nbsp;&nbsp;' * level)

    def renderID(self, token): 
        self.write(u'</p></article>')
        self.f.close()
        self.cb = self.books[token.value]
        self.f = open(self.outputDir + u'/c' + self.cb + u'001.html', 'w')
        self.write(u'<article class="chapter nt oeb" lang="en" dir="ltr" rel="c' + self.cb + u'001">')
        self.indentFlag = False
    def renderIDE(self, token):     pass
    def renderH(self, token):       self.write(u'</p><h1 class="bookname">' + token.value + u'</h1><p>')
    def renderMT(self, token):      self.write(u'</p><h3>' + token.value + u'</h3><p>')
    def renderMS(self, token):      self.write(u'</p><h4>' + token.value + u'</h4><p><br />')
    def renderMS2(self, token):     self.write(u'</p><h5>' + token.value + u'</h5><p><br />')
    def renderP(self, token):
        self.indentFlag = False
        self.write(u'<br /><br />')
    def renderS(self, token):
        self.indentFlag = False
        self.write(u'</p><p align="center">_____</p><p>')
    def renderC(self, token):
        self.cc = token.value.zfill(3)
        if self.cc == u'001':
            self.write(u'<h2 class="c-num">' + token.value + u'</h2><p>')
        else:
            self.write(u'<p></article>')
            self.f.close()
            self.f = open(self.outputDir + u'/c' + self.cb + self.cc + u'.html', 'w')
            self.write(u'<article class="chapter nt oeb" lang="en" dir="ltr" rel="c' + self.cb + self.cc + u'">\n')
            self.write(u'<h2 class="c-num">' + token.value + u'</h2><p>\n')        
    def renderV(self, token):
        self.cv = token.value.zfill(3)
        if self.cv == u'001':
            self.write(u'\n<span class="verse" rel="v' + self.cb + self.cc + self.cv + u'"><span class="v-num-1">' + token.value + u'&nbsp;</span>\n')
        else:
            self.write(u'</span>\n<span class="verse" rel="v' + self.cb + self.cc + self.cv + u'"><span class="v-num">' + token.value + u'&nbsp;</span>\n')
    def renderWJS(self, token):     self.write(u'<span class="woc">')
    def renderWJE(self, token):     self.write(u'</span>')
    def renderTEXT(self, token):    self.write(u" " + token.value + u" ")
    def renderQ(self, token):       self.writeIndent(1)
    def renderQ1(self, token):      self.writeIndent(1)
    def renderQ2(self, token):      self.writeIndent(2)
    def renderQ3(self, token):      self.writeIndent(3)
    def renderNB(self, token):      self.writeIndent(0)
    def renderQTS(self, token):     pass
    def renderQTE(self, token):     pass
    def renderFS(self, token):      pass
    def renderFE(self, token):      pass
    def renderIS(self, token):      self.write(u'<i>')
    def renderIE(self, token):      self.write(u'</i>')

    books = {
    u'MAT': u'040',
    u'MRK': u'041',
    u'LUK': u'042',
    u'JHN': u'043',
    u'ACT': u'044',
    u'ROM': u'045',
    u'1CO': u'046',
    u'2CO': u'047',
    u'GAL': u'048',
    u'EPH': u'049',
    u'PHP': u'050',
    u'COL': u'051',
    u'1TH': u'052',
    u'2TH': u'053',
    u'1TI': u'054',
    u'2TI': u'055',
    u'TIT': u'056',
    u'PHM': u'057',
    u'HEB': u'058',
    u'JAS': u'059',
    u'1PE': u'060',
    u'2PE': u'061',
    u'1JN': u'062',
    u'2JN': u'063',
    u'3JN': u'064',
    u'JUD': u'065',
    u'REV': u'066'
    }

class TransformForReader(object):
    outputDir = ''
    patchedDir = ''
    prefaceDir = ''

    def translateBook(self, name):

        f = open(self.patchedDir + '/' + name + '.usfm')
        fc = unicode(f.read(), 'utf-8')
        f.close()

        print '        > ' + name
        tokens = parseUsfm.parseString(fc)

        tp = ReaderPrinter(self.outputDir)
        for t in tokens: t.renderOn(tp)
 
    def setupAndRun(self, patchedDir, prefaceDir, outputDir):
        self.patchedDir = patchedDir
        self.prefaceDir = prefaceDir
        self.outputDir = outputDir

        # Setup list of patches and books to use
        #
        books = [   'Matthew',
                    'Mark',
                    'Luke',
                    'John',
                    'Acts',
                    'Romans',
                    '1 Corinthians',
                    '2 Corinthians',
                    'Galatians',
                    'Ephesians',
                    'Philippians',
                    'Colossians',
                    '1 Thessalonians',
                    '2 Thessalonians',
                    '1 Timothy',
                    '2 Timothy',
                    'Titus',
                    'Philemon',
                    'Hebrews',
                    'James',
                    '1 Peter',
                    '2 Peter',
                    '1 John',
                    '2 John',
                    '3 John',
                    'Jude',
                    'Revelation']
        for book in books:
            self.translateBook(book)
