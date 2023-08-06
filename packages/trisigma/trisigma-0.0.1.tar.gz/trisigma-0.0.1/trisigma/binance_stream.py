from binance.spot import Spot
from datetime import datetime, timedelta
import requests
import math
import time


class Stream:
    def __init__(self, api_key, secret_key):
      self.api_key = api_key
      self.secret_key = secret_key

    def connect(self, alg, symbols, load, fm):

        #Some initial setup
        self.client = Client(self.api_key, self.secret_key, [
                             sym['symbol'] for sym in symbols])
        self.wait = 0.1
        self.init = (datetime.now() - timedelta(days=1)).timestamp()
        self.resps = {}
        self.bots = {}
        for sym in symbols:
            self.bots[sym['symbol']] = {
                "alg": alg(), "freq": sym['freq'], "last": datetime.now().timestamp()}
            self.bots[sym['symbol']]['alg'].setup(
                Broker(sym['symbol'], sym['balance'], self.client), fm)
            for k, v in load.items():
              self.client.update_klines(sym['symbol'], k, v)

        #Start both client and Bot Controller
        self.start()

    def start(self):

        while True:
            try:
                time.sleep(self.wait)
                ready_bots = self.filter()
                self.update(ready_bots)
                self.fire(ready_bots)
                self.evaluate()
            except Exception as e:
                raise e
                break

    def filter(self):
        return dict(list(filter(lambda item: self.__is_ready(item[1]), self.bots.items())))

    def update(self, bots):
        pass

    def fire(self, bots):
        for k, v in bots.items():

            v['last'] = datetime.now().timestamp()
            resp = v['alg']()
            self.resps[k] = v

    def evaluate(self):
        pass

    def __is_ready(self, bot):
        now = datetime.now().timestamp()
        last_dur = bot['last'] - self.init
        cur_dur = now - self.init
        output = self.__floor(last_dur, bot['freq']) != self.__floor(
            cur_dur, bot['freq'])
        return output

    def __floor(self, date, interval, delta=None):
        if delta != None:
            delta = delta.total_seconds()
        else:
            delta = 0
        if not isinstance(date, (int, float)):
            date = date.timestamp()
        units = {'w': (604800, 345600), 'd': (86400, 0),
                 'h': (3600, 0), 'm': (60, 0), 's': (1, 0)}
        freq = int(''.join([i for i in interval if i.isdigit()]))
        unit = ''.join([i for i in interval if i.isalpha()])
        coef = units[unit][0] * freq
        delt = units[unit][1] + delta

        result = (date - delt) - ((date - delt) % coef) + delt
        return datetime.fromtimestamp(int(result))


class Client:
  def __init__(self, api, secret, symbols):
    self.spot = Spot(api, secret, show_limit_usage=True)

    self.quotes = {}
    self.klines = {}
    self.positions = {}
    self.orders = {}
    self.trades = {}

    self.fuel = 0
    self.weight = 0
    self.limit = 0
    self.order_count = 0
    self.delta = 0
    self.latency = 0
    self.server_time = 0
    self.ex_info = {}
    self.acc_info = {}
    self.symbols = symbols
    self.setup()

  def setup(self):
    self.update_exchange()
    self.ping()
    for sym in self.symbols:
      self.quotes[sym] = {'price': 0, 'bidPrice': 0,
                          'bidQty': 0, 'askPrice': 0, 'askQty': 0}
      self.klines[sym] = {}
      self.positions[sym] = {}
      self.orders[sym] = {}
      self.trades[sym] = {}

  def cancel(self, symbol, orderId):
    self.spot.cancel_order(symbol, orderId=orderId)

  def cancel_all(self, symbol):
    self.spot.cancel_open_orders(symbol)

  def trade(self, *argv, **kwargs):
    rules = list(filter(lambda x: x['symbol'] ==
                 argv[0], self.ex_info['symbols']))[0]
    price_filter = list(
        filter(lambda x: x['filterType'] == 'PRICE_FILTER', rules['filters']))[0]
    lot_size = list(
        filter(lambda x: x['filterType'] == 'LOT_SIZE', rules['filters']))[0]
    if 'quantity' in kwargs.keys():
      size = 1 / float(lot_size['stepSize'])
      kwargs['quantity'] = round(math.floor(
          kwargs['quantity'] * size) / size, 9)
    if 'price' in kwargs.keys():
      size = 1 / float(price_filter['tickSize'])
      kwargs['price'] = round(math.floor(kwargs['price'] * size) / size, 9)
    return self.spot.new_order_test(*argv, **kwargs)

  def update(self, symbol):
    buffer = self.weight
    self.update_balances()  # 10
    self.update_quote()  # 2
    self.update_orders(symbol)  # 5
    self.update_trades(symbol)  # 10
    self.ping()  # 1

  def ping(self):
    ts1 = datetime.now().timestamp() * 1000
    st = self.spot.time()
    self.update_weight(st)
    ts2 = datetime.now().timestamp() * 1000
    self.latency = ts2 - ts1
    self.delta = (ts1 + int(self.latency/2)) - st['data']['serverTime']
    self.server_time = st['data']['serverTime']

  def update_klines(self, symbol, interval, limit):
    klines = self.spot.klines(symbol, interval, limit=limit)
    self.update_weight(klines)
    output = []
    for r in reversed(klines['data']):
      entry = {'time': float(r[0]), 'open': float(r[1]), 'high': float(
          r[2]), 'low': float(r[3]), 'close': float(r[4]),  'volume': float(r[5])}
      output.append(entry)
    self.klines[symbol][interval] = output

  def update_exchange(self):
    ex_info = self.spot.exchange_info()
    self.update_weight(ex_info)

    self.ex_info = ex_info['data']
    m_limit = list(filter(
        lambda x: x['interval'] == 'MINUTE', ex_info['data']['rateLimits']))[0]['limit']
    self.limit = m_limit

  def update_orders(self, symbol):
    orders = self.spot.get_open_orders(symbol)
    self.update_weight(orders)

    self.orders[symbol] = orders['data']

  def update_trades(self, symbol):
    trades = self.spot.my_trades(symbol)
    self.update_weight(trades)

    self.trades[symbol] = trades['data']

  def update_quote(self):
    depths = self.spot.book_ticker(symbols=self.symbols)
    prices = self.spot.ticker_price(symbols=self.symbols)

    for v in depths['data']:
      entry = {'price': float(self.quotes[v['symbol']]['price']),
               'bidPrice': float(v['bidPrice']),
               'bidQty': float(v['bidQty']),
               'askPrice': float(v['askPrice']),
               'askQty': float(v['askQty'])}

      self.quotes[v['symbol']] = entry
    for v in prices['data']:
      self.quotes[v['symbol']]['price'] = float(v['price'])

    self.update_weight(depths)

  def update_balances(self):
    acc_info = self.spot.account()
    self.update_weight(acc_info)
    self.acc_info = acc_info

    for bal in acc_info['data']['balances']:
      free = float(bal['free'])
      locked = float(bal['locked'])
      full = free + locked
      self.positions[bal['asset']] = {
          'full': full, 'free': free, 'locked': locked}

  def update_weight(self, data):
    if type(data) == dict and 'limit_usage' in data.keys():
      if type(data['limit_usage']) == dict:
        if 'x-mbx-used-weight-1m' in data['limit_usage'].keys():
          self.weight = float(data['limit_usage']['x-mbx-used-weight-1m'])
        else:
          print('Limit response Error')
          values = [float(value) for value in data['limit_usage'].values()]
          self.weight = max(values)


class Broker:

    def __init__(self, symbol, balance, client):
        self.client = client
        self.symbol = symbol
        self.quote_asset = 'USDT'
        self.start_balance = balance
        self.balance = balance
        self.position = 0
        self.open_orders = {'BUY': [], 'SELL': []}
        self.__init_time = self.client.server_time
        self.__trade_buffer = {'BUY': -1, 'SELL': -1}

    def __call__(self):
        self.client.update(self.symbol)

        #Orders update
        self.open_orders['BUY'] = list(
            filter(lambda x: x['side'] == 'BUY', self.client.orders[self.symbol]))
        self.open_orders['SELL'] = list(
            filter(lambda x: x['side'] == 'SELL', self.client.orders[self.symbol]))

        #Balance update
        buys = list(filter(lambda x: self.__init_time <=
                    x['time'] and x['side'] == 'BUY', self.client.trades[self.symbol]))
        spent = sum([float(buy['price']) for buy in buys])
        sells = list(filter(lambda x: self.__init_time <=
                     x['time'] and x['side'] == 'SELL', self.client.trades[self.symbol]))
        earned = sum([float(sell['price']) for sell in sells])

        full = earned - spent + self.start_balance
        locked = sum([float(ord['price']) * float(ord['origQty'])
                     for ord in self.open_orders['BUY']])
        free = full - locked
        self.balance = {'full': full, 'free': free, 'locked': locked}

        #Position Update
        asset = self.symbol[:-len(self.quote_asset)]
        self.position = self.client.positions[asset]

    def buy(self, _type, qty, limit_price=None):
      if _type == 'MARKET':
        return self.client.trade(self.symbol, 'BUY', _type, quantity=qty)
      elif _type == 'LIMIT':
        return self.client.trade(self.symbol, 'BUY', _type, quantity=qty, price=limit_price)

    def quote_buy(self, _type, quote_price, limit_price=None):
        if _type == 'MARKET':
            qty = quote_price / self.get_price()
            return self.buy('MARKET', qty)
        if _type == 'LIMIT':
            qty = quote_price / limit_price
            return self.buy('LIMIT', qty, limit_price)

    def sell(self, _type, qty, limit_price=None):
      if _type == 'MARKET':
        return self.client.trade(self.symbol, 'SELL', _type, quantity=qty)
      elif _type == 'LIMIT':
        return self.client.trade(self.symbol, 'SELL', _type, quantity=qty, price=limit_price)

    def quote_sell(self, _type, quote_price, limit_price=None):
        if _type == 'MARKET':
            qty = quote_price / self.get_price()
            return self.sell('MARKET', qty)
        if _type == 'LIMIT':
            qty = quote_price / limit_price
            return self.sell('LIMIT', qty, limit_price)

    def cancel(self, orderId):
        return self.client.cancel(self.symbol, orderId=orderId)

    def cancel_all(self):
        return self.client.cancel_all(self.symbol)

    def get_open_orders(self):
        return self.open_orders

    def get_trades(self):
        return self.client.trades[self.symbol]

    def get_position(self):
        return self.position

    def get_balance(self, reserved=True):
        if reserved:
            return self.balance
        else:
            return -1

    def get_ohlc(self, interval, lookback=1):
        return self.client.klines[self.symbol][interval][:lookback]

    def get_price(self, lookback=1):
        return self.client.quotes[self.symbol]['price']

    def get_time(self, of_trade=False):
        return datetime.now()

    def get_timestamp(self, of_trade=False):
        time = datetime.now().timestamp()
        return time

    def get_bids(self):
        return self.client.quotes[self.symbol]['bidPrice']

    def get_asks(self):
        return self.client.quotes[self.symbol]['askPrice']

    def get_sell_price(self):
        return self.get_bids()

    def get_buy_price(self):
        return self.get_asks()

    def on_trade(self, side='all', _type='all'):
        output = {}
        last_buy = max(
            [trd['time'] for trd in self.client.trades[self.symbol] if trd['side'] == 'BUY'] + [-1])
        last_sell = max(
            [trd['time'] for trd in self.client.trades[self.symbol] if trd['side'] == 'SELL'] + [-1])

        output['BUY'] = last_buy not in [self.__trade_buffer['BUY'], -1]
        output['SELL'] = last_sell not in [self.__trade_buffer['SELL'], -1]
        output['all'] = output['BUY'] or output['SELL']

        self.__trade_buffer['BUY'] = last_buy
        self.__trade_buffer['SELL'] = last_sell

        return output[side]
