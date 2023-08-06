import pandas as pd
from datetime import datetime, timedelta
from .alg_exceptions import err
import os
from trisigma.filemanager import FileManager
from .time_utils import floor, ceil

class Backtesting ():
    def __init__(self, alg, symbols, load=['1s'], delta = timedelta(days=0)):
        self.alg = alg()
        self.symbol = symbols[0]
        self.delta = delta
        self.load = load
        self.setup()

    def setup(self):
        self.main = self.load[0]
        self.data = self.load_data(self.load)
        self.klines = dict([(freq, [[
            {'time': 0, 'open': 0, 'high': 0, 'low': 0, 'close': 0}], 0]) for freq in self.load])
        self.alg.setup(Broker(self), FileManager())
        self.start = self.data[self.main].iloc[0]['time'].to_pydatetime()
        self.start += self.delta

    def run(self, step = 1):
        for row in self.data[self.main].iterrows():
            if row[0] % step == 0:
                if row[1]['time'].to_pydatetime() >= self.start:
                    self.alg()
                    self.set_klines(row[1])

                else:
                    self.set_klines(row[1])



    def set_klines(self, new_row):
        time = new_row['time'].timestamp()
        for k in self.klines.keys():
            kline = self.klines[k][0][-1]
            kline['time'] = time

            if k == self.main:
                self.klines[k][0].append(new_row)

            else:
                if time > self.klines[k][1]:
                    self.klines[k][1] = ceil(time, k).timestamp()
                    self.klines[k][0].append(new_row)
                else:
                    kline['high'] = max(kline['high'], new_row['high'])
                    kline['low'] = min(kline['low'], new_row['low'])
                    kline['close'] = new_row['close']
                    self.klines[k][0][-1] = kline



    def load_data(self, intervals):
        data = {}
        tick = self.__load_tick()
        for interval in intervals:
            data[interval] = self.__load_kline(tick, interval)
        return data

    def validator(self, df):
        last = list(df['id'])[-1] - 1
        for n in reversed(list(df['id'])):
            if n - 1 != last:
                print('Something wrong')
                raise Exception
            last = n

    def __load_tick(self):
        tick = pd.read_csv(os.getcwd() + '\\data\\link_trades_100.csv')
        self.validator(tick)

        for num in range(2, 21):
            new_df = pd.read_csv(
                os.getcwd() + f'\\data\\link_trades_{num}00.csv')
            tick = tick.append(new_df, ignore_index=True)
        tick = tick[::-1].reset_index(drop=True)
        tick["time"] = pd.to_datetime(tick["time"], unit='ms')
        return tick

    def __load_kline(self, tick, interval):
        interval = interval.replace('m','min')
        dt = tick.set_index('time')
        dt = dt['price'].resample(interval).ohlc().dropna().reset_index()
        return dt

class Broker:

    def __init__(self, source):

        self.source = source
        self.open_orders = {'BUY': [], 'SELL': []}
        self.print_errors = True
        self.raise_errors = False
        self.commision_rate = 0
        self.commision_cut = 0
        self.start_balance = 45
        self.__full_bal = self.start_balance
        self.__full_pos = 0
        self.position = self.get_position()
        self.balance = self.get_balance()
        self.__file_buffer = []
        self.symbol = source.symbol
        self.trades = []

    def __call__(self):
        self.__file_orders()
        self.position = self.get_position()
        self.balance = self.get_balance()

    def buy(self, _type, qty, limit_price=None):
        return self.__trade('BUY', _type, qty, limit_price)

    def quote_buy(self, _type, quote_price, limit_price):
        qty = quote_price / limit_price
        return self.__trade('BUY', _type, qty, limit_price)

    def sell(self, _type, qty, limit_price=None):
        return self.__trade('SELL', _type, qty, limit_price)

    def quote_sell(self, _type, quote_price, limit_price):
        qty = quote_price / limit_price
        return self.__trade('SELL', _type, qty, limit_price)

    def cancel(self, side, index):
        self.open_orders[side].remove(self.open_orders[side][index])

    def cancel_all(self, side):
        self.open_orders[side] = []

    def get_open_orders(self):
        return self.open_orders

    def get_position(self):
        locked = sum([ord['qty'] for ord in self.get_open_orders()['SELL']])
        free = self.__full_pos - locked
        return {'full': self.__full_pos, 'free': free, 'locked': locked}

    def get_balance(self):
        locked = sum([ord['price'] * ord['qty'] for ord in self.get_open_orders()['BUY']])
        free = self.__full_bal - locked
        return {'full': self.__full_bal, 'free': free, 'locked': locked}

    def get_ohlc(self, interval, lookback = 1):
        return list(reversed(self.source.klines[interval][0][-lookback:]))

    def get_price(self, lookback = 1):
        return self.source.klines[self.source.main][0][-1]['close']

    def get_time(self):
        row = self.source.klines[self.source.main][0][-1]['time']
        return row.to_pydatetime() 

    def get_timestamp(self):
        return self.source.klines[self.source.main][0][-1]['time'].timestamp()

    def get_bids(self):
        pass

    def get_asks(self):
        pass

    def get_sell_price(self):
        ratio = 0.99999
        return self.get_price() * ratio

    def get_buy_price(self):
        ratio = 1.00001
        return self.get_price() * ratio

    def __is_fillable(self, side, qty, price):
        return (side == 'BUY' and price >= self.get_buy_price()) or (side == 'SELL' and price <= self.get_sell_price())

    def __file_orders(self):

        for ord in self.get_open_orders()['BUY']:
            if self.__is_fillable('BUY', ord['qty'], ord['price']):
                self.__file_buffer.append({'side': 'BUY', 'type':'LIMIT'})
                self.open_orders['BUY'].remove(ord)
                cost = ord['price'] * ord['qty']
                self.__full_pos += ord['qty']
                self.__full_bal -= cost
                self.commision_cut += cost * (1 + self.commision_rate)
                entry = {'symbol': self.symbol, 'side': 'BUY', 'type': 'LIMIT', 'qty': ord['qty'], 'price': ord['price'], 'time': self.get_timestamp()}
                self.trades.append(entry)

        for ord in self.get_open_orders()['SELL']:
            if self.__is_fillable('SELL', ord['qty'], ord['price']):
                self.__file_buffer.append({'side': 'SELL', 'type': 'LIMIT'})
                self.open_orders['SELL'].remove(ord)
                cost = ord['price'] * ord['qty']
                self.__full_pos -= ord['qty']
                self.__full_bal += cost
                self.commision_cut += cost * (1 + self.commision_rate)
                entry = {'symbol': self.symbol, 'side': 'SELL', 'type': 'LIMIT', 'qty': ord['qty'], 'price': ord['price'], 'time': self.get_timestamp()}
                self.trades.append(entry)

    def on_trade(self, side='all', _type='all'):
        if len(self.__file_buffer) != 0:
            cond1 = self.__file_buffer[-1]['side'] == side or side == 'all'
            cond2 = self.__file_buffer[-1]['type'] == _type or _type == 'all'
            if cond1 and cond2:
                self.__file_buffer = []
                return True
        return False

    def __trade(self, side, _type, qty, limit_price=None):

        if _type.upper() == 'LIMIT':

            if limit_price == None:
                return err('Limit price is empty', self.print_errors, self.raise_errors)

            if (side == 'BUY' and self.get_balance()['free'] < limit_price * qty) or (side == 'SELL' and self.get_position()['free'] < qty):
                return err('Insufficient balance.', self.print_errors, False)

            if not self.__is_fillable(side, qty, limit_price):
                entry = {'time': self.get_timestamp(), 'qty': qty, 'price': limit_price}
                self.open_orders[side].append(entry)

            else:
                return self.__trade(side, 'MARKET', qty)

        else:
            if side == 'BUY':
                cost = self.get_buy_price() * qty
                if cost <= self.get_balance()['free']:
                    self.__full_bal -= cost
                    self.__full_pos += qty
                    self.commision_cut += cost * (1 + self.commision_rate)
                    entry = {'symbol': self.symbol, 'side': side, 'type': _type,
                             'qty': qty, 'price': self.get_buy_price(), 'time': self.get_timestamp()}
                    self.trades.append(entry)
                else:
                    return err('Insufficient balance', self.print_errors, self.raise_errors)
            if side == 'SELL':
                cost = self.get_sell_price() * qty
                if qty <= self.get_position()['free']:
                    self.__full_bal += cost
                    self.__full_pos -= qty
                    self.commision_cut += cost * (1 + self.commision_rate)
                    entry = {'symbol': self.symbol, 'side': side, 'type': _type,
                            'qty': qty, 'price': self.get_sell_price(), 'time': self.get_timestamp()}
                    self.trades.append(entry)
                else:
                    return err('Insufficient balance', self.print_errors, self.raise_errors)



