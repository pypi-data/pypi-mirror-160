import cloudscraper
from bs4 import BeautifulSoup
import json
import requests
import cfscrape
import base64


session = requests.Session()

scraper = cfscrape.create_scraper()

parser = cloudscraper.create_scraper()


class GogoanimeParser():
    def __init__(self, page, animeid, episode_num, key):
        self.page = page
        self.animeid = animeid
        self.episode_num = episode_num

    def search(key, page):
        r = parser.get(
            f'https://gogoanime.lu/search.html?keyword={key}&page={page}').text
        soup = BeautifulSoup(r, 'html.parser')
        search = soup.find('div', 'last_episodes').find('ul', 'items')
        search_list = search.find_all('li')

        animes_res = [{}]
        animes = []
        for x in search_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            animes.append({"title": f"{title}", "image_url": f"{image_url}",
                          "url": f"{url}", "released": f"{released}"})

        animes_res.append(animes)
        searched_animes = json.dumps(animes)
        search_data = json.loads(searched_animes)
        return search_data

    def get_recently_uploaded(page):
        try:
            r = parser.get(f'https://gogoanime.lu/?page={page}').text
            soup = BeautifulSoup(r, 'html.parser')
            recently = soup.find('div', 'last_episodes').find('ul', 'items')
            recently_list = recently.find_all('li')
            anilist = dict()

            gen_ani_res = [{}]
            gen_ani = []
            for x in recently_list:
                title = x.find('p', 'name').text
                image_url = x.find('img')['src']
                url = x.find('a')['href']
                url = url.replace('/', '')
                get_id = image_url.replace(
                    '.png', '').replace('.jpg', '').split('/')
                id = get_id[-1]
                episode = x.find('p', 'episode').text
                episode = episode.replace('Episode ', '')

                gen_ani.append({"title": f"{title}", "id": f"{id}",
                                "image_url": f"{image_url}", "url": f"{url}", "episode": f"{episode}"})

            gen_ani_res.append(gen_ani)
            jsonlist = json.dumps(gen_ani)

        except:
            print('im sorry otto i cannnot get the data :( ')
        return jsonlist

    def newSeason(page):
        r = parser.get(
            f'https://gogoanime.lu/new-season.html?page={page}').text
        soup = BeautifulSoup(r, 'html.parser')
        popular = soup.find('div', 'last_episodes').find('ul', 'items')
        popular_list = popular.find_all('li')

        newseason_animes_res = [{}]
        newseason_animes = []
        for x in popular_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            newseason_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        newseason_animes_res.append(newseason_animes)
        new_animes = json.dumps(newseason_animes)
        return new_animes

    def popular(page):
        r = parser.get(f'https://gogoanime.lu/popular.html?page={page}').text
        soup = BeautifulSoup(r, 'html.parser')
        popular = soup.find('div', 'last_episodes').find('ul', 'items')
        popular_list = popular.find_all('li')

        popular_animes_res = [{}]
        popular_animes = []
        for x in popular_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            popular_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        popular_animes_res.append(popular_animes)
        pop_animes = json.dumps(popular_animes)
        return pop_animes

    def movies(page):
        r = parser.get(
            f'https://gogoanime.lu/anime-movies.html?page={page}').text
        soup = BeautifulSoup(r, 'html.parser')
        movies = soup.find('div', 'last_episodes').find('ul', 'items')
        movies_list = movies.find_all('li')

        movie_animes_res = [{}]
        movies_animes = []
        for x in movies_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            movies_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        movie_animes_res.append(movies_animes)
        mov_animes = json.dumps(movies_animes)
        return mov_animes

    def details(animeid):
        r = parser.get(f'https://gogoanime.lu/category/{animeid}').text
        soup = BeautifulSoup(r, 'html.parser')
        source_url = soup.find("div", {"class": "anime_info_body_bg"}).img
        image_url = source_url.get('src')
        title = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
        lis = soup.find_all('p', {"class": "type"})
        plot_sum = lis[1]
        pl = plot_sum.get_text().split(':')
        pl.remove(pl[0])
        sum = ""
        plot_summary = sum.join(pl)
        type_of_show = lis[0].a['title']
        ai = lis[2].find_all('a')  # .find_all('title')
        genres = []
        for link in ai:
            genres.append(link.get('title'))
        year1 = lis[3].get_text()
        year2 = year1.split(" ")
        year = year2[1]
        status = lis[4].a.get_text()
        oth_names = lis[5].get_text()
        lnk = soup.find(id="episode_page")
        source_url = lnk.find_all("li")[-1].a
        ep_num = int(source_url.get("ep_end"))
        print(ep_num)
        res_detail_search = {"title": f"{title}", "year": f"{year}", "other_names": f"{oth_names}",
                             "type": f"{type_of_show}", "status": f"{status}", "genre": f"{genres}",
                             "episodes": f"{ep_num}", "image_url": f"{image_url}", "plot_summary": f"{plot_summary}"}

        return res_detail_search

    def genre(genre_name, page):
        try:
            url = f"https://gogoanime.lu/genre/{genre_name}?page={page}"
            response = parser.get(url)
            plainText = response.text
            soup = BeautifulSoup(plainText, "html.parser")
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            gen_ani = []
            for anime in animes:  # For every anime found
                tits = anime.a["title"]
                image_url = anime.find('img')['src']
                urll = anime.a["href"]
                r = urll.split('/')
                released = anime.find('p', 'released').text
                released = released.strip()
                gen_ani.append(
                    {"title": f"{tits}", "url": f"{r[2]}", "image_url": f"{image_url}", "released": f"{released}"})

            return gen_ani
        except:
            print('not found')

    def episode(animeid, episode_num):
        links = {}
        URL_PATTERN = 'https://gogoanime.lu/{}-episode-{}'
        url = URL_PATTERN.format(animeid, episode_num)
        srcCode = parser.get(url).text
        soup = BeautifulSoup(srcCode, "html.parser")
        iframe = soup.find('div', 'anime_video_body')

        ifr = iframe.find('div', 'play-video').find('iframe')
        iframe = ifr['src']

        links['iframe'] = f"https:{iframe}"
        return links
