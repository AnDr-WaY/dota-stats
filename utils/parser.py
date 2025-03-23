import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# Создаем новый UserAgent для каждого запроса
def get_random_headers():
    ua = UserAgent().random
    return {
        'User-Agent': ua,
    }


def get_players_by_name(name: str) -> list | None:
    url = f'https://www.dotabuff.com/search?q={name}'
    response = requests.get(url, headers=get_random_headers())
    soup = BeautifulSoup(response.text, 'html.parser')
    players = soup.find('section', id='results_players').find_all('div', 'result-player')
    playersData = []
    for player in players:
        playerData = {}
        playerData['name'] = player.find('a', 'link-type-player').text
        playerData['id'] = player.find('div', 'inner')['data-player-id']
        playerData['avatar'] = player.find('img', 'image-player image-avatar')['src']
        
        lastmatch = player.find('time')
        if lastmatch is not None:
            playerData['lastmatch'] = lastmatch.text
        else:
            continue
        playersData.append(playerData)
    return playersData

def getPlayerData(id32) -> list | None:
    url = f'https://www.dotabuff.com/players/{id32}'
    response = requests.get(url, headers=get_random_headers())
    soup = BeautifulSoup(response.text, 'html.parser')
    print(response.status_code)
    
    accauntName = soup.find('h1').text.replace('Overview', '')
    topHeroData = []
    block = soup.find('div', 'r-table r-only-mobile-5 heroes-overview')
    private = soup.find("i", "fa fa-lock")
    if private is not None and "This profile is private" in private.get("title") or block is None:
        return None, None, None, None
    
    # userRank = soup.find('div', 'rank-tier-wrapper').get('title').replace("Rank: ", "")
    userRankMainImg = soup.find('img', 'rank-tier-base').get('src')
    userRankSecImg = soup.find('img', 'rank-tier-pip')
    userRankSecImg = userRankSecImg.get('src') if userRankSecImg is not None else None 

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
    return topHeroData, accauntName, userRankMainImg, userRankSecImg

def getPlayerLastMatches(id32) -> list:
    url = f'https://www.dotabuff.com/players/{id32}'
    response = requests.get(url, headers=get_random_headers())
    soup = BeautifulSoup(response.text, 'html.parser')
    block = soup.find('div', 'r-table r-only-mobile-5 performances-overview')
    lastPlayedData = []
    rows = block.find_all('div', 'r-row')

    for row in rows:
        match = {}

        heroName = row.find('div', 'r-body').find('a').find_next('a').text
        heroImgLink = row.find("img", 'tw-w-auto tw-h-6 sm:tw-h-8 tw-shrink-0 tw-rounded-sm tw-shadow-sm tw-shadow-black/20')
        heroImgLink = heroImgLink.get('src') if heroImgLink is not None else None
        heroImgLink = "https://www.dotabuff.com"+heroImgLink if heroImgLink is not None else 'https://www.dotabuff.com/assets/heroes/io.jpg'
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
    response = requests.get(url, headers=get_random_headers())
    soup = BeautifulSoup(response.text, 'html.parser')

    imgLink = soup.find('img', 'image-player image-bigavatar')['src']
    return imgLink


if __name__ == "__main__":
    print(get_players_by_name("Не"))
