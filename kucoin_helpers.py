import base64, hmac, hashlib, twiliodata, requests, kucoin_data, time, json, threading, datetime
from sqlalchemy import create_engine
from kucoin.client import Client
from twilio.rest import Client as twilioclient



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


def kline_data(tradingpair, timespan, start, end):

         ######"1545904980",             //Start time of the candle cycle
         ######"0.058",                  //opening price
         ######"0.049",                  //closing price
         ######"0.058",                  //highest price
         ######"0.049",                  //lowest price
         ######"0.018",                  //Transaction volume
         ######"0.000945"                //Transaction amount

    data = client.get_kline_data(tradingpair, kline_type=timespan, start=start, end=end)
    return(data)


def set_EMA5(database,tablename):

    ema5list = []

    db = create_engine("sqlite:///"+database)

    data_set = db.execute(f"SELECT * FROM {tablename} WHERE id > 41;")

    counter = 46
    for data in data_set:
        counter += 1
        datatime = data['timestamp']
        id = data['id']
        id = int(id)

        price = data['lastprice']
    
        #####
        #####DATA2 PRICE
        data2_id = id - 1
        data2_id = int(data2_id)
        data2 = db.execute(f"SELECT lastprice FROM {tablename} WHERE id like {data2_id}")
        data2money = data2.fetchall()

        data2price = 0
        for item2 in data2money:
            data2price = item2[0]
        


        #####
        #####DATA3 PRICE
        data3_id = id - 2
        data3_id = int(data3_id)
        data3 = db.execute(f"SELECT lastprice FROM {tablename} WHERE id like {data3_id}")
        data3money = data3.fetchall()

        data3price = 0
        for item3 in data3money:
            data3price = item3[0]



        
        #####
        #####DATA4 PRICE
        data4_id = id - 3
        data4_id = int(data4_id)
        data4 = db.execute(f"SELECT lastprice FROM {tablename} WHERE id like {data4_id}")
        data4money = data4.fetchall()

        data4price = 0
        for item4 in data4money:
            data4price = item4[0]




         #####
        #####DATA5 PRICE
        data5_id = id - 4
        data5_id = int(data5_id)
        data5 = db.execute(f"SELECT lastprice FROM {tablename} WHERE id like {data5_id}")
        data5money = data5.fetchall()

        data5price = 0
        for item5 in data5money:
            data5price = item5[0]

        
        ema5tempdata = []    
        ema5 = (data2price + data3price + data4price + data5price + price)/5
        ema5tempdata.append(id)
        ema5tempdata.append(ema5)
        ema5list.append(ema5tempdata)

        print("COMPLETED TASK!")
        print(id, ema5)

    for emadata in ema5list:
        emaid = emadata[0]
        emanumber = emadata[1]
        print(emaid)
        db.execute(f"UPDATE doge5min SET ema5price = {emanumber} WHERE id = {emaid}")


def set_ema10(database, tablename):

    emalist10 = []

    db = create_engine("sqlite:///"+database)

    data = db.execute(f"SELECT * FROM {tablename}")

    ema10list = []
    for info in data:

        price = info['lastprice']
        id = info['id']
        

        emanumbers = db.execute(f"SELECT lastprice FROM doge5min WHERE id < {id} ORDER BY id DESC LIMIT 10;")
        
        
        ema10sum = 0
        for info in emanumbers:
            
            number = info[0]
            ema10sum += number

        #print(f"EMASUM: {ema10sum}")
        ema10 = (ema10sum / 10)
        ##print(f"EMA10: {ema10}")
        emadata = []
        emadata.append(id)
        emadata.append(ema10)
        ema10list.append(emadata)
        
    for thing in ema10list:
        emaid = thing[0]
        ema10final = thing[1]
        db.execute(f"UPDATE doge5min SET ema10price = {ema10final} WHERE id = {emaid}")


def set_ema30(database, tablename):

    emalist30 = []

    db = create_engine("sqlite:///"+database)

    data = db.execute(f"SELECT * FROM {tablename}")

    ema30list = []
    for info in data:

        price = info['lastprice']
        id = info['id']
        

        emanumbers = db.execute(f"SELECT lastprice FROM doge5min WHERE id < {id} ORDER BY id DESC LIMIT 30;")
        
        
        ema30sum = 0
        for info in emanumbers:
            
            number = info[0]
            ema30sum += number

        #print(f"EMASUM: {ema10sum}")
        ema10 = (ema30sum / 30)
        ##print(f"EMA10: {ema10}")
        emadata = []
        emadata.append(id)
        emadata.append(ema10)
        ema30list.append(emadata)
        
    for thing in ema30list:
        emaid = thing[0]
        ema10final = thing[1]
        db.execute(f"UPDATE doge5min SET ema30price = {ema10final} WHERE id = {emaid}")



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



def execute_doge_musktrade():
  
    
    ###Due to technical difficulties in instanteous limit orders (delay has been up to 6seconds)
    ###I have decided to instanteously order via market order and independently
    #set the dogecoin price for monitoring
    doge_data = get_price("DOGE-USDT")
    doge_price = doge_data['price']
    doge_price = float(doge_price)
    symbol = "DOGE-USDT"
    size = 1
    client.create_market_order(symbol=symbol, side="buy", size=size)
    print(f"1 dogecoin was successfully purchased at {doge_price}")
    ##SET to Text you the purchase order and then after sale the sale order

    ##Then we want to monitor the price of said token, and we want to determine what percentage of profits/losses we want to accept
    desired_take_profit = 1.005
    take_profit_target = doge_price * desired_take_profit
    desired_stop_loss = 0.9975
    stop_loss_target = doge_price * desired_stop_loss
    print(take_profit_target, stop_loss_target)

    doge_coin_not_sold = True
    while doge_coin_not_sold:
        doge_monitor = get_price("DOGE-USDT")
        doge_monitor_price = doge_monitor['price']
        doge_monitor_price = float(doge_monitor_price)
        if doge_monitor_price <= stop_loss_target:
            doge_coin_not_sold = False
            client.create_market_order(symbol=symbol, side="sell", size=size)
            account_balance = doge_musk_check_balance()
            print(f"Dogecoin was sold for a 0.05% profit @{doge_monitor_price}")
            print(f"Account Balance:{account_balance}\n")
            return ("Success")
        ####If the take profit target is hit; trigger dogecoinsold, client.kucoin SELL, and print to the console
        if doge_monitor_price >= take_profit_target:
            doge_coin_not_sold = False
            client.create_market_order(symbol=symbol, side="sell", size=size)
            account_balance = doge_musk_check_balance()
            print(f"Dogecoin was sold for a 0.03% loss @{doge_monitor_price}")
            print(f"Account Balance: {account_balance}\n")
            return("Failure")
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

