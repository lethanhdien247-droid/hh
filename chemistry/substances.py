from dataclasses import dataclass


@dataclass(frozen=True)
class Substance:
    """
    Đại diện cho một chất hóa học.

    Attributes
    ----------
    formula:
        Công thức hóa học.

    molar_mass:
        Khối lượng mol, đơn vị g/mol.
    """

    formula: str
    molar_mass: float