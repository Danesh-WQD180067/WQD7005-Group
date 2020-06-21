@echo off 

echo "Activating Anaconda Environment"
call C:\Users\USER\Anaconda3\Scripts\activate.bat


echo "Deleting Old Data"
del /q "output\*.*"


echo "Starting Price Crawl"
python daily_price_scraper.py


echo "Starting News Crawl"
scrapy crawl news_crawler -o output\news.csv

echo "Starting Data Processing"
python daily_feature_engineering.py


echo "Starting Price Prediction"
python daily_forecasting_model.py


echo "Kill Straggling Processes"
taskkill /F /IM firefox.exe