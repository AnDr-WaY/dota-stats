import flet as ft
from utils.config_manager import ConfigManager

class Settings(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.title = "Settings"
        self.app = None  # Will be set by the main app
        
        # Initialize config manager
        self.config_manager = ConfigManager()
        
        # Load settings from config
        theme_mode = self.config_manager.get_setting("theme", "mode", "System")
        color_scheme = self.config_manager.get_setting("theme", "color_scheme", "#0078D7")
        opacity = self.config_manager.get_setting("theme", "opacity", 1.0)
        
        self.search_name_or_id_switch = ft.Switch(label="Search by name or ID", value=False, on_change=self.toogle_search_by_name)
        self.opacity_slider = ft.Slider(label="Opacity", min=0.5, max=1, value=opacity, on_change=self.change_opacity)
        self.theme_switch = ft.Dropdown(options=[
            ft.DropdownOption(leading_icon=ft.Icons.LIGHT_MODE, text="Light"), 
            ft.DropdownOption(leading_icon=ft.Icons.DARK_MODE, text="Dark"), 
            ft.DropdownOption(leading_icon=ft.Icons.SETTINGS, text="System")], 
                                        on_change=self.change_theme,
                                        label="Theme", value=theme_mode)
        self.search_name_or_id = True
        
        # Add color scheme picker with predefined colors
        self.color_scheme_picker = ft.Dropdown(
            options=[
                ft.DropdownOption(text="Blue", key="#0078D7"),
                ft.DropdownOption(text="Green", key="#107C10"), 
                ft.DropdownOption(text="Red", key="#E81123"),
                ft.DropdownOption(text="Purple", key="#881798"),
                ft.DropdownOption(text="Orange", key="#FF8C00"),
                ft.DropdownOption(text="Teal", key="#008080"),
                ft.DropdownOption(text="Pink", key="#FF69B4"),
                ft.DropdownOption(text="Yellow", key="#FFB900"),
            ],
            on_change=self.change_color_scheme,
            label="Color Theme",
            value=color_scheme
        )

        self.controls = [
            ft.Text("Search Settings", size=20, weight=500),
            self.search_name_or_id_switch,
            ft.Divider(),
            ft.Text("Window Settings", size=20, weight=500),
            ft.Row([ft.Text("Opacity"), self.opacity_slider]),
            ft.Row([ft.Text("Theme"), self.theme_switch]),
            ft.Row([ft.Text("Color Scheme"), self.color_scheme_picker])
        ]
        
        # Apply saved settings to the application
        self.apply_saved_settings()

    def apply_saved_settings(self):
        """Apply the loaded settings to the app"""
        # Apply theme
        self.change_theme(None)
        
        # Apply opacity
        self.change_opacity(None)
        
        # Apply color scheme
        self.change_color_scheme(None)

    def toogle_search_by_name(self, e):
        self.search_name_or_id = not self.search_name_or_id
        self.search_name_or_id_switch.value = self.search_name_or_id
        # Update the userIdField label
        if hasattr(self, 'app') and self.app is not None:
            self.app.update_field_label()

    def change_opacity(self, e):
        opacity = self.opacity_slider.value
        self.page.window.opacity = opacity
        # Save setting to config
        self.config_manager.set_setting("theme", "opacity", opacity)
        self.page.update()

    def change_theme(self, e):
        theme_mode = self.theme_switch.value
        if theme_mode == "Light":
            self.page.theme_mode = ft.ThemeMode.LIGHT
        elif theme_mode == "Dark":
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.SYSTEM
        
        # Save setting to config
        self.config_manager.set_setting("theme", "mode", theme_mode)
        self.page.update()
        
    def change_color_scheme(self, e):
        # Get color value
        color = self.color_scheme_picker.value
        
        # Update the app's color scheme with the selected color
        self.page.theme = ft.Theme(color_scheme_seed=color)
        self.page.dark_theme = ft.Theme(color_scheme_seed=color)
        
        # Save setting to config
        self.config_manager.set_setting("theme", "color_scheme", color)
        self.page.update()
