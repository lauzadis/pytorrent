import socket
import urllib.parse
import argparse
import random
import string
import bencode

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 8000))


def main():
    parser = argparse.ArgumentParser(description='download some bytes')
    parser.add_argument("--magnet_uri", type=str, required=True)
    args = parser.parse_args()

    infohash, display_name = parse_magnet_uri(args.magnet_uri)

    # ping()
    get_peers(infohash)

def get_peers(infohash):
    transaction_id = random_string(2)
    id = random_string(20)

    get_peers_request = {
        "t": transaction_id,
        "y": "q",
        "q": "get_peers",
        "a": {
            "id": id,
            "info_hash": infohash
        }
    }

    bencoded_get_peers_request = bencode.encode(get_peers_request)

    bencoded_get_peers_request_bytes = bencoded_get_peers_request.encode("utf-8")
    print(bencoded_get_peers_request)
    sock.sendto(bencoded_get_peers_request_bytes, ("67.215.246.10", 6881))

    bytes, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print(f"received message {bytes}")

    bencoded = bytes.decode("unicode-escape")
    bencoded = bytes.decode("latin-1")
    # bencoded = bytes.decode("latin-1")
    print(f"bencoded: {bencoded}")

    print(f"decoded: {bencode.decode(bencoded)}")



        
def ping():
    transaction_id = random_string(2)
    id = random_string(20)

    ping_request = {
        "t": transaction_id,
        "y": "q",
        "q": "ping",
        "a": {
            "id": id
        }
    }

    bencoded_ping_request = bencode.encode(ping_request)

    bencoded_ping_request_bytes = bencoded_ping_request.encode("utf-8")
    sock.sendto(bencoded_ping_request_bytes, ("67.215.246.10", 6881))

    bytes, addr = sock.recvfrom(1024)
    print(f"received message {bytes}")

    bencoded = bytes.decode("unicode-escape")
    print(f"bencoded: {bencoded}")

def random_string(n: int):
    return "".join(random.choices(string.ascii_lowercase, k=n))

def parse_magnet_uri(magnet_uri: str):
    magnet_uri = urllib.parse.unquote(magnet_uri)

    parsed = urllib.parse.urlparse(magnet_uri)
    query_terms = urllib.parse.parse_qs(parsed.query)

    if ("xt" not in query_terms or len(query_terms["xt"]) != 1 or "dn" not in query_terms or len(query_terms["dn"]) != 1):
        ValueError(f"Failed to parse magnet_uri {magnet_uri}")

    _, hash_algorithm, infohash = query_terms["xt"][0].split(":")
    display_name = query_terms["dn"][0]

    if hash_algorithm != "btih": 
        raise ValueError(f"hash algorithm {hash_algorithm} is not supported (only btih).")

    return infohash, display_name

if __name__ == "__main__":
    main()