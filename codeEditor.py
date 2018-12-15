import sys
import os


class Mainindow(QMainWindow,UI_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)

    self.setupUi(self)
    self.action_new=self.editAction(self.action_new,self.fileNew, QKeySequence.New, "filenew","clear the text window for new file!")
