# .z80 snapshot file loader
from utility import Bits


def _decompress_z80(data, expected_size=None, v1=False):
    result = bytearray()
    i = 0
    while i < len(data):
        if v1 and i + 3 < len(data) and data[i] == 0x00 and data[i+1] == 0xED and data[i+2] == 0xED and data[i+3] == 0x00:
            break
        if i + 3 < len(data) and data[i] == 0xED and data[i+1] == 0xED:
            count = data[i+2]
            value = data[i+3]
            result.extend([value] * count)
            i += 4
        else:
            result.append(data[i])
            i += 1
        if expected_size and len(result) >= expected_size:
            break
    return result


def load_z80(filename, cpu):
    with open(filename, 'rb') as f:
        raw = f.read()

    # Parse v1 header (30 bytes)
    a = raw[0]
    f = raw[1]
    c, b = raw[2], raw[3]
    l, h = raw[4], raw[5]
    pc = raw[6] | (raw[7] << 8)
    sp = raw[8] | (raw[9] << 8)
    i_reg = raw[10]
    r_reg = raw[11]
    flags1 = raw[12]
    if flags1 == 255:
        flags1 = 1
    e, d = raw[13], raw[14]
    c2, b2 = raw[15], raw[16]
    e2, d2 = raw[17], raw[18]
    l2, h2 = raw[19], raw[20]
    a2 = raw[21]
    f2 = raw[22]
    iy = raw[23] | (raw[24] << 8)
    ix = raw[25] | (raw[26] << 8)
    iff1 = 1 if raw[27] else 0
    iff2 = 1 if raw[28] else 0
    flags2 = raw[29]

    # Fix R register
    r_reg = (r_reg & 0x7F) | ((flags1 & 0x01) << 7)

    # Border color
    border = (flags1 >> 1) & 0x07

    # Interrupt mode
    im = flags2 & 0x03

    if pc != 0:
        # Version 1
        compressed = (flags1 & 0x20) != 0
        mem_data = raw[30:]
        if compressed:
            mem_data = _decompress_z80(bytes(mem_data), 49152, v1=True)
        # Load into 0x4000-0xFFFF
        for j in range(min(len(mem_data), 49152)):
            cpu.ram[0x4000 + j] = mem_data[j]
        print("[+] Z80 v1: loaded {} bytes into 0x4000-0xFFFF".format(min(len(mem_data), 49152)))
    else:
        # Version 2 or 3
        extra_len = raw[30] | (raw[31] << 8)
        pc = raw[32] | (raw[33] << 8)
        hw_mode = raw[34]

        offset = 32 + extra_len

        # Page to address mapping for 48K
        page_map = {
            4: 0x8000,
            5: 0xC000,
            8: 0x4000,
        }

        page_count = 0
        while offset < len(raw):
            if offset + 3 > len(raw):
                break
            block_len = raw[offset] | (raw[offset+1] << 8)
            page_num = raw[offset+2]
            offset += 3

            if block_len == 0xFFFF:
                page_data = raw[offset:offset+16384]
                offset += 16384
            else:
                page_data = _decompress_z80(bytes(raw[offset:offset+block_len]), 16384)
                offset += block_len

            if page_num in page_map:
                base = page_map[page_num]
                for j in range(min(len(page_data), 16384)):
                    cpu.ram[base + j] = page_data[j]
                page_count += 1

        version = "v2" if extra_len == 23 else "v3"
        print("[+] Z80 {}: loaded {} pages, hw={}".format(version, page_count, hw_mode))

    # Set CPU registers
    cpu.A = a
    cpu.F = f
    cpu.B = b
    cpu.C = c
    cpu.D = d
    cpu.E = e
    cpu.H = h
    cpu.L = l
    cpu.AF = (a << 8) | f
    cpu.AFPrim = (a2 << 8) | f2
    cpu.BCPrim = (b2 << 8) | c2
    cpu.DEPrim = (d2 << 8) | e2
    cpu.HLPrim = (h2 << 8) | l2
    cpu.IX = ix
    cpu.IY = iy
    cpu.SP = sp
    cpu.I = i_reg
    cpu.R = r_reg
    cpu.iff1 = iff1
    cpu.iff2 = iff2
    cpu.im = im
    cpu.pc = pc

    print("[+] Z80: PC=0x{:04X} SP=0x{:04X} IM={} border={}".format(pc, sp, im, border))
    return border
