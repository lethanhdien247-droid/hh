# ============================================================
# TEST Zn + HCl EXPERIMENT
# ============================================================

from experiments.zn_hcl import ZnHClExperiment


def test_zn_hcl():

    experiment = ZnHClExperiment()

    result = experiment.calculate(
        {
            "zn_mass": 1.00,
            "hcl_concentration": 1.0,
            "hcl_volume": 100,
        }
    )

    print()
    print("========== Zn + HCl ==========")

    print(
        "n(Zn):",
        result.initial_moles["Zn"]
    )

    print(
        "n(HCl):",
        result.initial_moles["HCl"]
    )

    print(
        "Limiting:",
        result.limiting_reagent
    )

    print(
        "n(H2):",
        result.product_moles["H2"]
    )

    print(
        "Zn remaining:",
        result.remaining_moles["Zn"]
    )

    print(
        "HCl remaining:",
        result.remaining_moles["HCl"]
    )