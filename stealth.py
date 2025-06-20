import argparse
import logging
import os
import socket
import time
from pathlib import Path

UDP_PORT = 40000
TCP_PORT = 40001
KNOCK_TIMEOUT = 4

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def run_stealth_server(udp_port, tcp_port, knock_timeout, knock_secret, dirpath):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.bind(('', udp_port))
        logging.info(f'Listening for knock on port {udp_port}')

        while True:
            data, addr = udp_sock.recvfrom(1024)
            if data != knock_secret:
                continue
            allowed_ip = addr[0]
            logging.info(f'Knock received from {allowed_ip}')

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
                tcp_sock.settimeout(knock_timeout)
                tcp_sock.bind(('', tcp_port))
                tcp_sock.listen(1)
                logging.info(f'Listening for file from {allowed_ip} on port {tcp_port}')

                try:
                    conn, addr = tcp_sock.accept()
                    if addr[0] == allowed_ip:
                        logging.info(f'Connection from {addr[0]} accepted')
                        path = dirpath / f'{addr[0]}_{int(time.time())}.bin'
                        with open(path, 'wb') as f:
                            while True:
                                data = conn.recv(4096)
                                if not data:
                                    break
                                f.write(data)
                        logging.info('File received and saved')
                    else:
                        logging.warning(f'Connection from {addr[0]} rejected')
                    conn.close()
                except socket.timeout:
                    logging.warning('No connection received within timeout window')


def stealth_send(ip, udp_port, tcp_port, knock_secret, filepath):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.sendto(knock_secret, (ip, udp_port))
    udp_sock.close()
    time.sleep(1)

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((ip, tcp_port))
    with open(filepath, 'rb') as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            tcp_sock.sendall(data)
    tcp_sock.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Stealth file transfer server/client.')
    parser.add_argument(
        '-s',
        '--server',
        action='store_true',
        help='Run in server mode',
    )
    parser.add_argument(
        '--udp-port',
        type=int,
        default=UDP_PORT,
        help='UDP port to listen/knock',
    )
    parser.add_argument(
        '--tcp-port',
        type=int,
        default=TCP_PORT,
        help='TCP port to receive/send file',
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=KNOCK_TIMEOUT,
        help='Timeout for TCP connection',
    )
    parser.add_argument(
        '--knock-secret',
        type=str,
        default=os.environ.get('KNOCK_SECRET'),
        help='Knock secret (string)',
    )
    parser.add_argument(
        '--dir',
        type=Path,
        default='.',
        help='Path to directory for receiving files (server mode only)',
    )
    parser.add_argument(
        'ip',
        nargs='?',
        type=str,
        help='Server IP address (client mode only)',
    )
    parser.add_argument(
        'filepath',
        nargs='?',
        type=str,
        help='Path to file to send (client mode only)',
    )

    args = parser.parse_args()

    if not (args.server or (args.ip and args.filepath)):
        parser.error('IP address and file path are required in client mode.')

    if args.knock_secret is None:
        parser.error(
            'KNOCK_SECRET environment variable must be set or provided via --knock-secret'
        )
    args.knock_secret = args.knock_secret.encode()

    return args


if __name__ == '__main__':
    args = parse_args()
    if args.server:
        if not args.dir.exists():
            args.dir.mkdir(parents=True)
        run_stealth_server(
            udp_port=args.udp_port,
            tcp_port=args.tcp_port,
            knock_timeout=args.timeout,
            knock_secret=args.knock_secret,
            dirpath=args.dir,
        )
    else:
        stealth_send(
            ip=args.ip,
            udp_port=args.udp_port,
            tcp_port=args.tcp_port,
            knock_secret=args.knock_secret,
            filepath=args.filepath,
        )
