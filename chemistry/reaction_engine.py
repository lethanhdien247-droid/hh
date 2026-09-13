from dataclasses import dataclass
from typing import Dict, Optional

from .reactions import Reaction


@dataclass
class ReactionResult:
    """
    Kết quả của một phản ứng hóa học.
    """

    limiting_reagent: Optional[str]

    reaction_extent: float

    initial_moles: Dict[str, float]

    consumed_moles: Dict[str, float]

    remaining_moles: Dict[str, float]

    product_moles: Dict[str, float]

    completion_percentage: float

class ReactionEngine:
    """
    Bộ máy tính toán stoichiometry.

    Engine không phụ thuộc vào Kivy.
    """

    EPSILON = 1e-9

    def calculate(
        self,
        reaction: Reaction,
        initial_moles: Dict[str, float],
    ) -> ReactionResult:

        self._validate_input(
            reaction,
            initial_moles
        )

        reaction_extent = self._calculate_extent(
            reaction,
            initial_moles
        )

        limiting_reagent = self._find_limiting_reagent(
            reaction,
            initial_moles,
            reaction_extent
        )

        consumed_moles = {}

        remaining_moles = {}

        for substance, coefficient in reaction.reactants.items():

            consumed = (
                reaction_extent
                * coefficient
            )

            initial = initial_moles.get(
                substance,
                0.0
            )

            consumed = min(
                consumed,
                initial
            )

            remaining = max(
                0.0,
                initial - consumed
            )

            consumed_moles[substance] = consumed

            remaining_moles[substance] = remaining

        product_moles = {}

        for substance, coefficient in reaction.products.items():

            product_moles[substance] = (
                reaction_extent
                * coefficient
            )

        completion_percentage = (
            self._calculate_completion(
                reaction,
                initial_moles,
                remaining_moles
            )
        )

        return ReactionResult(
            limiting_reagent=limiting_reagent,

            reaction_extent=reaction_extent,

            initial_moles=dict(
                initial_moles
            ),

            consumed_moles=consumed_moles,

            remaining_moles=remaining_moles,

            product_moles=product_moles,

            completion_percentage=completion_percentage,
        )

    # ========================================================
    # VALIDATION
    # ========================================================

    def _validate_input(
        self,
        reaction: Reaction,
        initial_moles: Dict[str, float],
    ):

        if not reaction.reactants:

            raise ValueError(
                "Phản ứng phải có chất phản ứng."
            )

        for substance, coefficient in (
            reaction.reactants.items()
        ):

            if coefficient <= 0:

                raise ValueError(
                    f"Hệ số của {substance} phải > 0."
                )

            if substance not in initial_moles:

                raise ValueError(
                    f"Thiếu số mol của {substance}."
                )

            moles = initial_moles[substance]

            if moles < 0:

                raise ValueError(
                    f"Số mol của {substance} không được âm."
                )

    # ========================================================
    # REACTION EXTENT
    # ========================================================

    def _calculate_extent(
        self,
        reaction: Reaction,
        initial_moles: Dict[str, float],
    ) -> float:

        ratios = []

        for substance, coefficient in (
            reaction.reactants.items()
        ):

            ratio = (
                initial_moles[substance]
                / coefficient
            )

            ratios.append(
                ratio
            )

        return min(
            ratios
        )

    # ========================================================
    # LIMITING REAGENT
    # ========================================================

    def _find_limiting_reagent(
        self,
        reaction: Reaction,
        initial_moles: Dict[str, float],
        reaction_extent: float,
    ) -> Optional[str]:

        limiting = None

        for substance, coefficient in (
            reaction.reactants.items()
        ):

            ratio = (
                initial_moles[substance]
                / coefficient
            )

            if abs(
                ratio - reaction_extent
            ) <= self.EPSILON:

                if limiting is not None:

                    # Hai chất vừa đủ theo
                    # tỉ lệ stoichiometry.
                    return None

                limiting = substance

        return limiting

    # ========================================================
    # COMPLETION
    # ========================================================

    def _calculate_completion(
        self,
        reaction: Reaction,
        initial_moles: Dict[str, float],
        remaining_moles: Dict[str, float],
    ) -> float:

        percentages = []

        for substance in reaction.reactants:

            initial = initial_moles[substance]

            if initial <= self.EPSILON:

                continue

            remaining = remaining_moles[substance]

            consumed_fraction = (
                1
                - remaining / initial
            )

            percentages.append(
                consumed_fraction
            )

        if not percentages:

            return 0.0

        return max(
            0.0,
            min(
                100.0,
                max(percentages) * 100
            )
        )