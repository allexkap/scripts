#!/bin/bash
set -e

orig="if new_escape_count == orig_escape_count and orig_quote == '\"':"
repl="if new_escape_count == orig_escape_count and orig_quote != '\"':"

find ~ -path ~/.vscode*black/strings.py -type f -print0 | while read -d $'\0' path
do
    if [ -z "$path" ]; then
        echo -e "\e[31mFile not found\e[0m"
        continue
    fi

    if [ $(grep -c "$orig" "$path" 2> /dev/null) -ne 1 ]; then
        echo -e "\e[31mString not found\e[0m: $path"
        continue
    fi

    # sed -i "s/$orig/$repl/" "$path"
    echo -e "\e[32mSuccess\e[0m: $path"
done





