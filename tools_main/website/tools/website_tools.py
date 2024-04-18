from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


async def get_website_info(url: str):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 '
                      'Safari/537.36 '
                      'Edg/114.0.1823.58'
    }
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取网站图标
    favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
    favicon_url = ''
    if favicon:
        favicon_url = favicon.get('href') or ''
        if 'https' not in favicon_url and 'http' not in favicon_url:
            favicon_url = f'https://{urlparse(url).netloc}{favicon_url}'

    # 获取网站描述
    description = soup.find('meta', attrs={'name': 'description'})
    description_content = description.get('content') if description else ''

    # 获取网站标题
    title = soup.title.string if soup.title else ''

    return {'url': url, 'name': title, 'description': description_content, 'icon': favicon_url}
