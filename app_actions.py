from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.graphics.texture import Texture


class AppActions:
    def __init__(self, user_app_instance, handler_instance) -> None:
        self.user_app = user_app_instance
        self.handler = handler_instance

        import os
        self.checkbox_store = JsonStore(os.path.abspath("checkbox_states.json"))

    def start_live_broadcast(self, source):
        if self.handler.init_cap(source, name="live") is False:
            self.pop_up(
                header="Camera Error",
                message="Unable to access the camera. "
                "Please check if the camera is not being used by "
                "another application or the camera index is correct."
            )
            return

        def update_live(dt):
            if self.handler.cap_check(name="live"):
                frame = self.handler.refresh_cap(name="live")
                self.user_app.root.ids.live_frame.texture = \
                    self.to_texture(frame)

        self.update_live_event = Clock.schedule_interval(
            update_live, 1.0 / self.handler.get_fps(name="live"))

    def stop_live_broadcast(self):
        if hasattr(self, "update_live_event"):
            Clock.unschedule(self.update_live_event)
        self.handler.cap_del(name="live")

    def static_display(self, format):
        if hasattr(self, "update_static_event"):
            Clock.unschedule(self.update_static_event)

        def update_static(dt):
            frame = self.handler.get_video(type="media_output")
            self.user_app.root.ids.static_frame.texture = \
                self.to_texture(frame)

        if format == "image":
            frame = self.handler.get_image(type="media_output")
            self.user_app.root.ids.static_frame.texture = \
                self.to_texture(frame)

        elif format == "video":
            self.update_static_event = Clock.schedule_interval(
                update_static, 1.0 / self.handler.get_fps(
                    name="media_output"))

    def to_texture(self, frame):
        if frame is None:
            return None

        frame = self.handler.frame_flip(frame)

        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(
            frame.tobytes(), colorfmt="bgr", bufferfmt="ubyte")
        return texture

    def pop_up(self, header, message):
        dialog = MDDialog(
            title=f"{header}",
            text=f"{message}",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda *x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    # TODO - more stable alignment
    def aruco_choose(self):
        checkbox_dictionaries = [
            ("DICT_4X4_1000"),
            ("DICT_5X5_1000"),
            ("DICT_6X6_1000"),
            ("DICT_7X7_1000"),
            ("DICT_ARUCO_ORIGINAL"),
            ("DICT_APRILTAG_16h5"),
            ("DICT_APRILTAG_25h9"),
            ("DICT_APRILTAG_36h10"),
            ("DICT_APRILTAG_36h11")
        ]

        dictionaries_for_shipment = []

        def handle_checkbox(dictionary):
            if dictionary in dictionaries_for_shipment:
                dictionaries_for_shipment.remove(dictionary)
                self.checkbox_store.put(dictionary, state=False)
            else:
                dictionaries_for_shipment.append(dictionary)
                self.checkbox_store.put(dictionary, state=True)

        dialog_layout = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            size=(400, 240),
            spacing=24,
        )

        text_label = Label(
            text="Please note: Choosing multiple dictionaries impacts performance.",
            color=(0, 0, 0, 1),
            size_hint=(.87, .87),
        )

        dialog_layout.add_widget(text_label)

        for dictionary in checkbox_dictionaries:
            checkbox_layout = MDBoxLayout(
                orientation="horizontal",
                size_hint=(.3, 1),
                spacing=108,
            )

            # TODO - Issue: Currently you have to aim for the very center of
            # the checkbox
            checkbox = MDCheckbox(
                on_release=lambda *x,
                to_send=dictionary: handle_checkbox(
                    dictionary=to_send)
            )

            try:
                if self.checkbox_store.get(dictionary)["state"] is True:
                    dictionaries_for_shipment.append(dictionary)
                    checkbox.active = True
                else:
                    checkbox.active = False
            except KeyError:
                checkbox.active = False

            checkbox_label = Label(

                text=dictionary,
                color=(0, 0, 0, 1),
            )

            checkbox_layout.add_widget(checkbox)
            checkbox_layout.add_widget(checkbox_label)

            dialog_layout.add_widget(checkbox_layout)

        def on_checkboxes_ok():
            dialog.dismiss()
            self.handler.transfer_aruco_dictionaries(dictionaries_for_shipment)
            self.handler.refresh_media_output()
            self.user_app.update_static_screen()

        def on_checkboxes_cancel():
            dialog.dismiss()

        dialog = MDDialog(
            title="Choose ArUco Dictionaries for Detection",
            type="custom",
            content_cls=dialog_layout,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda *x: on_checkboxes_ok()),
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda *x: on_checkboxes_cancel())]
        )
        dialog.open()

    def app_fps(self):
        # To showcase app performance
        def update_fps(dt):
            fps = Clock.get_fps()
            print(f"Current FPS: {fps}")

        Clock.schedule_interval(update_fps, 1)
