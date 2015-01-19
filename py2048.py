#!/usr/bin/env python
import sys
import random

from PyQt4 import QtCore, QtGui

class basicScene:
    def __init__(self):
        self.scene =    [   [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]]
        self.seed()
        
    def rotate(self, x, n=1):
        if n == 0: return x
        r = [list(l) for l in zip(*x[::-1])]
        if n == 1: return r
        else:
            return self.rotate(r, n-1)
            
    def compress(self, x):
        tmpArray = []
        for line in x:
            tmp = 0
            tmpLine = []
            for e in line:
                if e == 0:
                    continue
                elif tmp == 0:
                    # First figure of 'maybe a suite'
                    tmp = e
                elif e == tmp:
                    tmpLine.append(2*e)
                    tmp = 0
                else:
                    tmpLine.append(tmp)
                    tmp = e
            if tmp != 0:
                tmpLine.append(tmp)
            tmpArray.append(( tmpLine + [0]*4 )[0:4] )
        return tmpArray
        
    def seed(self):
        # Choose one empty place to add a '2'
        seedPlace = random.choice([iElem + 4*iLine for (iLine, line) in enumerate(self.scene) for (iElem, elem) in enumerate(line) if elem == 0])
        self.scene[seedPlace/4][seedPlace%4] = 2
        return self.scene
            
    def canPlay(self):
        return [(self.left, self.down, self.right, self.up)[i] for i in range(4) if (self.left, self.down, self.right, self.up)[i](self.scene[:]) != self.scene]
        
    def disp(self):
        print ''
        for line in self.scene:
            print line
    
    def left(self, scene=None):
        x = scene or self.scene
        x = self.compress(x)
        if not scene:
            self.scene = x
        return x
            
        return scene
    def down(self, scene=None):
        x = scene or self.scene
        x = self.rotate(self.compress(self.rotate(x, 1)), 3)
        if not scene:
            self.scene = x
        return x
    def right(self, scene=None):
        x = scene or self.scene
        x = self.rotate(self.compress(self.rotate(x, 2)), 2)
        if not scene:
            self.scene = x
        return x
    def up(self, scene=None):
        x = scene or self.scene
        x = self.rotate(self.compress(self.rotate(x, 3)), 1)
        if not scene:
            self.scene = x
        return x

class wgt(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            
            self.scene = basicScene()
            self.scene.seed()
            
            self.mainLayout = QtGui.QGridLayout()
            self.mainLayout.setSpacing(0)
            
            for i in range(16):
                x = QtGui.QLineEdit('0')
                x.setReadOnly(True)
                x.setAlignment(QtCore.Qt.AlignHCenter)
                f = x.font()
                f.setPointSize(15)
                x.setFont(f)

                self.mainLayout.addWidget(x, i/4, i%4)
            
            self.refresh()
            
            self.setLayout(self.mainLayout)
            
            self.setFocus(QtCore.Qt.OtherFocusReason)
            
        def refresh(self):
            for i in range(16):
                bgColor = { 0:QtGui.QColor('#333333'), 
                            2:QtGui.QColor('#CCCCFF'), 
                            4:QtGui.QColor('#FFFF99'), 
                            8:QtGui.QColor('#FF9933') , 
                            16:QtGui.QColor('#FF6600') , 
                            32:QtGui.QColor('#FF3333') , 
                            64:QtGui.QColor('#FF0000') , 
                            128:QtGui.QColor('#FFFF66') , 
                            256:QtGui.QColor('#FFFF33') , 
                            512:QtGui.QColor('#FFFF00') , 
                            1024:QtGui.QColor('#FFFF00') }
                fontColor = {   0:QtGui.QColor('#333333'), 
                                2:QtGui.QColor('#333333'), 
                                4:QtGui.QColor('#333333'), 
                                8:QtGui.QColor('#FFFFFF'), 
                                16:QtGui.QColor('#FFFFFF'), 
                                32:QtGui.QColor('#FFFFFF'), 
                                64:QtGui.QColor('#FFFFFF'), 
                                128:QtGui.QColor('#FFFFFF'), 
                                256:QtGui.QColor('#FFFFFF'), 
                                512:QtGui.QColor('#FFFFFF'), 
                                1024:QtGui.QColor('#FFFFFF'), 
                }
            
                (w, val) = (self.mainLayout.itemAtPosition(i/4, i%4).widget(), self.scene.scene[i/4][i%4])
                w.setText('%d' % val)
                p = QtGui.QPalette()
                p.setColor(QtGui.QPalette.Base, bgColor.get(val, bgColor[1024]))
                p.setColor(QtGui.QPalette.Text, fontColor.get(val, fontColor[1024]))
                w.setPalette(p)
                
        def keyPressEvent(self, event):
            f = {   QtCore.Qt.Key_Left:self.scene.left,
                QtCore.Qt.Key_Down:self.scene.down,
                QtCore.Qt.Key_Right:self.scene.right,
                QtCore.Qt.Key_Up:self.scene.up,
            }.get(event.key())
            if f in self.scene.canPlay():
                f()
                self.scene.seed()
                self.refresh()
            
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Choose between : auto/qt'
    else:
        if sys.argv[1].lower() == 'auto':
            scene = basicScene()
            try:
                for i in range(100):
                    scene.seed()
                    scene.disp()
                    random.choice(scene.canPlay())()
            except:
                print 'Perdu'
        elif sys.argv[1].lower() == 'qt':
            app = QtGui.QApplication([])
            app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
            
            x = wgt()
            x.resize(100, 100)
            x.show()
            
            app.exec_()
        else:
            print 'Unknown mode ' + sys.argv[1]
