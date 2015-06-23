import os
import re
import sys
import getopt

class WikiConfig:
    '''
    Section number:
    - Alphanumeric characters are accepted
    - For letters, only upper case is accepted
    - Subsections can be specified by using dots
    - A dash (-) separates the section from the title
    '''
    SECTION_RE = "([A-Z0-9]+(\.[A-Z0-9]+)*-)"

    '''
    Page or section title:
    - Accepts most characters (let the file system impose the file name
      restrictions)
    - Dots (.) and white spaces are not accepted
    - "Words" should be separated by dashes (-)
    '''
    TITLE_RE = "([^\s\.-]+(-[^\s\.-]+)*)"

    '''
    Optionally starts with a section number, followed by a title.
    '''
    DIR_RE = SECTION_RE + "?" + TITLE_RE + "$"

    '''
    Optionally starts with a section number, followed by a title, followed by 
    the ".md" file extension.
    '''
    PAGE_RE = SECTION_RE + "?" + TITLE_RE + "\.md$"

    DEFAULT_IGNORE_LIST = [
        "^\..*", # Hidden files
        "^_.*" # Sidebars and footers
    ]
    
    SIDEBAR_PREFIX = "_Sidebar"
    FOOTER_PREFIX = "_Footer"
    DEFAULT_PAGE = "Home"

class WikiItem:
    def __init__(self, entry, parent):
        self.entry = entry
        self._parent = parent
        
        if parent is None:
            self._path = "."
            self._level = 0
            self._is_dir = True
            self.link = WikiConfig.DEFAULT_PAGE
            self.title = WikiConfig.DEFAULT_PAGE
        else:
            self._path = os.path.join(parent.get_path(), entry)
            self._level = parent._level + 1

            self._is_dir = os.path.isdir(self._path)
            if self._is_dir:
                match = re.match(WikiConfig.DIR_RE, entry)
            else:
                match = re.match(WikiConfig.PAGE_RE, entry)
            
            if match is not None:
                section = (match.group(1) if match.group(1) is not None else "")
                self.link = section + match.group(3)
                self.title = self.link.replace("-", " ")
                
                if self.link == parent.link:
                    raise Exception("TOC wiki item")
            else:
                raise Exception("Unrecognized wiki item")

        self.children = []

    def get_path(self):
        return self._path
    
    def get_level(self):
        return self._level

    def get_parent(self):
        return self._parent

    def is_dir(self):
        return self._is_dir

    def is_root(self):
        return self._parent is None

    def toc_exists(self):
        if not self._is_dir:
            return False

        return os.path.exists(self._get_toc_path())

    def generate_toc(self):
        if not self._is_dir:
            return

        if self.is_root():
            toc = self._generate_home_toc()
            path = WikiConfig.DEFAULT_PAGE + ".md"
        else:
            toc = self._generate_section_toc()
            path = self._get_toc_path()

        f = open(path, "w")
        self._write_toc_to_file(toc, f)
        f.close()

    def generate_footer(self):
        if not self._is_dir:
            return
        
        footer = self._generate_footer(self)
        f = open(self._get_footer_path(), "w")
        f.write(footer)
        f.close()

    def generate_sidebar(self):
        if not self._is_dir:
            return

        item_list = []
        item_list.append("* [" + WikiConfig.DEFAULT_PAGE + "](" +
                         WikiConfig.DEFAULT_PAGE + ")")
        
        if self.is_root():
            self._generate_tree(item_list, 0, 0)
        else:
            item_list.append("* [" + self.title + "](" + self.link + ")")
            self._generate_tree(item_list, 1)
        
        f = open(self._get_sidebar_path(), "w")
        self._write_toc_to_file(item_list, f)
        f.close()

    def get_toc_name(self):
        if not self._is_dir:
            return ""

        if self.is_root():
            return WikiConfig.DEFAULT_PAGE + ".md"
        else:
            return self.entry + ".md"

    def _get_toc_path(self):
        return os.path.join(self._path, self.get_toc_name())

    def _get_footer_path(self):
        if self.is_root():
            return WikiConfig.FOOTER_PREFIX + "_Main.md"
        else:
            return os.path.join(self._path, WikiConfig.FOOTER_PREFIX + "_" +
                                self.entry + ".md")
    
    def _get_sidebar_path(self):
        if self.is_root():
            return WikiConfig.SIDEBAR_PREFIX + "_Main.md"
        else:
            return os.path.join(self._path, WikiConfig.SIDEBAR_PREFIX + "_" +
                                self.entry + ".md")

    def _generate_home_toc(self):
        toc = []
        for item in self.children:
            toc.append("* [" + item.title + "](" + item.link + ")")
        return toc

    def _generate_section_toc(self):
        toc = []
        self._generate_tree(toc, 0)
        return toc
    
    def _generate_footer(self, item):
        if item.get_parent() is None:
            return "[" + item.title + "](" + item.link + ")"
        else:
            return self._generate_footer(item.get_parent()) + " -> [" + \
                   item.title + "](" + item.link + ")"

    def _generate_tree(self, item_list, level, max_level=sys.maxint):
        for item in self.children:
            item_list.append((" " * (level * 4)) + "* [" +
                             item.title + "](" + item.link + ")")
            if item.is_dir() and level < max_level:
                item._generate_tree(item_list, level + 1)
    
    def _write_toc_to_file(self, toc, output_file):
        for item in toc:
            output_file.write(item + "\n");

def ignore(entry, ignore_list):
    for exp in ignore_list:
        if re.match(exp, entry) is not None:
            return True
    return False

def process_dir(parent_wiki_item, ignore_list, verbose):
    for entry in sorted(os.listdir(parent_wiki_item.get_path())):
        if ignore(entry, ignore_list):
            if verbose:
                print "NOTE: ignoring \"" + entry + "\""
            continue
        
        try:
            child_wiki_item = WikiItem(entry, parent_wiki_item)
        except Exception as ex:
            if verbose:
                print "NOTE: skipping \"" + entry + "\":", str(ex)
            continue

        if child_wiki_item.is_dir():
            process_dir(child_wiki_item, ignore_list, verbose)
            parent_wiki_item.children.append(child_wiki_item)
        else:
            parent_wiki_item.children.append(child_wiki_item)

def generate_navigation_items(wiki_tree, ignore_list, verbose, toc):
    if not wiki_tree.is_dir():
        return 
    
    # Generate sidebars only for the first two levels of directories
    if wiki_tree.get_level() < 2:
        if verbose:
            print "Generating sidebar in: " + wiki_tree.get_path()
        wiki_tree.generate_sidebar()
    # Don't generate footer for root level
    if not wiki_tree.is_root():
        if verbose:
            print "Generating footer in: " + wiki_tree.get_path()
        wiki_tree.generate_footer()
    # If TOC already exists, don't overwrite it, as the user may be
    # maintaining it (unless the user forces it with "--toc")
    if not wiki_tree.toc_exists() or (toc and not ignore(wiki_tree.get_toc_name(), ignore_list)):
        if verbose:
            print "Generating TOC in: " + wiki_tree.get_path()
        wiki_tree.generate_toc()
    elif verbose:
        print "NOTE: TOC not generated for \"" + wiki_tree.get_path() + "\":", \
              "file already exists"
    
    for item in wiki_tree.children:
        if item.is_dir():
            generate_navigation_items(item, ignore_list, verbose, toc)

def get_ignore_list_from_file(file_name):
    try:
        f = open(file_name, "r")
        ignore_list = []
        for line in f:
            line = line.replace("\n", "")
            if line != "":
                ignore_list.append(line)
                #print line
        f.close()
        return ignore_list
    except Exception as ex:
        print "Unable to obtain ignore list from file:", str(ex)
        sys.exit(1)

def usage():
    help_text = \
"""
Usage: wikinav.py [options]
Automatically generate wiki navigation items (sidebars, footers, and TOCs)
based on pages and directory structure.

Options:
  -h, --help                Print this help text.
  -i, --ignore=<file>       Provide a list of items (files and directories) to
                            ignore during processing.  The ignore list consists 
                            of Python regular expressions (one per line).
  -t, --toc                 Force generation of TOC files even if they already
                            exist.
  -v, --verbose             Enable verbose output.
"""
    print help_text

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:tv",
                                   ["help", "ignore=", "toc", "verbose"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(1)
    
    ignore_list = WikiConfig.DEFAULT_IGNORE_LIST
    verbose = False
    toc = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        if o in ("-i", "--ignore"):
            ignore_list = get_ignore_list_from_file(a)
        if o in ("-t", "--toc"):
            toc = True
        if o in ("-v", "--verbose"):
            verbose = True

    wiki_tree = WikiItem(".", None)
    process_dir(wiki_tree, ignore_list, verbose)
    generate_navigation_items(wiki_tree, ignore_list, verbose, toc)

    print "Done!"
