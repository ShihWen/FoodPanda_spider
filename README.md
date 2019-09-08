# FoodPanda Spider
The __foodPandas_spider.py__ is consist of 3 parts:
- foodPandas_url.py: Dowlaod urls from the site page using Selenium.
- foodPandas_html_download.py: Send requests to the url to get html.
- foodPandas_html_process.py: Extract dish data from htmls and save as csv file.


Out put columns include:
- extract_date
- store_name
- store_price_lv: from "$" to "$$$" given by FoodPanda
- store_type
- dish_type
- dish_name
- dish_price: in NTD

![](https://github.com/ShihWen/FoodPandas_spider/blob/master/image/data_sample_img.png)
