import flet as ft

class searchResultView:
    def __init__(self):
        super().__init__()
    
    def set_height(self, height: int):
        self.height = height
        if len(self.controls) > 1 and isinstance(self.controls[1], ft.ListView):
            self.controls[1].height = self.height-180
        elif len(self.controls) > 1 and isinstance(self.controls[1], ft.GridView):
            self.controls[1].height = self.height-180