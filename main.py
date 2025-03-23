from utils import parser
import flet as ft
from views import settings, titlebar, userProfileContent, searchresult, playerSelectView


class DotaStatsApp(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.padding = 10
        self.settingsToggled = False
        
        # Initialize settings
        self.settings = settings.Settings(self.page)
        self.settings.app = self
        
        # Apply settings from config at app start
        self.settings.apply_saved_settings()
        self.page.update()
    
        self.userIdField = ft.TextField(value="", text_align="left", expand=True, label="User steam name", on_submit=self.search)
        self.searchButton = ft.IconButton(ft.Icons.SEARCH_OUTLINED, on_click=self.search)
        self.settingsButton = ft.IconButton(ft.Icons.SETTINGS_OUTLINED, on_click=self.toogle_settings)
        self.settingsRow = ft.Row([self.settings], visible=False)
        self.usercontent = ft.Column()
        
        self.update_field_label()
        
        self.content = ft.Column(controls=[
            ft.Row(
                [
                    self.userIdField,
                    self.searchButton,
                    self.settingsButton,
                ]
            ),
            self.settingsRow,
            self.usercontent
        ])
        self.page.update()
    
    def resize(self, e):
        if len(self.usercontent.controls) > 0 and isinstance(self.usercontent.controls[0], searchresult.searchResultView):
            self.usercontent.controls[0].set_height(self.page.height)
            self.page.update()
    
    def toogle_settings(self, e):
        self.settingsToggled = not self.settingsToggled
        self.settingsRow.visible = self.settingsToggled
        self.usercontent.visible = not self.settingsToggled
        self.page.update()
    
    def update_field_label(self):
        if self.settings.search_name_or_id_switch.value:
            self.userIdField.label = "User steam 32id"
        else:
            self.userIdField.label = "User name"
        self.page.update()
        
    def search(self, e):
        if self.settings.search_name_or_id_switch.value:
            self.searchById(e)
        else:
            self.searchByName(e)
        
    def searchById(self, e):
        if self.userIdField.value == "":
            self.usercontent.controls = [ft.Text(value="Please enter a user ID", color=ft.Colors.RED_900,  text_align=ft.TextAlign.CENTER)]
            self.page.update()
            return
        if self.userIdField.value == "1": #TEST ID
            self.userIdField.value = "1182626946"
        data, userName, userRankMainImgLink, userRankSecImgLink = parser.getPlayerData(self.userIdField.value)

        if data is None: #IF profile is closed or not found
            self.usercontent.controls = [ft.Text(value="User not found or profile is closed!", color=ft.Colors.RED_900,  text_align=ft.TextAlign.CENTER)]
            self.page.update()
            return
        lastMatchesData = parser.getPlayerLastMatches(self.userIdField.value)
        userImage = parser.getPlayerImageLink(self.userIdField.value)
        self.userProfileContent = userProfileContent.userProfileContent(
            height=self.page.height,
            userName=userName,
            userRankMainImgLink=userRankMainImgLink,
            userRankSecImgLink=userRankSecImgLink,
            userData=data,
            userLastMatches=lastMatchesData,
            userId=self.userIdField.value,
            userImageLink=userImage,
        )
        self.usercontent.controls = [self.userProfileContent]
        self.page.update()

    def searchByName(self, e):
        if self.userIdField.value == "":
            self.usercontent.controls = [ft.Text(value="Please enter a user name", color=ft.Colors.RED_900,  text_align=ft.TextAlign.CENTER)]
            self.page.update()
            return
        playersData = parser.get_players_by_name(self.userIdField.value)
        if len(playersData) == 0:
            self.usercontent.controls = [ft.Text(value="No players found", color=ft.Colors.RED_900,  text_align=ft.TextAlign.CENTER)]
            self.page.update()
            return
        self.playerSelectView = playerSelectView.PlayerSelectView(height=self.page.height, playersData=playersData, onSelect=self.searchSelectedPlayer)
        self.usercontent.controls = [self.playerSelectView]
        self.page.update()
    
    def searchSelectedPlayer(self, id32):
        data, userName, userRankMainImgLink, userRankSecImgLink = parser.getPlayerData(id32)

        if data is None: #IF profile is closed or not found
            self.usercontent.controls = [ft.Text(value="User not found or profile is closed!", color=ft.Colors.RED_900,  text_align=ft.TextAlign.CENTER)]
            self.page.update()
            return
        lastMatchesData = parser.getPlayerLastMatches(id32)
        userImage = parser.getPlayerImageLink(id32)
        self.userProfileContent = userProfileContent.userProfileContent(
            height=self.page.height,
            userName=userName,
            userRankMainImgLink=userRankMainImgLink,
            userRankSecImgLink=userRankSecImgLink,
            userData=data,
            userLastMatches=lastMatchesData,
            userId=id32,
            userImageLink=userImage,
        )
        self.usercontent.controls = [self.userProfileContent]
        self.page.update()
        
        
if __name__ == "__main__": 
    def main(page: ft.Page):
        #Window 
        page.title = "Dota Stats"
        page.window.min_width = 460
        page.window.width = 460
        page.window.min_height = 650
        
        #App
        app = DotaStatsApp(page)
        page.on_resized = app.resize
        
        #Custom title bar
        page.window.title_bar_hidden = True
                
        title_bar = ft.WindowDragArea(titlebar.TitleBar(page))
        page.add(title_bar)   
        page.add(app)         
        #Padding and alignment
        page.padding = 0
        page.spacing = 0
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        page.update()
 
    ft.app(main)