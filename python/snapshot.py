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
        port_7ffd = raw[35]

        # Detect 128K hardware.
        # v2 (extra_len=23):  hw_mode 3 or 4 => 128K
        # v3 (extra_len=54+): hw_mode 4, 5, 6 => 128K (plain, +If1, +MGT)
        is_128k = ((extra_len == 23 and hw_mode in (3, 4)) or
                   (extra_len >= 54 and hw_mode in (4, 5, 6)))

        # Snapshot expects page selection to be applied BEFORE RAM is
        # written via cpu.ram[addr] for addresses in the paged window.
        # For 128K we write pages directly via banked RAM, so this mainly
        # matters for 48K-style fallback; but apply it early for safety.
        banked = is_128k and hasattr(cpu.ram, 'pages')
        if banked:
            cpu.ram.rom_select = (port_7ffd >> 4) & 1
            cpu.ram.page_select = port_7ffd & 0x07
            cpu.ram.screen_select = (port_7ffd >> 3) & 1
            cpu.ram.paging_locked = bool(port_7ffd & 0x20)

        offset = 32 + extra_len

        # 48K-mode page-number -> CPU address base
        page_map_48k = {
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

            if banked and 3 <= page_num <= 10:
                bank = page_num - 3
                cpu.ram.pages[bank][:len(page_data)] = page_data[:16384]
                page_count += 1
            elif page_num in page_map_48k:
                base = page_map_48k[page_num]
                for j in range(min(len(page_data), 16384)):
                    cpu.ram[base + j] = page_data[j]
                page_count += 1

        version = "v2" if extra_len == 23 else "v3"
        mode = "128K" if is_128k else "48K"
        print("[+] Z80 {} {}: loaded {} pages, hw={}".format(version, mode, page_count, hw_mode))

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


def save_z80(filename, cpu, border=7):
    header = bytearray(30)

    header[0] = cpu.A
    header[1] = cpu.F
    header[2] = cpu.C
    header[3] = cpu.B
    header[4] = cpu.L
    header[5] = cpu.H
    header[6] = cpu.pc & 0xFF
    header[7] = cpu.pc >> 8
    header[8] = cpu.SP & 0xFF
    header[9] = cpu.SP >> 8
    header[10] = cpu.I
    header[11] = cpu.R & 0x7F
    # Byte 12: bit 0 = R bit 7, bits 1-3 = border, bit 5 = compressed
    header[12] = ((cpu.R >> 7) & 1) | ((border & 7) << 1)
    header[13] = cpu.E
    header[14] = cpu.D
    header[15] = cpu.BCPrim & 0xFF
    header[16] = cpu.BCPrim >> 8
    header[17] = cpu.DEPrim & 0xFF
    header[18] = cpu.DEPrim >> 8
    header[19] = cpu.HLPrim & 0xFF
    header[20] = cpu.HLPrim >> 8
    header[21] = cpu.AFPrim >> 8
    header[22] = cpu.AFPrim & 0xFF
    header[23] = cpu.IY & 0xFF
    header[24] = cpu.IY >> 8
    header[25] = cpu.IX & 0xFF
    header[26] = cpu.IX >> 8
    header[27] = 1 if cpu.iff1 else 0
    header[28] = 1 if cpu.iff2 else 0
    header[29] = cpu.im & 3

    # Write uncompressed v1 format (49152 bytes of RAM from 0x4000-0xFFFF)
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(bytes(cpu.ram[addr] for addr in range(0x4000, 0x10000)))

    print("[+] State saved: {}".format(filename))
