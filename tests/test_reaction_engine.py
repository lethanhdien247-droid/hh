from chemistry.reaction_engine import ReactionEngine
from chemistry.reactions import ZN_HCL


def test_zn_hcl_hcl_limiting():

    engine = ReactionEngine()

    result = engine.calculate(
        reaction=ZN_HCL,
        initial_moles={
            "Zn": 0.1,
            "HCl": 0.1,
        }
    )

    assert result.limiting_reagent == "HCl"

    assert abs(
        result.product_moles["H2"] - 0.05
    ) < 1e-9

    assert abs(
        result.remaining_moles["Zn"] - 0.05
    ) < 1e-9

    assert abs(
        result.remaining_moles["HCl"]
    ) < 1e-9