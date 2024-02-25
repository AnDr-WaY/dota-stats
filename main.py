import flet as ft
import requests
from bs4 import BeautifulSoup
from typing import List, Union
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {'user-agent': ua}

def getPlayerData(id32) -> list | None:
    url = f'https://www.dotabuff.com/players/{id32}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    accauntName = soup.find('h1').text.replace('Overview', '')
    topHeroData = []
    block = soup.find('div', 'r-table r-only-mobile-5 heroes-overview')
    private = soup.find("i", "fa fa-lock")
    if private is not None and "This profile is private" in private.get("title") or block is None:
        return None, None, None
    
    userRank = soup.find('div', 'rank-tier-wrapper').get('title').replace("Rank: ", "")
    rows = block.find_all('div', 'r-row')
    for row in rows:
        hero = {}
        heroName = row.find('div', 'r-none-mobile').find('a').text
        hero['name'] = heroName
        heroImgLink = row.find("img", 'image-hero image-icon').get('src')
        hero['img'] = "https://www.dotabuff.com"+heroImgLink
        graphs = row.find_all('div', 'r-line-graph')
        grahpIndex = 1
        for graph in graphs:
            graphdata = graph.find('div', 'r-body').text
            if grahpIndex == 1:
                hero['matches'] = graphdata
            elif grahpIndex == 2:
                hero['winrate'] = graphdata
            elif grahpIndex == 3:
                hero['kda'] = graphdata
            grahpIndex+=1
            
            
        # roleData = row.find('div', 'r-role-graph').find('div', 'group').text.replace(' ', '')
        # lineData = row.find('div', 'r-lane-graph').find('div', 'group').text.replace(' ', '')
        # hero.append(roleData)
        # hero.append(lineData)

        topHeroData.append(hero)
    return topHeroData, accauntName, userRank

def getPlayerLastMatches(id32) -> list:
    url = f'https://www.dotabuff.com/players/{id32}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    block = soup.find('div', 'r-table r-only-mobile-5 performances-overview')
    lastPlayedData = []
    rows = block.find_all('div', 'r-row')

    for row in rows:
        match = {}

        heroName = row.find('div', 'r-body').find('a').find_next('a').text
        heroImgLink = row.find("img", 'image-hero image-icon').get('src')
        heroImgLink = "https://www.dotabuff.com"+heroImgLink
        rank = row.find('div', 'r-body').find('div', 'subtext').text

        matchResult = row.find('div', 'r-match-result').find('div', 'r-body')
        matchWinOrLost = matchResult.find('a').text
        matchDate = matchResult.find('div', 'subtext').text

        matchType = row.find('div', 'r-first').find('div', 'r-body')
        matchRanked = matchType.text[0:6]
        matchRezim = matchType.find('div', 'subtext').text

        matchDurationBlock = row.find('div',
                                      'r-duration')  # to find nex el dont use .find('div', 'r-body') 
        matchDuration = matchDurationBlock.find('div', 'r-body').text

        matchKDA = matchDurationBlock.find_next('div', 'r-line-graph').find('div', 'r-body').text

        match['heroName'] = heroName
        match['heroImg'] = heroImgLink
        match['rank'] = rank
        match['result'] = matchWinOrLost
        match['date'] = matchDate
        match['type'] = matchRanked
        match['mode'] = matchRezim
        match['duration'] = matchDuration
        match['kda'] = matchKDA

        lastPlayedData.append(match)
    return lastPlayedData

def getPlayerImageLink(id32):
    url = f'https://www.dotabuff.com/players/{id32}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    imgLink = soup.find('img', 'image-player image-bigavatar')['src']
    return imgLink


class userProfileContent(ft.UserControl):
    def __init__(self, userName, userRank, userData, userLastMatches, userId, userImageLink):
        super().__init__()
        self.userName = userName
        self.userRank: str = userRank
        self.userData = userData
        self.userLastMatches = userLastMatches
        self.userId = userId
        self.userImageLink = userImageLink
        
    def build(self):
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
        if self.userRank != "Not Calibrated" and "Immortal" not in self.userRank:
            userRankName = self.userRank.split(' ')[-2].lower()
            userRankStars = self.userRank.split(' ')[-1]
            userRankImg = ft.Stack(
                            controls=[
                                    ft.Image(src=f"/stars/{userRankStars}.png", width=70, height=70, fit=ft.ImageFit.FILL),
                                    ft.Image(src=f"/ranks/{userRankName}.png", width=70, height=70, fit=ft.ImageFit.FILL),
                                ]
                            )
        elif 'Immortal' in self.userRank:
            userRankImg = ft.Image(src=f"/ranks/immortal.png", width=70, height=70, fit=ft.ImageFit.FILL)
        else:
            userRankImg = ft.Image(src=f"/ranks/Not Calibrated.png", width=70, height=70, fit=ft.ImageFit.FILL)
            
        userInfoRow = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[userDataRow, userRankImg])
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
            
        for hero in self.userLastMatches:
            lastMatchesRows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Image(width=65, src=hero['heroImg'], tooltip=hero['heroName'])
                        ),
                        ft.DataCell(
                            ft.Text(hero['result'], color="#722622" if hero['result'] == "Lost Match" else ft.colors.GREEN)
                        ),
                        ft.DataCell(
                            ft.Text(f"{hero['type']}\n", spans=[ft.TextSpan(hero['mode'], style=ft.TextStyle(color=ft.colors.GREY, size=12))]),      
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
            
        topHeroDataColumn = ft.Column(
            controls=[
                ft.Text(value="Герои с найбольшим количеством игр", size=20, weight=500),
                ft.DataTable(
                    width=2000,
                    columns=[
                        ft.DataColumn(ft.Text("Герой")),
                        ft.DataColumn(ft.Text("Матчей")),
                        ft.DataColumn(ft.Text("Винрейт")),
                        ft.DataColumn(ft.Text("KDA")),
                    ],
                    rows=topHeroRows
                )
            ]
        )
        
        lastMatchesColumn = ft.Column(
            controls=[
                ft.Text(value="Последние матчи", size=20, weight=500),
                ft.DataTable(
                    width=2000,
                    columns=[
                        ft.DataColumn(ft.Text("Герой")),
                        ft.DataColumn(ft.Text("Результат")),
                        ft.DataColumn(ft.Text("Режим")),
                        ft.DataColumn(ft.Text("Время")),
                        ft.DataColumn(ft.Text("KDA")),
                    ],
                    rows=lastMatchesRows,
                    column_spacing=-10
                )
            ]
        )
                                  
        return ft.Column(
            controls=[userInfoRow, ft.ListView(height=450, auto_scroll=False, controls=[topHeroDataColumn, lastMatchesColumn])]
        )
        
        

class App(ft.UserControl):
    def __init__(self):
        super().__init__()
    
    
    def build(self):
        self.userIdField = ft.TextField(value="", text_align="left", expand=True, label="User steam 32id")
        self.searchButton = ft.IconButton(ft.icons.SEARCH_OUTLINED, on_click=self.search)
        self.dataStats = ft.Column(controls=[])


        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.userIdField,
                        self.searchButton
                    ],
                ),
                self.dataStats,
            ],
        )


    
    def search(self, e):
        data, userName, userRank = getPlayerData(self.userIdField.value)
        self.dataStats.controls = []
        if data is None: #IF profile is private or 
            self.dataStats.controls.append(ft.Text(value="Пользователь не найден или его профиль закрыт!", color=ft.colors.RED_900,  text_align=ft.TextAlign.CENTER))
            self.update()
            return
        lastMatchesData = getPlayerLastMatches(self.userIdField.value)
        userImage = getPlayerImageLink(self.userIdField.value)
        content = userProfileContent(userData=data, userName=userName, userRank=userRank, userLastMatches=lastMatchesData, userId=self.userIdField.value, userImageLink=userImage)
        self.dataStats.controls.append(content)
        self.update()
        

def main(page: ft.Page):
    page.title = "Dota stats"
    page.window_min_width=450
    page.window_min_height=650
    page.window_width = 450
    page.window_height = 650
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    app = App()

    page.add(app)

ft.app(target=main, assets_dir="assets")