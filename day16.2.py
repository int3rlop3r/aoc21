import operator
import sys
from io import StringIO
from functools import partial, reduce

def test_lval():
    fd = StringIO("D2FE28")
    bs = BitStream(fd)
    root = parse(bs)
    assert bs.bits == 21
    bs.flush()
    assert bs.bits == 24
    assert root.lval == 2021

def test_op_len0():
    fd = StringIO("38006F45291200")
    bs = BitStream(fd)
    root = parse(bs)
    assert len(root.pkts) == 2
    assert root.lenval == 27
    vals = (
        (6, 4, 10),
        (2, 4, 20),
    )
    for i, p in enumerate(root.pkts):
        x, y, z = vals[i]
        # print('i', i)
        # print('p', p)
        assert p.ver == x
        assert p.tid == y
        assert p.lval == z

def test_op_len1():
    fd = StringIO("EE00D40C823060")
    bs = BitStream(fd)
    root = parse(bs)
    assert len(root.pkts) == 3
    assert root.lenval == 3
    vals = (1, 2, 3)
    for i, p in enumerate(root.pkts):
        assert p.lval == vals[i]

def read_num_bits(chrstrm, n):
    """Read `n` no. of bits from `chrstrm`"""
    bits = ""
    for i in range(n):
        ch = next(chrstrm)
        bits += ch
    return bits

class BitStream:
    def __init__(self, fd):
        self.fd = fd
        self.currword = ""
        self.bitsleft = ""
        self.stream = self._bit_gen()
        self.bits = 0

    def __iter__(self):
        return self

    def __next__(self):
        self._inc_bit()
        return next(self.stream)

    def _inc_bit(self):
        self.bits += 1

    def _word_gen(self):
        """Read 8 bits at a time"""
        b = self.fd.read(2)
        while b.strip() != '':
            self.currword = b
            yield format(int(b, 16), '08b')
            b = self.fd.read(2)

    def _bit_gen(self):
        """Read a single bit from `word_gen` at a time"""
        for w in self._word_gen():
            for i, c in enumerate(w):
                self.bitsleft = w[i+1:]
                yield c

    def flush(self):
        """Drain the buffer, move on to the next word"""
        return [(next(self.stream), self._inc_bit()) for i in range(len(self.bitsleft))]

class Packet:
    def __init__(self, ver, tid):
        self.ver = int(ver)
        self.tid = int(tid)

class LPacket(Packet):
    def __init__(self, ver, tid, lval, pkt_len):
        super().__init__(ver, tid)
        self.lval = lval
        self.pkt_len = pkt_len

    def __str__(self):
        return (f'<LPacket ver={self.ver}, tid={self.tid}, '
                f'lval={self.lval}, pkt_len={self.pkt_len}>')

    def set_val(self, lval):
        self.lval = lval

class OPacket(Packet):
    def __init__(self, ver, tid, lid, lenval):
        super().__init__(ver, tid)
        self.pkts = []
        self.lid = lid
        self.lenval = lenval

    def __str__(self):
        return (f'<OPacket pver={self.ver}, ptid={self.tid}, '
                f'lenval={self.lenval} lid={self.lid} pkts={len(self.pkts)}>')

    def add(self, pkt):
        self.pkts.append(pkt)

getvtid = lambda x: (int(x[:3], 2), int(x[3:], 2))

def parse_lval(ver, tid, bs):
    is_last = False
    buff = ""
    buff_len = 0
    hdr_len = 6
    while not is_last:
        buff_len += 5
        bits = read_num_bits(bs, 5)
        is_last = bits[0] == '0'
        buff += bits[1:]
    pkt_len = hdr_len+buff_len
    return LPacket(ver, tid, int(buff, 2), pkt_len)

def parse_operator(ver, tid, bs):
    lid = int(read_num_bits(bs, 1))
    lenfunc = [
        lambda x: int(read_num_bits(x, 15), 2), # nob
        lambda x: int(read_num_bits(x, 11), 2), # nop
    ][lid]
    lenval = lenfunc(bs)
    return OPacket(ver, tid, lid, int(lenval))

def parse(bs):
    root = None
    buff = ""
    for bit in bs:
        buff += bit
        if len(buff) == 6:
            ver, tid = getvtid(buff)

            if int(tid) == 4:
                # print("lval")
                lpkt = parse_lval(ver, tid, bs)
                return lpkt
            else:
                # print("not lval", ver, tid, buff)
                opkt = parse_operator(ver, tid, bs)
                # print(opkt)
                if opkt.lid == 0:
                    lenval = opkt.lenval
                    currbits = bs.bits
                    # print('prev:', lenval)
                    # @TODO: try lenval > (bs.bits - currbits)
                    # while lenval - (bs.bits - currbits) > 0:
                    while lenval > (bs.bits - currbits):
                        subp = parse(bs)
                        opkt.add(subp)
                    return opkt
                else:
                    lenval = opkt.lenval
                    pkt_cnt = 0
                    while lenval > pkt_cnt:
                        subp = parse(bs)
                        pkt_cnt += 1
                        opkt.add(subp)
                    return opkt
                return opkt, bits
    return root

opers = [
    sum,
    partial(reduce, operator.mul),
    min,
    max,
    lambda x: x, # place holder
    lambda x: 1 if x[0] > x[1] else 0,
    lambda x: 1 if x[0] < x[1] else 0,
    lambda x: 1 if x[0] == x[1] else 0,
]

def eval_pkt(root):
    if isinstance(root, LPacket):
        return root.lval
    vals = []
    for p in root.pkts:
        vals.append(eval_pkt(p))
    try:
        return opers[root.tid](vals)
    except IndexError:
        print(root.tid)
        raise

def main(fd):
    bs = BitStream(fd)
    root = parse(bs)
    print(eval_pkt(root))

if __name__ == '__main__':
    try:
        fpath = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fpath) as f:
            main(f)
    # test_lval()
    # test_op_len0()
    # test_op_len1()
    # # root = parse(BitStream(StringIO("8A004A801A8002F478")))
    # root = parse(BitStream(StringIO("A0016C880162017C3686B18A3D4780")))
    # # __import__('pdb').set_trace()
    # print(sum_vers(root))
