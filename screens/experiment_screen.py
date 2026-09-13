# ============================================================
# Virtual Chemistry Lab
# screens/experiment_screen.py
# ============================================================

import random

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView

from experiments.zn_hcl import ZnHClExperiment

from widgets.result_card import ResultCard
from widgets.reaction_chamber import ReactionChamber
from widgets.responsive_layout import ResponsiveLayout


# ============================================================
# CONSTANTS
# ============================================================

BREAKPOINT = dp(700)

HEADER_HEIGHT = dp(52)

MOBILE_SIMULATION_HEIGHT = dp(390)
DESKTOP_SIMULATION_HEIGHT = dp(1)
MOBILE_SIMULATION_MIN_HEIGHT = dp(360)
INPUT_HEIGHT = dp(42)
BUTTON_HEIGHT = dp(45)

M_H2 = 2.016


# ============================================================
# EXPERIMENT SCREEN
# ============================================================

class ExperimentScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # ====================================================
        # CHEMISTRY
        # ====================================================

        self.experiment = ZnHClExperiment()

        self.reaction_result = None

        # ====================================================
        # SIMULATION STATE
        # ====================================================

        self.running = False

        self.clock_event = None

        self.reaction_progress = 0.0

        self.speed = 1.0

        # ====================================================
        # CHEMISTRY STATE USED BY ANIMATION
        # ====================================================

        self.n_zn_initial = 0.0
        self.n_hcl_initial = 0.0

        self.n_zn_consumed = 0.0
        self.n_hcl_consumed = 0.0

        self.n_h2 = 0.0

        self.limiting = "--"

        # ====================================================
        # ROOT
        #
        # Không dùng ScrollView ở root.
        #
        # Desktop:
        #
        #   Simulation | ControlsScroll
        #
        # Mobile:
        #
        #   Simulation
        #   -----------
        #   ControlsScroll
        #
        # Điều này giúp chúng ta kiểm soát layout rõ ràng.
        # ====================================================

        self.root_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(4),
            padding=dp(4)
        )

        self.add_widget(
            self.root_layout
        )

        # ====================================================
        # HEADER
        # ====================================================

        self._build_header()

        # ====================================================
        # BODY
        # ====================================================

        self._build_body()

        # ====================================================
        # RESPONSIVE
        # ====================================================

        self.bind(
            size=self._on_resize
        )

        Clock.schedule_once(
            self._update_responsive_layout,
            0
        )

    # ========================================================
    # HEADER
    # ========================================================

    def _build_header(self):

        self.header = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=HEADER_HEIGHT
        )

        # ----------------------------------------------------
        # HOME BUTTON
        # ----------------------------------------------------

        self.home_button = Button(
            text="← Trang chủ",
            size_hint_x=None,
            width=dp(140)
        )

        self.home_button.bind(
            on_release=self.go_home
        )

        self.header.add_widget(
            self.home_button
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.title_label = Label(
            text="THÍ NGHIỆM: Zn + HCl",
            font_size="21sp",
            bold=True,
            halign="center",
            valign="middle"
        )

        self.title_label.bind(
            size=self.title_label.setter(
                "text_size"
            )
        )

        self.header.add_widget(
            self.title_label
        )

        self.root_layout.add_widget(
            self.header
        )

    # ========================================================
    # BODY
    # ========================================================

    def _build_body(self):

        self.main_layout = ResponsiveLayout(
            spacing=dp(10),
            size_hint_y=1
        )

        self.root_layout.add_widget(
            self.main_layout
        )

        # ----------------------------------------------------
        # LEFT / TOP
        # ----------------------------------------------------

        self._build_simulation_panel()

        # ----------------------------------------------------
        # RIGHT / BOTTOM
        # ----------------------------------------------------

        self._build_controls_panel()

    # ========================================================
    # SIMULATION PANEL
    # ========================================================

    def _build_simulation_panel(self):

        self.simulation = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(8),
            size_hint_y=None
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.simulation_title = Label(
            text="MÔ PHỎNG PHẢN ỨNG",
            font_size="19sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(40)
        )

        self.simulation_title.bind(
            size=self.simulation_title.setter(
                "text_size"
            )
        )

        self.simulation.add_widget(
            self.simulation_title
        )

        # ----------------------------------------------------
        # CHAMBER
        # ----------------------------------------------------

        self.chamber = ReactionChamber(
            size_hint_y=1
        )

        self.simulation.add_widget(
            self.chamber
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status = Label(
            text="Sẵn sàng",
            font_size="16sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(40)
        )

        self.status.bind(
            size=self.status.setter(
                "text_size"
            )
        )

        self.simulation.add_widget(
            self.status
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=dp(12)
        )

        self.simulation.add_widget(
            self.progress
        )

        self.main_layout.add_widget(
            self.simulation
        )

    # ========================================================
    # CONTROLS PANEL
    # ========================================================

    def _build_controls_panel(self):

        # ====================================================
        # SCROLL VIEW
        # ====================================================

        self.controls_scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(5),
            scroll_type=["bars", "content"],
            size_hint_y=1
        )

        # ====================================================
        # CONTENT INSIDE SCROLL
        # ====================================================

        self.controls_content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(10),
            size_hint_y=None
        )

        self.controls_content.bind(
            minimum_height=self.controls_content.setter(
                "height"
            )
        )

        self.controls_scroll.add_widget(
            self.controls_content
        )

        self.main_layout.add_widget(
            self.controls_scroll
        )

        # ====================================================
        # BUILD CONTENT
        # ====================================================

        self._build_inputs()

        self._build_buttons()

        self._build_results()

    # ========================================================
    # INPUTS
    # ========================================================

    def _build_inputs(self):

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.input_title = Label(
            text="THÔNG SỐ ĐẦU VÀO",
            font_size="19sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(40)
        )

        self.input_title.bind(
            size=self.input_title.setter(
                "text_size"
            )
        )

        self.controls_content.add_widget(
            self.input_title
        )

        # ----------------------------------------------------
        # ZINC
        # ----------------------------------------------------

        self._add_input(
            "Khối lượng Zn (g)",
            "6.54",
            "zn_input"
        )

        # ----------------------------------------------------
        # HCL CONCENTRATION
        # ----------------------------------------------------

        self._add_input(
            "Nồng độ HCl (mol/L)",
            "1.0",
            "hcl_conc_input"
        )

        # ----------------------------------------------------
        # HCL VOLUME
        # ----------------------------------------------------

        self._add_input(
            "Thể tích HCl (mL)",
            "100",
            "hcl_volume_input"
        )

        # ----------------------------------------------------
        # SPEED
        # ----------------------------------------------------

        self._add_input(
            "Tốc độ mô phỏng",
            "1.0",
            "speed_input"
        )

    # ========================================================
    # ADD INPUT
    # ========================================================

    def _add_input(
        self,
        label_text,
        default_text,
        attribute_name
    ):

        label = Label(
            text=label_text,
            font_size="16sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(30)
        )

        label.bind(
            size=label.setter(
                "text_size"
            )
        )

        self.controls_content.add_widget(
            label
        )

        input_box = TextInput(
            text=default_text,
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=INPUT_HEIGHT
        )

        setattr(
            self,
            attribute_name,
            input_box
        )

        self.controls_content.add_widget(
            input_box
        )

    # ========================================================
    # BUTTONS
    # ========================================================

    def _build_buttons(self):

        self.start_button = Button(
            text="▶ BẮT ĐẦU",
            size_hint_y=None,
            height=BUTTON_HEIGHT
        )

        self.start_button.bind(
            on_release=self.start_experiment
        )

        self.controls_content.add_widget(
            self.start_button
        )

        self.reset_button = Button(
            text="↻ LÀM LẠI",
            size_hint_y=None,
            height=BUTTON_HEIGHT
        )

        self.reset_button.bind(
            on_release=self.reset
        )

        self.controls_content.add_widget(
            self.reset_button
        )

    # ========================================================
    # RESULTS
    # ========================================================

    def _build_results(self):

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.result_title = Label(
            text="KẾT QUẢ",
            font_size="19sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(40)
        )

        self.result_title.bind(
            size=self.result_title.setter(
                "text_size"
            )
        )

        self.controls_content.add_widget(
            self.result_title
        )

        # ----------------------------------------------------
        # GRID
        # ----------------------------------------------------

        self.result_grid = GridLayout(
            cols=2,
            spacing=dp(7),
            padding=dp(2),
            size_hint_y=None
        )

        self.result_grid.bind(
            minimum_height=self.result_grid.setter(
                "height"
            )
        )

        self.controls_content.add_widget(
            self.result_grid
        )

        # ----------------------------------------------------
        # CARDS
        # ----------------------------------------------------

        self.zn_result = ResultCard(
            "n(Zn)",
            "--",
            "mol"
        )

        self.hcl_result = ResultCard(
            "n(HCl)",
            "--",
            "mol"
        )

        self.limiting_result = ResultCard(
            "Chất giới hạn",
            "--"
        )

        self.h2_result = ResultCard(
            "n(H₂)",
            "--",
            "mol"
        )

        self.h2_mass_result = ResultCard(
            "m(H₂)",
            "--",
            "g"
        )

        self.zn_remaining_result = ResultCard(
            "Zn còn lại",
            "--",
            "mol"
        )

        self.hcl_remaining_result = ResultCard(
            "HCl còn lại",
            "--",
            "mol"
        )

        self.result_cards = [
            self.zn_result,
            self.hcl_result,
            self.limiting_result,
            self.h2_result,
            self.h2_mass_result,
            self.zn_remaining_result,
            self.hcl_remaining_result
        ]

        for card in self.result_cards:

            self.result_grid.add_widget(
                card
            )

    # ========================================================
    # RESPONSIVE
    # ========================================================

    def _on_resize(
        self,
        *args
    ):

        Clock.unschedule(
            self._update_responsive_layout
        )

        Clock.schedule_once(
            self._update_responsive_layout,
            0
        )

    # ========================================================
    # UPDATE RESPONSIVE
    # ========================================================

    def _update_responsive_layout(
        self,
        *args
    ):

        if self.width <= 0:
            return

        # ====================================================
        # DESKTOP / LANDSCAPE
        # ====================================================

        if self.width >= BREAKPOINT:

            self._desktop_layout()

        # ====================================================
        # MOBILE / PORTRAIT
        # ====================================================

        else:

            self._mobile_layout()

    def _reset_mobile_scroll(self, *args):

        if self.width < BREAKPOINT:

            self.controls_scroll.scroll_y = 1
    # ========================================================
    # DESKTOP LAYOUT
    # ========================================================

    def _desktop_layout(self):

        # ----------------------------------------------------
        # MAIN
        # ----------------------------------------------------

        self.main_layout.orientation = (
            "horizontal"
        )

        # ----------------------------------------------------
        # SIMULATION
        # ----------------------------------------------------

        self.simulation.size_hint_x = 0.58
        self.simulation.size_hint_y = 1

        # ----------------------------------------------------
        # CONTROLS
        # ----------------------------------------------------

        self.controls_scroll.size_hint_x = 0.42
        self.controls_scroll.size_hint_y = 1

        # ----------------------------------------------------
        # CHAMBER
        # ----------------------------------------------------

        self.chamber.size_hint_y = None
        self.chamber.height = dp(270)

        # ----------------------------------------------------
        # RESULT GRID
        # ----------------------------------------------------

        self.result_grid.cols = 2

        # ----------------------------------------------------
        # FONT
        # ----------------------------------------------------

        self.title_label.font_size = "21sp"

        self.simulation_title.font_size = "19sp"

        self.input_title.font_size = "19sp"

        self.result_title.font_size = "19sp"

    # ========================================================
    # MOBILE LAYOUT
    # ========================================================

    def _mobile_layout(self):

        # ========================================================
        # MOBILE / PORTRAIT
        # ========================================================

        # --------------------------------------------------------
        # MAIN LAYOUT
        # --------------------------------------------------------

        self.main_layout.orientation = "vertical"

        # --------------------------------------------------------
        # SIMULATION
        # --------------------------------------------------------

        self.simulation.size_hint_x = 1
        self.simulation.size_hint_y = None

        # Gọn hơn desktop rất nhiều.
        self.simulation.height = MOBILE_SIMULATION_HEIGHT

        # --------------------------------------------------------
        # CONTROLS
        # --------------------------------------------------------

        self.controls_scroll.size_hint_x = 1
        self.controls_scroll.size_hint_y = 1

        # --------------------------------------------------------
        # RESULT CARDS
        # --------------------------------------------------------

        # Trên điện thoại dùng 1 cột.
        self.result_grid.cols = 1

        # --------------------------------------------------------
        # FONT
        # --------------------------------------------------------

        self.title_label.font_size = "17sp"

        self.simulation_title.font_size = "18sp"

        self.input_title.font_size = "18sp"

        self.result_title.font_size = "18sp"

        # --------------------------------------------------------
        # HOME BUTTON
        # --------------------------------------------------------

        self.home_button.width = dp(120)

        # --------------------------------------------------------
        # RESET SCROLL POSITION
        # --------------------------------------------------------

        # Khi chuyển từ landscape -> portrait,
        # ScrollView có thể đang giữ vị trí cuối.
        #
        # Đưa nó về đầu để người dùng luôn thấy:
        #
        # THÔNG SỐ ĐẦU VÀO
        #
        # trước.

        Clock.schedule_once(
            self._reset_mobile_scroll,
            0
        )

    # ========================================================
    # START EXPERIMENT
    # ========================================================

    def start_experiment(
        self,
        instance
    ):

        if self.running:
            return

        self.stop_clock()

        # ----------------------------------------------------
        # READ INPUT
        # ----------------------------------------------------

        try:

            zn_mass = float(
                self.zn_input.text
            )

            hcl_conc = float(
                self.hcl_conc_input.text
            )

            hcl_volume = float(
                self.hcl_volume_input.text
            )

            speed = float(
                self.speed_input.text
            )

        except ValueError:

            self.status.text = (
                "⚠ Vui lòng nhập số hợp lệ"
            )

            return

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if (
            zn_mass <= 0
            or hcl_conc <= 0
            or hcl_volume <= 0
            or speed <= 0
        ):

            self.status.text = (
                "⚠ Các giá trị phải lớn hơn 0"
            )

            return

        # ----------------------------------------------------
        # CALCULATE
        # ----------------------------------------------------

        try:

            self.reaction_result = (
                self.experiment.calculate(
                    {
                        "zn_mass": zn_mass,
                        "hcl_concentration": hcl_conc,
                        "hcl_volume": hcl_volume
                    }
                )
            )

        except Exception as error:

            self.status.text = (
                f"⚠ Lỗi tính toán: {error}"
            )

            return

        result = self.reaction_result

        # ----------------------------------------------------
        # CACHE DATA
        # ----------------------------------------------------

        self.n_zn_initial = (
            result.initial_moles["Zn"]
        )

        self.n_hcl_initial = (
            result.initial_moles["HCl"]
        )

        self.n_zn_consumed = (
            result.consumed_moles["Zn"]
        )

        self.n_hcl_consumed = (
            result.consumed_moles["HCl"]
        )

        self.n_h2 = (
            result.product_moles["H2"]
        )

        self.limiting = (
            result.limiting_reagent
            if result.limiting_reagent
            else "Vừa đủ"
        )

        self.speed = speed

        # ----------------------------------------------------
        # UPDATE RESULTS
        # ----------------------------------------------------

        self.update_results()

        # ----------------------------------------------------
        # RESET SIMULATION
        # ----------------------------------------------------

        self.reaction_progress = 0

        self.progress.value = 0

        self.chamber.reset()

        self.running = True

        self.start_button.disabled = True

        self.status.text = (
            "Zn bắt đầu phản ứng với HCl..."
        )

        # ----------------------------------------------------
        # START CLOCK
        # ----------------------------------------------------

        self.clock_event = Clock.schedule_interval(
            self.update_simulation,
            0.05
        )

    # ========================================================
    # UPDATE RESULTS
    # ========================================================

    def update_results(self):

        if self.reaction_result is None:
            return

        result = self.reaction_result

        # ----------------------------------------------------
        # INITIAL Zn
        # ----------------------------------------------------

        self.zn_result.set_value(
            f"{result.initial_moles['Zn']:.4f}",
            "mol"
        )

        # ----------------------------------------------------
        # INITIAL HCl
        # ----------------------------------------------------

        self.hcl_result.set_value(
            f"{result.initial_moles['HCl']:.4f}",
            "mol"
        )

        # ----------------------------------------------------
        # LIMITING
        # ----------------------------------------------------

        limiting = (
            result.limiting_reagent
            if result.limiting_reagent
            else "Vừa đủ"
        )

        self.limiting_result.set_value(
            limiting
        )

        # ----------------------------------------------------
        # H2
        # ----------------------------------------------------

        h2 = result.product_moles["H2"]

        self.h2_result.set_value(
            f"{h2:.4f}",
            "mol"
        )

        # ----------------------------------------------------
        # H2 MASS
        # ----------------------------------------------------

        self.h2_mass_result.set_value(
            f"{h2 * M_H2:.4f}",
            "g"
        )

        # ----------------------------------------------------
        # Zn REMAINING
        # ----------------------------------------------------

        self.zn_remaining_result.set_value(
            f"{result.remaining_moles['Zn']:.4f}",
            "mol"
        )

        # ----------------------------------------------------
        # HCl REMAINING
        # ----------------------------------------------------

        self.hcl_remaining_result.set_value(
            f"{result.remaining_moles['HCl']:.4f}",
            "mol"
        )

    # ========================================================
    # SIMULATION UPDATE
    # ========================================================

    def update_simulation(
        self,
        dt
    ):

        if not self.running:
            return False

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        self.reaction_progress += (
            0.8 * self.speed
        )

        progress = min(
            100,
            self.reaction_progress
        )

        self.progress.value = progress

        fraction = progress / 100.0

        # ----------------------------------------------------
        # ZINC REMAINING
        # ----------------------------------------------------

        if self.n_zn_initial > 0:

            consumed_fraction = (
                self.n_zn_consumed
                / self.n_zn_initial
            )

        else:

            consumed_fraction = 0

        zinc_fraction = (
            1
            - fraction * consumed_fraction
        )

        zinc_fraction = max(
            0,
            min(
                1,
                zinc_fraction
            )
        )

        self.chamber.set_zinc_remaining(
            zinc_fraction
        )

        # ----------------------------------------------------
        # BUBBLES
        # ----------------------------------------------------

        bubble_probability = min(
            0.8,
            0.25 * self.speed
        )

        if random.random() < bubble_probability:

            self.chamber.create_bubble()

        self.chamber.update_bubbles(
            dt
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if progress < 15:

            self.status.text = (
                "Zn tiếp xúc với dung dịch HCl..."
            )

        elif progress < 50:

            self.status.text = (
                "💨 Đang sinh khí H₂..."
            )

        elif progress < 85:

            self.status.text = (
                "💨 Phản ứng đang diễn ra..."
            )

        else:

            self.status.text = (
                "Phản ứng gần hoàn thành..."
            )

        # ----------------------------------------------------
        # FINISH
        # ----------------------------------------------------

        if progress >= 100:

            self.finish_experiment()

            return False

        return True

    # ========================================================
    # FINISH
    # ========================================================

    def finish_experiment(self):

        self.running = False

        self.stop_clock()

        self.progress.value = 100

        self.start_button.disabled = False

        # ----------------------------------------------------
        # FINAL Zn
        # ----------------------------------------------------

        if self.n_zn_initial > 0:

            final_fraction = max(
                0,
                1
                - (
                    self.n_zn_consumed
                    / self.n_zn_initial
                )
            )

        else:

            final_fraction = 0

        self.chamber.set_zinc_remaining(
            final_fraction
        )

        self.status.text = (
            "✓ Phản ứng hoàn thành"
        )

    # ========================================================
    # STOP CLOCK
    # ========================================================

    def stop_clock(self):

        if self.clock_event is not None:

            self.clock_event.cancel()

            self.clock_event = None

    # ========================================================
    # RESET
    # ========================================================

    def reset(
        self,
        instance=None
    ):

        self.running = False

        self.stop_clock()

        # ----------------------------------------------------
        # CHEMISTRY
        # ----------------------------------------------------

        self.reaction_result = None

        self.n_zn_initial = 0
        self.n_hcl_initial = 0

        self.n_zn_consumed = 0
        self.n_hcl_consumed = 0

        self.n_h2 = 0

        self.limiting = "--"

        # ----------------------------------------------------
        # SIMULATION
        # ----------------------------------------------------

        self.reaction_progress = 0

        self.progress.value = 0

        self.chamber.reset()

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        self.status.text = "Sẵn sàng"

        self.start_button.disabled = False

        # ----------------------------------------------------
        # RESULT CARDS
        # ----------------------------------------------------

        self.zn_result.set_value(
            "--",
            "mol"
        )

        self.hcl_result.set_value(
            "--",
            "mol"
        )

        self.limiting_result.set_value(
            "--"
        )

        self.h2_result.set_value(
            "--",
            "mol"
        )

        self.h2_mass_result.set_value(
            "--",
            "g"
        )

        self.zn_remaining_result.set_value(
            "--",
            "mol"
        )

        self.hcl_remaining_result.set_value(
            "--",
            "mol"
        )

    # ========================================================
    # GO HOME
    # ========================================================

    def go_home(
        self,
        instance
    ):

        self.reset()

        if self.manager:

            self.manager.current = "home"

    # ========================================================
    # LEAVE SCREEN
    # ========================================================

    def on_leave(
        self,
        *args
    ):

        self.running = False

        self.stop_clock()