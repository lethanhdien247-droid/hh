# ============================================================
# HOME SCREEN
# screens/home_screen.py
# ============================================================

import unicodedata

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from widgets.experiment_card import ExperimentCard
from services.experiment_service import ExperimentService


class HomeScreen(Screen):
    """Màn hình thư viện thí nghiệm của VCL."""

    MOBILE_BREAKPOINT = dp(500)
    TABLET_BREAKPOINT = dp(850)

    MOBILE_PADDING = dp(8)
    TABLET_PADDING = dp(10)
    DESKTOP_PADDING = dp(14)

    MOBILE_SPACING = dp(7)
    TABLET_SPACING = dp(9)
    DESKTOP_SPACING = dp(11)

    MOBILE_HEADER_HEIGHT = dp(92)
    TABLET_HEADER_HEIGHT = dp(105)
    DESKTOP_HEADER_HEIGHT = dp(120)

    SEARCH_HEIGHT = dp(42)
    CATEGORY_HEIGHT = dp(45)
    CATEGORY_BUTTON_WIDTH = dp(125)

    CARD_HEIGHT = dp(220)
    CARD_SPACING = dp(10)
    CARD_PADDING = dp(4)

    EXPERIMENT_ROUTES = {
        "zn_hcl": "experiment",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # HomeScreen chỉ biết Service, không biết Registry.
        self.service = ExperimentService()
        self.experiments = self.service.get_all_experiments()
        self.current_category = "Tất cả"

        self._build_ui()

        self.bind(
            width=self._on_screen_resize,
            height=self._on_screen_resize,
        )

        Clock.schedule_once(self._update_layout, 0)

    def _build_ui(self):
        self.root_layout = BoxLayout(
            orientation="vertical",
            spacing=self.DESKTOP_SPACING,
            padding=self.DESKTOP_PADDING,
        )
        self.add_widget(self.root_layout)

        self.header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=self.DESKTOP_HEADER_HEIGHT,
            spacing=dp(3),
        )
        self.root_layout.add_widget(self.header)

        self.title_label = Label(
            text="VIRTUAL CHEMISTRY LAB",
            font_size="30sp",
            bold=True,
            halign="center",
            valign="middle",
        )
        self.title_label.bind(size=self._update_text_size)
        self.header.add_widget(self.title_label)

        self.subtitle_label = Label(
            text="Thư viện thí nghiệm hóa học",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(35),
        )
        self.subtitle_label.bind(size=self._update_text_size)
        self.header.add_widget(self.subtitle_label)

        self.search = TextInput(
            hint_text="Tìm kiếm thí nghiệm...",
            multiline=False,
            size_hint_y=None,
            height=self.SEARCH_HEIGHT,
            padding=[dp(12), dp(10)],
        )
        self.search.bind(text=self._on_search)
        self.root_layout.add_widget(self.search)

        self.category_scroll = ScrollView(
            size_hint_y=None,
            height=self.CATEGORY_HEIGHT,
            do_scroll_x=True,
            do_scroll_y=False,
            bar_width=dp(4),
        )
        self.category_layout = BoxLayout(
            orientation="horizontal",
            size_hint_x=None,
            spacing=dp(6),
        )
        self.category_layout.bind(
            minimum_width=self.category_layout.setter("width")
        )
        self.category_scroll.add_widget(self.category_layout)
        self.root_layout.add_widget(self.category_scroll)

        self.experiment_scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(6),
        )
        self.experiment_grid = GridLayout(
            cols=3,
            spacing=self.CARD_SPACING,
            padding=self.CARD_PADDING,
            size_hint_y=None,
        )
        self.experiment_grid.bind(
            minimum_height=self.experiment_grid.setter("height")
        )
        self.experiment_scroll.add_widget(self.experiment_grid)
        self.root_layout.add_widget(self.experiment_scroll)

        self._build_categories()
        self._refresh_experiments()

    @staticmethod
    def _update_text_size(instance, value):
        instance.text_size = value

    @staticmethod
    def _normalize_text(text):
        text = str(text).lower().strip()
        normalized = unicodedata.normalize("NFD", text)
        return "".join(
            char for char in normalized
            if unicodedata.category(char) != "Mn"
        )

    def _get_categories(self):
        return ["Tất cả", *sorted(self.service.get_categories())]

    def _build_categories(self):
        self.category_layout.clear_widgets()

        for category in self._get_categories():
            button = Button(
                text=category,
                size_hint_x=None,
                width=self.CATEGORY_BUTTON_WIDTH,
            )
            button.bind(
                on_release=lambda instance, selected_category=category:
                self._select_category(selected_category)
            )
            self.category_layout.add_widget(button)

    def _select_category(self, category):
        if category == self.current_category:
            return

        self.current_category = category
        self._refresh_experiments()
        self.experiment_scroll.scroll_y = 1

    def _on_search(self, instance, text):
        self._refresh_experiments()

    def _refresh_experiments(self):
        self.experiment_grid.clear_widgets()

        search_text = self.search.text.strip()

        if self.current_category == "Tất cả":
            experiments = self.service.get_all_experiments()
        else:
            experiments = self.service.filter_by_category(
                self.current_category
            )

        if search_text:
            search_results = self.service.search_experiments(search_text)
            search_ids = {experiment.id for experiment in search_results}
            experiments = [
                experiment for experiment in experiments
                if experiment.id in search_ids
            ]

        self.experiments = list(experiments)

        for experiment in self.experiments:
            self._add_experiment_card(experiment)

    def _add_experiment_card(self, experiment):
        info = experiment.get_info()

        card = ExperimentCard(
            experiment_id=info["id"],
            experiment_name=info["name"],
            description=info["description"],
            equation=info["equation"],
            category=info["category"],
            available=info["available"],
            on_open=self._open_experiment,
        )
        card.height = self.CARD_HEIGHT
        self.experiment_grid.add_widget(card)

    def _open_experiment(self, experiment_id):
        if not experiment_id or self.manager is None:
            return

        screen_name = self.EXPERIMENT_ROUTES.get(experiment_id)
        if screen_name is None:
            return

        self.manager.current = screen_name

    def _on_screen_resize(self, *args):
        self._update_layout()

    def _update_layout(self, *args):
        width = self.width
        if width <= 0:
            return

        if width < self.MOBILE_BREAKPOINT:
            self._apply_mobile_layout()
        elif width < self.TABLET_BREAKPOINT:
            self._apply_tablet_layout()
        else:
            self._apply_desktop_layout()

    def _apply_mobile_layout(self):
        self.root_layout.padding = self.MOBILE_PADDING
        self.root_layout.spacing = self.MOBILE_SPACING
        self.header.height = self.MOBILE_HEADER_HEIGHT
        self.title_label.font_size = "21sp"
        self.subtitle_label.font_size = "15sp"
        self.experiment_grid.cols = 1
        self.experiment_grid.spacing = dp(10)
        self.experiment_grid.padding = dp(4)

    def _apply_tablet_layout(self):
        self.root_layout.padding = self.TABLET_PADDING
        self.root_layout.spacing = self.TABLET_SPACING
        self.header.height = self.TABLET_HEADER_HEIGHT
        self.title_label.font_size = "25sp"
        self.subtitle_label.font_size = "16sp"
        self.experiment_grid.cols = 2
        self.experiment_grid.spacing = dp(10)
        self.experiment_grid.padding = dp(4)

    def _apply_desktop_layout(self):
        self.root_layout.padding = self.DESKTOP_PADDING
        self.root_layout.spacing = self.DESKTOP_SPACING
        self.header.height = self.DESKTOP_HEADER_HEIGHT
        self.title_label.font_size = "30sp"
        self.subtitle_label.font_size = "18sp"
        self.experiment_grid.cols = 3
        self.experiment_grid.spacing = dp(10)
        self.experiment_grid.padding = dp(4)