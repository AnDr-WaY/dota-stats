from typing import List
import requests
import bs4
import flet as ft


class userProfileContent(ft.UserControl):
    def __init__(self):
        super.__init__(self)


class App(ft.UserControl):
    def __init__(self):
        super().__init__()
    
    
    def build(self):
        userIdField = ft.TextField(value="", text_align="left", expand=True, label="Steam 32id")
        searchButton = ft.IconButton(ft.icons.SEARCH_OUTLINED, on_click=self.search)
        self.dataStats = ft.Column()

        return ft.Row(
            [
                userIdField,
                searchButton
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            )
    
    def search(self, e):
        print(e)




def main(page: ft.Page):
    page.title = "Dota stats"
    page.window_min_width=350
    page.window_min_height=450
    page.window_width = 450
    page.window_height = 650
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    app = App()

    page.add(app)

ft.app(target=main)