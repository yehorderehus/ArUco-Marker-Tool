from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty

from handler import Handler
from app_actions import AppActions
from app_helper import app_helper


class UserApp(MDApp):
    def __init__(self) -> None:
        super().__init__()

        self.handler = Handler()
        self.app_actions = AppActions(
            user_app_instance=self,
            handler_instance=self.handler
        )

        self.live_source = 0  # Default OpenCV camera index

    def build(self):
        self.title = "ArUco Marker Tool"
        return Builder.load_string(app_helper)

    def on_start(self):
        self.app_actions.app_fps()  # App performance
        self.app_actions.start_live_broadcast(self.live_source)
        self.app_actions.aruco_choose()

    def change_screen_callback(self, current_screen):
        if current_screen != "live":
            self.app_actions.stop_live_broadcast()

        elif current_screen == "live":
            self.app_actions.start_live_broadcast(self.live_source)

    def file_select_callback(self, type):
        if self.handler.select_file(type) is False:
            self.app_actions.pop_up(
                header="File Error", message="Unable to access the file. "
                "Please check if the file exists and the file extension is correct.")
            return

        self.update_static_screen()

    # Update the static screen based on
    # the_media_output instance (image or video)
    def update_static_screen(self):
        format = self.handler.get_format()
        if format:
            self.app_actions.static_display(format)

    def aruco_choose_callback(self):
        self.app_actions.aruco_choose()

    def cam_flip_callback(self):
        # Camera index (live source) ranges from 0 to 1
        self.live_source = self.handler.cam_flip(self.live_source)
        self.app_actions.start_live_broadcast(self.live_source)

    def cam_screenshot_callback(self):
        if self.handler.capture_frame() is False:
            self.app_actions.pop_up(
                header="Screenshot Error",
                message="Unable to take a screenshot. "
                "Please check if the media output or live broadcast is active.")

    def open_url_callback(self, url):
        import webbrowser
        webbrowser.open(url)


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


if __name__ == "__main__":
    UserApp().run()
