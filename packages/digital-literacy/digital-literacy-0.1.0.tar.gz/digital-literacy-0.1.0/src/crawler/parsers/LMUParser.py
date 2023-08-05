"""
A parser that scrapes the required information from the PDFs
that were scraped by Scrapy + Selenium from the LMU's website.

Because all the PDFs have a constant structure throughout, we
use RegExp to get the desired information. But we first divide
the PDF into smaller blocks for a faster execution.
"""

import re
import fitz
from typing import Optional, List


def get_blocks(pdf: fitz.Document, page_num: int) -> List:
    """Get a PDF page as blocks of content"""
    return [block[4] for block in pdf[page_num].get_textpage().extractBLOCKS()]


def check_module(page_blocks: List) -> bool:
    """To check if a PDF page contains a module that needs to be scraped"""
    for block in page_blocks:
        if re.search('insgesamt \d+ ECTS.? ?Punkte erworben werden.', block):
            return True
        if re.search('For successful completion of the module, \d+ ECTS '
                     'credits have to be acquired.', block):
            return True
        if re.search('\d+ credit points are awarded for this module.', block):
            return True
    return False


def get_ects(page_blocks: List) -> Optional[str]:
    """To parse the ECTS of a module from a PDF page"""
    for block in page_blocks:
        if re.search('insgesamt \d+ ECTS-? ?Punkte erworben werden.', block):
            return re.findall(r'\d+', block)[0]
        if re.search('For successful completion of the module, \d+ ECTS credits '
                     'have to be acquired.', block):
            return re.findall(r'\d+', block)[0]
        if re.search('\d+ credit points are awarded for this module.', block):
            return re.findall(r'\d+', block)[0]
    return None


def get_name(page_blocks: List) -> Optional[str]:
    """To parse the name of a module from a PDF page"""
    for block in page_blocks:
        if re.search(r'(?:Modul:|Module:|(?:P|M|T) ?\d+.+? ?:? )(?:.|\n)+', block):
            return block.replace('-\n', '').replace('\n', ' ').strip()
    return None


def get_level(page_blocks: List) -> Optional[str]:
    """To parse the level of a module (Bachelor or Master) from a PDF page"""
    for block in page_blocks:
        if re.search(r'Bachelor', block):
            return 'Bachelor'
        if re.search(f'Master', block):
            return 'Master'
    return None


def get_contents(page_blocks: List) -> Optional[str]:
    """To scrape the contents of a module from a PDF page"""
    max_block = len(page_blocks)
    cur_block = 0
    module_content = str()
    while cur_block < max_block:
        if re.search(r'(?:Inhalte ?\n|Contents? ?\n)', page_blocks[cur_block]):
            block = page_blocks[cur_block]
            while True:
                cur_block += 1
                try:
                    new_block = page_blocks[cur_block]
                except IndexError:
                    break
                else:
                    if re.search(r'(?:Form der Modul|Type of examination)', new_block):
                        break
                    if re.search(r'Qualifikation Aims ?\n', new_block):
                        block += new_block + page_blocks[cur_block+1]
                        break
                    block += new_block
            module_content = block
        else:
            cur_block += 1
    if module_content:
        return module_content.replace('-\n', '').strip()
    return None


def get_lang(page_blocks: List) -> Optional[str]:
    """To scrape the language of a module from a PDF page"""
    lang = []
    for block in page_blocks:
        if re.search(r'(?:Deutsch|German)', block):
            lang.append('Deutsch')
        if re.search(r'(?:Englisch|English)', block):
            lang.append('Englisch')
        if lang:
            return '/'.join(lang)
    return None
