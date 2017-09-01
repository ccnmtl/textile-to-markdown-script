import sys
import re
import unicodedata

import pdb


def slugify(value):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
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
# join all the lines together, then regex the words between the keywords and
# line breaks. For the body, match the lines between "BODY: " and "-----"
    def __init__(self, lines):
        pdb.set_trace()
        for line in lines:
            # How do you get these values?
            if re.match('AUTHOR', line):
                self._author = line

            if re.match('TITLE', line):
                self._title = line

            if re.match('STATUS', line):
                self._status = line

            if re.match('PRIMARY CATEGORY', line):
                self._primary_category = line
            else:
                self._primary_category = 'foo'

            if re.match('CATEGORY', line):
                self._category = line
            else:
                self._category = 'foo'

            if re.match('DATE', line):
                self._date = line

        for line in lines:
            if re.match('BODY', line):
                self._body = line

    def convert_to_markdown(self):
        # TODO: create a file using the title as a file name
        # then write out the MD file
        f = open(slugify(self._title) + '.md', 'w')
        f.writelines([
            self._author,
            self._title,
            self._status,
            self._primary_category,
            self._category,
            self._date,
            self._body])
        f.close()


def process_file():
    pages = []
    with open(sys.argv[1], 'r') as source:
        line_buffer = []
        for line in source:
            if re.match(r'--------', line):
                # export_file = open('file_%s.test' % str(filename).zfill(3), 'w')
                # export_file.writelines(line_buffer)
                # export_file.close()
                pages.append(Page(line_buffer))
                line_buffer = []
            else:
                line_buffer.append(line)

    for page in pages:
        page.convert_to_markdown()


if __name__ == '__main__':
    if (sys.argv[1]):
        process_file()
    else:
        print("Please pass in file")
