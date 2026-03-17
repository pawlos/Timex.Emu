# Z80 register and flag name lookup tables


class IndexToReg(object):
    @staticmethod
    def translate16Bit(ind, ix=False, iy=False, af=False):
        if ind == 0:
            return "BC"
        if ind == 1:
            return "DE"
        if ind == 2 and not ix and not iy:
            return "HL"
        if ind == 2 and ix:
            return "IX"
        if ind == 2 and iy:
            return "IY"
        if ind == 3 and not af:
            return "SP"
        if ind == 3 and af:
            return "AF"

    @staticmethod
    def translate8Bit(ind):
        if ind == 0:
            return "B"
        if ind == 1:
            return "C"
        if ind == 2:
            return "D"
        if ind == 3:
            return "E"
        if ind == 4:
            return "H"
        if ind == 5:
            return "L"
        if ind == 7:
            return "A"


class IndexToFlag(object):
    @staticmethod
    def translate(ind):
        if ind == 0:
            return "NZ"
        if ind == 1:
            return "Z"
        if ind == 2:
            return "NC"
        if ind == 3:
            return "C"
        if ind == 4:
            return "NPV"
        if ind == 5:
            return "PV"
        if ind == 6:
            return "NS"
        if ind == 7:
            return "S"
