@echo off 

echo "Activating Anaconda Environment"
call C:\Users\USER\Anaconda3\Scripts\activate.bat

echo "Starting Price Crawl"

call python daily_price_scraper.py
call scrapy daily_crawl news_crawler -o output\news.csv

echo "Starting Data Processing"

call python daily_feature_engineering.py

echo "Starting Price Prediction"

call python daily_forecasting_model.py