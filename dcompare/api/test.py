"""
Author: chiyuan
Date created: 12/10/17
python version: 3.6

Gives the ability to iterate in order of all xml elements instead of just images or paragraphs individually
"""

from docx.document import Document
from docx import Document as Document2
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import pdb

def iter_block_items(parent):
    """
    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of either Table or Paragraph. *parent*
    would most commonly be a reference to a main Document object, but
    also works for a _Cell object, which itself can contain paragraphs and tables.
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

            
if __name__ == '__main__':

    d = Document2("C:/Users/mas_cygoh/Desktop/stressfulshit/stressfulshit/Consolidated Tender Docs/2.docx")
    dd = iter_block_items(d)
    
    for item in dd:
        
        if type(item) == Table:
            pdb.set_trace()
        elif type(item) == Paragraph:
            print(item.text)