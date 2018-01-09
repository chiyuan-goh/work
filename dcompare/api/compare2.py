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
from .test import iter_block_items
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_ALIGN_PARAGRAPH

ITT_SECTIONS = ['instructions to tenderers', 'conditions of contract', 'requirement specifications']

class DocCompare(object):
    """Parses a tender document and return a document in terms of map<big_section, <small_clause, clause_content>>"""
    def __init__(self):
        self.documents = []
        self.document_struct = []

    def parseHeader(self, text):
        try:
            float(text.strip())
            return True
        except:
            return False

    def add_doc(self, fname):
        self.documents.append(fname)

    def all_contents(self):
        all_content = [self.get_content(Document(d)) for d in self.documents]
        return all_content

    def is_clause_header(self, para):
        return type(para) == Paragraph and \
               self.parseHeader(para.text.split("\t")[0]) and \
               (para.text.isupper() or para.style.font.all_caps is True) and \
               len(para.text.split("\t")) > 1
        
    def is_section_header(self, block):
        return type(block) == Table and \
               len(block.rows) == 1 and \
               block.rows[0].cells[0].text.strip().startswith("SECTION") and \
        ":" in block.rows[0].cells[0].text

    def is_valid_section(self, block):
        text = block.rows[0].cells[0].text
        h = text.split(":")[1].strip()
        return h.lower() in ITT_SECTIONS, text.strip()

    def is_new_term(self, block):
        return self.parseHeader(block.text.split("\t")[0])

    def get_doc_struct(self, doc):
        """
        Gives an overview of the documents structure e.g name of sections, clauses and number of terms in clause
        :param doc:
        :return:
        """
        doc_struct = {}
        for section, section_content in doc.items():
            clauses = {}
            for clause, content in section_content.items():
                count_terms = 0
                for p in content['content']:
                    if self.is_new_term(p):
                        count_terms += 1

                clauses[clause] = {'num_para':count_terms, 'num': content['num']}

            doc_struct[section] = clauses

        return doc_struct

        
    def get_content(self, doc):
        content_str = 'content'
        clauses = {}
        sections = {}
        clause_content = []
        clause_header = None
        section_header = None
        
        all_blocks = iter_block_items(doc)
        
        for num, p in enumerate(all_blocks):
            is_cheader = self.is_clause_header(p)
            is_sheader = self.is_section_header(p)

            #reach a new section
            if is_sheader:
                if section_header != None:
                    if clause_header is not None and clause_content:
                        clauses[clause_header] = {content_str: clause_content, 'num': clause_num}
                    sections[section_header] = clauses
                
                valid, h = self.is_valid_section(p)
                if valid:
                    section_header =  h
                else:
                    section_header = None
                
                clauses = {}
                clause_content = []
                clause_header = None

            #reach a new clause
            elif is_cheader:
                if len(clause_content) != 0 and clause_header is not None:
                    clauses[clause_header] = {content_str: clause_content, 'num': clause_num}
                # x =  p.text.split("\t")
                #[clause_num, clause_header] = p.text.split("\t")
                arr = p.text.split("\t")
                clause_num = arr[0]
                clause_header = arr[1]
                clause_header = clause_header.strip().lower()
                clause_content = []
            
            else:
                if type(p) == Paragraph and p.text.strip() != '':
                    clause_content.append(p)

        clauses[clause_header] = {content_str: clause_content, 'num': clause_num}
        if section_header != None:
            sections[section_header] = clauses
            
        ################################################### calculate hashes ############################################
        for bk, bv in sections.items():
            for i,(k,v) in enumerate(bv.items()):
                text_chunk = []
                raw_text = v[content_str][0].text
                text = re.sub(r'(\xa0+)', '\t', raw_text)
                text = re.sub(r'(\s\s+)', '\t', text)
                if len(text.split("\t")) > 1:
                    leave_subsec = text.split("\t")[1].strip().lower()
                else:
                    leave_subsec = text.strip().lower()
         
                text_chunk.append(leave_subsec)

                for p in v[content_str][1:]:
                    if p.text.strip() != '':
                        text_chunk.append(p.text.strip().lower())
                text_str = "\n\n".join(text_chunk)
                hashstr = hashlib.md5(text_str.encode("utf-8")).hexdigest()
                bv[k]['hash'] = hashstr

        return sections

if __name__ == '__main__':
    file1 = 'itt_edited.docx'
    file2 = 'itt_edited_modified.docx'
    #compare_docs(file1, file2)