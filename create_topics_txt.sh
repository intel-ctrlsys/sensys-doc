#!/bin/bash
if [[ $# -ne 3 ]]
then
    echo "Usage: $0 <version> <md_files_path> <topics_file_path>"
    echo " Where:"
    echo -e "\t <version> is the format #.#.#"
    echo -e "\t <md_files_path> is the path where the md files will be searched."
    echo -e "\t <topics_file_path> is the path to create the v*topics.txt file."
    exit 1
fi

file_name=$3/v$1_topics.txt
echo "File $file_name generated based on $2"

if [ -e $file_name ]; then
    rm $file_name
fi
for i in $(find $2 -name '*.md' | grep -v _Sidebar | grep -v _Footer | \
           grep -v Home | egrep "^$2[0-9]+[-.]" | egrep -v "/[4].[123]|/5-"); do
    echo $(basename $i).pdf >> $file_name
done
if [ -e $file_name ]; then
    echo -e "$(sort -V $file_name  | tr '\n' ' ')" > $file_name
fi
