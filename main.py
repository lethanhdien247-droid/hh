from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.home_screen import HomeScreen
from screens.experiment_screen import ExperimentScreen


class ChemistryLabApp(App):

    def build(self):

        self.title = "Virtual Chemistry Lab"

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(
                name="home"
            )
        )

        manager.add_widget(
            ExperimentScreen(
                name="experiment"
            )
        )

        return manager


if __name__ == "__main__":

    ChemistryLabApp().run()