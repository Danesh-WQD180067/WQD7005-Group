# WQD7005-Group

Data Mining Assignment

# Title

Analyzing crude oil prices using Data Mining Techniques

# Group Members

1.  Danesh A/L Durairetnam  WQD180067  (17029027/1)
    #### Flask App
    #### Github Link : https://github.com/Danesh-WQD180067/WQD7005-Group
2.  Rinashini A/P Arunasalam Sukormaru  WQD170077  (17013672/1)
    #### Kivy App
    #### Github Link : https://github.com/RinashiniA/WQD7005-Group

# Video Link

1.  Milestone 1:
    * [Danesh Milestone 1](https://drive.google.com/file/d/112n7HU8r7dV-mMbPd0B5j3vIGM0dJ8Vg/view?usp=sharing)
    * [Rinashini Milestone 1](https://share.vidyard.com/watch/8yYka7SPTdXBcJSkhYFYxX)
    
2.  Milestone 2:
    * [Danesh Milestone 2](https://drive.google.com/file/d/117O0hJXfQRXM9vF9q6p_eMoqWxdGn2Lf/view?usp=sharing)
    * [Rinashini Milestone 2](https://share.vidyard.com/watch/rwUuw5fBP3WP4LZpNSuvxq?)

3.  Milestone 3:
    * [Danesh (Milestone 3 & 4)](https://drive.google.com/file/d/11KEo6PisDYOyNBJiw2YQ26wDdQrHPjMU/view?usp=sharing)
    * [Rinashini Milestone 3]()
    
4.  Milestone 4:
    * [Danesh (Milestone 3 & 4)](https://drive.google.com/file/d/11KEo6PisDYOyNBJiw2YQ26wDdQrHPjMU/view?usp=sharing) same as above
    * [Rinashini Milestone 4]()
    
4.  Milestone 5:
    * [Danesh Milestone 5](https://drive.google.com/file/d/11RgFsm2fk5npx-WyF57akETcjF0gNsE4/view?usp=sharing)
    * [Rinashini Milestone 5]()

# Scraping

## Data Mining

First navigate to the **data_mining** directory

1.  Price Scraping:
    -   install geckodriver and firefox
    -   run python script `python price_scraper.py`
2.  News Scraping:
    -   install scrapy
    -   cd to news_crawler folder
    -   use scrapy command `scrapy crawl news_crawler -o ..\output\news.csv`
3.  Warehousing
    -   run python script `python warehousing_price.py`
    -   run python script `python warehousing_news.py`
4.  Feature Engineering
    -   run python script `python feature_engineering.py`
5.  Train Forecasting Model
    -   run python script `python forecasting_model.py`


##  Daily Prediction

1. Create a schedule in Windows Task Scheduler
    -   set the trigger to Daily at 7:00 AM (UTC-5:00) Eastern Time (7:00 PM Malaysia)
    -   set the action to run `daily_job.bat` located in the **daily_crawl** directory
    -   ensure that the **start in** parameter is set to the **daily_crawl** directory
    -   stop the task if it runs longer than 1 hour


## Flask App

1. run python script `python app.py`