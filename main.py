import requests
import bs4
import flet as ft






def main(page: ft.Page):
    page.title = "Dota stats"
    page.window_width = 450
    page.window_height = 650
    
    
    def search(e):
        print(e)
        page.update()
    
    
    userIdField = ft.TextField(value="", text_align="left", width=250, label="Steam 32id")
    searchButton = ft.IconButton(ft.icons.SEARCH_OUTLINED, on_click=search)

    page.add(
        ft.Row(
            [
                userIdField,
                searchButton
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            ))

ft.app(target=main)