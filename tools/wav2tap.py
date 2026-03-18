#!/usr/bin/env python3
"""
wav2tap - Convert ZX Spectrum cassette audio recordings to .tap files

Usage: python3 wav2tap.py input.wav [output.tap]

ZX Spectrum tape signal format:
- Pilot tone: 8063 pulses of ~855 T-states for headers, 3223 for data
- Sync pulses: 667 T-states + 735 T-states
- Data bits: 0 = two 855 T-state pulses, 1 = two 1710 T-state pulses
- Each byte: 8 data bits (MSB first) + 1 parity bit
- Block structure: flag byte + data bytes + checksum byte
"""

import struct
import sys
import wave


# ZX Spectrum timing constants (in samples at given sample rate)
# T-state durations at 3.5MHz
PILOT_PULSE_TSTATES = 2168
SYNC1_TSTATES = 667
SYNC2_TSTATES = 735
ZERO_PULSE_TSTATES = 855
ONE_PULSE_TSTATES = 1710
CPU_FREQ = 3500000


def tstates_to_samples(tstates, sample_rate):
    return tstates * sample_rate / CPU_FREQ


def read_wav(filename):
    with wave.open(filename, 'rb') as w:
        nchannels = w.getnchannels()
        sampwidth = w.getsampwidth()
        sample_rate = w.getframerate()
        nframes = w.getnframes()
        raw = w.readframes(nframes)

    # Convert to mono float samples
    if sampwidth == 1:
        fmt = '{}B'.format(nframes * nchannels)
        samples = struct.unpack(fmt, raw)
        samples = [(s - 128) / 128.0 for s in samples]
    elif sampwidth == 2:
        fmt = '<{}h'.format(nframes * nchannels)
        samples = struct.unpack(fmt, raw)
        samples = [s / 32768.0 for s in samples]
    else:
        print("[!] Unsupported sample width: {} bytes".format(sampwidth))
        sys.exit(1)

    # Mix to mono if stereo
    if nchannels == 2:
        samples = [(samples[i] + samples[i+1]) / 2.0
                   for i in range(0, len(samples), 2)]

    print("[+] WAV: {}Hz, {}-bit, {} channels, {:.1f}s".format(
        sample_rate, sampwidth * 8, nchannels, len(samples) / sample_rate))
    return samples, sample_rate


def find_pulses(samples, sample_rate):
    """Find zero-crossing intervals (pulse lengths) in the audio signal."""
    pulses = []
    prev_positive = samples[0] >= 0
    last_crossing = 0

    for i in range(1, len(samples)):
        is_positive = samples[i] >= 0
        if is_positive != prev_positive:
            pulse_len = i - last_crossing
            pulses.append(pulse_len)
            last_crossing = i
            prev_positive = is_positive

    return pulses


def classify_pulse(pulse_len, sample_rate):
    """Classify a pulse as pilot, sync, zero bit, or one bit."""
    # Convert pulse length to T-states
    tstates = pulse_len * CPU_FREQ / sample_rate

    if 1500 < tstates < 3000:
        return 'pilot'
    elif 400 < tstates < 1000:
        if tstates < 800:
            return 'sync'
        else:
            return 'zero'
    elif 1000 < tstates < 2500:
        return 'one'
    else:
        return 'unknown'


def decode_blocks(pulses, sample_rate):
    """Decode pulse stream into data blocks."""
    blocks = []
    i = 0
    total = len(pulses)

    while i < total:
        # Look for pilot tone (sequence of pilot pulses)
        pilot_count = 0
        while i < total and classify_pulse(pulses[i], sample_rate) == 'pilot':
            pilot_count += 1
            i += 1

        if pilot_count < 100:
            i += 1
            continue

        # Look for sync pulses
        if i + 1 >= total:
            break
        p1 = classify_pulse(pulses[i], sample_rate)
        p2 = classify_pulse(pulses[i+1], sample_rate)
        if p1 == 'sync' and (p2 == 'sync' or p2 == 'zero' or p2 == 'one'):
            i += 2  # skip both sync pulses
        elif p1 == 'sync':
            i += 1
        else:
            continue

        print("[+] Found pilot ({} pulses) at pulse #{}".format(pilot_count, i))

        # Decode data bits
        data_bytes = []
        current_byte = 0
        bit_count = 0
        parity = 0

        while i + 1 < total:
            p1 = classify_pulse(pulses[i], sample_rate)
            p2 = classify_pulse(pulses[i+1], sample_rate)

            if p1 == 'zero' and p2 == 'zero':
                bit_val = 0
            elif p1 == 'one' and p2 == 'one':
                bit_val = 1
            else:
                break

            i += 2
            current_byte = (current_byte << 1) | bit_val
            bit_count += 1

            if bit_count == 8:
                data_bytes.append(current_byte)
                parity ^= current_byte
                current_byte = 0
                bit_count = 0

        if len(data_bytes) >= 2:
            # Last byte is checksum (parity)
            flag = data_bytes[0]
            checksum = data_bytes[-1]
            data = data_bytes[1:-1]
            # Verify: parity of all bytes including flag should equal checksum
            calc_parity = 0
            for b in data_bytes[:-1]:
                calc_parity ^= b
            parity_ok = calc_parity == checksum
            print("[+] Block: flag=0x{:02X}, {} data bytes, checksum {} ({})".format(
                flag, len(data), "OK" if parity_ok else "FAIL",
                "header" if flag == 0 else "data"))
            blocks.append((flag, bytes(data), checksum))
        else:
            print("[!] Block too short ({} bytes), skipping".format(len(data_bytes)))

    return blocks


def write_tap(filename, blocks):
    """Write blocks to .tap file format."""
    with open(filename, 'wb') as f:
        for flag, data, checksum in blocks:
            # Block length = flag(1) + data(n) + checksum(1)
            block_len = 1 + len(data) + 1
            f.write(struct.pack('<H', block_len))
            f.write(bytes([flag]))
            f.write(data)
            f.write(bytes([checksum]))

    print("[+] Saved {} blocks to {}".format(len(blocks), filename))


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 wav2tap.py input.wav [output.tap]")
        print("\nConverts ZX Spectrum cassette audio recordings to .tap files.")
        print("Record your cassette as a WAV file (44.1kHz, mono or stereo, 16-bit)")
        print("then run this tool to extract the data blocks.")
        sys.exit(1)

    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = input_file.rsplit('.', 1)[0] + '.tap'

    print("[*] Reading {}...".format(input_file))
    samples, sample_rate = read_wav(input_file)

    print("[*] Finding pulses...")
    pulses = find_pulses(samples, sample_rate)
    print("[+] Found {} pulses".format(len(pulses)))

    print("[*] Decoding blocks...")
    blocks = decode_blocks(pulses, sample_rate)

    if blocks:
        write_tap(output_file, blocks)
    else:
        print("[!] No valid blocks found. Try adjusting recording volume or quality.")


if __name__ == '__main__':
    main()
