import requests
from twilio.rest import Cilent


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
Api_key = "KS8YP40FEWRGUOFQ"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
New_api_key = "d7c48722f52f45a185986896e1705605"
NEW_ENDPOINT = "https://newsapi.org/v2/everything"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : Api_key,

}



response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

TWILIO_SID = "AC9e61113d56f59a86bc6cba92212c4645"
TWILIO_AUTH = "d3b7cdd1d506df5a397f0fcb7bcee00b"


#get price difference
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

#get percent change

diff_percent = (difference / float(yesterday_closing_price)) * 100
print(diff_percent)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 


if diff_percent > 0:
    print("get news")
    new_params = {
        "apiKey": New_api_key,
        "qInTitle": COMPANY_NAME,
    }

    new_response = requests.get(NEW_ENDPOINT, params=new_params)
    articles = new_response.json()['articles']

    three_articles = articles[:3]
    print(three_articles)


formatted_articles = [f"Topic: {article['title']}. \nInformation: {article['description']}" for article in three_articles]




## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

cilent = Cilent(TWILIO_SID, TWILIO_AUTH)


for article in formatted_articles:
    message = cilent.messages.creeate(
        body=article,
        from_="+13187065842",
        to="+660902861212"
    )



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

