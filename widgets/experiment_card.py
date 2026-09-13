# ============================================================
# EXPERIMENT CARD
# widgets/experiment_card.py
# ============================================================

from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ObjectProperty,
)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class ExperimentCard(BoxLayout):
    """
    Card hiển thị thông tin của một thí nghiệm.

    ExperimentCard chỉ phụ trách UI.

    Không chứa:
        - Chemistry Engine
        - phép tính hóa học
        - logic phản ứng
        - ScreenManager

    Khi người dùng nhấn:
        "MỞ THÍ NGHIỆM"

    Card gửi experiment_id về HomeScreen.
    """

    # ========================================================
    # DATA
    # ========================================================

    experiment_id = StringProperty("")

    experiment_name = StringProperty("")

    description = StringProperty("")

    equation = StringProperty("")

    category = StringProperty("")

    available = BooleanProperty(False)

    on_open = ObjectProperty(
        None,
        allownone=True
    )

    # ========================================================
    # CONSTANTS
    # ========================================================

    CARD_HEIGHT = dp(220)

    CARD_PADDING = dp(14)

    CARD_SPACING = dp(7)

    TITLE_HEIGHT = dp(32)

    CATEGORY_HEIGHT = dp(22)

    DESCRIPTION_HEIGHT = dp(38)

    EQUATION_HEIGHT = dp(30)

    BUTTON_HEIGHT = dp(40)

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        experiment_id="",
        experiment_name="",
        description="",
        equation="",
        category="",
        available=False,
        on_open=None,
        **kwargs
    ):

        super().__init__(**kwargs)

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        self.experiment_id = experiment_id

        self.experiment_name = experiment_name

        self.description = description

        self.equation = equation

        self.category = category

        self.available = available

        self.on_open = on_open

        # ----------------------------------------------------
        # CARD LAYOUT
        # ----------------------------------------------------

        self.orientation = "vertical"

        self.padding = self.CARD_PADDING

        self.spacing = self.CARD_SPACING

        self.size_hint_y = None

        self.height = self.CARD_HEIGHT

        # ====================================================
        # TITLE
        # ====================================================

        self.title_label = Label(
            text=self.experiment_name,
            font_size="18sp",
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=self.TITLE_HEIGHT,
        )

        self.title_label.bind(
            size=self._update_text_size
        )

        self.add_widget(
            self.title_label
        )

        # ====================================================
        # CATEGORY
        # ====================================================

        self.category_label = Label(
            text=self.category,
            font_size="13sp",
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=self.CATEGORY_HEIGHT,
        )

        self.category_label.bind(
            size=self._update_text_size
        )

        self.add_widget(
            self.category_label
        )

        # ====================================================
        # DESCRIPTION
        # ====================================================

        self.description_label = Label(
            text=self.description,
            font_size="14sp",
            halign="left",
            valign="top",
            size_hint_y=None,
            height=self.DESCRIPTION_HEIGHT,
        )

        self.description_label.bind(
            size=self._update_text_size
        )

        self.add_widget(
            self.description_label
        )

        # ====================================================
        # EQUATION
        # ====================================================

        self.equation_label = Label(
            text=self._safe_equation(
                self.equation
            ),
            font_size="14sp",
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=self.EQUATION_HEIGHT,
        )

        self.equation_label.bind(
            size=self._update_text_size
        )

        self.add_widget(
            self.equation_label
        )

        # ====================================================
        # BUTTON
        # ====================================================

        self.open_button = Button(
            text=(
                "MỞ THÍ NGHIỆM"
                if self.available
                else "ĐANG PHÁT TRIỂN"
            ),

            size_hint_y=None,

            height=self.BUTTON_HEIGHT,

            disabled=not self.available,
        )

        self.open_button.bind(
            on_release=self._open_experiment
        )

        self.add_widget(
            self.open_button
        )

    # ========================================================
    # EQUATION
    # ========================================================

    @staticmethod
    def _safe_equation(equation):
        """
        Chuẩn hóa phương trình để tránh lỗi hiển thị
        trên các font không hỗ trợ đầy đủ Unicode.

        Giữ nguyên phương trình chuẩn trong Reaction object.
        Chỉ thay đổi chuỗi dùng cho UI.
        """

        if not equation:
            return ""

        equation = str(equation)

        # Các ký tự subscript
        equation = equation.replace(
            "₀", "0"
        )
        equation = equation.replace(
            "₁", "1"
        )
        equation = equation.replace(
            "₂", "2"
        )
        equation = equation.replace(
            "₃", "3"
        )
        equation = equation.replace(
            "₄", "4"
        )
        equation = equation.replace(
            "₅", "5"
        )
        equation = equation.replace(
            "₆", "6"
        )
        equation = equation.replace(
            "₇", "7"
        )
        equation = equation.replace(
            "₈", "8"
        )
        equation = equation.replace(
            "₉", "9"
        )

        # Một số ký tự có thể không được font mặc định hỗ trợ
        equation = equation.replace(
            "→", "->"
        )

        equation = equation.replace(
            "↑", ""
        )

        return equation

    # ========================================================
    # TEXT
    # ========================================================

    @staticmethod
    def _update_text_size(
        instance,
        value
    ):
        """
        Cho phép Label wrap text theo kích thước.
        """

        instance.text_size = value

    # ========================================================
    # CALLBACK
    # ========================================================

    def _open_experiment(
        self,
        *args
    ):
        """
        Gửi experiment_id về HomeScreen.

        Card không biết:
            - ScreenManager
            - ExperimentScreen
            - Chemistry Engine
            - Zn + HCl
        """

        if not self.available:
            return

        if not self.experiment_id:
            return

        if callable(self.on_open):

            self.on_open(
                self.experiment_id
            )