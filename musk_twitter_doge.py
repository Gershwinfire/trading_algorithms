######For this program I want to monitor elon musks twitter every 1-10 seconds and wait for him to mention "DOGE"

        ###USE tweepy module
            ###Must monitor comments, retweets and tweets

        #when a tweet that contains the key phrases is detected, execute a trade with the following information:
                ###use kucoin api
                    #####Quantity
                    #####Price to buy in
                        ####Monitor Price for XXXXXX minutes
                                ####When buy OR
                                ####When sell limits are detected. 
                                    #####Execute the trade.

                            ###For basis, this concept should be performed with risk management in mind
                            ###Start small and quick, lower stop loss limits
                            ###Med/medHigh take profit limit

##########################################################################
##########################################################################
##########################################################################
import twiliodata, tweepy, twitter_data, time, kucoin_data, kucoin_helpers
from twilio.rest import Client as twilioCleint
from bs4 import BeautifulSoup
from kucoin.client import Client
import pandas as pd
from fbchat import Client as fbClient

###############################################
        #TWITTER API INFO
#Tokens, but these need to be stored separately for security reasons
api_key = 'FhdzFmM3fozi6J97SOETmT3Pv'
api_secret = 'Lu366xhuFYzUNwflXHPfO5z8QfBp4tEFZqeZpGtnTiPTk0XzIv'
aaccess_token = '1501961191027060791-03CP7zsrtjJGcxc0fYo4vrDAxkngfH'
aaccess_secret = 'L13OOqBS0DzbDPFvkWFrMvhF2BvZX0umUFzMJLeYwr48i'
#First authentication documentation----this is for V2
auth = tweepy.OAuth1UserHandler(
   api_key, api_secret, 
   aaccess_token,  aaccess_secret
)
api = tweepy.API(auth)


##############################################
            #TWILIO CLIENT DATA
########Set up access for twilio client to text
####API key and secret
twilio_api_key = twiliodata.auth_token
twilio_sid = twiliodata.account_sid
####Pass them into twilioclient and set the authorization equal to text_client for callable function
text_client = twilioCleint(twilio_sid, twilio_api_key)


################################################
            #KUCOIN CLIENT DATA
kucoin_api_key = kucoin_data.kucoin_api_key
kucoin_api_secret = kucoin_data.kucoin_api_secret

kucoin_client = Client(kucoin_api_key, kucoin_api_secret, passphrase='2008013Ag!')


##################################################
            ##FACEBOOK API



#########################################
##  INFORMATION ABOVE HERE IS NOT TO BE CHANGED
##  IN THE FUTURE THIS INFORMATION SHOULD BE SAVED TO A SEPARATE doc
#########################################

####First find the users id for whom we will be tracking
screen_name = "GoodBot21913682"
elon = api.get_user(screen_name=screen_name)
elon_id = elon.id

###Now we Search through all the tweets attached to this id and the keyword search

###Key word variable
keyword = "doge"
keyword2 = "dogecoin"
keyword = keyword.lower().strip()


##Create a repeating loop that will access the twitter.api data once every second until the loop is complete.
keyword_not_found = True

while keyword_not_found:
    ####Begin by extracting all tweets attached to the id
    user_timeline = api.user_timeline(user_id=elon_id, count=1)
    for tweet in user_timeline:
        text = tweet.text
        body = text
        text = text.split()
        for word in text:
            new_word = ''.join(filter(str.isalnum, word)) 
            new_word = new_word.lower().strip()
            if new_word == keyword or new_word == keyword2:
                text_client.messages.create(to="7177295751", from_=twiliodata.phone_number, body=body)
                print(body)
                kucoin_helpers.execute_doge_musktrade()
                keyword_not_found = False
        if word not in text:
            print("Nothing Yet")

        
    time.sleep(1)       
