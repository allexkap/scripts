#!/bin/bash
set -e

path=$(find ~ -path ~/.vscode*black/strings.py)

orig="if new_escape_count == orig_escape_count and orig_quote == '\"':"
repl="if new_escape_count == orig_escape_count and orig_quote != '\"':"

if [ -z "$path" ]; then
    echo -e "\e[31mFile not found\e[0m"
    exit 1
fi

if [ $(grep -c "$orig" "$path") -ne 1 ]; then
    echo -e "\e[31mPattern not found\e[0m"
    exit 1
fi

sed -i "s/$orig/$repl/" "$path"
echo -e "\e[32mSuccess\e[0m"
