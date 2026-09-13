# ============================================================
# ZN + HCL EXPERIMENT
# experiments/zn_hcl.py
# ============================================================

from chemistry.reaction_engine import ReactionEngine
from chemistry.reactions import ZN_HCL

from .base_experiment import BaseExperiment


class ZnHClExperiment(BaseExperiment):
    """
    Thí nghiệm:

        Zn + 2HCl → ZnCl₂ + H₂↑

    Input:

        zn_mass
            Khối lượng Zn, đơn vị gram.

        hcl_concentration
            Nồng độ HCl, đơn vị mol/L.

        hcl_volume
            Thể tích HCl, đơn vị mL.
    """

    # ========================================================
    # EXPERIMENT INFORMATION
    # ========================================================

    id = "zn_hcl"

    name = "Zn + HCl"

    category = "Kim loại + axit"

    description = (
        "Kẽm tác dụng với axit clohiđric"
    )

    equation = ZN_HCL.equation

    # Thí nghiệm đã được triển khai
    available = True

    # ========================================================
    # CONSTANTS
    # ========================================================

    M_ZN = 65.38

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):
        self.engine = ReactionEngine()

    # ========================================================
    # CALCULATION
    # ========================================================

    def calculate(self, inputs):
        """
        Chuyển dữ liệu đầu vào thành số mol
        rồi gửi cho ReactionEngine.

        inputs:

            {
                "zn_mass": 1.00,
                "hcl_concentration": 1.0,
                "hcl_volume": 100
            }
        """

        self.validate_inputs(inputs)

        # ----------------------------------------------------
        # GET INPUT
        # ----------------------------------------------------

        zn_mass = self._get_positive_value(
            inputs,
            "zn_mass"
        )

        hcl_concentration = self._get_positive_value(
            inputs,
            "hcl_concentration"
        )

        hcl_volume = self._get_positive_value(
            inputs,
            "hcl_volume"
        )

        # ----------------------------------------------------
        # Zn → mol
        # ----------------------------------------------------

        n_zn = (
            zn_mass
            / self.M_ZN
        )

        # ----------------------------------------------------
        # mL → L
        # ----------------------------------------------------

        hcl_volume_l = (
            hcl_volume
            / 1000.0
        )

        # ----------------------------------------------------
        # HCl → mol
        # ----------------------------------------------------

        n_hcl = (
            hcl_concentration
            * hcl_volume_l
        )

        # ----------------------------------------------------
        # REACTION ENGINE
        # ----------------------------------------------------

        result = self.engine.calculate(
            reaction=ZN_HCL,
            initial_moles={
                "Zn": n_zn,
                "HCl": n_hcl,
            }
        )

        return result

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_inputs(self, inputs):

        super().validate_inputs(inputs)

        required = [
            "zn_mass",
            "hcl_concentration",
            "hcl_volume",
        ]

        for key in required:

            if key not in inputs:
                raise ValueError(
                    f"Thiếu thông số: {key}"
                )

            try:
                value = float(
                    inputs[key]
                )

            except (
                TypeError,
                ValueError
            ):

                raise ValueError(
                    f"{key} phải là một số."
                )

            if value <= 0:

                raise ValueError(
                    f"{key} phải > 0."
                )

    # ========================================================
    # PRIVATE HELPER
    # ========================================================

    def _get_positive_value(
        self,
        inputs,
        key
    ):

        value = float(
            inputs[key]
        )

        if value <= 0:

            raise ValueError(
                f"{key} phải > 0."
            )

        return value