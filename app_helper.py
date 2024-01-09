# Purpose: General layout of the app
app_helper = """
<ContentNavigationDrawer>:
    MDList:
        spacing: "12dp"
        OneLineListItem:
            text: "Live Replacement"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "live"
                app.change_screen_callback("live")
        OneLineListItem:
            text: "Replace on Media"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "static"
                app.change_screen_callback("static")
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: self.minimum_height
            OneLineListItem:
                text: "GitHub"
                divider: None
                theme_text_color: "Secondary"
                on_press:
                    root.nav_drawer.set_state("close")
                    app.open_url_callback("https://github.com/yehorderehus/ArUco-Marker-Tool")
            OneLineListItem:
                text: "Rate App"
                divider: None
                theme_text_color: "Secondary"
                on_press:
                    root.nav_drawer.set_state("close")
                    app.open_url_callback("https://github.com/yehorderehus/ArUco-Marker-Tool/issues/new?assignees=&labels=positive-feedback&template=positive-feedback.md&title=%5BLeave-feedback-or-suggestion%5D")

MDScreen:
    MDNavigationLayout:
        MDScreenManager:
            id: screen_manager
            MDScreen:
                name: "live"
                Image:
                    id: live_frame
                    allow_stretch: True
                MDIconButton:
                    icon: "menu"
                    pos_hint: {"top": 1}
                    on_release: nav_drawer.set_state("open")
                MDIconButton:
                    icon: "qrcode"
                    pos_hint: {"top": 1, "right": 1}
                    on_release: app.aruco_choose_callback()
                MDIconButton:
                    icon: "cube-outline"
                    pos_hint: {"bottom": 1}
                    on_release: app.file_select_callback("asset")
                MDIconButton:
                    icon: "record"
                    pos_hint: {"bottom": 1, "center_x": .5}
                    on_release: app.cam_screenshot_callback()
                MDIconButton:
                    icon: "rotate-3d-variant"
                    pos_hint: {"bottom": 1, "right": 1}
                    on_release: app.cam_flip_callback()
            MDScreen:
                name: "static"
                Image:
                    id: static_frame
                    allow_stretch: True
                MDIconButton:
                    icon: "menu"
                    pos_hint: {"top": 1}
                    on_release: nav_drawer.set_state()
                MDIconButton:
                    icon: "qrcode"
                    pos_hint: {"top": 1, "right": 1}
                    on_release: app.aruco_choose_callback()
                MDIconButton:
                    icon: "cube-outline"
                    pos_hint: {"bottom": 1}
                    on_release: app.file_select_callback("asset")
                MDIconButton:
                    icon: "record"
                    pos_hint: {"bottom": 1, "center_x": .5}
                    on_release: app.cam_screenshot_callback()
                MDIconButton:
                    icon: "file-image-plus"
                    pos_hint: {"bottom": 1, "right": 1}
                    on_release: app.file_select_callback("media")
        MDNavigationDrawer:
            id: nav_drawer
            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                spacing: "12dp"
                MDNavigationDrawerHeader:
                    title: "ArUco Marker Tool"
                    padding: "16dp"
                    font_style: "Overline"
                ContentNavigationDrawer:
                    screen_manager: screen_manager
                    nav_drawer: nav_drawer
"""
