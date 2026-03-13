# Z80 Opcodes - combined from category modules

from ops_load import OpsLoad
from ops_alu import OpsAlu
from ops_branch import OpsBranch
from ops_bitshift import OpsBitshift
from ops_incdec import OpsIncdec
from ops_block import OpsBlock
from ops_misc import OpsMisc


class Opcodes(OpsLoad, OpsAlu, OpsBranch, OpsBitshift, OpsIncdec, OpsBlock, OpsMisc):
    pass
