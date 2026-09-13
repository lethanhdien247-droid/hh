from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
class ResultCard(BoxLayout):

    def __init__(
        self,
        title,
        value="--",
        unit="",
        **kwargs
    ):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        self.padding = (
            dp(8),
            dp(4)
        )

        self.spacing = dp(2)

        self.size_hint_y = None
        self.height = dp(65)

        with self.canvas.before:

            Color(
                0.10,
                0.13,
                0.18,
                1
            )

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )

        self.bind(
            pos=self._update_background,
            size=self._update_background
        )

        self.title_label = Label(
            text=title,
            font_size="13sp",
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(23)
        )

        self.title_label.bind(
            size=self.title_label.setter(
                "text_size"
            )
        )

        self.add_widget(
            self.title_label
        )

        self.value_label = Label(
            text=self._format(
                value,
                unit
            ),
            font_size="17sp",
            bold=True,
            color=(
                0.4,
                0.85,
                1,
                1
            ),
            halign="left",
            valign="middle"
        )

        self.value_label.bind(
            size=self.value_label.setter(
                "text_size"
            )
        )

        self.add_widget(
            self.value_label
        )

    def _format(
        self,
        value,
        unit
    ):

        if unit:
            return f"{value} {unit}"

        return str(value)

    def set_value(
        self,
        value,
        unit=""
    ):

        self.value_label.text = self._format(
            value,
            unit
        )

    def _update_background(
        self,
        *args
    ):

        self.background.pos = self.pos
        self.background.size = self.size

