import requests
from bs4 import BeautifulSoup
import csv

def get_google_news_headlines(country):
    # Get news headlines from Google News
    base_url = f'https://news.google.com/rss/search?q={country}&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = []
        for item in soup.find_all('item')[:100]:
            title = item.title.text
            pub_date = item.pubdate.text if item.pubdate else None
            link = item.link.next_sibling.strip()
            headlines.append((title,pub_date,link)) 
        return headlines
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def save_to_csv(country, data, filename):
    # Save data to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Country Name', 'Title', 'Pub Date', 'Description' 'Link'])
        for title, pub_date, link in data:
            csv_writer.writerow([country, title, pub_date, link])


if __name__ == '__main__':
    
    # Get news headlines from Google News for happy and unhappy countries
    happy_countries = ['Finland', 'Denmark', 'Iceland', 'Switzerland', 'Netherlands', 'Luxembourg', 'Sweden', 'Norway', 'Israel', 'New Zealand',
                        'Austria', 'Australia', 'Ireland', 'Germany', 'Canada', 'United States', 'United Kingdom','Czechia', 'Belgium', 'France']
    unhappy_countries = ['Afghanistan', 'Lebanon', 'Zimbabwe', 'Rwanda', 'Botswana', 'Lesotho', 'Sierra Leone', 'Tanzania', 'Malawi', 'Zambia',
                         'India', 'Togo', 'Jordan', 'Mauritania', 'Yemen', 'Ethiopia', 'Chad', 'Egypt', 'Madagascar', 'Sri Lanka']

    for country in happy_countries:
        news_headlines = get_google_news_headlines(country)
        csv_filename = f'./news_headlines_happy_countries/{country}_news_headlines.csv'
        save_to_csv(country, news_headlines, csv_filename)
        print(f"\nResults saved to {csv_filename}")

    for country in unhappy_countries:
        news_headlines = get_google_news_headlines(country)
        csv_filename = f'./news_headlines_unhappy_countries/{country}_news_headlines.csv'
        save_to_csv(country, news_headlines, csv_filename)
        print(f"\nResults saved to {csv_filename}")
