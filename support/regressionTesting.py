# -*- coding: utf-8 -*-
#

import os
import re

class Tester(object):
    def loadBooks(self, path):
        books = {}
        dirList=os.listdir(path)
        print '     Checking ' + path
        #print '     Loading all Usfm files from ' + path
        for fname in dirList:
          try:
              f = open(path + '/' + fname,'U') # U handles line endings
              usfm = f.read().decode('utf-8-sig')
              books[fname] = usfm
              #print '     Loaded ' + fname
              f.close()
          except:
              if not fname == '.DS_Store':
                  print '     - Couldn\'t open ' + fname
        #print '     Finished loading'
        return books
    
    def test(self, dir):
        books = self.loadBooks(dir)
        for b in books:
            self.testMalformedCodes(b, books[b])
            self.testDuplicates(b, books[b])
            self.testMisplacedSpaces(b, books[b])
            self.testMissingSpaces(b, books[b])
            self.testExtraSpaces(b, books[b])
            self.testParas(b, books[b])
            self.testSectionHeaders(b, books[b])
            self.testWJ(b, books[b])
            self.testB(b, books[b])
            self.testM(b, books[b])

    def testMalformedCodes(self, b, u):
        w = u.split(u' \n\t.,:?;\'\"')
        self.checkForCode('sea', w)
        
    def checkForCode(self, c, w):
        if c in w:  print '     - Malformed code? \'' + c + '\' in ' + u[:50]
    
    def testDuplicates(self, b, u):
        for c in u':.,\'"‘’“”':
            if c + c in u:
                print 'Duplicate "' + c + '" in ' + b
                
    def testExtraSpaces(self, b, u):
        for i, l in enumerate(u.split('\n')):
            if not l == '' and l[-1] == ' ':
                print 'Extra space on line: ' + str(i +1) + ' of ' + b


    def testMisplacedSpaces(self, b, u):
        for i, l in enumerate(u.split('\n')):
            if u' .' in l:
                print 'Misplaced ~. on line: ' + str(i +1) + ' of ' + b
            if u' ,' in l:
                print 'Misplaced ~, on line: ' + str(i +1) + ' of ' + b
            if u' ;' in l:
                print 'Misplaced ~; on line: ' + str(i +1) + ' of ' + b
                
    def testMissingSpaces(self, b, u):
        t = u'.,;:'
        for i, c in enumerate(u):
            if c in t: 
                if i < len(u) - 1:
                    if not u[i+1] in u' \n\\”’)0123456789':
                        print 'Missing space in ' + b + ' at ' + str(i)
                        
    def testParas(self, b, u):
        """
        When a paragraph and verse start together, always put the paragraph marker before the verse marker.
        (If there is no actual paragraph starting there, use \nb.)
        """
        if u'\\p\n\\c' in u:
            print 'Misplaced Paragraph marker against chapter in: ' + b
        rx = re.compile('\\\\v [0-9]+\\n\\\\p')
        if not rx.search(u) == None:
            print 'Misplaced Paragraph marker against verse in: ' + b
            
    def testSectionHeaders(self, b, u):
        """
        Section headers associated with a chapter should appear at the beginning of that chapter rather than the end of it.
        """
        i = 0
        while i < len(u):
            i = u.find(r'\s', i)
            if i == -1:
                return
            c = u.find(r'\c', i)        
            if c == -1:
                return
            if c - i < 50:
                print 'Misplaced Section Header against chapter in: ' + b
            i = c

    def testWJ(self, b, u):
        """
        Character styles cannot cross paragraph or verse boundaries, but must be stopped and restarted at those points. This is significant with \wj ...\wj*.
Character styles (like \wj ...\wj*) cannot continue through footnotes, but must be stopped and restarted around the footnote.
        """
        i = 0
        while i < len(u):
            i = u.find(r'\wj ', i)
            if i == -1:
                return
            f = u.find(r'\f', i)        
            if f== -1:
                return
            e = u.find(r'\wj*', i)        
            if e == -1:
                return
            if f < e:
                print 'Interrupted \wj in: ' + b
            i = e
            
    def testB(self, b, u):
        """
        \b cannot have text content.
        """
        if not u.find(r'\b ') == -1: print '\\b tag with text content in: ' + b
        
    def testM(self, b, u):
        """
        \m cannot be empty of text content.
        """
        i = 0
        while i < len(u):
            i = u.find('\\m\n', i)
            if i == -1: return
            if not u[i+3] == '\\': print '\\m tag with no text content in: ' + b
            i = i + 3
