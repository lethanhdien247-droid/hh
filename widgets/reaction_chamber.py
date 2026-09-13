import random

from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import (
    Color,
    RoundedRectangle,
    Ellipse,
    Line
)

# ============================================================
# BUBBLE
# ============================================================

class Bubble(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        diameter = dp(
            random.randint(5, 10)
        )

        self.size = (
            diameter,
            diameter
        )

        with self.canvas:

            Color(
                0.65,
                0.90,
                1,
                0.8
            )

            self.circle = Ellipse(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self._update_graphics,
            size=self._update_graphics
        )

    def _update_graphics(
        self,
        *args
    ):

        self.circle.pos = self.pos
        self.circle.size = self.size


# ============================================================
# REACTION CHAMBER
# ============================================================

class ReactionChamber(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.bubbles = []

        self.zinc_remaining = 1.0

        with self.canvas:

            # Liquid

            Color(
                0.75,
                0.90,
                0.95,
                0.65
            )

            self.liquid = RoundedRectangle(
                pos=(0, 0),
                size=(0, 0),
                radius=[dp(10)]
            )

            # Zinc

            Color(
                0.55,
                0.58,
                0.62,
                1
            )

            self.zinc = RoundedRectangle(
                pos=(0, 0),
                size=(0, 0),
                radius=[dp(5)]
            )

            # Glass

            Color(
                0.70,
                0.85,
                0.95,
                1
            )

            self.glass = Line(
                width=2
            )

        self.bind(
            pos=self._update_graphics,
            size=self._update_graphics
        )

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    def _update_graphics(
        self,
        *args
    ):

        x = self.x + self.width * 0.25
        y = self.y + self.height * 0.10

        width = self.width * 0.50
        height = self.height * 0.78

        # Liquid

        self.liquid.pos = (
            x,
            y
        )

        self.liquid.size = (
            width,
            height * 0.55
        )

        # Zinc

        zinc_width = max(
            dp(2),
            width * 0.35 * self.zinc_remaining
        )

        self.zinc.pos = (
            x + width * 0.325,
            y + height * 0.05
        )

        self.zinc.size = (
            zinc_width,
            height * 0.08
        )

        # Glass

        self.glass.rectangle = (
            x,
            y,
            width,
            height
        )

    # --------------------------------------------------------
    # SET ZINC
    # --------------------------------------------------------

    def set_zinc_remaining(
        self,
        fraction
    ):

        self.zinc_remaining = max(
            0.0,
            min(
                1.0,
                fraction
            )
        )

        self._update_graphics()

    # --------------------------------------------------------
    # BUBBLE
    # --------------------------------------------------------

    def create_bubble(self):

        if self.width <= 0 or self.height <= 0:
            return

        x = (
            self.x
            + self.width * 0.35
            + random.random()
            * self.width * 0.30
        )

        y = (
            self.y
            + self.height * 0.20
        )

        bubble = Bubble(
            pos=(x, y)
        )

        self.add_widget(
            bubble
        )

        self.bubbles.append(
            bubble
        )

        # Bubble movement is controlled
        # by the main simulation loop.

        bubble._target_y = (
            self.y
            + self.height * 0.70
            + random.random()
            * self.height * 0.15
        )

        bubble._speed = random.uniform(
            40,
            80
        )

    # --------------------------------------------------------
    # UPDATE BUBBLES
    # --------------------------------------------------------

    def update_bubbles(
        self,
        dt
    ):

        for bubble in list(
            self.bubbles
        ):

            bubble.y += (
                bubble._speed * dt
            )

            bubble.x += random.uniform(
                -15,
                15
            ) * dt

            if bubble.y >= bubble._target_y:

                self.remove_bubble(
                    bubble
                )

    # --------------------------------------------------------
    # REMOVE BUBBLE
    # --------------------------------------------------------

    def remove_bubble(
        self,
        bubble
    ):

        if bubble in self.bubbles:

            self.remove_widget(
                bubble
            )

            self.bubbles.remove(
                bubble
            )

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    def reset(self):

        for bubble in list(
            self.bubbles
        ):

            self.remove_bubble(
                bubble
            )

        self.zinc_remaining = 1.0

        self._update_graphics()

