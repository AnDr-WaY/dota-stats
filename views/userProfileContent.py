import flet as ft
from .searchresult import searchResultView
class userProfileContent(ft.Column, searchResultView):
    def __init__(self, height, userName, userRankMainImgLink, userRankSecImgLink, userData, userLastMatches, userId, userImageLink):
        super().__init__()
        self.height = height
        self.userName = userName
        self.userRankMainImgLink = userRankMainImgLink
        self.userRankSecImgLink = userRankSecImgLink
        self.userData = userData
        self.userLastMatches = userLastMatches
        self.userId = userId
        self.userImageLink = userImageLink
        
        # USER INFO ROW
        userDataRow = ft.Row(
            controls=[
                ft.Image(
                    src=self.userImageLink,
                    width=50,
                    height=50,
                    fit=ft.ImageFit.FILL,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                ),
                ft.Text(value=self.userName, size=25, weight=500, tooltip=self.userId),
            ]
        )
        
        if self.userRankSecImgLink is not None:
            RankControls=[
                ft.Image(src=self.userRankMainImgLink, width=70, height=70, fit=ft.ImageFit.FILL),
                ft.Image(src=self.userRankSecImgLink, width=70, height=70, fit=ft.ImageFit.FILL)
            ]
        else:
            RankControls=[
                ft.Image(src=self.userRankMainImgLink, width=70, height=70, fit=ft.ImageFit.FILL)
            ]
        userRankImg = ft.Stack(controls=RankControls)  
        userInfoRow = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[userDataRow, userRankImg])
        
        # TOP HEROES ROWS
        topHeroRows = []
        lastMatchesRows = []
        
        for hero in self.userData:
            topHeroRows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Image(width=65, src=hero['img'], tooltip=hero['name'])
                        ),
                        ft.DataCell(
                            ft.Text(hero['matches'])
                        ),
                        ft.DataCell(
                            ft.Text(hero['winrate'])
                        ),
                        ft.DataCell(
                            ft.Text(hero['kda'])
                        ),
                    ]
                )
            )
            
        # LAST MATCHES ROWS
        for hero in self.userLastMatches:
            lastMatchesRows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Image(width=65, src=hero['heroImg'], tooltip=hero['heroName'])
                        ),
                        ft.DataCell(
                            ft.Text(hero['result'], color="#722622" if hero['result'] == "Lost Match" else ft.Colors.GREEN)
                        ),
                        ft.DataCell(
                            ft.Text(f"{hero['type']}\n", spans=[ft.TextSpan(hero['mode'], style=ft.TextStyle(color=ft.Colors.GREY, size=12))]),      
                        ),
                        ft.DataCell(
                            ft.Text(hero['duration'])
                        ),
                        ft.DataCell(
                            ft.Text(hero['kda'])
                        ),
                    ]
                )
            )
            
        # TOP HEROES COLUMN
        topHeroDataColumn = ft.Column(
            controls=[
                ft.Text(value="Most Played Heroes", size=20, weight=500),
                ft.DataTable(
                    width=2000,
                    columns=[
                        ft.DataColumn(ft.Text("Hero")),
                        ft.DataColumn(ft.Text("Matches")),
                        ft.DataColumn(ft.Text("Winrate")),
                        ft.DataColumn(ft.Text("KDA")),
                    ],
                    rows=topHeroRows
                )
            ]
        )
        
        # LAST MATCHES COLUMN
        lastMatchesColumn = ft.Column(
            controls=[
                ft.Text(value="Latest Matches", size=20, weight=500),
                ft.DataTable(
                    width=2000,
                    columns=[
                        ft.DataColumn(ft.Text("Hero")),
                        ft.DataColumn(ft.Text("Result")),
                        ft.DataColumn(ft.Text("Type")),
                        ft.DataColumn(ft.Text("Duration")),
                        ft.DataColumn(ft.Text("KDA")),
                    ],
                    rows=lastMatchesRows,
                    column_spacing=-10
                )
            ]
        )
                              
        self.controls = [
            userInfoRow, 
            ft.ListView(
                height=self.height-180, 
                auto_scroll=False, 
                controls=[topHeroDataColumn, lastMatchesColumn]
            )
        ]
    
