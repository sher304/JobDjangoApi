from bs4 import BeautifulSoup as bs
import requests


def get_html(url):
    response = requests.get(url)
    return response.text


def get_data(html):
    soup = bs(html, 'lxml')
    catalog = soup.find('div', class_='jobs-list')
    ads = catalog.find_all('a', class_='link')
    for ad in ads:
        try: 
            company = ad.find('div', class_='company').text.strip()
            # print(company)
        except:
            company = ''
        try:
            position = ad.find('div', class_='position').text.strip()
            # print(position)
        except:
            position = ''
        try:
            price = ad.find('div', class_='price').text.strip()
            # print(price)
        except:
            price = ''
        try:
            work_type = ad.find('div', class_='type').text.strip()
            # print(work_type)
        except:
            work_type = ''
        try:
            image = ad.find('img').get('src')
            # print(image)
        except:
            image = ''
        # print(company, position, price, work_type, image)
        
        data = {
            'company': company,
            'work_type': work_type,
            'position': position,
            'price': price,
            'image': image
        }

        # print(data)
        return data


def main():
    url = 'https://devkg.com/ru/jobs'
    html = get_html(url)
    # get_data(html)
    # print(get_data(html))
    return get_data(html)


if __name__ == '__main__':
    main()
