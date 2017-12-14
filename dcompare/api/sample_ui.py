from PyQt5 import QtCore, QtGui
#from compare import DocCompare
import os
import re
import io
import difflib, pdb
#from tesserocr import PyTessBaseAPI, RIL, PSM
from docx import Document





try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def __init__(self):
        self.compare = DocCompare()

    def getfile1(self):
        fname = QtGui.QFileDialog.getOpenFileName(None, "Open Doc 1", ".", "*.docx")
        if os.path.exists(fname):
            self.document = Document(str(fname))

            # self.compare.set_doc1(fname)
            # self.browse1_button.setIcon(QtGui.QIcon("loaded_word.png"))
            # # self.browse1_button.setIconSize(QtCore.QSize(80, 80))
            # filename = os.path.basename(str(fname))
            # print 'filename is %s' %filename
            # self.browse1_button.setText(filename)
            # self.toplabel_container.setTitle(filename)

            # self.browse2_button.setEnabled(True)
            # self.doc1_fname = filename

    def getfile2(self):
        fname = QtGui.QFileDialog.getOpenFileName(None, "Open PDF", ".", " PDF (*.pdf)")
        # if os.path.exists(fname):
        #     os.system('convert -background "#FFFFFF" -units PixelsPerInch -density 300  %s tmp.png' %fname)
        #
        #     self.pngpdf = []
        #     for f in os.listdir('.'):
        #         if 'tmp-' in f and f.endswith('.png'):
        #             self.pngpdf.append(f)
        #
        #     self.pngpdf.sort()

            # self.compare.set_doc2(fname)
            # self.browse2_button.setIcon(QtGui.QIcon("loaded_word.png"))
            # # self.browse2_button.setIconSize(QtCore.QSize(80, 80))
            # filename = os.path.basename(str(fname))
            # self.browse2_button.setText(filename)
            # self.btmlabel_container.setTitle(filename)

            # self.browse3_button.setEnabled(True)
            # self.compare_button.setEnabled(True)

            # self.doc2_fname = filename
        self.pdf_filename = fname

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(528, 250)

        ##### set up top row
        self.compare_button = QtGui.QPushButton("compare NDA")
        # self.compare_button.setEnabled(False)

        self.browse1_button = QtGui.QToolButton(None)
        self.browse1_button.setIcon(QtGui.QIcon("unloaded_word.png"))
        self.browse1_button.setIconSize(QtCore.QSize(80, 80))
        self.browse1_button.setText("Base Template")
        self.browse1_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        #self.browse2_button = QtGui.QPushButton("Doc 2")
        """
        self.browse2_button = QtGui.QToolButton(None)
        self.browse2_button.setIcon(QtGui.QIcon("unloaded_word.png"))
        self.browse2_button.setIconSize(QtCore.QSize(80, 80))
        self.browse2_button.setText("User NDA")
        self.browse2_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.browse2_button.setEnabled(True)
        """
        
        self.browse1_button.clicked.connect(self.getfile1)
        #self.browse2_button.clicked.connect(self.getfile2)
        self.compare_button.clicked.connect(self.compare_now)
        #self.browse1_button.setText("Select doc1")
        #self.browse2_button.setText("Select doc2")

        self.btm_row_hlayout = QtGui.QHBoxLayout()
        self.btm_row_hlayout.addStretch(1)
        self.btm_row_hlayout.addWidget(self.compare_button)

        self.top_row_hlayout = QtGui.QHBoxLayout()
        self.top_row_hlayout.setObjectName("top rowh")
        # self.top_row_hlayout.addStretch(1)
        self.top_row_hlayout.addWidget(self.browse1_button)
        self.top_row_hlayout.addWidget(self.browse2_button)

        self.top_row_vlayout = QtGui.QVBoxLayout()
        # self.top_row_vlayout.addStretch(1)
        self.top_row_vlayout.addLayout(self.top_row_hlayout)
        self.top_row_vlayout.addLayout(self.btm_row_hlayout)
        ##### end set up top row

        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("top_level")

        self.vlayout = QtGui.QVBoxLayout()
        self.vlayout.setObjectName("vlayout_top")

        self.hlayout = QtGui.QHBoxLayout()
        self.hlayout.setObjectName("content layout")

        self.clause_list = QtGui.QListWidget()
        self.clause_list.setObjectName("clause_list")

        self.clause_list.itemClicked.connect(self.clause_clicked)

        # self.toplabel_frame = QtGui.QFrame()
        # self.toplabel_frame.setStyleSheet("QFrame {background-color: rgb(255,0,0);}")
        # self.toplabel_frame.addWidget(self.top_label)
        self.toplabel_container = QtGui.QGroupBox("Document 1")
        tlc_layout = QtGui.QVBoxLayout()
        self.top_label = QtGui.QLabel()
        tlc_layout.addWidget(self.top_label)
        self.toplabel_container.setLayout(tlc_layout)
        
        self.btmlabel_container = QtGui.QGroupBox("Document 2")
        tlc_layout2 = QtGui.QVBoxLayout()
        self.btm_label = QtGui.QLabel()
        tlc_layout2.addWidget(self.btm_label)
        self.btmlabel_container.setLayout(tlc_layout2)

        self.top_label.setText("Load and Compare your documents first.")
        self.btm_label.setText("Load and Compare your documents first.")

        self.hlayout.addWidget(self.clause_list)
        self.btm_vlayout = QtGui.QVBoxLayout()
        self.btm_vlayout.addWidget(self.toplabel_container)
        self.btm_vlayout.addWidget(self.btmlabel_container)
        # self.btm_vlayout.addWidget(self.top_label)
        # self.btm_vlayout.addWidget(self.btm_label)
        self.hlayout.addLayout(self.btm_vlayout)

        self.vlayout.addLayout(self.top_row_vlayout)
        self.vlayout.addLayout(self.hlayout)

        self.gridLayout.addLayout(self.vlayout, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

