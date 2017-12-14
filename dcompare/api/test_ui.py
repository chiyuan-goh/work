"""
Author: chiyuan
Date created: 12/10/17
python version: 3.6

entry point for the application. Defines a simple qt user interface.
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

from sample_ui import Ui_Form
from runword import run
import pdb

class MyWizard(QtWidgets.QWizard):
    NUM_PAGES = 1
    delimiter = "|"

    (SelectPageID, ) = range(NUM_PAGES)

    def __init__(self, parent = None):
        super(MyWizard, self).__init__(parent)

        self.setPage(self.SelectPageID, SelectPage())
        #self.setPage(self.ProcessPageID, ProcessPage())
        self.setStartId(self.SelectPageID)

        self.setWizardStyle(self.ModernStyle)
        self.setWindowTitle("Document Comparison By DAG")

class ProcessPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        self.total_items = 0

        super(ProcessPage, self).__init__(parent)
        top_layout = QtWidgets.QVBoxLayout()

        butt_layout = QtWidgets.QHBoxLayout()

        self.cbox = QtWidgets.QComboBox()
        self.tbox = QtWidgets.QComboBox()
        prev = QtWidgets.QPushButton()
        next = QtWidgets.QPushButton()
        compare = QtWidgets.QPushButton()
        self.disp = QtWidgets.QLabel()
        prev.setText("prev")
        next.setText("next")
        compare.setText("go")

        prev.clicked.connect(self.prevItem)
        next.clicked.connect(self.nextItem)
        compare.clicked.connect(self.do_compare)
        self.cbox.currentIndexChanged.connect(self.curChanged)

        butt_layout.addWidget(self.cbox)
        butt_layout.addWidget(self.tbox)
        butt_layout.addWidget(prev)
        butt_layout.addWidget(next)
        butt_layout.addWidget(self.disp)
        butt_layout.addWidget(compare)

        top_layout.addLayout(butt_layout)
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        top_layout.addWidget(line)

        hlayout = QtWidgets.QHBoxLayout()

        self.clause_list = QtWidgets.QListWidget()
        self.clause_list.itemClicked.connect(self.clause_clicked)

        toplabel_container = QtWidgets.QGroupBox("Document 1")
        tlc_layout = QtWidgets.QVBoxLayout()
        self.top_label = QtWidgets.QLabel()
        tlc_layout.addWidget(self.top_label)
        toplabel_container.setLayout(tlc_layout)

        btmlabel_container = QtWidgets.QGroupBox("Document 2")
        tlc_layout2 = QtWidgets.QVBoxLayout()
        self.btm_label = QtWidgets.QLabel()
        tlc_layout2.addWidget(self.btm_label)
        btmlabel_container.setLayout(tlc_layout2)

        self.top_label.setText("Load and Compare your documents first.")
        self.btm_label.setText("Load and Compare your documents first.")

        hlayout.addWidget(self.clause_list)
        btm_vlayout = QtWidgets.QVBoxLayout()
        btm_vlayout.addWidget(toplabel_container)
        btm_vlayout.addWidget(btmlabel_container)
        hlayout.addLayout(btm_vlayout)

        top_layout.addLayout(hlayout)
        self.setLayout(top_layout)

    def initializePage(self):
        fields = self.field("pdfs")
        field2 = self.field("docx")
        items = str(fields.toString()).split(MyWizard.delimiter)

        for field in items:
            self.cbox.addItem(field)

        self.cbox.setCurrentIndex(0)
        self.tbox.clear()
        self.tbox.addItem(field2.toString())
        self.tbox.setEnabled(False)

        t = "%d/%d" %(1, self.cbox.count())
        self.disp.setText(t)

    def clause_clicked(self, item):
        d_twrapper = '<span style="background-color: rgb(255, 0 ,0, 100);"><font color="red">'
        i_twrapper = '<span style="background-color: rgb(0,255,0, 100);"><font color="green">'
        r_twrapper = '<span style="background-color: rgb(0,0,255, 100);"><font color="blue">'
        close_wrapper = '</font></span>'

        item_text = str(item.text())
        ret = self.dc.get_para_changes(item_text)

        if ret[0] == 'replaced':
            _, seqm, rev = ret

            output_top, output_btm = '', ''

            for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
                if opcode == 'equal':
                    if rev:
                        output_btm += seqm.a[a0:a1]
                        output_top += seqm.b[b0:b1]
                    else:
                        output_top += seqm.a[a0:a1]
                        output_btm += seqm.b[b0:b1]
                elif opcode == 'insert':
                    if rev:
                        output_top += d_twrapper + seqm.b[b0:b1] + close_wrapper
                    else:
                        output_btm += i_twrapper + seqm.b[b0:b1] + close_wrapper
                elif opcode == 'delete':
                    if rev:
                        output_btm += i_twrapper + seqm.a[a0:a1] + close_wrapper
                    else:
                        output_top += d_twrapper + seqm.a[a0:a1] + close_wrapper
                elif opcode == 'replace':
                    if rev:
                        output_btm += r_twrapper + seqm.a[a0:a1] + close_wrapper
                        output_top += r_twrapper + seqm.b[b0:b1] + close_wrapper
                    else:
                        output_top += r_twrapper + seqm.a[a0:a1] + close_wrapper
                        output_btm += r_twrapper + seqm.b[b0:b1] + close_wrapper

            self.top_label.setText(output_top)
            self.btm_label.setText(output_btm)
            self.top_label.setWordWrap(True)
            self.btm_label.setWordWrap(True)

        elif ret[0] == 'deleted':
            text = d_twrapper + ret[1] + close_wrapper
            self.top_label.setText(text)
            self.top_label.setWordWrap(True)
            self.btm_label.clear()
        elif ret[0] == 'added':
            text = i_twrapper + ret[1] + close_wrapper
            self.btm_label.setText(text)
            self.btm_label.setWordWrap(True)
            self.top_label.clear()


    def curChanged(self, v):
        t = "%d/%d" %(v+1, self.cbox.count())
        self.disp.setText(t)

    def nextItem(self):
        if self.cbox.currentIndex() + 1 >= self.cbox.count():
            return
        self.cbox.setCurrentIndex(self.cbox.currentIndex() + 1)

    def prevItem(self):
        if self.cbox.currentIndex() <= 0:
            return
        self.cbox.setCurrentIndex(self.cbox.currentIndex() - 1)

    def do_compare(self):
        self.dc = DocumentComparer(str(self.cbox.itemText(self.cbox.currentIndex())),
                              str(self.tbox.itemText(0)))

        edits = self.dc.compare_now()

        for e in edits:
            text, op = e
            w = QtGui.QListWidgetItem(text)
            #print op
            if op == 'added':
                w.setBackgroundColor(QtGui.QColor(0,255,0,80))
            elif op == 'deleted':
                w.setBackgroundColor(QtGui.QColor(255,0,0,80))
            elif op == 'replaced':
                w.setBackgroundColor(QtGui.QColor(0,0,255,80))

            self.clause_list.addItem(w)


#TODO: use events instead of class variables
class SelectPage(QtWidgets.QWizardPage):
    def set_docx(self, s):
        self.docx = str(self.template_list.item(0).text())
        self.docx_changed.emit()

    def get_docx(self):
        return self.docx

    def get_pdfs(self):
        return self.l

    def set_pdfs(self, v):
        fnames = [str(self.pdf_list.item(i).text()) for i in range(self.pdf_list.count())]
        self.l = MyWizard.delimiter.join(fnames)
        #self.list_changed.emit()
    
    
    def select(self):
        run( [str(self.pdf_list.item(i).text()) for i in range(self.pdf_list.count())] )

    def rm(self):
        items = self.pdf_list.selectedItems()
        for item in items:
            self.pdf_list.takeItem(self.pdf_list.row(item))

    def add(self):
        fnames = QtWidgets.QFileDialog.getOpenFileNames(None, "Open tender document", ".", " docx (*.docx)")
        for f in fnames[0]:
            #pdb.set_trace()
            w = QtWidgets.QListWidgetItem(f)
            self.pdf_list.addItem(w)

    def __init__(self, parent=None):
        super(SelectPage, self).__init__(parent)

        self.l = ""
        self.docx = ""

        self.setTitle("Select Documents for Comparisons")
        self.setSubTitle("You can select multiple tender documents for comparison.")
        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap, QtGui.QPixmap("logo.jpg"))
        # self.setS
        grid = QtWidgets.QGridLayout()

        self.pdf_list = QtWidgets.QListWidget()
        #self.template_list = QtWidgets.QListWidget()

        browse1_button = QtWidgets.QPushButton(None)
        browse1_button.setText("Add files")
        browse1_button.setEnabled(True)
        browse1_button.clicked.connect(self.add)
        # browse1_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        del_button = QtWidgets.QPushButton(None)
        del_button.setText("Remove")
        del_button.setEnabled(True)
        del_button.clicked.connect(self.rm)
        # del_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        doc_button = QtWidgets.QPushButton(None)
        doc_button.setText("go")
        doc_button.setEnabled(True)
        doc_button.clicked.connect(self.select)
        
        
        butt_layout = QtWidgets.QHBoxLayout()
        butt_layout.addStretch(1)
        butt_layout.addWidget(browse1_button)
        butt_layout.addWidget(del_button)
        butt_layout.addWidget(doc_button)

        grid.addWidget(self.pdf_list, 0, 0)
        #grid.addWidget(self.template_list, 0, 1)
        grid.addLayout(butt_layout, 1, 0)
        #grid.addWidget(doc_button)

        self.setLayout(grid)

        pdf_model = self.pdf_list.model()
        #docx_model = self.template_list.model()
        pdf_model.rowsInserted.connect(self.set_pdfs)
        pdf_model.rowsRemoved.connect(self.set_pdfs)
        #docx_model.rowsInserted.connect(self.set_docx)
        #self.registerField("docx", self.template_list)
        #self.registerField("pdfs*", self, "pdf_files", self.list_changed)
        #self.registerField("docx*", self, "docx_file", self.docx_changed)

    #def nextId(self):
    #    return MyWizard.ProcessPageID

    #TODO: it is v strange, list wouldnt work for fields
    #pdf_files = QtCore.pyqtProperty(str, get_pdfs, set_pdfs)
    #docx_file = QtCore.pyqtProperty(str, get_docx, set_docx)
    #list_changed = QtCore.pyqtSignal()
    #docx_changed = QtCore.pyqtSignal()



class MyForm(QtWidgets.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.setWindowTitle("Document Comparison By DAG")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
	#myapp = MyForm()
    #myapp.show()
    mywizard = MyWizard()
    mywizard.show()

    sys.exit(app.exec_() )


