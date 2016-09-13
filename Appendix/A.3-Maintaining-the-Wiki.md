###A.3.1 How Do I Add a Page to the Wiki?

The Sensys wiki repo has a certain directory structure, and pages and directories follow a certain naming convention.  This is to organize content better and make it easier to generate the wiki's navigation items (sidebars, footers, etc.).  To add a page to the wiki:

1. Clone the orcm.wiki repo (see lower right corner on the wiki's [main page](Home))
2. Decide where in the directory structure the new page belongs
3. Create the page and reorder any items if necessary (by renaming pages and directories)
4. Regenerate the sidebars, footers and TOCs by using the wiki script (see below)

The following sections provide details on the naming conventions and directory structure that should be followed.  There is also a section that explains how to use the wiki script to generate the wiki's navigation items.

###A.3.2 Naming Conventions

* Each page name must be unique regardless of where it is in the directory tree\*
* Page names: "\<section number\>-\<page title using dashes for spaces\>.md"
* Directory names: "\<section number\>-\<section title using dashes for spaces\>"
* Section numbers:
    * Dot notation may be used for indicating content structure (sections and subsections)
    * Letters and numbers are accepted
    * More specifically: `[A-Z0-9]+(\.[A-Z0-9]+)*`
    * Section numbers also provide a way to specify the order in which pages and sections should appear in sidebars and TOCs
* Titles:
    * For titles, please follow standard Title Case rules
    * [Title Capitalization](http://titlecapitalization.com/)
    * Within a page, do not include a header with the title as the page name is automatically displayed as the title when the page is rendered\*
    * In file and directory names, use dashes to separate words (dashes are automatically converted to spaces when a page is rendered\*)
* Sidebars: "\_Sidebar\_\<section number\>-\<section title\>"\*
* Footers: "\_Footer\_\<section number\>-\<section title\>"\*

\* Due to GitHub wiki feature, restriction or standard

###A.3.3 Directory structure

* The directory tree within the wiki repo can be used to organize content according to its structure (sections and subsections)
* In general, there should be a page per section
* To avoid letting the directory tree grow too deep and to avoid having pages with too little content, a good rule of thumb is to have at most three directory levels.  After this, multiple subsections can be included in the same page.
* Each directory should contain a page to serve as its TOC.  The page should have the same name as the directory plus a ".md" extension.
* For the root directory, the "Home.md" page can serve as the TOC.
* Each directory should contain a footer to make navigation easier.  There is no need for the root directory to have a footer.
* A sidebar should be included in at least the first two levels of the directory tree.  The root-level sidebar can include links to the main (top-level) sections, while the section sidebars can include the entire tree for that section.

###A.3.4 Other Rules and Conventions

* Please try to follow proper grammar rules
* For titles, please follow standard Title Case rules: [Title Capitalization](http://titlecapitalization.com/)
* In shell output examples, use "#" for root prompts and "%" for regular user prompts
* Use of literal blocks:
    * Use them for showing examples of command input/output and for code or configuration file excerpts or examples
    * When including a file as an example that's already present in the repo, if possible, try to include a link to it instead of copying its contents to the wiki
    * To avoid any confusion between wiki instructions and literal input/output (e.g. for installation instructions), try to avoid including comments inside literal blocks
    * For one-line command examples it's okay to use embedded literal blocks

###A.3.5 The Wiki Script

To facilitate maintaining sidebars, footers and TOCs, a tool is available in the repo: "wikinav.py".  It automatically generates wiki navigation items based on pages and directory structure.  Usage: `wikinav.py [options]`.  Options:

* -h, --help: Print help text.
* -i, --ignore=\<file\>: Provide a list of items (files and directories) to ignore during processing.  The ignore list consists of Python regular expressions (one per line).
* -t, --toc: Force generation of TOC files even if they already exist.
* -v, --verbose: Enable verbose output.

Important notes:

* The tool will replace all sidebars and footers found in the repo
* However, the tool will not replace TOC files (it will only generate them if not found), as these may contain a section overview being maintained by the user
* The tool will only generate sidebars for the first two levels of directories

Example:
```
python wikinav.py --ignore=ignore.list --toc --verbose
```

The previous command will generate all the wiki navigation items ignoring the files specified in the "ignore.list" file, forcing regeneration of all TOC files, and producing a verbose output.  This is going to be the most common method of invocation.  To avoid overwriting TOC files being maintained manually, simply add them to the ignore list.  The "ignore.list" file is included in the repo.
