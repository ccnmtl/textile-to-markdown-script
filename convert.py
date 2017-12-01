import sys
import re
import unicodedata

import pypandoc


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
    re_author = re.compile(r'(AUTHOR: )(.*)')
    re_title = re.compile(r'(TITLE: )(.*)')
    re_status = re.compile(r'(STATUS: )(.*)')
    re_primary_category = re.compile(r'(PRIMARY CATEGORY: )(.*)')
    re_category = re.compile(r'(CATEGORY: )(.*)')
    re_date = re.compile(r'(DATE: )(.*)')
    re_body = re.compile(r'(?s)(?<=BODY:\n).*?(?=-----)')

    def __init__(self, text):
        author = self.re_author.search(text)
        self._author = author.group(2) if author and author.group(2) else ''

        title = self.re_title.search(text)
        self._title = title.group(2) if title and title.group(2) else ''

        status = self.re_status.search(text)
        self._status = status.group(2) if status and status.group(2) else ''

        primary_category = self.re_primary_category.search(text)
        self._primary_category = primary_category.group(2) if primary_category\
            and primary_category.group(2) else ''

        category = self.re_category.search(text)
        self._category = category.group(2) if category and category.group(2)\
            else ''

        date = self.re_date.search(text)
        self._date = date.group(2) if date and date.group(2) else ''

        body = self.re_body.search(text)
        self._body = body.group() if body else ''

    def convert_to_markdown(self):
        f = open(slugify(self._title) + '.md', 'w')
        f.writelines([
            self._author,
            self._title,
            self._status,
            self._primary_category,
            self._category,
            self._date,
            pypandoc.convert_text(self._body, 'textile', format='md')])
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


def process_file(filename):
    for page in get_page(filename):
        Page(page).convert_to_markdown()


if __name__ == '__main__':
    while True:
        filename = input("Please enter a file name: ")
        try:
            process_file(filename)
        except OSError:
            print("Huh, didn't catch it. Try one more time. Thanks.")
        except (KeyboardInterrupt, EOFError):
            sys.exc_clear()
            pass
