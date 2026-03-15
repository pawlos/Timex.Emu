# ZX Spectrum .tap file loader


class TapeBlock:
    def __init__(self, flag, data, checksum):
        self.flag = flag
        self.data = data
        self.checksum = checksum

    def verify_checksum(self):
        calc = self.flag
        for b in self.data:
            calc ^= b
        return calc == self.checksum


class TapeFile:
    def __init__(self, filename):
        self.blocks = []
        self.position = 0
        self._parse(filename)

    def _parse(self, filename):
        with open(filename, 'rb') as f:
            raw = f.read()

        offset = 0
        while offset + 2 <= len(raw):
            block_len = raw[offset] | (raw[offset + 1] << 8)
            offset += 2
            if offset + block_len > len(raw) or block_len < 2:
                break
            flag = raw[offset]
            data = bytes(raw[offset + 1:offset + block_len - 1])
            checksum = raw[offset + block_len - 1]
            self.blocks.append(TapeBlock(flag, data, checksum))
            offset += block_len

        print("[+] Tape loaded: {} blocks".format(len(self.blocks)))

    def next_block(self):
        if self.position >= len(self.blocks):
            return None
        block = self.blocks[self.position]
        self.position += 1
        return block

    def rewind(self):
        self.position = 0
