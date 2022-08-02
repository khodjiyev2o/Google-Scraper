from main.scraping import Scraping

with Scraping() as bot:
    bot.land_first_page()
    bot.search()   
    bot.products_list()
