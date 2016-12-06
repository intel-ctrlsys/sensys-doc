#!/bin/bash
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
find . -name '*.md' | grep -v _Sidebar | grep -v _Footer | egrep '^./[1234]-' |  while read -r i; do
    name=`basename $i | sed 's/\.md//' | sed 's/-/ /g'`
    echo -e "$name\n======" | cat - $i > pdfs/`basename $i`
    rm -f pdfs/`basename $i`.pdf
    echo "generating PDF for $i..."
    pandoc --from markdown_github -t latex --listings --standalone --latex-engine=xelatex --template=template.tex -o pdfs/`basename $i`.pdf pdfs/`basename $i`
done
echo -e "Version $1 User Guide\n======\n* [1 Sensys](1-Sensys)\n* [2 Build and Installation Guide](2-Build-and-Installation-Guide)\n* [3 Sensys User Guide](3-Sensys-User-Guide)\n* [4 Developer Guide](4-Developer-Guide)"  > pdfs/title.md
echo -e "Version $1 Release Notes\n======" | cat - ReleaseNotes/V$1-release-notes.md > pdfs/v$1-release-notes.md
pandoc --from markdown_github -t latex --listings --standalone --latex-engine=xelatex --template=template.tex -o pdfs/00-v$1-release-notes.pdf pdfs/v$1-release-notes.md
pandoc --from markdown_github -t latex --listings --standalone --latex-engine=xelatex --template=template.tex -o pdfs/02-title.pdf pdfs/title.md
echo -e "Version $1 Legal Notice\n======" | cat - ReleaseNotes/Legal-Disclaimers.md > pdfs/Legal-Disclaimers.md
pandoc --from markdown_github -t latex --listings --standalone --latex-engine=xelatex --template=template.tex -o pdfs/01-Legal-Disclaimers.pdf pdfs/Legal-Disclaimers.md

cd pdfs
IFS=$oIFS
topics_file=../v$1_topics.txt
if [ ! -e $topics_file ]; then
    rewrite_topics_file=1
fi
if [ $rewrite_topics_file != "false" ]; then
    ../create_topics_txt.sh $1 ../ ../
    echo -e "00-v$1-release-notes.pdf 01-Legal-Disclaimers.pdf 02-title.pdf $(cat $topics_file)" > $topics_file
fi
pdftk `cat $topics_file ` cat output out.pdf
#pdfjoin --paper letter --outfile out.pdf `cat ../v0.29.0_topics.txt`
cd ..
cp -f pdfs/out.pdf sensys-release-$1.pdf
