import base64, hmac, hashlib, twiliodata, requests, kucoin_data, time, json, threading, datetime
from sqlalchemy import create_engine
from kucoin.client import Client
from twilio.rest import Client as twilioclient
import pandas as pd
import pandas_ta as ta



'''
CRITIQUES TO ADD TO FILE:

    -useless wrappers around Kucoin API
    -improper storage of api keys
    -remove useless reptitive functions
    -reconsider using limit orders versus stop orders to avoid using sl/tp triggers
        --This also allows you to avoids miscalculations in profit/loss math.
            --When doing this, perhaps it would also be a good idea to monitor orders placed, so that when one order
            is executed, we can cancel the opposing option in order to maintain a 0 outstanding balance before repeating
    -Use futures contacts as there is more movement, and you can still use 1x leverage.
        --Increase leverage as necessary.
    -look into pandas-ta/talib libraries to calculate MA and EMA
    -if new_word in [keyword, keyword2]:
    -CONSIDER typehints and specifying return type
    -GOOGLE 'unit testing' how to write tests in python
    -Use ReadMe file
    -Look into FuzzyWuzzy package module for sentiment trading
'''


kucoin_api_key = kucoin_data.kucoin_api_key
kucoin_api_secret = kucoin_data.kucoin_api_secret

client = Client(kucoin_api_key, kucoin_api_secret,"2008013Ag!")
text_client = twilioclient(twiliodata.account_sid, twiliodata.auth_token)



def place_order(tradingpair, side, size):

    client.create_market_order(symbol=tradingpair, side=side, size=size)
    print("This trade was performed sucessfully.")


def get_price(tradingpair):

    data = client.get_ticker(symbol=tradingpair)
    return (data)


def kline_data(tradingpair, timespan, **kwargs):
    start = kwargs.get("start", None)
    end = kwargs.get("end", None)

         ######"1545904980",             //Start time of the candle cycle
         ######"0.058",                  //opening price
         ######"0.049",                  //closing price
         ######"0.058",                  //highest price
         ######"0.049",                  //lowest price
         ######"0.018",                  //Transaction volume
         ######"0.000945"                //Transaction amount

    data = client.get_kline_data(tradingpair, kline_type=timespan, start=start, end=end)
    return(data)


def set_smas(tradingpair, timespan, **kwargs):
    start = kwargs.get("start", None)
    end = kwargs.get("end", None)

    doge_data = kline_data(tradingpair="DOGE-USDT", timespan="5min", start=1649609853)

    df = pd.DataFrame(doge_data)
    df = df.rename(columns={0: 'timestamp', 1: 'open', 2: 'close', 3: 'high', 4: 'low', 5: 'volume'})

    is_int = False
    while not is_int:
        how_many_times = input("How many times: ")
        if how_many_times.strip().isdigit():
            how_many_times = int(how_many_times)
            is_int = True
    smalist_to_obtain = []

    for i in range(how_many_times):
        sma_to_calculate = input("SMA to Calulate: ")
        if sma_to_calculate.strip().isdigit:
            sma_to_calculate = int(sma_to_calculate)
            smalist_to_obtain.append(sma_to_calculate) 

    for number_to_calculate in smalist_to_obtain:
        sma = ta.sma(df['high'], length=number_to_calculate)

        total= 0.0
        counter = 0
        list_of_ema30 = []
        for simple in sma:
            ema30 = simple 
            list_of_ema30.append(ema30)

        df[f'ema{number_to_calculate}'] = list_of_ema30


    return (df)


def set_ma10(database, tablename):

    ma10 = []

    db = create_engine("sqlite:///"+database)

    data = db.execute(f"SELECT * FROM {tablename}")

    ma10list = []
    for info in data:

        volume = info['volume']
        id = info['id']
        

        emanumbers = db.execute(f"SELECT volume FROM doge5min WHERE id < {id} ORDER BY id DESC LIMIT 10;")
        
        
        ma10sum = 0
        for info in emanumbers:
            
            number = info[0]
            ma10sum += number

        #print(f"EMASUM: {ema10sum}")
        ma10 = (ma10sum / 10)
        ##print(f"EMA10: {ema10}")
        madata = []
        madata.append(id)
        madata.append(ma10)
        ma10list.append(madata)
        
    for thing in ma10list:
        maid = thing[0]
        ma10final = thing[1]
        
        db.execute(f"UPDATE doge5min SET ma10volume = {ma10final} WHERE id = {maid}")



def set_ma10(database, tablename):

    ma10 = []

    db = create_engine("sqlite:///"+database)

    data = db.execute(f"SELECT * FROM {tablename}")

    ma10list = []
    for info in data:

        volume = info['volume']
        id = info['id']
        

        emanumbers = db.execute(f"SELECT volume FROM doge5min WHERE id < {id} ORDER BY id DESC LIMIT 10;")
        
        
        ma10sum = 0
        for info in emanumbers:
            
            number = info[0]
            ma10sum += number

        #print(f"EMASUM: {ema10sum}")
        ma10 = (ma10sum / 10)
        ##print(f"EMA10: {ema10}")
        madata = []
        madata.append(id)
        madata.append(ma10)
        ma10list.append(madata)
        
    for thing in ma10list:
        maid = thing[0]
        ma10final = thing[1]
        
        db.execute(f"UPDATE doge5min SET ma10volume = {ma10final} WHERE id = {maid}")



def set_ma10(database, tablename):

    ma10 = []

    db = create_engine("sqlite:///"+database)

    data = db.execute(f"SELECT * FROM {tablename}")

    ma10list = []
    for info in data:

        volume = info['volume']
        id = info['id']
        

        emanumbers = db.execute(f"SELECT volume FROM doge5min WHERE id < {id} ORDER BY id DESC LIMIT 10;")
        
        
        ma10sum = 0
        for info in emanumbers:
            number = info[0]
            ma10sum += number

        #print(f"EMASUM: {ema10sum}")
        ma10 = (ma10sum / 10)
        ##print(f"EMA10: {ema10}")
        madata = []
        madata.append(id)
        madata.append(ma10)
        ma10list.append(madata)
        
    for thing in ma10list:
        maid = thing[0]
        ma10final = thing[1]
        
        db.execute(f"UPDATE doge5min SET ma10volume = {ma10final} WHERE id = {maid}")



def set_ma5(database, tablename):

    ma5 = []

    db = create_engine("sqlite:///"+database)

    data = db.execute(f"SELECT * FROM {tablename}")

    ma5list = []
    for info in data:

        volume = info['volume']
        id = info['id']
        

        emanumbers = db.execute(f"SELECT volume FROM doge5min WHERE id < {id} ORDER BY id DESC LIMIT 5;")
        
        
        ma5sum = 0
        for info in emanumbers:
            
            number = info[0]
            ma5sum += number

        #print(f"EMASUM: {ema10sum}")
        ma5 = (ma5sum / 5)
        ##print(f"EMA10: {ema10}")
        madata = []
        madata.append(id)
        madata.append(ma5)
        ma5list.append(madata)
        
    for thing in ma5list:
        maid = thing[0]
        ma5final = thing[1]
        
        db.execute(f"UPDATE doge5min SET ma5volume = {ma5final} WHERE id = {maid}")




def set_ma30(database, tablename):

    ma5 = []

    db = create_engine("sqlite:///"+database)

    data = db.execute(f"SELECT * FROM {tablename}")

    ma30list = []
    for info in data:

        volume = info['volume']
        id = info['id']
        

        emanumbers = db.execute(f"SELECT volume FROM doge5min WHERE id < {id} ORDER BY id DESC LIMIT 30;")
        
        
        ma30sum = 0
        for info in emanumbers:
            
            number = info[0]
            ma30sum += number

        #print(f"EMASUM: {ema10sum}")
        ma30 = (ma30sum / 30)
        ##print(f"EMA10: {ema10}")
        madata = []
        madata.append(id)
        madata.append(ma30)
        ma30list.append(madata)
        
    for thing in ma30list:
        maid = thing[0]
        ma5final = thing[1]
        
        db.execute(f"UPDATE doge5min SET ma30volume = {ma5final} WHERE id = {maid}")



def execute_doge_musktrade(input_tp, input_sl):
  
    
    ###Due to technical difficulties in instanteous limit orders (delay has been up to 6seconds)
    ###I have decided to instanteously order via market order and independently
    #set the dogecoin price for monitoring
    doge_data = get_price("DOGE-USDT")
    doge_price = doge_data['price']
    doge_price = float(doge_price)
    symbol = "DOGE-USDT"
    size = 1
    #client.create_market_order(symbol=symbol, side="buy", size=size)
    print(f"1 dogecoin was successfully purchased at {doge_price}")
    ##SET to Text you the purchase order and then after sale the sale order

    ##Then we want to monitor the price of said token, and we want to determine what percentage of profits/losses we want to accept
    desired_take_profit = input_tp
    take_profit_target = doge_price * desired_take_profit
    desired_stop_loss = input_sl
    stop_loss_target = doge_price * desired_stop_loss
    print(take_profit_target, stop_loss_target)

    doge_coin_not_sold = True
    while doge_coin_not_sold:
        doge_monitor = get_price("DOGE-USDT")
        doge_monitor_price = doge_monitor['price']
        doge_monitor_price = float(doge_monitor_price)
        if doge_monitor_price <= stop_loss_target:
            doge_coin_not_sold = False
            #client.create_market_order(symbol=symbol, side="sell", size=size)
            account_balance = doge_musk_check_balance()
            print(f"Dogecoin was sold for a loss @{doge_monitor_price}")
            print(f"Account Balance:{account_balance}\n")
            return ("Failure")
            doge_coin_not_sold = False
        ####If the take profit target is hit; trigger dogecoinsold, client.kucoin SELL, and print to the console
        if doge_monitor_price >= take_profit_target:
            doge_coin_not_sold = False
            #client.create_market_order(symbol=symbol, side="sell", size=size)
            account_balance = doge_musk_check_balance()
            print(f"Dogecoin was sold for a profit @{doge_monitor_price}")
            print(f"Account Balance: {account_balance}\n")
            return("Success")
            doge_coin_not_sold = False
    time.sleep(0.5)
    

def get_account_balances():
    
    positive_balances = []

    api_key = kucoin_data.kucoin_api_key
    api_secret = kucoin_data.kucoin_api_secret
    api_passphrase = kucoin_data.kucoin_api_passphrase
    url = 'https://api.kucoin.com/api/v1/accounts'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    result = requests.request('get', url, headers=headers)
    balance_data = json.loads(result.text)
    balance_data = balance_data['data']
    
    for token in balance_data:
        #get token balances for every token
        token_balance = token['balance']
        token_balance = float(token_balance)
        #set variable holding each corresponding balances token name for printing/returning
        currency = token['currency']

        if token_balance > 0.0:
            ##print(f"{currency}: {token_balance}")
            positive_balance_data = []
            positive_balance_data.append(currency)
            positive_balance_data.append(token_balance)
            positive_balances.append(positive_balance_data)

    return positive_balances


def doge_musk_check_balance():

    positive_balances = []

    api_key = kucoin_data.kucoin_api_key
    api_secret = kucoin_data.kucoin_api_secret
    api_passphrase = kucoin_data.kucoin_api_passphrase
    url = 'https://api.kucoin.com/api/v1/accounts'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    result = requests.request('get', url, headers=headers)
    balance_data = json.loads(result.text)
    balance_data = balance_data['data']
    
    for token in balance_data:
        #get token balances for every token
        token_balance = token['balance']
        token_balance = float(token_balance)
        #set variable holding each corresponding balances token name for printing/returning
        currency = token['currency']

        if token_balance > 0.0:
            ##print(f"{currency}: {token_balance}")
            positive_balance_data = []
            positive_balance_data.append(currency)
            positive_balance_data.append(token_balance)
            positive_balances.append(positive_balance_data)

    total_usdt = 0 

    balances = get_account_balances()
    for balance in balances:
        currency = balance[0]
        currency_balance = balance[1]
        if currency == "DOGE":
            doge_data = get_price(tradingpair="DOGE-USDT")
            doge_price = doge_data['price']
            doge_price = float(doge_price)
            converted_to_usdt = doge_price * currency_balance
            total_usdt += converted_to_usdt

        if currency == "USDT":
            total_usdt += currency_balance
    return(total_usdt)

