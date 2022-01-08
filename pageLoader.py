import time
from selenium import webdriver
import pandas as pd


class PageScraper(webdriver.Chrome):
    def __init__(self, url="https://www.vivino.com/explore?e=eJzLLbI11rNQy83MszVQy02ssDU1MDCxNFJLrrT1dFFLBhJBagW2hmrpabZliUWZqSWJOWr5RSm2avlJlbZq5SXRsbaGALW2FPM%3D"):
        self.web_url = url
        super(PageScraper, self).__init__()

    # Load data
    # create excel
    # :return: list of data in pandas
    def get_data(self):
        # find the tag class for each data
        vintage_class = "wineInfoVintage__wineInfoVintage--bXr7s wineInfoVintage__large--OaWjm wineInfo__vintage--2wqwE"
        loc_class = "wineInfoLocation__regionAndCountry--1nEJz"
        rating_class = "vivinoRating__averageValue--3Navj"
        total_rating_class = "vivinoRating__caption--3tZeS"

        # Scrape
        vintage = self.find_elements_by_xpath(f'//div[@class="{vintage_class}"]')
        loc = self.find_elements_by_xpath(f'//div[@class="{loc_class}"]')
        rating = self.find_elements_by_xpath(f'//div[@class="{rating_class}"]')
        total_rating = self.find_elements_by_xpath(f'//div[@class="{total_rating_class}"]')

        # Enumerate for each data
        vintage_list = []
        loc_list = []
        rating_list = []
        total_rating_list = []

        print("\n\nCOLLECTING DATA ...")

        for vs in vintage:
           vintage_list.append(vs.text.replace("\n", " "))
        
        for l in loc:
            loc_list.append(l.text)
        
        for r in rating:
            rating_list.append(r.text)
        
        for tr in total_rating:
            total_rating_list.append(tr.text)

        df = pd.DataFrame()
        df['Vintage'] = vintage_list
        df['Location'] = loc_list
        df['Rating'] = rating_list
        df['Total Rating'] = total_rating_list

        print("\n\nCREATING EXCEL FILE ...")

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter("Data Wine.xlsx", engine="xlsxwriter")
        
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name="Sheet1")

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    # Scroll to the botom of the page
    # Scroll based on a spesific time or when it's the end of the pages
    def scroll(self, scroll_time = 60, scroll_pause_time = 2.5):

        # Get scroll height
        last_height = self.execute_script("return document.body.scrollHeight")

        # Get current time
        start_time = time.time()

        print("LOADING PAGE INFORMATION ...")

        while (time.time() - start_time) < scroll_time:
            # Scroll down to bottom
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height

        self.get_data()

    # Load page
    def get_page(self):
        self.get(self.web_url)

        self.scroll()