import aiohttp
import src.message as msg
import typing as tp
import googlesearch

from src.keys import keys


class Cinema:
    def __init__(self) -> None:
        self.max_n_films = 3

    def get_url_by_type(self, type: str = '') -> str:
        return f'http://kinopoiskapiunofficial.tech/api/v2.1/films/{type}'

    async def get_description(self, film_id: int) -> str:
        headers: tp.Dict[str, str] = {'accept': 'application/json', 'X-API-KEY': keys["X_API_KEY"]}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(self.get_url_by_type(str(film_id))) as response:
                info = await response.json()
                if 'description' in info['data'].keys() and info['data']['description']:
                    return info['data']['description']
                else:
                    return ''
        return ''

    def parse_json(self, json: tp.Dict[str, tp.Any]) -> str:
        n_films = min(self.max_n_films, len(json['films']))
        if n_films == 0:
            out = msg.ERROR_MSG
        else:
            out = ''

        for film in json['films'][:n_films]:

            google_query = film['nameRu']
            out += '🍿 ' + film['nameRu'] + ', '
            if 'year' in film.keys():
                out += film['year'] + '\n'
                google_query += ' ' + film['year']

            if 'posterUrl' in film.keys():
                out += film['posterUrl'] + '\n'

            if film['description']:
                desc_len = len(film['description'])
                out += film['description'][:min(300, desc_len)] + '...\n'

            for q in googlesearch.search(google_query + ' смотреть онлайн', tld='co.in',
                                         lang='ru', num=3, stop=3, pause=1):
                out += '🔹 ' + q + '\n'

            out += '\n\n'

        return out

    async def search(self, title: str, include_rating: str) -> str:
        headers: tp.Dict[str, str] = {'accept': 'application/json', 'X-API-KEY': keys["X_API_KEY"]}
        async with aiohttp.ClientSession(headers=headers) as session:
            params = {'keyword': title}
            async with session.get(self.get_url_by_type('search-by-keyword'), params=params) as response:
                info = await response.json()
                n_films = min(self.max_n_films, len(info['films']))
                lenn = 0
                for i, film in enumerate(info['films'][:n_films]):
                    if film['rating'] == 'null' or float(film['rating']) > 6.0 or include_rating == 'false':
                        film_id: int = film['filmId']
                        description = await self.get_description(film_id)
                        info['films'][i].update([('description', description)])
                        lenn += 1
                    else:
                        continue

                info['films'] = info['films'][:lenn]
                return self.parse_json(info)
