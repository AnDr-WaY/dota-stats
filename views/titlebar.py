import flet as ft
from utils.windowutils import minimize_window, close_window

class TitleBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.setOnTop = False
        self.height = 30
        self.padding = ft.padding.only(left=10, right=10)
        self.bgcolor = ft.Colors.ON_PRIMARY
        
        
        self.leading = ft.Container(ft.Image(src="assets/icon.png", width=25, height=25), on_click=lambda e: print("Home")) #HIDDEN FOR NOW
        self.title = ft.Text("Dota Stats", size=18, weight=ft.FontWeight.W_500)
        
        self.pin_on_top_button = ft.IconButton(ft.Icons.PUSH_PIN_OUTLINED, on_click=self.pin_on_top, icon_size=20, width=25, height=25, padding=0, icon_color=ft.Colors.BLACK)
        self.minimize_button = ft.IconButton(ft.Icons.MINIMIZE_ROUNDED, on_click=self.minimize, icon_size=20, width=25, height=25, padding=0, icon_color=ft.Colors.BLACK)
        self.maximize_button = ft.IconButton(ft.Icons.CHECK_BOX_OUTLINE_BLANK_OUTLINED, on_click=self.maximize, icon_size=15, width=25, height=25, padding=0, icon_color=ft.Colors.BLACK)
        self.close_button = ft.IconButton(ft.Icons.CLOSE_ROUNDED, on_click=self.close, icon_size=20, width=25, height=25, padding=0, icon_color=ft.Colors.BLACK)
        
        
        self.content = ft.Row(
            [
                ft.Row([self.title]), 
                ft.Row([self.pin_on_top_button, self.minimize_button, self.maximize_button, self.close_button]),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )


    def pin_on_top(self, e):
        self.setOnTop = not self.setOnTop
        self.pin_on_top_button.icon = ft.Icons.PUSH_PIN_ROUNDED if self.setOnTop else ft.Icons. PUSH_PIN_OUTLINED
        self.page.window.always_on_top = self.setOnTop
        self.page.update()

    def maximize(self, e):
        self.page.window.maximized = not self.page.window.maximized
        self.page.update()

    def minimize(self, e):
        try:
            minimize_window()
        except:
            self.page.window.minimized = True
            self.page.update()

    def close(self, e):
        try:
            close_window()
        except:
            self.page.window.destroy()
            self.page.event_handlers.clear()
            self.page._close()