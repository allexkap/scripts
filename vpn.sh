#!/bin/bash
set -e

server_pos=nl3
cmd=xdg-open
file_path=~/Downloads/wg.conf

while getopts ":s:c:f:" opt; do
  case ${opt} in
    s )
      server_pos="$OPTARG" ;;
    c )
      cmd="$OPTARG" ;;
    f )
      file_path="$OPTARG" ;;
  esac
done

if ! command -v $cmd &> /dev/null; then
  cmd=echo
fi

eval "$cmd 'https://www.vpnjantit.com/create-free-account?server=$server_pos&type=WireGuard' 2> /dev/null"

echo "Save profile to $file_path"
echo "Press any key to continue..."
read -sn1

if [ ! -f "$file_path" ]; then
    echo -e "\e[31;1mError:\e[0m File not found :("
    exit 1
fi

sudo mv "$file_path" /etc/wireguard/last.conf

echo -e "\e[32;1mSuccess\e[0m"
