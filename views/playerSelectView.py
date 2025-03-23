import flet as ft
from .searchresult import searchResultView

class PlayerSelectView(ft.Column, searchResultView):
    def __init__(self, height: int, playersData: list, onSelect):
        super().__init__()
        self.height = height
        self.playersData = playersData
        self.onSelect = onSelect
        self.playerGrid = ft.GridView(
            height=self.height-180,
            runs_count=4,
            max_extent=200,
            child_aspect_ratio=2,
            spacing=5,
            run_spacing=5,
        )
        
        for player in self.playersData:
            self.playerGrid.controls.append(ft.Container(
                ft.Row([
                    ft.Image(src=player['avatar'], width=50, height=50),
                    ft.Column([
                        ft.Text(player['name']),
                        ft.Text(player['lastmatch'])
                    ])
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                
                expand=1,
                data=player['id'],
                on_click=self.selectPlayer,
            ))
        
        self.controls = [ft.Text("Select player", size=40, weight=ft.FontWeight.BOLD), self.playerGrid]

    def selectPlayer(self, e):
        print(e.control.data)
        self.onSelect(e.control.data)

