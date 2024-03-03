from bs4 import BeautifulSoup 
import time 
import requests 
import re 
import os

class CraigslistScraper:
    def __init__(self):
        self.headers = {'User-agent': 'Mozilla/5.0'}
        self.urls_directory = "./urls"

    def fetch_top_250_url(self):
        """
        Function to fetch top 250 URLS.
        """
        url = "https://sfbay.craigslist.org/search/zip?sort=date"
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        results_list = soup.select('li',class_='cl-results-page')

        items_url = []
        for i in list(range(1,251)):
            items_url.append(results_list[i].select_one('a').get('href'))
        return items_url

    def save_url(self, urls):
        """
        Function to save URLs.
        """
        for url in urls:
            id = re.findall('.*/(.*).html',url)[0]
            time.sleep(8)
            page = requests.get(url, headers=self.headers)
            with open(f'{self.urls_directory}/{id}.html', 'wb') as file:
                file.write(page.content)

    def read_saved_html_files(self):
        """
        Function to read saved HTML files.
        """
        for filename in os.listdir(self.urls_directory):
            if filename.endswith(".html"):
                filepath = os.path.join(self.urls_directory, filename)
                id = re.findall('./urls/(.*).html',filepath)[0]
                with open(filepath, 'r', encoding='utf-8') as file:
                    html = file.read()
                    self.extract_information(html,id)

    def extract_information(self, page, id):
        """
        Function to extract information from individual listing pages.
        """
        soup = BeautifulSoup(page,'html.parser')
        title = soup.select('h1',class_='postingtilte')[0].select('#titletextonly')[0].text
        img_url = soup.find('div',class_='slide first visible').find('img').get('src') if soup.find('div',class_='slide first visible') is not None else "Not Available"
        des = soup.select_one('#postingbody').text
        des = re.findall('QR Code Link to This Post\n\n\n(.*)',des)[0]
        post_id = re.findall('.*: (.*)',soup.find('div',class_='postinginfos').select_one('p').text)[0]
        posted_date = soup.find('div',class_='postinginfos').select('p')[1].select('time')[0].get('datetime') 
        posted_date= re.findall('(\d{4}-\d{2}-\d{2})T.*',posted_date)[0]
        last_updated_date = re.findall('(\d{4}-\d{2}-\d{2})T.*',soup.find('div',class_='postinginfos').select('p')[2].select('time')[0].get('datetime'))[0] if len(re.findall('updated',soup.find('div',class_='postinginfos').select('p')[2].text))>0 else "Date not available!"

        print(f"For HTML File ID: {id}\n")
        print(f"Title of the listing: {title}\n")
        print(f"The URL of the first image: {img_url}\n") if img_url is not None else print("Image not found for this url!\n")
        print(f"The description of the listing: {des}\n") 
        print(f"The Post ID: {post_id}\n")
        print(f"The posted date of the listing: {posted_date}\n")
        print(f"The last updated date of the listing: {last_updated_date}\n")
        print("\n\n")

if __name__ == "__main__":
    scraper = CraigslistScraper()
    top_250_urls = scraper.fetch_top_250_url()
    scraper.save_url(top_250_urls)
    scraper.read_saved_html_files()
