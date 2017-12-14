"""
Author: chiyuan
Date created: 12/10/17
python version: 3.6

 parses the .docx files (python-docx) and represents each document as a set of clause headers e.g "VALIDITY PERIOD" and their respective content.
"""

from docx import Document
import pdb
import hashlib
import re
from test import iter_block_items
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_ALIGN_PARAGRAPH

class DocCompare(object):
"""Parses a tender document and return a document in terms of map<big_section, <small_clause, clause_content>>"""
    def __init__(self):
        self.documents = []

    def parseHeader(self, text):
        try:
            float(text.strip())
        except:
            return False
        return True

    def add_doc(self, fname):
        self.documents.append(fname)

    def all_contents(self):
        all_shit = [self.get_content(Document(d)) for d in self.documents]
        return all_shit

    def is_clause_header(self, para):
        if type(para) != Paragraph or len(para.text.split("\t")) == 0:
            return False
            
        text = para.text
        #return self.parseHeader(text.split("\t")[0]) and para.style.font.all_caps and len(text.split("\t")) > 1
        return self.parseHeader(text.split("\t")[0]) and (para.text.isupper() or para.style.font.all_caps is True) and len(text.split("\t")) > 1
        
    def is_bigsection_header(self, block):
        #pdb.set_trace()
        return type(block) == Table and len(block.rows) == 1 and block.rows[0].cells[0].text.strip().startswith("SECTION") and \
        ":" in block.rows[0].cells[0].text
        #return block.text.startswith("SECTION") and ":" in block.text # and para.alignment == WD_ALIGN_PARAGRAPH.CENTER
        
    def is_valid_bigsection(self, block):
        text = block.rows[0].cells[0].text
        h = text.split(":")[1].strip()
        return h.lower() in ['instructions to tenderers', 'conditions of contract', 'requirement specifications'], text.strip()

        
    def get_content(self, doc):
        clause_text = {}
        bigsections = {}
        section = []
        header_text = None
        bigsection_text = None
        
        all_blocks = iter_block_items(doc)
        
        for num, p in enumerate(all_blocks):
            is_header = self.is_clause_header(p)
            is_bigheader = self.is_bigsection_header(p)
            
            #if type(p) == Paragraph and p.text.lower().strip().endswith("in performance"):
            #   pdb.set_trace()
            
            #print(p.text)
            #if 'SECTION' in p.text and 'conditions of contract' in p.text.lower():
            #    pdb.set_trace()
            if is_bigheader: #reach a new big section
                #pdb.set_trace()
                if bigsection_text != None: 
                    if header_text is not None and section:
                        clause_text[header_text] = {'section': section}
                    bigsections[bigsection_text] = clause_text
                
                valid, h = self.is_valid_bigsection(p)
                #if valid and 'REQUIREMENT' in h:
                #   pdb.set_trace()
                if valid:
                    bigsection_text =  h
                else:
                    bigsection_text = None
                
                clause_text = {}
                section = []
                header_text = None

            elif is_header: #reach a new section:
                if len(section) != 0 and header_text is not None:
                    clause_text[header_text] = {'section': section}
                
                header_text = p.text.split("\t")[1].strip().lower()
                section = []
            
            else:
                if type(p) == Paragraph and p.text.strip() != '':
                    section.append(p)

        clause_text[header_text] = {'section': section}
        if bigsection_text != None:
            bigsections[bigsection_text] = clause_text
            
        ################################################### calculate hashes ############################################
        for bk, bv in bigsections.items():
            for i,(k,v) in enumerate(bv.items()):
                text_chunk = []
                raw_text = v['section'][0].text
                text = re.sub(r'(\xa0+)', '\t', raw_text)
                text = re.sub(r'(\s\s+)', '\t', text)
                if len(text.split("\t")) > 1:
                    leave_subsec = text.split("\t")[1].strip().lower()
                else:
                    leave_subsec = text.strip().lower()
         
                text_chunk.append(leave_subsec)

                for p in v['section'][1:]:
                    if p.text.strip() != '':
                        text_chunk.append(p.text.strip().lower())
                text_str = "\n\n".join(text_chunk)
                hashstr = hashlib.md5(text_str.encode("utf-8")).hexdigest()
                bv[k]['hash'] = hashstr
                
                #if k == "withdrawal of tender proposal": 
                 #   pdb.set_trace()
        
        return bigsections

if __name__ == '__main__':
    file1 = 'itt_edited.docx'
    file2 = 'itt_edited_modified.docx'
    #compare_docs(file1, file2)