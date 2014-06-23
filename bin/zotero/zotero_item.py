#-*- coding:utf-8 -*-

"""
This file is part of Gnotero.

Gnotero is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Gnotero is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Gnotero.  If not, see <http://www.gnu.org/licenses/>.
"""

term_collection = None, u"collection"
term_tag = None, u"tag"
term_author = None, u"author"
term_date = None, u"date", u"year"
term_publication = None, u"publication", u"journal"
term_title = None, u"title"

cache = {}

from bibliographydatabase import *

class zoteroItem(object):
    """Represents a single zotero item."""

    def __init__(self, init=None, noteProvider=None):

        """
        Constructor.

        Keyword arguments:
        init			--	A `dict` with item information, or an `int` with the
                            item id	. (default=None)
        noteProvider	--	A noteProvider object. (default=None)
        """

        self.gnotero_format_str = None
        self.simple_format_str = None
        self.filename_format_str = None
        self.collection_color = u"#000000"
        self.noteProvider = noteProvider
        self.note = -1
        if isinstance(init, dict):
            if u"item_id" in item:
                self.id = item[u"item_id"]
            else:
                self.id = None

            if u"publicationTitle" in item:
                self.publication = item[u"publicationTitle"]
            else:
                self.publication = None

            if u"title" in item:
                self.title = item[u"title"]
            else:
                self.title = None

            if u"author" in item:
                self.authors = item[u"author"]
            else:
                self.authors = []

            if u"date" in item:
                self.date = item[u"date"]
            else:
                self.date = None

            if u"issue" in item:
                self.issue = item[u"issue"]
            else:
                self.issue = None

            if u"volume" in item:
                self.volume = item[u"volume"]
            else:
                self.volume = None

            if u"fulltext" in item:
                self.fulltext = item[u"fulltext"]
            else:
                self.fulltext = None

            if u"collections" in item:
                self.collections = item[u"collections"]
            else:
                self.collections = []

            if u"tags" in item:
                self.tags = item[u"tags"]
            else:
                self.tags = []

            if u"key" in item:
                self.key = item[u"key"]
            else:
                self.key = None

            if u"DOI" in item:
                self.doi = item[u"DOI"]
            else:
                self.doi = None

            if u"typeName" in item:
                self.item_type = item[u"typeName"]
            else:
                self.item_type = None

            if u"pages" in item:
                self.pages = item[u"pages"]
            else:
                self.pages = None

        else:
            self.title = None
            self.collections = []
            self.publication = None
            self.authors = []
            self.tags = []
            self.issue = None
            self.volume = None
            self.fulltext = None
            self.date = None
            self.key = None
            self.item_type = None
            self.doi = None
            self.pages = None
            if isinstance(init, int):
                self.id = init
            else:
                self.id = None

    def match(self, terms):

        """
        Matches the current item against a term.

        Arguments:
        terms	--	A list of (term_type, term) tuples.

        Returns:
        True if the current item matches the terms, False otherwise.
        """

        global term_collection, term_author, term_title, term_date, \
            term_publication, term_tag

        # Author is a required field. Without it we don't search
        if len(self.authors) > 0:
            # Do all criteria match?
            match_all = True
            # Walk through all search terms
            for term_type, term in terms:
                match = False
                if term_type in term_tag:
                    for tag in self.tags:
                        if term in tag.lower():
                            match = True
                if term_type in term_collection:
                    for collection in self.collections:
                        if term in collection.lower():
                            match = True
                if not match and term_type in term_author:
                    for author in self.authors:
                        for author_component in author:
                            if term in author_component.lower():
                                match = True
                if not match and self.date is not None and term_type in term_date:
                    if term in self.date:
                        match = True
                if not match and self.title is not None and term_type in \
                        term_title and term in self.title.lower():
                    match = True
                if not match and self.publication is not None and term_type in \
                        term_publication and term in self.publication.lower():
                    match = True
                if not match:
                    match_all = False
                    break
            return match_all
        return False

    def get_note(self):

        """
        Retrieves a note.

        Returns:
        A note for the current item.
        """

        if self.note != -1:
            return self.note
        self.note = self.noteProvider.search(self)
        return self.note

    def format_single_author(self, author):
        if len(author) > 1:
            return u'{0}, {1}'.format(author[0], author[1])
        else:
            return author[0]

    def format_multiple_author(self, authors):
        author_string = u''

        for author in authors[:-1]:
            if len(author) > 1:
                author_string += u'{0}, {1}, '.format(author[0], author[1])
            else:
                author_string += author[0]

        for author in authors[-1:]:
            if len(author) > 1:
                author_string += u'& {0}, {1}'.format(author[0], author[1])
            else:
                author_string += author[0]

        return author_string

    def format_author(self):
        """
        Returns:
        A pretty representation of the author.
        """

        if len(self.authors) == 0:
            return u"Unknown author"
        if len(self.authors) > 5:
            return u"%s et al." % self.format_single_author(self.authors[0])
        if len(self.authors) > 2:
            return self.format_multiple_author(self.authors)
        if len(self.authors) == 2:
            return self.format_single_author(self.authors[0]) + u" & " + self.format_single_author(self.authors[1])
        return self.format_single_author(self.authors[0])

    def format_date(self):

        """
        Returns:
        A pretty representation of the date.
        """

        if self.date == None:
            return u"(Date unknown)"

        return u"(%s)" % self.date

    def format_title(self):

        """
        Returns:
        A pretty representation of the title.
        """

        if self.title == None:
            return u"Unknown title"
        return self.title

    def format_publication(self):

        """
        Returns:
        A pretty representation of the publication (journal).
        """

        if self.publication is None:
            return u"Unknown journal"
        return self.publication

    def format_tags(self):

        """
        Returns:
        A pretty representation of the tags.
        """

        return u", ".join(self.tags)

    def gnotero_format(self):

        """
        Returns:
        A pretty apa-like representation of the item, which can be used as a
        label in Qnotero.
        """

        if self.gnotero_format_str is None:
            s = u"<b>" + self.format_author() + u" " + self.format_date() + \
                u"</b>"
            if self.title is not None:
                s += u"\n<small>" + self.title
            if self.publication is not None:
                s += u"\n<i>" + self.publication
                if self.volume is not None:
                    s += u", %s" % self.volume
                s += u"</i>"
                if self.issue is not None:
                    s += u"(%s)" % self.issue
            s += u"</small>"
            self.gnotero_format_str = s.replace(u"&", u"&amp;")
        return self.gnotero_format_str

    def full_format(self):

        """
        Returns:
        A pretty, extensive representation of the current item.
        """

        if self.gnotero_format_str is None:
            s = self.format_author() + u" " + self.format_date()
            if self.title is not None:
                s += u"\n" + self.title
            if self.publication is not None:
                s += u"\n" + self.publication
                if self.volume is not None:
                    s += u", %s" % self.volume
                if self.issue is not None:
                    s += u"(%s)" % self.issue
            else:
                s += u"\n"
            if self.tags is not None:
                s += u"\n" + self.format_tags()
            self.gnotero_format_str = s
        return self.gnotero_format_str

    def simple_format(self):

        """
        Returns:
        A pretty, simple representation of the current item.
        """

        if self.simple_format_str is None:
            self.simple_format_str = self.format_author() + u" " + self.format_date()
        return self.simple_format_str

    def JATS_format(self):
        page_regex = re.compile('^\s*\d+\s*-\s*\d+\s*$')
        fpage = None
        lpage = None

        if self.pages is not None:
            if page_regex.match(self.pages):
                fpage = self.pages.split('-')[0].strip()
                lpage = self.pages.split('-')[1].strip()

        if self.item_type == 'journalArticle':
            authors = []

            for author in self.authors:
                if len(author) > 1:
                    p = Person(author[1], author[0])
                else:
                    p = Person('', author[0])
                authors.append(p)

            ja = JournalArticle(authors=authors, title=self.title, journal=self.publication, issue=self.issue,
                                volume=self.volume,
                                doi=self.doi, fpage=fpage, lpage=lpage)

            return ja.get_citation()

    def hashKey(self):

        """
        Returns:
        A hash representation of the current object.
        """

        global cache
        hashKey = unicode(self)
        cache[hashKey] = self
        return hashKey

