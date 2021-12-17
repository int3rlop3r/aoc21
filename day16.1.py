import sys
import binascii
from itertools import count
from io import StringIO, BytesIO

LITERAL = 4
LEN_TOTAL = 0
LEN_NO_PKT = 1

def get_bytestream(fd):
    b = fd.read(2)
    while b.strip() != '':
        # return the byte and hex so that it's easy to debug!
        # yield binascii.unhexlify(b)[0], b
        # yield bin(int(b, 16))[2:], b
        yield format(int(b, 16), '08b'), b #[2:], b
        b = fd.read(2)

def get_word(fd):
    b = fd.read(1)
    while b.strip() != '':
        yield format(int(b, 16), '04b'), b #[2:], b
        b = fd.read(1)

def string_to_chrstream(s):
    sio = StringIO(s)
    for s in sio:
        for c in s:
            yield c, sio.tell()

def read_char(ws):
    for w in ws:
        # print("new word:", w[1])
        for i, c in enumerate(w[0]):
            yield c, w[0][i:]

def read_num_bits(n, chrstrm):
    bits = ""
    for i in range(n):
        ch, left = next(chrstrm)
        bits += ch
    return bits

def get_version_sum(fd, steps=10): 
    # bin & ascii
    # for b, a in get_byte(fd):
    # fd = StringIO("D2FE28")
    fd = StringIO("38006F45291200")
    # bstream = get_bytestream(fd)
    wstream = get_word(fd)
    chrstrm = read_char(wstream)
    # for b, a in bstream:
    for pkt in parse_packet(chrstrm):
        print("pkt::", pkt)

def parse_packet(chrstrm):
    ver, ptid = get_ver_ptid(chrstrm)
    print("res:", ver, ptid)
    if ptid == LITERAL:
        literal = decode_literal(chrstrm) # wstream) # bstream)
        # print("literal", literal)
        yield {'ver': ver, 'ptid': ptid, 'val': literal}
        print('cont')
    else:
        # print("notliteral!", ptid)
        for do in decode_operator(chrstrm):
            yield {'ver': ver, 'ptid': ptid, 'val': do}
    print('cont1')

def decode_operator(chrstrm):
    oper = next(chrstrm)[0]
    if oper == '0':
        # get total len
        pktlen = int(read_num_bits(15, chrstrm), 2)
        rawpkts = read_num_bits(pktlen, chrstrm) #get_packets_by_len(chrstrm)
        # nchrstrm = string_to_chrstream(rawpkts)
        nchrstrm = read_char(rawpkts)
        pkts = []
        for c, t in nchrstrm:
            print(c, t)
        # for ppacket in parse_packet(nchrstrm):
            # # print(ppacket)
            # # yield ppacket['val']
            # pkts.append(ppacket['val'])
        # return pkts

    # get no of packets
    l = read_num_bits(11, chrstrm)
    return get_packets_by_cnt(chrstrm)

def get_packets_by_len(chrstrm):
    print("carry", carry)
    for i in chrstrm:
        print(i[0], end='')
    print()

def get_packets_by_cnt(carry, chrstrm):
    pass

def get_no_packets(hdr, chrstrm):
    return _get_len(hdr, chrstrm, 11)

def get_total_len(chrstrm):
    return _get_len(chrstrm, 15)

def _get_len(hdr, chrstrm, bits):
    prevbits = hdr[-1]
    c = count(1)
    left = ""
    # lenchr = ""
    while next(c) < bits:
        ch, left = next(chrstrm)
        prevbits += ch
    return int(prevbits, 2), left

def decode_literal(chrstrm):
    """hrd & literal parts, we need
    both of them to decode the literal"""
    islast = False
    counter = count(1) # first bit was read (lb)
    digits = ""
    while not islast:
        digs = read_num_bits(5, chrstrm)
        islast = digs[0] == '0'
        digits += digs[1:]
    return int(''.join(digits), 2)

def get_ver_ptid(chrstrm):
    """Version and packet ID"""
    verbin = read_num_bits(3, chrstrm)
    ptidbin = read_num_bits(3, chrstrm)
    return int(verbin, 2), int(ptidbin, 2)

def main(fd):
    print(get_version_sum(fd))

if __name__ == '__main__':
    try:
        fpath = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fpath) as f:
            main(f)
