# pandoc comes from https://github.com/jgm/pandoc/releases
# and pdfjoin is part of TeX
if [[ $# -ne 1 ]]
then
    echo "Usage: $0 <version>"
    echo " where version is the format #.#.#"
    exit 1
fi
oIFS=$IFS
IFS=$'\n'
mkdir pdfs
find . -name '*.md' | grep -v _Sidebar | grep -v _Footer | egrep '^./[1234]-' | grep -v Developer | while read -r i; do 
    name=`basename $i | sed 's/\.md//' | sed 's/-/ /g'`
    echo -e "$name\n======" | cat - $i > pdfs/`basename $i`
    rm -f pdfs/`basename $i`.pdf
    echo "generating PDF for $i..."
    pandoc --from markdown_github -t latex --listings --standalone --latex-engine=xelatex --template=template.tex -o pdfs/`basename $i`.pdf pdfs/`basename $i`
done
echo -e "Version $1 User Guide\n======\n* [1 ORCM](1-ORCM)\n* [2 Build and Installation Guide](2-Build-and-Installation-Guide)\n* [3 ORCM User Guide](3-ORCM-User-Guide)" > pdfs/title.md
echo -e "Version $1 Release Notes\n======" | cat - ReleaseNotes/V$1-release-notes.md > pdfs/v$1-release-notes.md
pandoc --from markdown_github -t latex --listings --standalone --latex-engine=xelatex --template=template.tex -o pdfs/00v$1-release-notes.pdf pdfs/v$1-release-notes.md
pandoc --from markdown_github -t latex --listings --standalone --latex-engine=xelatex --template=template.tex -o pdfs/01-title.md.pdf pdfs/title.md
echo -e "Version $1 Legal Notice\n======" | cat - ReleaseNotes/Legal-Notice.md > pdfs/Legal-Notice.md
pandoc --from markdown_github -t latex --listings --standalone --latex-engine=xelatex --template=template.tex -o pdfs/Legal-Notice.pdf pdfs/Legal-Notice.md
cd pdfs
IFS=$oIFS
pdfjoin --paper letter --outfile out.pdf `cat ../v0.25_topics.txt`
cd ..
cp -f pdfs/out.pdf orcm-release-$1.pdf
#rm -rf pdfs
