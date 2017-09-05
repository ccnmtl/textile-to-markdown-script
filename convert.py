import sys
import re
import unicodedata

import pdb


def slugify(value):
    """
    Convert to ASCII. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.

    Borrowed from Django:
    https://github.com/django/django/blob/master/django/utils/text.py#L403
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value)\
        .encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


class Page:
    """Page is a representation of single page to be exported"""
    re_author = re.compile(r'(?s)(?<=AUTHOR: )*?(?=\n)')
    re_title = re.compile(r'(?s)(?<=TITLE: )*?(?=\n)')
    re_status = re.compile(r'(?s)(?<=STATUS: )*?(?=\n)')
    re_primary_category = re.compile(r'(?s)(?<=PRIMARY CATEGORY: )*?(?=\n)')
    re_category = re.compile(r'(?s)(?<=CATEGORY: )*?(?=\n)')
    re_date = re.compile(r'(?s)(?<=DATE: )*?(?=\n)')
    re_body = re.compile(r'(?s)(?<=BODY:\n)*?(?=-----)')

    def __init__(self, text):
        pdb.set_trace()
        self._author = self.re_author.search(text).group()
        self._title = self.re_title.search(text).group()
        self._status = self.re_status.search(text).group()
        self._primary_category = self.re_primary_category.search(text).group()
        self._category = self.re_category.search(text).group()
        self._date = self.re_date.search(text).group()
        self._body = self.re_body.search(text).group()

    def convert_to_markdown(self):
        # TODO: create a file using the title as a file name
        # then write out the MD file
        f = open(slugify(self._title) + '.md', 'w')
        f.writelines([
            self._author if self._author else '',
            self._title if self._title else '',
            self._status if self._status else '',
            self._primary_category if self._primary_category else '',
            self._category if self._category else '',
            self._date if self._date else '',
            self._body if self._body else ''])
        f.close()


def get_page(mt_export_file):
    """ Takes in a content export from MovableType and returns a string
    contianing the content of page"""
    with open(mt_export_file, 'r') as source:
        line_buffer = []
        for line in source:
            if re.match(r'--------', line):
                yield "".join(line_buffer)
                line_buffer = []
            else:
                line_buffer.append(line)


def process_file():
    for page in get_page(sys.argv[1]):
        Page(page).convert_to_markdown()


if __name__ == '__main__':
    if (sys.argv[1]):
        process_file()
    else:
        print("Please pass in file")
