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
    if private is not None and "This profile is private" in private.get("title"):
        return None
    
    rows = block.find_all('div', 'r-row')
    for row in rows:
        hero = []
        heroName = row.find('div', 'r-none-mobile').find('a').text
        hero.append(heroName)
        graphs = row.find_all('div', 'r-line-graph')
        for graph in graphs:
            graphdata = graph.find('div', 'r-body').text
            hero.append(graphdata)
        # roleData = row.find('div', 'r-role-graph').find('div', 'group').text.replace(' ', '')
        # lineData = row.find('div', 'r-lane-graph').find('div', 'group').text.replace(' ', '')
        # hero.append(roleData)
        # hero.append(lineData)

        topHeroData.append(hero)
    return topHeroData

def getPlayerLastMatches(id32) -> list:
    url = f'https://www.dotabuff.com/players/{id32}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    block = soup.find('div', 'r-table r-only-mobile-5 performances-overview')
    lastPlayedData = []
    rows = block.find_all('div', 'r-row')

    for row in rows:
        match = []

        heroName = row.find('div', 'r-body').find('a').find_next('a').text
        match.append(heroName)
        rank = row.find('div', 'r-body').find('div', 'subtext').text
        match.append(rank)

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

        match.append(matchWinOrLost)
        match.append(matchDate)
        match.append(matchRanked)
        match.append(matchRezim)
        match.append(matchDuration)
        match.append(matchKDA)

        lastPlayedData.append(match)
    return lastPlayedData


def getPlayerImage(id32):
    url = f'https://www.dotabuff.com/players/{id32}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    imgLink = soup.find('img', 'image-player image-bigavatar')['src']
    return imgLink


class userProfileContent(ft.UserControl):
    def __init__(self):
        super.__init__(self)


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
        data = getPlayerData(self.userIdField.value)
        self.dataStats.controls = []
        if data is None:
            self.dataStats.controls.append(ft.Text(value="Пользователь не найден или его профиль закрыт!", color=ft.colors.RED_900,  text_align=ft.TextAlign.CENTER))
            self.update()
            return
        print(data)




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