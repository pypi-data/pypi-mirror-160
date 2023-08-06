from datetime import datetime, timedelta
import threading
import requests
import asyncio
import json
import websockets
import time
import traceback
import urllib.parse
import hashlib
import hmac
import math


#Credentials
api_key = 'PgpdKo1pgq93XowlRLIPockBhVItiPuj8szeekaGX2b7xx4vYBNGzLxGY4p6Kpz3'
secret_key = 'VAgQQ0FjI1EhlTBCXomOxuDbWtJOzq4N0Mikhkk4OoHsNG6KmlBivDSepVVahSza'
api_url = "https://api.binance.us"


class Stream:

    def __init__(self, alg, symbol, listen, fm):
        self.market_stream_id = None
        self.market_data = {}
        self.book_data = {}
        self.trade_data = {}
        self.default_size = {'1m': 1, '3m': 1, '5m': 1, '15m':1, '30m':1, '1h':1,'2h':1,'4h':1,'6h':1,'8h':1,'12h':1,'1d':1,'3d':1,'1w':1,'1M':1}
        self.listening = {}
        self.symbols = []
        self.bots = {}

        self.orders = []
        self.balances = []
        self.trades = []
        self.user_stream_id = None
        self.user_buffer = []
        self.fm = fm
        self.updating = False
        self.connect(alg,symbol,listen, fm)

    def connect(self, alg, symbol, listen, fm):

        self.setup(alg, symbol, listen)

        try:
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(self.__main())
        except KeyboardInterrupt:
            pass
        print('Stream ended.')

    def setup(self, alg, sym, listen):

        book_prices = Rest.get_best_prices()
        for s in sym.keys():
            past_price = Rest.get_past_price(s)
            self.book_data[s] = book_prices[s]
            self.market_data[s] = {}
            self.trade_data[s] = {'price':float(past_price['price']), 'time':float(past_price['time'])} 
            for k, v in listen.items():
                self.market_data[s][k] = Rest.get_past_klines(s, k, v)
        self.listening = listen
        self.symbols = list(sym.keys())
        for k, v in sym.items():
            self.bots[k] = (alg())
            self.bots[k].setup(Broker(k, v, self), self.fm)

        self.balances = Rest.balance()
        self.orders = Rest.get_orders()

    async def __main(self):
        task = asyncio.create_task(self.user_stream())
        await self.market_stream()

#Market Data Stream

    async def market_recv(self, websocket):
        resp = json.loads(await websocket.recv())
        if 's' in resp.keys():  
            if 'e' in resp.keys():
                if resp['e'] == 'kline':
                    self.update_data(resp)
                    return (True, resp['s'])
                else:
                    print('Err, Unknown response: ' + json.dumps(resp))
                    return (False, resp['s'])
            elif 'u' in resp.keys():
                self.update_data(resp, 'book')
                return (False, resp['s'])
        else:
            print('Err, Unknown response: ' + json.dumps(resp))

    async def subscribe(self, websocket, symbol, interval):
        subs = []
        for sym in symbol:
            sym = sym.lower()
            for intr in interval:
                subs.append(f"{sym}@kline_{intr}")
            subs.append(f"{sym}@bookTicker")

        payload = json.dumps({"method": "SUBSCRIBE", "params": subs, "id": 0})
        await websocket.send(payload)
        resp = await websocket.recv()
        print(resp)

    async def market_stream(self):
        disconnected = False
        reconn_count = 0
        recv_count = 0
        uri = "wss://stream.binance.us:9443/ws"
        last_ping = datetime.now()
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    try:
                        await self.subscribe(websocket, self.symbols, list(self.listening.keys()))
                        self.market_stream_id = time.time_ns()
                        socket_id = self.market_stream_id
                        while self.market_stream_id == socket_id:

                            resp = await asyncio.wait_for(self.market_recv(websocket), 20)
                            recv_count += 1
                            if recv_count % 10 != 0 or resp[0]:
                                time.sleep(0.1)
                                continue

                            if last_ping + timedelta(minutes=1) < datetime.now():
                                last_ping = datetime.now()
                                Rest.ping()
                                
                            stat = self.bots[resp[1]]()
                            if stat == 'disconnect':
                                break
                        break

                    except asyncio.exceptions.TimeoutError as e:
                        print('Connection lost\nReconnecting...')
                        disconnected = True
                        self.fm.log('stream_market', e)
                    except websockets.ConnectionClosed as e:
                        print('Connection lost\nReconnecting...')
                        disconnected = True
                        self.fm.log('stream_market', e)


                time.sleep(0.2)

            except Exception as a:
                if disconnected:
                    reconn_count += 1
                    time.sleep(0.2)
                    if reconn_count % 50 == 0:
                        print('Still reconnecting...')
                        self.fm.log('stream_market', a)

                else:
                    print('Not connected to internet.\nOR ' + str(a))
                    traceback.print_exc()
                    break
        self.fm.log('stream_market', 'ended')

    def update_data (self, resp, _type='market'):

        if _type == 'market':
            sym = resp['s']
            interval = resp['k']['i']
            entry = {'time': float(resp['k']['t']), 'open': float(resp['k']['o']), 'high': float(resp['k']['h']), 
                    'low': float(resp['k']['l']), 'close': float(resp['k']['c'])}
            if self.market_data[sym][interval][0]['time'] == entry['time']:
                self.market_data[sym][interval][0] = entry
            else:
                self.market_data[sym][interval].insert(0,entry)
                self.market_data[sym][interval].pop(-1)
            self.trade_data[sym]['price'] = entry['close']
            self.trade_data[sym]['time'] = float(resp['E'])

        elif _type == 'book':
            sym = resp['s']
            self.book_data[sym]['bidPrice'] = resp['b']
            self.book_data[sym]['bidQty'] = resp['B']
            self.book_data[sym]['askPrice'] = resp['a']
            self.book_data[sym]['askQty'] = resp['A']

#User Data Stream

    async def user_stream(self):
        listen_key = self.get_listen_key()
        uri = "wss://stream.binance.us:9443/ws/" + listen_key
        async with websockets.connect(uri) as websocket:
            try:
                start_time = datetime.now()
                self.user_stream_id = time.time_ns()
                socket_id = self.user_stream_id
                while self.user_stream_id == socket_id:
                    await self.update(websocket, socket_id)
                    delta = (datetime.now() - start_time)
                    if delta.seconds > 1800:
                        print('New stream')
            except Exception as a:
                self.fm.log('stream_user', a)
                print(a)
        self.fm.log('stream_user', 'ended')

    async def update(self, websocket, socket_id):
        #watch -1
        resp = json.loads(await websocket.recv())
        print(resp)
        if self.user_stream_id != socket_id:
            self.fm.log('stream_user', 'err, stream no longer active')
            return
        if 'e' in resp.keys() and 'E' in resp.keys():
            if resp['e'] == 'executionReport':
                self.update_order(resp)
            elif resp['e'] == 'outboundAccountPosition':
                for bal in resp['B']:
                    self.update_pos(bal)
                Rest.rest_update(self)
            else:
                print('err: event type')
        else:
            self.fm.log('stream_user', 'err, unknown payload: + ' + str(resp))
        self.user_buffer.append(resp)
        print()
        print(self.orders)

    def get_listen_key(self):
        headers = {'X-MBX-APIKEY': api_key}
        resp = requests.post(
        'https://api.binance.us/api/v3/userDataStream', headers=headers).json()
        return resp['listenKey']

    def update_pos(self, data):
        for i, bal in enumerate(self.balances):
            if bal['asset'] == data['a']:
                self.balances[i]['free'] = float(data['f'])
                self.balances[i]['locked'] = float(data['l'])

    def is_locked(self, sym):
        for bal in self.balances:
            if bal['asset'] == sym:
                return float(bal['locked']) != 0.0
        print('Invalid symbol')
        raise Exception

    def add_order(self, data):
        new_order = {'clientOrderId': data['c'],
                'executedQty': float(data['z']),
                'orderId': data['i'],
                'origQty': float(data['q']),
                'price': float(data['p']),
                'side': data['S'],
                'status': data['X'],
                'symbol': data['s'],
                'timeInForce': data['f'],
                'transactTime': data['T'],
                'type': data['o']}
        self.orders.append(new_order)

    def add_trade(self, data):
        new_order = {'clientOrderId': data['c'],
                    'executedQty': float(data['z']),
                    'orderId': data['i'],
                    'origQty': float(data['q']),
                    'price': float(data['Z']),
                    'side': data['S'],
                    'status': data['X'],
                    'symbol': data['s'],
                    'timeInForce': data['f'],
                    'transactTime': data['T'],
                    'type': data['o'],
                    'maker': data['m']}
        self.trades.append(new_order)

    def update_order(self, data):

        for i, ord in enumerate(self.orders):
            if ord['orderId'] == data['i']:


                if data['X'] in ['CANCELED', 'REPLACED', 'REJECTED', 'EXPIRED']:
                    del self.orders[i]
                    return None



                elif data['X'] == 'FILLED':
                    self.add_trade(data)
                    if float(ord['origQty']) == float(data['z']):
                        del self.orders[i]
                        return None


                return None


        if data['X'] == 'NEW':
            self.add_order(data)

    def rest_update(self, delay):
        if not self.updating:
            self.updating = True
            threading.Thread(target=Rest.rest_update, args=[self,delay]).start()
            


class Rest:

    __exchange_info = {}
    __lot_size = {}
    weight = 0
    weight_high = 0
    weight_limit = 1200
    order_count = 0
    order_count_high = 0 
    order_count_limit = 100
    raw_requests = 0


    def setup ():
        Rest.exchange_info()
        Rest.__lot_size = dict([(x['baseAsset'], x['filters'][2])for x in Rest.__exchange_info['symbols']])
        Rest.weight_limit = int(list(filter(lambda x: x['interval'] == 'MINUTE' and x['rateLimitType'] == 'REQUEST_WEIGHT', Rest.__exchange_info['rateLimits']))[0]['limit'])
        Rest.order_count_limit = int(list(filter(lambda x: x['interval'] == 'SECOND' and x['rateLimitType'] == 'ORDERS', Rest.__exchange_info['rateLimits']))[0]['limit'])


    def get_ts():
        return int(round(time.time() * 1000))

    def get_binanceus_signature(data, secret):
        postdata = urllib.parse.urlencode(data)
        message = postdata.encode()
        byte_key = bytes(secret, 'UTF-8')
        mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return mac

    def binanceus_get(uri_path, data, api_key, api_sec):
        headers = {}
        headers['X-MBX-APIKEY'] = api_key
        signature = Rest.get_binanceus_signature(data, api_sec)
        params = {
            **data,
            "signature": signature,
        }
        resp = requests.get((api_url + uri_path), params=params, headers=headers)
        Rest.add_weight(resp)
        return resp.text

    def binanceus_post(uri_path, data, api_key, api_sec):
        headers = {}
        headers['X-MBX-APIKEY'] = api_key
        signature = Rest.get_binanceus_signature(data, api_sec)
        payload = {
            **data,
            "signature": signature,
        }
        resp = requests.post((api_url + uri_path), headers=headers, data=payload)
        Rest.add_weight(resp)
        return resp.text

    def binanceus_delete(uri_path, data, api_key, api_sec):
        headers = {}
        headers['X-MBX-APIKEY'] = api_key
        signature = Rest.get_binanceus_signature(data, api_sec)
        payload = {
            **data,
            "signature": signature,
        }
        resp = requests.delete((api_url + uri_path), headers=headers, data=payload)
        Rest.add_weight(resp)
        return resp.text

    def exchange_info():
        resp = requests.get('https://api.binance.us/api/v3/exchangeInfo')
        Rest.add_weight(resp)
        Rest.__exchange_info = resp.json()
        return Rest.__exchange_info

    def lot_size(sym):
        return Rest.__lot_size[sym]

    def rate_limits():
        pass

    def acc_info():
        uri_path = "/api/v3/account"
        data = {"timestamp": int(round(time.time() * 1000))}
        result = Rest.binanceus_get(uri_path, data, api_key, secret_key)
        output = json.loads(result)
        return output
    
    def balance(sym='all'):
        sym = Rest.rmv_quote(sym)
        bal = Rest.acc_info()['balances']
        amounts = list(filter(lambda x: sym == x['asset'] or sym == 'all', bal))

        return amounts

    def get_fuel():
        fuel = float(Rest.balance('BNB')[0]['free'])
        return fuel

    def trade(sym, side, t, q, price=None, tif='GTC'):
        uri_path = "/api/v3/order"
        if t == 'MARKET':
            data = {
                "symbol": sym,
                "side": side,
                "type": t,
                "quantity": str(q),
                "timestamp": int(round(time.time() * 1000)), }
            result = json.loads(Rest.binanceus_post(
                uri_path, data, api_key, secret_key))
            return result
        if t == 'LIMIT':
            if price == None:
                return 'Price must be entered'
            data = {
                "symbol": sym,
                "side": side,
                "type": t,
                "timeInForce": tif,
                "quantity": str(q),
                "price": Rest.round_price(sym, price),
                "timestamp": int(round(time.time() * 1000)), }
            result = json.loads(Rest.binanceus_post(
                uri_path, data, api_key, secret_key))
            return result

    def cancel_all(sym):
        data = {"symbol": sym, "timestamp": Rest.get_ts()}
        resp = Rest.binanceus_delete('/api/v3/openOrders', data, api_key, secret_key)
        return json.loads(resp)

    def round_qty(sym, qty=None):
        sym = Rest.rmv_quote(sym)
        prec = 1 / float(Rest.lot_size(sym)['minQty'])
        if qty == None:
            qty = float(Rest.balance(sym)[0]['free'])
        result = round(math.floor(round(qty * prec, 8)) / prec, 8)
        return result

    def round_price(sym, price):
        symbol = Rest.rmv_quote(sym)
        filters = list(filter(
            lambda x: x['baseAsset'] == symbol and x['quoteAsset'] == 'USD', Rest.__exchange_info['symbols']))[0]['filters']
        size = float(list(filter(lambda x: x['filterType'] == 'PRICE_FILTER', filters))[
                    0]['tickSize'])
        step = int(round(math.log(size**-1, 10)))
        return round(price, step)


    def wallet_status():
        uri_path = "/sapi/v1/capital/config/getall"
        data = {"timestamp": int(round(time.time() * 1000))}
        result = Rest.binanceus_get(uri_path, data, api_key, secret_key)
        output = json.loads(result)
        return output

    def get_orders(sym='all'):
        if sym == 'all':
            payload = {'timestamp': Rest.get_ts()}
        else:
            payload = {'symbol': sym, 'timestamp': Rest.get_ts()}

        resp = Rest.binanceus_get('/api/v3/openOrders', payload, api_key, secret_key)
        resp = json.loads(resp)
        return resp

    def get_trades(sym):
        payload = {'symbol': sym, 'timestamp': Rest.get_ts()}
        resp = Rest.binanceus_get('/api/v3/myTrades', payload, api_key, secret_key)
        resp = json.loads(resp)
        return resp

    def rmv_quote(sym):
        quotes = ['USD']
        for q in quotes:
            if len(sym) > len(q) and sym[-len(q):] == q:
                sym = sym[:-len(q)]
                return sym
            return sym

    def log(msg):
        print(msg)

    def get_past_price(sym, limit=1):
        resp = requests.get(
            f'https://api.binance.us/api/v3/trades?symbol={sym}&limit={limit}')
        Rest.add_weight(resp)
        return resp.json()[0]

    def get_past_klines(sym, interval, limit):
        resp = requests.get(
            f'https://api.binance.us/api/v3/klines?symbol={sym}&interval={interval}&limit={limit}')
        Rest.add_weight(resp)
        output = []
        for r in reversed(resp.json()):
            entry = {'time': float(r[0]), 'open': float(r[1]), 'high': float(r[2]),
                    'low': float(r[3]), 'close': float(r[4]),  'volume': float(r[5])}
            output.append(entry)
        return output

    def get_best_prices():
        resp = requests.get(
            'https://api.binance.us/api/v3/ticker/bookTicker')
        Rest.add_weight(resp)

        output = {}
        for r in resp.json():
            output[r['symbol']] = r
        return output

    def rest_update(strm, delay = 0):
        time.sleep(delay)
        strm.orders = Rest.get_orders()
        strm.balances = Rest.balance()
        strm.updating = False

    def server_time():
        resp = requests.get('https://api.binance.us/api/v3/time')
        Rest.add_weight(resp)

        return resp.json()['serverTime']

    def add_weight(resp):
        Rest.raw_requests += 1

        if 'x-mbx-used-weight' in resp.headers.keys():
            Rest.weight = int(resp.headers['x-mbx-used-weight'])
            if Rest.weight > Rest.weight_high:
                Rest.weight_high = Rest.weight

        if 'x-mbx-order-count-10s' in resp.headers.keys():
            Rest.order_count = int(resp.headers['x-mbx-order-count-10s'])
            if Rest.order_count > Rest.order_count_high:
                Rest.order_count_high = Rest.order_count

    def ping():
        resp = requests.get('https://api.binance.us/api/v3/ping')
        Rest.add_weight(resp)
        print('ping')
        return resp

    def delta():
        ts1 = Rest.get_ts()
        st = Rest.server_time()
        ts2 = Rest.get_ts()
        ping = ts2 - ts1
        diff = (ts1 + int(ping/2)) - st
        return (ping, diff)

class Broker:
    def __init__ (self, symbol, balance, strm):
        self.strm = strm
        self.symbol = symbol
        self.quote_asset = 'USD'
        self.start_balance = balance
        self.balance = balance
        self.position = 0
        self.open_orders = {'BUY':[], 'SELL':[]}
        self.__trades_size = len(self.strm.trades)


    def __call__ (self):

        #Orders update
        self.open_orders['BUY'] = list(
            filter(lambda x: self.symbol == x['symbol'] and x['side'] == 'BUY', self.strm.orders))
        self.open_orders['SELL'] = list(
            filter(lambda x: self.symbol == x['symbol'] and x['side'] == 'SELL', self.strm.orders))

        #Balance update
        buys = list(filter(lambda x: self.symbol ==
                    x['symbol'] and x['side'] == 'BUY', self.strm.trades))
        spent = sum([float(buy['price']) for buy in buys])
        sells = list(filter(lambda x: self.symbol ==
                     x['symbol'] and x['side'] == 'SELL', self.strm.trades))
        earned = sum([float(sell['price']) for sell in sells])
        full = earned - spent + self.start_balance
        locked = sum([float(ord['price']) * float(ord['origQty']) for ord in self.open_orders['BUY']])
        free = full - locked
        self.balance = {'full': full, 'free': free, 'locked': locked}

        #Position Update
        amounts = list(filter(lambda x: Rest.rmv_quote(
            self.symbol) == x['asset'], self.strm.balances))[0]
        amounts['free'] = Rest.round_qty(self.symbol, float(amounts['free']))
        amounts['locked'] = Rest.round_qty(
            self.symbol, float(amounts['locked']))

        self.position = {'full': amounts['free'] + amounts['locked'], 'free': amounts['free'], 'locked': amounts['locked']}




    def buy(self, _type, qty, limit_price=None):
        return Rest.trade(self.symbol, 'BUY', _type, qty, limit_price)

    def quote_buy(self, _type, quote_price, limit_price=None):
        if _type == 'MARKET':
            qty = Rest.round_qty(self.symbol, quote_price / self.get_price())
            return Rest.trade(self.symbol, 'BUY', 'MARKET', qty)
        if _type == 'LIMIT':
            qty = Rest.round_qty(self.symbol, quote_price / limit_price)
            return Rest.trade(self.symbol, 'BUY', 'LIMIT', qty, Rest.round_price(self.symbol, limit_price))

    def sell(self, _type, qty, limit_price=None):
        return Rest.trade(self.symbol, 'SELL', _type, qty, limit_price)

    def quote_sell(self, _type, quote_price, limit_price=None):
        if _type == 'MARKET':
            qty = Rest.round_qty(self.symbol, quote_price / self.get_price())
            return Rest.trade(self.symbol, 'SELL', 'MARKET', qty)
        if _type == 'LIMIT':
            qty = Rest.round_qty(self.symbol, quote_price / limit_price)
            return Rest.trade(self.symbol, 'SELL', 'LIMIT', qty, Rest.round_price(self.symbol, limit_price))

    def cancel(self, side, orderId):
        filtered = list(filter(lambda x: self.symbol == x['asset'] and x['orderId'] == orderId, self.open_orders))
        return

    def cancel_all(self, side):
        return Rest.cancel_all(self.symbol)

    def get_open_orders(self):
        return self.open_orders

    def get_trades(self):
        return list(filter(lambda trd: trd['symbol'] == self.symbol, self.strm.trades))

    def get_position(self):
        self()
        return self.position

    def get_balance(self, reserved=True):
        if reserved:
            self()
            return self.balance

        else:
            bal = self.strm.balances
            amounts = list(filter(lambda x: self.quote_asset == x['asset'], bal))
            output = {'full': amounts['free'] + amounts['locked'], 'free':amounts['free'], 'locked':amounts['locked']}
            return output

    def get_ohlc(self, interval, lookback=1):
        return self.strm.market_data[self.symbol][interval][:lookback]

    def get_price(self, lookback=1):
        price = self.strm.trade_data[self.symbol]['price']
        return price

    def get_time(self, of_trade=False):
        if of_trade:
            time = datetime.fromtimestamp(
                round(self.strm.trade_data[self.symbol]['time'] / 1000))
        else:
            time = datetime.now()
        return time

    def get_timestamp(self, of_trade = False):
        if of_trade:
            time = round(self.strm.trade_data[self.symbol]['time'] / 1000)
        else:
            time = round(datetime.now().timestamp() / 1000)
        return time

    def get_bids(self):
        price = float(self.strm.book_data[self.symbol]['bidPrice'])
        qty = float(self.strm.book_data[self.symbol]['bidQty'])
        return {'price':price, 'qty':qty}

    def get_asks(self):
        price = float(self.strm.book_data[self.symbol]['askPrice'])
        qty = float(self.strm.book_data[self.symbol]['askQty'])
        return {'price':price, 'qty':qty}

    def get_sell_price(self):
        return self.get_bids()['price']

    def get_buy_price(self):
        return self.get_asks()['price']

    def file_orders(self):
        pass

    def on_trade (self, side='all', _type='all'):
        if len(self.strm.trades) > self.__trades_size:
            cond1 = self.strm.trades[-1]['side'] == side.upper() or side == 'all'
            cond2 = self.strm.trades[-1]['type'] == _type.upper() or _type == 'all'
            if cond1 and cond2:
                self.__trades_size = len(self.strm.trades)
                return True
        return False



"""
class Report:
    sa = gspread.service_account(filename=self.fm.key('gspread'))
    sh = sa.open(self.fm.sheets['Trades'][0])
    wks = sh.worksheet(self.fm.sheets['Trades'][1])
    active = False

    def update():
        if Report.active:
            df = Report.__pull_trades()
            arr = [df.columns.values.tolist()] + df.values.tolist()
            Report.wks.update(arr)
            Report.active = False       

    def add(data):
        Report.wks.insert_row(data, 2)

    def compare():
        pass

    def __pull_trades(n=90):
        symbols = sheets.symbols
        xss = [Rest.get_trades(sym) for sym in symbols]
        trd = [x for xs in xss for x in xs]
        df = pd.DataFrame(trd)
        df["time"] = pd.to_datetime(df["time"], unit='ms')
        df.set_index('time',inplace=True)
        df.sort_index(inplace=True)
        df = df[::-1]
        df = df[df.index > datetime.now() - timedelta(days=n)]
        df = df[df.index > datetime(2022, 6, 25)].reset_index()

        df['time'] = df['time'].values.astype(np.int64) // 10 ** 9
        df = df[['orderId','time','symbol','price','qty','quoteQty','commission','commissionAsset','isBuyer','isMaker']]
        return df

    def days_filter (df, n):
        return df[df.index > datetime.datetime.now() - datetime.timedelta(days=n)]



"""
if __name__ == '__main__':
    d = Rest.delta()
    print(f'ping {d[0]}')
    print(f'delta {d[1]}')
Rest.setup()