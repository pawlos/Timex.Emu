# Z80 opcode dispatch tables
# Auto-generated from cpu.py dispatch table

from opcodes import Opcodes


def build_base_table():
    t = [None] * 256
    t[0x00] = Opcodes.nop
    t[0x01] = Opcodes.ld16
    t[0x02] = Opcodes.ld_bc_a
    t[0x03] = Opcodes.inc16
    t[0x04] = Opcodes.inc8
    t[0x05] = Opcodes.dec8b
    t[0x06] = Opcodes.ld8n
    t[0x07] = Opcodes.rlca
    t[0x08] = Opcodes.ex_af_afprim
    t[0x09] = Opcodes.add16
    t[0x0A] = Opcodes.ld_a_bc
    t[0x0B] = Opcodes.dec16b
    t[0x0C] = Opcodes.inc8
    t[0x0D] = Opcodes.dec8b
    t[0x0E] = Opcodes.ld8n
    t[0x0F] = Opcodes.rrca
    t[0x10] = Opcodes.djnz
    t[0x11] = Opcodes.ld16
    t[0x12] = Opcodes.ld_de_a
    t[0x13] = Opcodes.inc16
    t[0x14] = Opcodes.inc8
    t[0x15] = Opcodes.dec8b
    t[0x16] = Opcodes.ld8n
    t[0x17] = Opcodes.lra
    t[0x18] = Opcodes.jr_e
    t[0x19] = Opcodes.add16
    t[0x1A] = Opcodes.ld_a_de
    t[0x1B] = Opcodes.dec16b
    t[0x1C] = Opcodes.inc8
    t[0x1D] = Opcodes.dec8b
    t[0x1E] = Opcodes.ld8n
    t[0x1F] = Opcodes.rra
    t[0x20] = Opcodes.jpnz
    t[0x21] = Opcodes.ld16
    t[0x22] = Opcodes.ldNnHl
    t[0x23] = Opcodes.inc16
    t[0x24] = Opcodes.inc8
    t[0x25] = Opcodes.dec8b
    t[0x26] = Opcodes.ld8n
    t[0x27] = Opcodes.daa
    t[0x28] = Opcodes.jr_z
    t[0x29] = Opcodes.add16
    t[0x2A] = Opcodes.ldHl_addr
    t[0x2B] = Opcodes.dec16b
    t[0x2C] = Opcodes.inc8
    t[0x2D] = Opcodes.dec8b
    t[0x2E] = Opcodes.ld8n
    t[0x2F] = Opcodes.cpl
    t[0x30] = Opcodes.jpnc
    t[0x31] = Opcodes.ld16
    t[0x32] = Opcodes.ldnn_a
    t[0x33] = Opcodes.inc16
    t[0x34] = Opcodes.inc_at_hl
    t[0x35] = Opcodes.dec_at_hl
    t[0x36] = Opcodes.ld_addr
    t[0x37] = Opcodes.scf
    t[0x38] = Opcodes.jr_c
    t[0x39] = Opcodes.add16
    t[0x3A] = Opcodes.ld_a_nn
    t[0x3B] = Opcodes.dec16b
    t[0x3C] = Opcodes.inc8
    t[0x3D] = Opcodes.dec8b
    t[0x3E] = Opcodes.ld8n
    t[0x3F] = Opcodes.ccf
    t[0x40] = Opcodes.ld8
    t[0x41] = Opcodes.ld8
    t[0x42] = Opcodes.ld8
    t[0x43] = Opcodes.ld8
    t[0x44] = Opcodes.ld8
    t[0x45] = Opcodes.ld8
    t[0x46] = Opcodes.ld_r_hl
    t[0x47] = Opcodes.ld8
    t[0x48] = Opcodes.ld8
    t[0x49] = Opcodes.ld8
    t[0x4A] = Opcodes.ld8
    t[0x4B] = Opcodes.ld8
    t[0x4C] = Opcodes.ld8
    t[0x4D] = Opcodes.ld8
    t[0x4E] = Opcodes.ld_r_hl
    t[0x4F] = Opcodes.ld8
    t[0x50] = Opcodes.ld8
    t[0x51] = Opcodes.ld8
    t[0x52] = Opcodes.ld8
    t[0x53] = Opcodes.ld8
    t[0x54] = Opcodes.ld8
    t[0x55] = Opcodes.ld8
    t[0x56] = Opcodes.ld_r_hl
    t[0x57] = Opcodes.ld8
    t[0x58] = Opcodes.ld8
    t[0x59] = Opcodes.ld8
    t[0x5A] = Opcodes.ld8
    t[0x5B] = Opcodes.ld8
    t[0x5C] = Opcodes.ld8
    t[0x5D] = Opcodes.ld8
    t[0x5E] = Opcodes.ld_r_hl
    t[0x5F] = Opcodes.ld8
    t[0x60] = Opcodes.ld8
    t[0x61] = Opcodes.ld8
    t[0x62] = Opcodes.ld8
    t[0x63] = Opcodes.ld8
    t[0x64] = Opcodes.ld8
    t[0x65] = Opcodes.ld8
    t[0x66] = Opcodes.ld_r_hl
    t[0x67] = Opcodes.ld8
    t[0x68] = Opcodes.ld8
    t[0x69] = Opcodes.ld8
    t[0x6A] = Opcodes.ld8
    t[0x6B] = Opcodes.ld8
    t[0x6C] = Opcodes.ld8
    t[0x6D] = Opcodes.ld8
    t[0x6E] = Opcodes.ld_r_hl
    t[0x6F] = Opcodes.ld8
    t[0x70] = Opcodes.ldhlr
    t[0x71] = Opcodes.ldhlr
    t[0x72] = Opcodes.ldhlr
    t[0x73] = Opcodes.ldhlr
    t[0x74] = Opcodes.ldhlr
    t[0x75] = Opcodes.ldhlr
    t[0x76] = Opcodes.hlt
    t[0x77] = Opcodes.ldhlr
    t[0x78] = Opcodes.ld8
    t[0x79] = Opcodes.ld8
    t[0x7A] = Opcodes.ld8
    t[0x7B] = Opcodes.ld8
    t[0x7C] = Opcodes.ld8
    t[0x7D] = Opcodes.ld8
    t[0x7E] = Opcodes.ld_r_hl
    t[0x7F] = Opcodes.ld8
    t[0x80] = Opcodes.add_r
    t[0x81] = Opcodes.add_r
    t[0x82] = Opcodes.add_r
    t[0x83] = Opcodes.add_r
    t[0x84] = Opcodes.add_r
    t[0x85] = Opcodes.add_r
    t[0x86] = Opcodes.add_a_hl
    t[0x87] = Opcodes.add_r
    t[0x88] = Opcodes.adc_r
    t[0x89] = Opcodes.adc_r
    t[0x8A] = Opcodes.adc_r
    t[0x8B] = Opcodes.adc_r
    t[0x8C] = Opcodes.adc_r
    t[0x8D] = Opcodes.adc_r
    t[0x8E] = Opcodes.adc_a_hl
    t[0x8F] = Opcodes.adc_r
    t[0x90] = Opcodes.sub_r
    t[0x91] = Opcodes.sub_r
    t[0x92] = Opcodes.sub_r
    t[0x93] = Opcodes.sub_r
    t[0x94] = Opcodes.sub_r
    t[0x95] = Opcodes.sub_r
    t[0x96] = Opcodes.sub_a_hl
    t[0x97] = Opcodes.sub_r
    t[0x98] = Opcodes.sbc_r
    t[0x99] = Opcodes.sbc_r
    t[0x9A] = Opcodes.sbc_r
    t[0x9B] = Opcodes.sbc_r
    t[0x9C] = Opcodes.sbc_r
    t[0x9D] = Opcodes.sbc_r
    t[0x9E] = Opcodes.sbc_hl
    t[0x9F] = Opcodes.sbc_r
    t[0xA0] = Opcodes._and
    t[0xA1] = Opcodes._and
    t[0xA2] = Opcodes._and
    t[0xA3] = Opcodes._and
    t[0xA4] = Opcodes._and
    t[0xA5] = Opcodes._and
    t[0xA6] = Opcodes._and_hl
    t[0xA7] = Opcodes._and
    t[0xA8] = Opcodes.xorA
    t[0xA9] = Opcodes.xorA
    t[0xAA] = Opcodes.xorA
    t[0xAB] = Opcodes.xorA
    t[0xAC] = Opcodes.xorA
    t[0xAD] = Opcodes.xorA
    t[0xAE] = Opcodes.xor_hl
    t[0xAF] = Opcodes.xorA
    t[0xB0] = Opcodes._or
    t[0xB1] = Opcodes._or
    t[0xB2] = Opcodes._or
    t[0xB3] = Opcodes._or
    t[0xB4] = Opcodes._or
    t[0xB5] = Opcodes._or
    t[0xB6] = Opcodes._or_hl
    t[0xB7] = Opcodes._or
    t[0xB8] = Opcodes.cp
    t[0xB9] = Opcodes.cp
    t[0xBA] = Opcodes.cp
    t[0xBB] = Opcodes.cp
    t[0xBC] = Opcodes.cp
    t[0xBD] = Opcodes.cp
    t[0xBE] = Opcodes.cp_hl
    t[0xBF] = Opcodes.cp
    t[0xC0] = Opcodes.ret_cc
    t[0xC1] = Opcodes.pop
    t[0xC2] = Opcodes.jp_cond
    t[0xC3] = Opcodes.jp
    t[0xC4] = Opcodes.call_cond
    t[0xC5] = Opcodes.push
    t[0xC6] = Opcodes.add_r_n
    t[0xC7] = Opcodes.rst
    t[0xC8] = Opcodes.ret_cc
    t[0xC9] = Opcodes.ret
    t[0xCA] = Opcodes.jp_cond
    t[0xCC] = Opcodes.call_cond
    t[0xCD] = Opcodes.call
    t[0xCE] = Opcodes.adc_n
    t[0xCF] = Opcodes.rst
    t[0xD0] = Opcodes.ret_cc
    t[0xD1] = Opcodes.pop
    t[0xD2] = Opcodes.jp_cond
    t[0xD3] = Opcodes.out
    t[0xD4] = Opcodes.call_cond
    t[0xD5] = Opcodes.push
    t[0xD6] = Opcodes.sub_n
    t[0xD7] = Opcodes.rst
    t[0xD8] = Opcodes.ret_cc
    t[0xD9] = Opcodes.exx
    t[0xDA] = Opcodes.jp_cond
    t[0xDB] = Opcodes.in_a_n
    t[0xDC] = Opcodes.call_cond
    t[0xDE] = Opcodes.sbc_n
    t[0xDF] = Opcodes.rst
    t[0xE0] = Opcodes.ret_cc
    t[0xE1] = Opcodes.pop
    t[0xE2] = Opcodes.jp_cond
    t[0xE3] = Opcodes.ex_sp_hl
    t[0xE4] = Opcodes.call_cond
    t[0xE5] = Opcodes.push
    t[0xE6] = Opcodes.and_n
    t[0xE7] = Opcodes.rst
    t[0xE8] = Opcodes.ret_cc
    t[0xE9] = Opcodes.jp_hl
    t[0xEA] = Opcodes.jp_cond
    t[0xEB] = Opcodes.ex_de_hl
    t[0xEC] = Opcodes.call_cond
    t[0xEE] = Opcodes.xor_n
    t[0xEF] = Opcodes.rst
    t[0xF0] = Opcodes.ret_cc
    t[0xF1] = Opcodes.pop
    t[0xF2] = Opcodes.jp_cond
    t[0xF3] = Opcodes.disableInterrupts
    t[0xF4] = Opcodes.call_cond
    t[0xF5] = Opcodes.push
    t[0xF6] = Opcodes.or_n
    t[0xF7] = Opcodes.rst
    t[0xF8] = Opcodes.ret_cc
    t[0xF9] = Opcodes.ld_sp_hl
    t[0xFA] = Opcodes.jp_cond
    t[0xFB] = Opcodes.enableInterrupts
    t[0xFC] = Opcodes.call_cond
    t[0xFE] = Opcodes.cp_n
    t[0xFF] = Opcodes.rst
    return t


def build_cb_table():
    t = [None] * 256
    t[0x00] = Opcodes.rlc_n
    t[0x01] = Opcodes.rlc_n
    t[0x02] = Opcodes.rlc_n
    t[0x03] = Opcodes.rlc_n
    t[0x04] = Opcodes.rlc_n
    t[0x05] = Opcodes.rlc_n
    t[0x06] = Opcodes.rlc_at_hl
    t[0x07] = Opcodes.rlc_n
    t[0x08] = Opcodes.rrc_n
    t[0x09] = Opcodes.rrc_n
    t[0x0A] = Opcodes.rrc_n
    t[0x0B] = Opcodes.rrc_n
    t[0x0C] = Opcodes.rrc_n
    t[0x0D] = Opcodes.rrc_n
    t[0x0E] = Opcodes.rrc_at_hl
    t[0x0F] = Opcodes.rrc_n
    t[0x10] = Opcodes.rl_n
    t[0x11] = Opcodes.rl_n
    t[0x12] = Opcodes.rl_n
    t[0x13] = Opcodes.rl_n
    t[0x14] = Opcodes.rl_n
    t[0x15] = Opcodes.rl_n
    t[0x16] = Opcodes.rl_at_hl
    t[0x17] = Opcodes.rl_n
    t[0x18] = Opcodes.rr_n
    t[0x19] = Opcodes.rr_n
    t[0x1A] = Opcodes.rr_n
    t[0x1B] = Opcodes.rr_n
    t[0x1C] = Opcodes.rr_n
    t[0x1D] = Opcodes.rr_n
    t[0x1E] = Opcodes.rr_at_hl
    t[0x1F] = Opcodes.rr_n
    t[0x20] = Opcodes.sla_n
    t[0x21] = Opcodes.sla_n
    t[0x22] = Opcodes.sla_n
    t[0x23] = Opcodes.sla_n
    t[0x24] = Opcodes.sla_n
    t[0x25] = Opcodes.sla_n
    t[0x26] = Opcodes.sla_at_hl
    t[0x27] = Opcodes.sla_n
    t[0x28] = Opcodes.sra_n
    t[0x29] = Opcodes.sra_n
    t[0x2A] = Opcodes.sra_n
    t[0x2B] = Opcodes.sra_n
    t[0x2C] = Opcodes.sra_n
    t[0x2D] = Opcodes.sra_n
    t[0x2E] = Opcodes.sra_at_hl
    t[0x2F] = Opcodes.sra_n
    t[0x30] = Opcodes.sll_n
    t[0x31] = Opcodes.sll_n
    t[0x32] = Opcodes.sll_n
    t[0x33] = Opcodes.sll_n
    t[0x34] = Opcodes.sll_n
    t[0x35] = Opcodes.sll_n
    t[0x36] = Opcodes.sll_at_hl
    t[0x37] = Opcodes.sll_n
    t[0x38] = Opcodes.srl_r
    t[0x39] = Opcodes.srl_r
    t[0x3A] = Opcodes.srl_r
    t[0x3B] = Opcodes.srl_r
    t[0x3C] = Opcodes.srl_r
    t[0x3D] = Opcodes.srl_r
    t[0x3E] = Opcodes.srl_at_hl
    t[0x3F] = Opcodes.srl_r
    t[0x40] = Opcodes.bit_r_n
    t[0x41] = Opcodes.bit_r_n
    t[0x42] = Opcodes.bit_r_n
    t[0x43] = Opcodes.bit_r_n
    t[0x44] = Opcodes.bit_r_n
    t[0x45] = Opcodes.bit_r_n
    t[0x46] = Opcodes.bit_r_at_hl
    t[0x47] = Opcodes.bit_r_n
    t[0x48] = Opcodes.bit_r_n
    t[0x49] = Opcodes.bit_r_n
    t[0x4A] = Opcodes.bit_r_n
    t[0x4B] = Opcodes.bit_r_n
    t[0x4C] = Opcodes.bit_r_n
    t[0x4D] = Opcodes.bit_r_n
    t[0x4E] = Opcodes.bit_r_at_hl
    t[0x4F] = Opcodes.bit_r_n
    t[0x50] = Opcodes.bit_r_n
    t[0x51] = Opcodes.bit_r_n
    t[0x52] = Opcodes.bit_r_n
    t[0x53] = Opcodes.bit_r_n
    t[0x54] = Opcodes.bit_r_n
    t[0x55] = Opcodes.bit_r_n
    t[0x56] = Opcodes.bit_r_at_hl
    t[0x57] = Opcodes.bit_r_n
    t[0x58] = Opcodes.bit_r_n
    t[0x59] = Opcodes.bit_r_n
    t[0x5A] = Opcodes.bit_r_n
    t[0x5B] = Opcodes.bit_r_n
    t[0x5C] = Opcodes.bit_r_n
    t[0x5D] = Opcodes.bit_r_n
    t[0x5E] = Opcodes.bit_r_at_hl
    t[0x5F] = Opcodes.bit_r_n
    t[0x60] = Opcodes.bit_r_n
    t[0x61] = Opcodes.bit_r_n
    t[0x62] = Opcodes.bit_r_n
    t[0x63] = Opcodes.bit_r_n
    t[0x64] = Opcodes.bit_r_n
    t[0x65] = Opcodes.bit_r_n
    t[0x66] = Opcodes.bit_r_at_hl
    t[0x67] = Opcodes.bit_r_n
    t[0x68] = Opcodes.bit_r_n
    t[0x69] = Opcodes.bit_r_n
    t[0x6A] = Opcodes.bit_r_n
    t[0x6B] = Opcodes.bit_r_n
    t[0x6C] = Opcodes.bit_r_n
    t[0x6D] = Opcodes.bit_r_n
    t[0x6E] = Opcodes.bit_r_at_hl
    t[0x6F] = Opcodes.bit_r_n
    t[0x70] = Opcodes.bit_r_n
    t[0x71] = Opcodes.bit_r_n
    t[0x72] = Opcodes.bit_r_n
    t[0x73] = Opcodes.bit_r_n
    t[0x74] = Opcodes.bit_r_n
    t[0x75] = Opcodes.bit_r_n
    t[0x76] = Opcodes.bit_r_at_hl
    t[0x77] = Opcodes.bit_r_n
    t[0x78] = Opcodes.bit_r_n
    t[0x79] = Opcodes.bit_r_n
    t[0x7A] = Opcodes.bit_r_n
    t[0x7B] = Opcodes.bit_r_n
    t[0x7C] = Opcodes.bit_r_n
    t[0x7D] = Opcodes.bit_r_n
    t[0x7E] = Opcodes.bit_r_at_hl
    t[0x7F] = Opcodes.bit_r_n
    t[0x80] = Opcodes.res_r_n
    t[0x81] = Opcodes.res_r_n
    t[0x82] = Opcodes.res_r_n
    t[0x83] = Opcodes.res_r_n
    t[0x84] = Opcodes.res_r_n
    t[0x85] = Opcodes.res_r_n
    t[0x86] = Opcodes.res_r_at_hl
    t[0x87] = Opcodes.res_r_n
    t[0x88] = Opcodes.res_r_n
    t[0x89] = Opcodes.res_r_n
    t[0x8A] = Opcodes.res_r_n
    t[0x8B] = Opcodes.res_r_n
    t[0x8C] = Opcodes.res_r_n
    t[0x8D] = Opcodes.res_r_n
    t[0x8E] = Opcodes.res_r_at_hl
    t[0x8F] = Opcodes.res_r_n
    t[0x90] = Opcodes.res_r_n
    t[0x91] = Opcodes.res_r_n
    t[0x92] = Opcodes.res_r_n
    t[0x93] = Opcodes.res_r_n
    t[0x94] = Opcodes.res_r_n
    t[0x95] = Opcodes.res_r_n
    t[0x96] = Opcodes.res_r_at_hl
    t[0x97] = Opcodes.res_r_n
    t[0x98] = Opcodes.res_r_n
    t[0x99] = Opcodes.res_r_n
    t[0x9A] = Opcodes.res_r_n
    t[0x9B] = Opcodes.res_r_n
    t[0x9C] = Opcodes.res_r_n
    t[0x9D] = Opcodes.res_r_n
    t[0x9E] = Opcodes.res_r_at_hl
    t[0x9F] = Opcodes.res_r_n
    t[0xA0] = Opcodes.res_r_n
    t[0xA1] = Opcodes.res_r_n
    t[0xA2] = Opcodes.res_r_n
    t[0xA3] = Opcodes.res_r_n
    t[0xA4] = Opcodes.res_r_n
    t[0xA5] = Opcodes.res_r_n
    t[0xA6] = Opcodes.res_r_at_hl
    t[0xA7] = Opcodes.res_r_n
    t[0xA8] = Opcodes.res_r_n
    t[0xA9] = Opcodes.res_r_n
    t[0xAA] = Opcodes.res_r_n
    t[0xAB] = Opcodes.res_r_n
    t[0xAC] = Opcodes.res_r_n
    t[0xAD] = Opcodes.res_r_n
    t[0xAE] = Opcodes.res_r_at_hl
    t[0xAF] = Opcodes.res_r_n
    t[0xB0] = Opcodes.res_r_n
    t[0xB1] = Opcodes.res_r_n
    t[0xB2] = Opcodes.res_r_n
    t[0xB3] = Opcodes.res_r_n
    t[0xB4] = Opcodes.res_r_n
    t[0xB5] = Opcodes.res_r_n
    t[0xB6] = Opcodes.res_r_at_hl
    t[0xB7] = Opcodes.res_r_n
    t[0xB8] = Opcodes.res_r_n
    t[0xB9] = Opcodes.res_r_n
    t[0xBA] = Opcodes.res_r_n
    t[0xBB] = Opcodes.res_r_n
    t[0xBC] = Opcodes.res_r_n
    t[0xBD] = Opcodes.res_r_n
    t[0xBE] = Opcodes.res_r_at_hl
    t[0xBF] = Opcodes.res_r_n
    t[0xC0] = Opcodes.set_r_n
    t[0xC1] = Opcodes.set_r_n
    t[0xC2] = Opcodes.set_r_n
    t[0xC3] = Opcodes.set_r_n
    t[0xC4] = Opcodes.set_r_n
    t[0xC5] = Opcodes.set_r_n
    t[0xC6] = Opcodes.set_r_at_hl
    t[0xC7] = Opcodes.set_r_n
    t[0xC8] = Opcodes.set_r_n
    t[0xC9] = Opcodes.set_r_n
    t[0xCA] = Opcodes.set_r_n
    t[0xCB] = Opcodes.set_r_n
    t[0xCC] = Opcodes.set_r_n
    t[0xCD] = Opcodes.set_r_n
    t[0xCE] = Opcodes.set_r_at_hl
    t[0xCF] = Opcodes.set_r_n
    t[0xD0] = Opcodes.set_r_n
    t[0xD1] = Opcodes.set_r_n
    t[0xD2] = Opcodes.set_r_n
    t[0xD3] = Opcodes.set_r_n
    t[0xD4] = Opcodes.set_r_n
    t[0xD5] = Opcodes.set_r_n
    t[0xD6] = Opcodes.set_r_at_hl
    t[0xD7] = Opcodes.set_r_n
    t[0xD8] = Opcodes.set_r_n
    t[0xD9] = Opcodes.set_r_n
    t[0xDA] = Opcodes.set_r_n
    t[0xDB] = Opcodes.set_r_n
    t[0xDC] = Opcodes.set_r_n
    t[0xDD] = Opcodes.set_r_n
    t[0xDE] = Opcodes.set_r_at_hl
    t[0xDF] = Opcodes.set_r_n
    t[0xE0] = Opcodes.set_r_n
    t[0xE1] = Opcodes.set_r_n
    t[0xE2] = Opcodes.set_r_n
    t[0xE3] = Opcodes.set_r_n
    t[0xE4] = Opcodes.set_r_n
    t[0xE5] = Opcodes.set_r_n
    t[0xE6] = Opcodes.set_r_at_hl
    t[0xE7] = Opcodes.set_r_n
    t[0xE8] = Opcodes.set_r_n
    t[0xE9] = Opcodes.set_r_n
    t[0xEA] = Opcodes.set_r_n
    t[0xEB] = Opcodes.set_r_n
    t[0xEC] = Opcodes.set_r_n
    t[0xED] = Opcodes.set_r_n
    t[0xEE] = Opcodes.set_r_at_hl
    t[0xEF] = Opcodes.set_r_n
    t[0xF0] = Opcodes.set_r_n
    t[0xF1] = Opcodes.set_r_n
    t[0xF2] = Opcodes.set_r_n
    t[0xF3] = Opcodes.set_r_n
    t[0xF4] = Opcodes.set_r_n
    t[0xF5] = Opcodes.set_r_n
    t[0xF6] = Opcodes.set_r_at_hl
    t[0xF7] = Opcodes.set_r_n
    t[0xF8] = Opcodes.set_r_n
    t[0xF9] = Opcodes.set_r_n
    t[0xFA] = Opcodes.set_r_n
    t[0xFB] = Opcodes.set_r_n
    t[0xFC] = Opcodes.set_r_n
    t[0xFD] = Opcodes.set_r_n
    t[0xFE] = Opcodes.set_r_at_hl
    t[0xFF] = Opcodes.set_r_n
    return t


def build_dd_table():
    return {
        0x09: Opcodes.add_ix_rr,
        0x19: Opcodes.add_ix_rr,
        0x21: Opcodes.ld_ix_nn,
        0x22: Opcodes.ld_nn_ix,
        0x23: Opcodes.inc_ix,
        0x24: Opcodes.inc_ixh,
        0x25: Opcodes.dec_ixh,
        0x26: Opcodes.ld_ixh_nn,
        0x29: Opcodes.add_ix_rr,
        0x2A: Opcodes.ld_ix_at_nn,
        0x2B: Opcodes.dec_ix,
        0x2C: Opcodes.inc_ixl,
        0x2D: Opcodes.dec_ixl,
        0x2E: Opcodes.ld_ixl_nn,
        0x34: Opcodes.inc_at_ix_d,
        0x35: Opcodes.dec_at_ix_d,
        0x36: Opcodes.ld_at_ix_d_nn,
        0x39: Opcodes.add_ix_rr,
        0x40: Opcodes.ld8,
        0x41: Opcodes.ld8,
        0x42: Opcodes.ld8,
        0x43: Opcodes.ld8,
        0x44: Opcodes.ld_r_ixh,
        0x45: Opcodes.ld_r_ixl,
        0x46: Opcodes.ld_r_ix_d,
        0x47: Opcodes.ld8,
        0x48: Opcodes.ld8,
        0x49: Opcodes.ld8,
        0x4A: Opcodes.ld8,
        0x4B: Opcodes.ld8,
        0x4C: Opcodes.ld_r_ixh,
        0x4D: Opcodes.ld_r_ixl,
        0x4E: Opcodes.ld_r_ix_d,
        0x4F: Opcodes.ld8,
        0x50: Opcodes.ld8,
        0x51: Opcodes.ld8,
        0x52: Opcodes.ld8,
        0x53: Opcodes.ld8,
        0x54: Opcodes.ld_r_ixh,
        0x55: Opcodes.ld_r_ixl,
        0x56: Opcodes.ld_r_ix_d,
        0x57: Opcodes.ld8,
        0x58: Opcodes.ld8,
        0x59: Opcodes.ld8,
        0x5A: Opcodes.ld8,
        0x5B: Opcodes.ld8,
        0x5C: Opcodes.ld_r_ixh,
        0x5D: Opcodes.ld_r_ixl,
        0x5E: Opcodes.ld_r_ix_d,
        0x5F: Opcodes.ld8,
        0x60: Opcodes.ld_ixh_r,
        0x61: Opcodes.ld_ixh_r,
        0x62: Opcodes.ld_ixh_r,
        0x63: Opcodes.ld_ixh_r,
        0x64: Opcodes.ld_ixh_r,
        0x65: Opcodes.ld_ixh_r,
        0x66: Opcodes.ld_r_ix_d,
        0x67: Opcodes.ld_ixh_r,
        0x68: Opcodes.ld_ixl_r,
        0x69: Opcodes.ld_ixl_r,
        0x6A: Opcodes.ld_ixl_r,
        0x6B: Opcodes.ld_ixl_r,
        0x6C: Opcodes.ld_ixl_ixh,
        0x6D: Opcodes.ld_ixl_r,
        0x6E: Opcodes.ld_r_ix_d,
        0x6F: Opcodes.ld_ixl_r,
        0x70: Opcodes.ld_at_ix_d_r,
        0x71: Opcodes.ld_at_ix_d_r,
        0x72: Opcodes.ld_at_ix_d_r,
        0x73: Opcodes.ld_at_ix_d_r,
        0x74: Opcodes.ld_at_ix_d_r,
        0x75: Opcodes.ld_at_ix_d_r,
        0x77: Opcodes.ld_at_ix_d_r,
        0x78: Opcodes.ld8,
        0x79: Opcodes.ld8,
        0x7A: Opcodes.ld8,
        0x7B: Opcodes.ld8,
        0x7C: Opcodes.ld_r_ixh,
        0x7D: Opcodes.ld_r_ixl,
        0x7E: Opcodes.ld_r_ix_d,
        0x7F: Opcodes.ld8,
        0x84: Opcodes.add_a_ixh,
        0x85: Opcodes.add_a_ixl,
        0x86: Opcodes.add_a_ix_d,
        0x8C: Opcodes.adc_a_ixh,
        0x8D: Opcodes.adc_a_ixl,
        0x8E: Opcodes.adc_a_ix_d,
        0x94: Opcodes.sub_ixh,
        0x95: Opcodes.sub_ixl,
        0x96: Opcodes.sub_ix_d,
        0x9C: Opcodes.sbc_a_ixh,
        0x9D: Opcodes.sbc_a_ixl,
        0x9E: Opcodes.sbc_a_ix_d,
        0xA4: Opcodes.and_ixh,
        0xA5: Opcodes.and_ixl,
        0xA6: Opcodes.and_ix_d,
        0xAC: Opcodes.xor_ixh,
        0xAD: Opcodes.xor_ixl,
        0xAE: Opcodes.xor_ix_d,
        0xB4: Opcodes.or_ixh,
        0xB5: Opcodes.or_ixl,
        0xB6: Opcodes.or_ix_d,
        0xBC: Opcodes.cp_ixh,
        0xBD: Opcodes.cp_ixl,
        0xBE: Opcodes.cp_ix_d,
        0xE1: Opcodes.pop_ix,
        0xE5: Opcodes.push_ix,
        0xE9: Opcodes.jp_ix,
    }


def build_ed_table():
    return {
        0x42: Opcodes.sbc,
        0x43: Opcodes.ldNnRr,
        0x44: Opcodes.neg,
        0x45: Opcodes.retn,
        0x46: Opcodes.im0,
        0x4D: Opcodes.reti,
        0x47: Opcodes.ldExt,
        0x4A: Opcodes.add_Hl_rr_c,
        0x4B: Opcodes.ld16_nn,
        0x4F: Opcodes.ldra,
        0x52: Opcodes.sbc,
        0x53: Opcodes.ldNnRr,
        0x55: Opcodes.retn,
        0x56: Opcodes.im1,
        0x57: Opcodes.ldai,
        0x5A: Opcodes.add_Hl_rr_c,
        0x5B: Opcodes.ld16_nn,
        0x5E: Opcodes.im2,
        0x5F: Opcodes.ldar,
        0x62: Opcodes.sbc,
        0x63: Opcodes.ldNnRr,
        0x65: Opcodes.retn,
        0x67: Opcodes.rrd,
        0x6A: Opcodes.add_Hl_rr_c,
        0x6B: Opcodes.ld16_nn,
        0x6F: Opcodes.rld,
        0x72: Opcodes.sbc,
        0x73: Opcodes.ldNnRr,
        0x75: Opcodes.retn,
        0x78: Opcodes.portIn,
        0x7A: Opcodes.add_Hl_rr_c,
        0x7B: Opcodes.ld16_nn,
        0xA0: Opcodes.ldi,
        0xA1: Opcodes.cpi,
        0xA8: Opcodes.ldd,
        0xA9: Opcodes.cpd,
        0xB0: Opcodes.ldir,
        0xB1: Opcodes.cpir,
        0xB8: Opcodes.lddr,
        0xB9: Opcodes.cpdr,
    }


def build_fd_table():
    return {
        0x09: Opcodes.add_iy_rr,
        0x19: Opcodes.add_iy_rr,
        0x21: Opcodes.ldiy,
        0x22: Opcodes.ld_nn_iy,
        0x23: Opcodes.inc_iy,
        0x26: Opcodes.ld_ihy_nn,
        0x29: Opcodes.add_iy_rr,
        0x2A: Opcodes.ld_iy_at_nn,
        0x2B: Opcodes.dec_iy,
        0x2E: Opcodes.ld_iyl_nn,
        0x34: Opcodes.inc_mem_at_iy,
        0x35: Opcodes.dec_mem_at_iy,
        0x36: Opcodes.ldiy_d_n,
        0x39: Opcodes.add_iy_rr,
        0x40: Opcodes.ld8,
        0x41: Opcodes.ld8,
        0x42: Opcodes.ld8,
        0x43: Opcodes.ld8,
        0x44: Opcodes.ld_r_iyh,
        0x45: Opcodes.ld_r_iyl,
        0x46: Opcodes.ld_r_iy_d,
        0x47: Opcodes.ld8,
        0x48: Opcodes.ld8,
        0x49: Opcodes.ld8,
        0x4A: Opcodes.ld8,
        0x4B: Opcodes.ld8,
        0x4C: Opcodes.ld_r_iyh,
        0x4D: Opcodes.ld_r_iyl,
        0x4E: Opcodes.ld_r_iy_d,
        0x4F: Opcodes.ld8,
        0x50: Opcodes.ld8,
        0x51: Opcodes.ld8,
        0x52: Opcodes.ld8,
        0x53: Opcodes.ld8,
        0x54: Opcodes.ld_r_iyh,
        0x55: Opcodes.ld_r_iyl,
        0x56: Opcodes.ld_r_iy_d,
        0x57: Opcodes.ld8,
        0x58: Opcodes.ld8,
        0x59: Opcodes.ld8,
        0x5A: Opcodes.ld8,
        0x5B: Opcodes.ld8,
        0x5C: Opcodes.ld_r_iyh,
        0x5D: Opcodes.ld_r_iyl,
        0x5E: Opcodes.ld_r_iy_d,
        0x5F: Opcodes.ld8,
        0x60: Opcodes.ld_iyh_r,
        0x61: Opcodes.ld_iyh_r,
        0x62: Opcodes.ld_iyh_r,
        0x63: Opcodes.ld_iyh_r,
        0x64: Opcodes.ld_iyh_r,
        0x65: Opcodes.ld_iyh_r,
        0x66: Opcodes.ld_r_iy_d,
        0x67: Opcodes.ld_iyh_r,
        0x68: Opcodes.ld_iyl_r,
        0x69: Opcodes.ld_iyl_r,
        0x6A: Opcodes.ld_iyl_r,
        0x6B: Opcodes.ld_iyl_r,
        0x6C: Opcodes.ld_iyl_iyh,
        0x6D: Opcodes.ld_iyl_r,
        0x6E: Opcodes.ld_r_iy_d,
        0x6F: Opcodes.ld_iyl_r,
        0x70: Opcodes.ld_at_iy_d_r,
        0x71: Opcodes.ld_at_iy_d_r,
        0x72: Opcodes.ld_at_iy_d_r,
        0x73: Opcodes.ld_at_iy_d_r,
        0x74: Opcodes.ld_at_iy_d_r,
        0x75: Opcodes.ld_at_iy_d_r,
        0x77: Opcodes.ld_at_iy_d_r,
        0x78: Opcodes.ld8,
        0x79: Opcodes.ld8,
        0x7A: Opcodes.ld8,
        0x7B: Opcodes.ld8,
        0x7C: Opcodes.ld_r_iyh,
        0x7D: Opcodes.ld_r_iyl,
        0x7E: Opcodes.ld_r_iy_d,
        0x7F: Opcodes.ld8,
        0x84: Opcodes.add_a_iyh,
        0x85: Opcodes.add_a_iyl,
        0x86: Opcodes.add_a_iy_d,
        0x8C: Opcodes.adc_a_iyh,
        0x8D: Opcodes.adc_a_iyl,
        0x8E: Opcodes.adc_a_iy_d,
        0x94: Opcodes.sub_iyh,
        0x95: Opcodes.sub_iyl,
        0x96: Opcodes.sub_iy_d,
        0x9C: Opcodes.sbc_a_iyh,
        0x9D: Opcodes.sbc_a_iyl,
        0x9E: Opcodes.sbc_a_iy_d,
        0xA4: Opcodes.and_iyh,
        0xA5: Opcodes.and_iyl,
        0xA6: Opcodes.and_iy_d,
        0xAC: Opcodes.xor_iyh,
        0xAD: Opcodes.xor_iyl,
        0xAE: Opcodes.xor_iy_d,
        0xB4: Opcodes.or_iyh,
        0xB5: Opcodes.or_iyl,
        0xB6: Opcodes.or_iy_d,
        0xBC: Opcodes.cp_iyh,
        0xBD: Opcodes.cp_iyl,
        0xBE: Opcodes.cp_iy_d,
        0xE1: Opcodes.pop_iy,
        0xE5: Opcodes.push_iy,
        0xE9: Opcodes.jp_iy,
    }


def build_ddcb_table():
    t = [None] * 256
    t[0x06] = Opcodes.rlc_at_ix_n
    t[0x0E] = Opcodes.rrc_at_ix_n
    t[0x16] = Opcodes.rl_at_ix_n
    t[0x1E] = Opcodes.rr_at_ix_n
    t[0x26] = Opcodes.sla_at_ix_n
    t[0x2E] = Opcodes.sra_at_ix_n
    t[0x36] = Opcodes.sll_at_ix_n
    t[0x3E] = Opcodes.srl_at_ix_n
    t[0x46] = Opcodes.bit_bit_ix
    t[0x4E] = Opcodes.bit_bit_ix
    t[0x56] = Opcodes.bit_bit_ix
    t[0x5E] = Opcodes.bit_bit_ix
    t[0x66] = Opcodes.bit_bit_ix
    t[0x6E] = Opcodes.bit_bit_ix
    t[0x76] = Opcodes.bit_bit_ix
    t[0x7E] = Opcodes.bit_bit_ix
    t[0x86] = Opcodes.bit_res_ix
    t[0x8E] = Opcodes.bit_res_ix
    t[0x96] = Opcodes.bit_res_ix
    t[0x9E] = Opcodes.bit_res_ix
    t[0xA6] = Opcodes.bit_res_ix
    t[0xAE] = Opcodes.bit_res_ix
    t[0xB6] = Opcodes.bit_res_ix
    t[0xBE] = Opcodes.bit_res_ix
    t[0xC6] = Opcodes.bit_set_ix
    t[0xCE] = Opcodes.bit_set_ix
    t[0xD6] = Opcodes.bit_set_ix
    t[0xDE] = Opcodes.bit_set_ix
    t[0xE6] = Opcodes.bit_set_ix
    t[0xEE] = Opcodes.bit_set_ix
    t[0xF6] = Opcodes.bit_set_ix
    t[0xFE] = Opcodes.bit_set_ix
    return t


def build_fdcb_table():
    t = [None] * 256
    t[0x06] = Opcodes.rlc_at_iy_n
    t[0x0E] = Opcodes.rrc_at_iy_n
    t[0x16] = Opcodes.rl_at_iy_n
    t[0x1E] = Opcodes.rr_at_iy_n
    t[0x26] = Opcodes.sla_at_iy_n
    t[0x2E] = Opcodes.sra_at_iy_n
    t[0x36] = Opcodes.sll_at_iy_n
    t[0x3E] = Opcodes.srl_at_iy_n
    t[0x46] = Opcodes.bit_bit_iy
    t[0x4E] = Opcodes.bit_bit_iy
    t[0x56] = Opcodes.bit_bit_iy
    t[0x5E] = Opcodes.bit_bit_iy
    t[0x66] = Opcodes.bit_bit_iy
    t[0x6E] = Opcodes.bit_bit_iy
    t[0x76] = Opcodes.bit_bit_iy
    t[0x7E] = Opcodes.bit_bit_iy
    t[0x86] = Opcodes.bit_res_iy
    t[0x8E] = Opcodes.bit_res_iy
    t[0x96] = Opcodes.bit_res_iy
    t[0x9E] = Opcodes.bit_res_iy
    t[0xA6] = Opcodes.bit_res_iy
    t[0xAE] = Opcodes.bit_res_iy
    t[0xB6] = Opcodes.bit_res_iy
    t[0xBE] = Opcodes.bit_res_iy
    t[0xC6] = Opcodes.bit_set_iy
    t[0xCE] = Opcodes.bit_set_iy
    t[0xD6] = Opcodes.bit_set_iy
    t[0xDE] = Opcodes.bit_set_iy
    t[0xE6] = Opcodes.bit_set_iy
    t[0xEE] = Opcodes.bit_set_iy
    t[0xF6] = Opcodes.bit_set_iy
    t[0xFE] = Opcodes.bit_set_iy
    return t

