# ============================================================
# CHEMICAL REACTIONS
# chemistry/reactions.py
# ============================================================

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Reaction:
    """
    Đại diện cho một phản ứng hóa học.

    reactants:
        Các chất tham gia phản ứng và hệ số cân bằng.

    products:
        Các sản phẩm và hệ số cân bằng.

    equation:
        Phương trình hóa học dùng để hiển thị.
    """

    reactants: Dict[str, int]

    products: Dict[str, int]

    equation: str


# ============================================================
# Zn + HCl
# ============================================================

ZN_HCL = Reaction(

    reactants={
        "Zn": 1,
        "HCl": 2,
    },

    products={
        "ZnCl2": 1,
        "H2": 1,
    },

    equation="Zn + 2HCl → ZnCl₂ + H₂↑",
)