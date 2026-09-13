# ============================================================
# RESPONSIVE LAYOUT
# widgets/responsive_layout.py
# ============================================================

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout


class ResponsiveLayout(BoxLayout):
    """
    Layout tự động chuyển giữa:

        Mobile:
            vertical

        Tablet / Desktop:
            horizontal

    BREAKPOINT tính theo dp.
    """

    BREAKPOINT = dp(700)

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.orientation = "vertical"

        self.bind(
            width=self._on_width
        )

        Clock.schedule_once(
            self.update_layout,
            0
        )

    # ========================================================
    # WIDTH CHANGE
    # ========================================================

    def _on_width(
        self,
        instance,
        width
    ):

        self.update_layout()

    # ========================================================
    # UPDATE
    # ========================================================

    def update_layout(
        self,
        *args
    ):

        if self.width < self.BREAKPOINT:

            self.orientation = "vertical"

        else:

            self.orientation = "horizontal"