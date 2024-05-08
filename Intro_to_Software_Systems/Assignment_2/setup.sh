#!/bin/bash
# Author: Éloi Dallaire
# McGill Student ID: 260794674

# Ex. 2: Backup
if [ "$1" = "backup" ]; then
        # 1
        echo "$(pwd)"
        ls *.txt

        # 2
        mkdir backup
        cd backup
        echo "Moved to backup directory"
        echo "$(pwd)"

        # 3
        cp ../*.txt .
        echo "Copied all text files to backup directory"

        # 4
        echo "Current backup:" > date.txt
        date >> date.txt
        cat date.txt


# Ex. 3: Archive
elif [ "$1" = "archive" ]; then
        # 1
        if [ $# -ne 2 ]; then
        	echo "Error: Archive task requires file format"
        	echo "Usage: ./setup.sh archive <fileformat>"
        	exit 5
    	fi
        # 2
        archive_name="archive-$(date +'%Y-%m-%d').tgz"
        tar -czvf "$archive_name" *."$2"
        echo "Created archive $archive_name"
        ls -l "$archive_name"


# Ex. 4: Sortedcopy
elif [ "$1" = "sortedcopy" ]; then
   # 1: Arguments validation
	# 2 additional 
	if [ $# -ne 3 ]; then
        	echo "Error: Expected two additional input parameters."
        	echo "Usage: ./setup.sh sortedcopy <sourcedirectory> <targetdirectory>"
        	exit 1
	fi
	# Source directory
	sourcedir="$2"
	targetdir="$3"
	if [ ! -d "$sourcedir" ]; then
        	echo "Error: Input parameter #2 '$sourcedir' is not a directory."
        	echo "Usage: ./setup.sh sortedcopy <sourcedirectory> <targetdirectory>"
        	exit 2
    	fi
    	# Target directory
	if [ -d "$targetdir" ]; then
        	read -p "Directory '$targetdir' already exists. Overwrite? (y/n) " response
	        if [ "$response" != "y" ]; then
            		exit 3
        	else
            		rm -rf "$targetdir"
        	fi
	fi
    
    # 2: Create sorted copy
	mkdir "$targetdir"
	# List in reverse order
	cd "$sourcedir"
	files=( $(ls -r) )
	count=${#files[@]}
	index=1
	for (( i=0; i<$count; i++ )); do
	# Validate item is not directory
        	if [ -f "${files[i]}" ]; then
            		cp "${files[i]}" "../$targetdir/$index.${files[i]}"
			((index++))
        	fi
    	done

	# Terminate program    
    	exit 0


# Ex. 1: Invalid 1st argument
else
        echo "Error: Invalid task specified. Supported tasks: backup, archive, sortedcopy."
        echo "Usage: ./setup.sh <task> <additional_arguments>"
        exit 4
fi




