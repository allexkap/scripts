#!/bin/bash
set -e

server_type=WireGuard
server_pos=nl3

while getopts ":t:p:" opt; do
  case ${opt} in
    t )
      server_type="$OPTARG" ;;
    p )
      server_pos="$OPTARG" ;;
  esac
done

link_cmd=xdg-open
if ! command -v $link_cmd &> /dev/null; then
  link_cmd=echo
fi

eval "$link_cmd 'https://www.vpnjantit.com/create-free-account?server=$server_pos&type=$server_type' 2> /dev/null"

echo "Save profile to ~/Downloads/ as 'wg[0-9]*.conf'"
echo "Press any key to continue..."
read -sn1

find_cmd="find ~/Downloads/ -regex '.*/wg[0-9]*.conf' -type f"
if [ $(eval "$find_cmd" | wc -l) -ne 1 ]; then
    echo "Multiple matches (or none) :("
    exit 1
fi

eval "$find_cmd -exec sudo mv {} /etc/wireguard/last.conf \;"
