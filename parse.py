import requests
from typing import Union
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {'user-agent': ua}
razdelitel1 = '============================='
razdelitel2 = '=============================\n'


def getPlayerData(id32) -> Union[str, list]:
    url = f'https://www.dotabuff.com/players/{id32}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    accauntName = soup.find('h1').text.replace('Overview', '')

    topHeroData = []
    block = soup.find('div', 'r-table r-only-mobile-5 heroes-overview')

    rows = block.find_all('div', 'r-row')

    for row in rows:
        hero = []
        heroName = row.find('div', 'r-none-mobile').find('a').text
        hero.append(heroName)
        graphs = row.find_all('div', 'r-fluid r-10 r-line-graph')
        for graph in graphs:
            graphdata = graph.find('div', 'r-body').text
            hero.append(graphdata)

        roleData = row.find('div', 'r-role-graph').find('div', 'group').text.replace(' ', '')
        lineData = row.find('div', 'r-lane-graph').find('div', 'group').text.replace(' ', '')
        hero.append(roleData)
        hero.append(lineData)

        topHeroData.append(hero)
    return accauntName, topHeroData


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

        # cant do for loop all graphs are diffrent

        matchResult = row.find('div', 'r-match-result').find('div', 'r-body')
        matchWinOrLost = matchResult.find('a').text
        matchDate = matchResult.find('div', 'subtext').text

        matchType = row.find('div', 'r-first').find('div', 'r-body')
        matchRanked = matchType.text[0:6]
        matchRezim = matchType.find('div', 'subtext').text

        matchDurationBlock = row.find('div',
                                      'r-duration')  # to find nex el dont use .find('div', 'r-body') straightaway
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


def displayData():
    UserId = input('Input steam 32 id: ')
    accauntName, topHeroData = getPlayerData(UserId)
    lastPlayedData = getPlayerLastMatches(UserId)

    print(f'\nData for player: {accauntName};\nAll data has been parsed from Dotabuff;\n')
    print('Most played heroes:\n')

    for hero in topHeroData:
        print(razdelitel1)
        print(
            f'Name: {hero[0]};\nMatches: {hero[1]};\nWin %: {hero[2]};\nKDA: {hero[3]};\nRole: {hero[4]};\nLane: {hero[5]}.')
        print(razdelitel2)

    print(f'\n\n\nLast played matches:\n')

    for match in lastPlayedData:
        print(razdelitel1)
        print(
            f'Name: {match[0]};\nRank: {match[1]};\nResult: {match[2]};\nDate: {match[3]};\nType: {match[4]};\nGameModeType:{match[5]};\nDuration: {match[6]};\nKDA: {match[7]}.')
        print(razdelitel2)


if __name__ == '__main__':
    while True:
        displayData()
        wantToContinue = input("Want to continue? (y/n): ")

        if wantToContinue == 'N' or wantToContinue == 'n':
            break
        else:
            continue
