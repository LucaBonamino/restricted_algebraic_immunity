import enum


class FileName(enum.Enum):
    DEGREES = "degs"
    REED_MILLER = "RMs"
    MONOMIALS = "monomials"

class ReturnType(enum.Enum):
    DATA_FRAME = 'DataFrame'