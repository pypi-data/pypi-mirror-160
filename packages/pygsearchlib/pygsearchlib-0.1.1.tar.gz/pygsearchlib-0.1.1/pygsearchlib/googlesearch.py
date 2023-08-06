from bs4 import BeautifulSoup
from requests import get


class GoogleSearch:
    def __init__(self, results=10, lang="en", proxy=None):
        self.results = results
        self.lang = lang
        self.proxy = proxy
        self.usr_agent = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/61.0.3163.100 Safari/537.36'}

    def search(self, term):

        def get_results(search_term, number_results, language_code):
            escaped_search_term = search_term.replace(' ', '+')

            google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results + 1,
                                                                                  language_code)
            proxies = None
            if self.proxy:
                if self.proxy[:5] == "https":
                    proxies = {"https": self.proxy}
                else:
                    proxies = {"http": self.proxy}

            response = get(google_url, headers=self.usr_agent, proxies=proxies)
            response.raise_for_status()

            return response.text

        def parse_results(raw_html):
            soup = BeautifulSoup(raw_html, 'html.parser')
            result_block = soup.find_all('div', attrs={'class': 'g'})
            for result in result_block:
                link = result.find('a', href=True)
                title = result.find('h3')
                if link and title:
                    yield link['href']

        html = get_results(term, self.results, self.lang)
        return list(parse_results(html))
