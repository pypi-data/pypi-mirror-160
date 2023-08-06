from alg_exceptions import err
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly.io as pio
import filemanager as fm
import threading
import socket
import time
import json


class Alarm:

    def __init__(self, broker, interval, delta=None):
        self.intervals = {'1w': [7, 'D'], '1d': [1, 'D'],
                          '1h': [1, 'h'], '30m': [30, 'm'], '15m': [15, 'm'], '1m': [1, 'm'], '1s': [1, 's']}

        if interval.lower() in self.intervals.keys():
            self.args = self.intervals[interval.lower()]
        else:
            err('No such interval for an alarm')
            self.args = None
        self.delta = delta
        self.broker = broker
        self.time_buffer = self.broker.get_time()

    def __call__(self):
        time = self.broker.get_time()
        cur_floor = datetime.timestamp(self.floor(
            time, self.args[0], self.args[1], self.delta))
        last_floor = datetime.timestamp(self.floor(
            self.time_buffer, self.args[0], self.args[1], self.delta))
        cond = cur_floor != last_floor
        self.time_buffer = time
        return cond

    def floor(self, time, interval, unit, delta=None):
        result = time
        if delta != None:
            result = (time - delta)
        if unit == 'D':
            result -= timedelta(days=(result.weekday() % interval), hours=result.hour,
                                minutes=result.minute, seconds=result.second, microseconds=result.microsecond)

        if unit == 'h':
            result -= timedelta(hours=(result.hour %
                                       interval), minutes=result.minute, seconds=result.second, microseconds=result.microsecond)

        if unit == 'm':
            result -= timedelta(minutes=(result.minute % interval),
                                seconds=result.second, microseconds=result.microsecond)

        if unit == 's':
            result -= timedelta(seconds=(result.second %
                                interval), microseconds=result.microsecond)

        return result

    def _floor(date, interval, delta=0):
        date = date.timestamp()
        units = {'w': (604800, 345600), 'd': (86400, 0),
                 'h': (3600, 0), 'm': (60, 0), 's': (1, 0)}
        freq = int(''.join([i for i in interval if i.isdigit()]))
        unit = ''.join([i for i in interval if i.isalpha()])
        coef = units[unit][0] * freq
        delt = units[unit][1] + delta

        result = (date - delt) - ((date - delt) % coef) + delt
        return datetime.fromtimestamp(int(result))

class Broker_Debug:
    def __init__(self, broker):
        self.broker = broker

    def get_report(self, interval='15m'):
        bal = self.broker.get_balance()
        pos = self.broker.get_position()
        orders = self.orders_clean()
        #d = binance.delta()

        market = '\n'.join(['MARKET',
                            f'price: {self.broker.get_price()}',
                            f'ohlc: {self.broker.get_ohlc(interval)}',
                            f'best_bid: {self.broker.get_sell_price()}',
                            f'best_ask: {self.broker.get_buy_price()}',
                            f'time: {self.broker.get_time()}'])

        balance = '\n'.join(['RESERVED BALANCE',
                             f'full: {bal["full"]}',
                             f'free: {bal["free"]}',
                             f'locked: {bal["locked"]}'])

        position = '\n'.join(['POSITION',
                              f'full: {pos["full"]}',
                              f'free: {pos["free"]}',
                              f'locked: {pos["locked"]}'])

        open_buys = '\n'.join(['OPEN ORDERS (BUY)'] + orders[0])
        open_sells = '\n'.join(['OPEN ORDERS (SELL)'] + orders[1])

        #system = '\n'.join(['SYSTEM', f'ping {d[0]}', f'delta {d[1]}'])

        msg = '\n\n'.join(['\n'] + [market] + [open_buys] +
                          [open_sells] + [balance] + [position])
        return msg

    def get_report_sheets(self, interval):

        bal = self.broker.get_balance()
        pos = self.broker.get_position()
        orders = self.orders_clean()

        market = [['MARKET', ''],
                  ['price:', self.broker.get_price()],
                  ['best_bid:', self.broker.get_sell_price()],
                  ['best_ask:', self.broker.get_buy_price()],
                  ['time:', str(self.broker.get_time())]]

        balance = [['RESERVED BALANCE', ''],
                   ['full:', bal["full"]],
                   ['free:', bal["free"]],
                   ['locked:', bal["locked"]]]

        position = [['POSITION', ''],
                    ['full:', pos["full"]],
                    ['free:', pos["free"]],
                    ['locked:', pos["locked"]]]

        open_buys = [['OPEN ORDERS (BUY)', '']] + [['', ord]
                                                   for ord in orders[0]]
        open_sells = [['OPEN ORDERS (SELL)', '']] + [['', ord]
                                                     for ord in orders[1]]

        #system = '\n'.join(['SYSTEM', f'ping {d[0]}', f'delta {d[1]}'])

        msg = market + open_buys + open_sells + \
            balance + position + ([['', '']] * 20)
        return msg

    def take_action(self):
        action = input('>>')
        if action == 'buy':
            self.broker.buy('MARKET', 2)
        if action == 'sell':
            self.broker.sell('MARKET', 2)
        if action == 'lbuy':
            self.broker.buy('LIMIT', 2, 7.0081)
        if action == 'lsell':
            self.broker.sell('LIMIT', 2, 7.0138)
        if action == 'cancelbuy':
            self.broker.cancel_all('BUY')
        if action == 'cancelsell':
            self.broker.cancel_all('SELL')

    def orders_clean(self):
        buys = self.broker.get_open_orders()['BUY']
        sells = self.broker.get_open_orders()['SELL']
        buys = ['#' + str(ord['orderId']) + '\t' + str(ord['origQty']
                                                       ) + '\t' + str(ord['price']) for ord in buys]
        sells = ['#' + str(ord['orderId']) + '\t' + str(ord['origQty']
                                                        ) + '\t' + str(ord['price']) for ord in sells]

        return (buys, sells)

class Trailling_Loss:
    def __init__(self, broker, perc):
        self.perc = perc
        self.broker = broker
        self.locked = False
        self.trail = -1
        self.last_trail = -1

    def __call__(self):
        price = self.broker.get_price()
        if not self.locked and price * self.perc >= self.trail:
            self.last_trail = self.trail
            self.trail = price * self.perc

    def reset(self, target_price=None):
        if target_price == None:
            self.trail = self.broker.get_price() * self.perc
        else:
            self.trail = target_price * self.perc

        self.last_trail = -1

    def on_change(self, dir):
        cond1 = self.last_trail != -1
        cond2 = dir == 'higher' and self.trail > self.last_trail
        cond3 = dir == 'lower' and self.trail < self.last_trail

        return not self.locked and cond1 and (cond2 or cond3)

    def on_hit(self):
        return not self.locked and self.broker.get_price() <= self.trail

class Traces:
    def __init__(self, broker):
        self.traces = {}
        self.labels = {}
        self.broker = broker
        self.region = None
        self.__changed = False
        self.hist = {}

    def __call__(self):
        price = self.broker.get_price()
        region = None
        size = len(self.traces.keys())
        for i, v in enumerate(self.traces.values()):
            region = size - round((size) / 2)
            if price < v:
                region = i - round(size / 2)
                break

        self.__changed = self.region != None and region != self.region
        self.region = region

    def set_traces(self, new_traces, save=None):
        self.traces = dict(sorted(new_traces.items(), key=lambda x: x[1]))
        if save != None:
            self.hist[save] = new_traces


    def get_traces(self):
        return self.traces

    def get_region(self):
        return self.region

    def is_inside(self, region, ohlc):
        r = region + int(len(self.traces.keys()) / 2)
        s = region + int(len(self.traces.keys()) / 2) - 1
        for kline in ohlc:
            cond1 = r == len(self.traces) or list(
                self.traces.values())[r] > kline['high']
            cond2 = s == -1 or list(self.traces.values())[s] < kline['low']
            if not (cond1 and cond2):
                return False
        return True

    def on_change(self, region=None):
        if region == None:
            region = self.region
        return self.__changed and self.region == region

class Plot:

    def browser(broker, traces, trades, interval, lookback):

        k = pd.DataFrame(broker.get_ohlc(interval, lookback))
        k['time'] = pd.to_datetime(k["time"], unit='ms')

        k = Plot.__merge_traces(k, traces)

        start = k.iloc[0]['time']
        trades = [trd for trd in trades if trd[0] > start]

        fig = go.Figure(data=[go.Candlestick(
            x=k['time'], open=k['open'], high=k['high'], low=k['low'], close=k['close'])])

        traced = k.loc[k['T1'] != 0]

        fig.add_trace(go.Scatter(x=traced['time'], y=traced['T1'],
                                 line=dict(color='red', dash='dot', width=1)))
        fig.add_trace(go.Scatter(x=traced['time'], y=traced['T2'],
                                 line=dict(color='red', dash='dot', width=1)))
        fig.add_trace(go.Scatter(x=traced['time'], y=traced['T3'],
                                 line=dict(color='green', dash='dot', width=1)))
        fig.add_trace(go.Scatter(x=traced['time'], y=traced['T4'],
                                 line=dict(color='green', dash='dot', width=1)))

        buys = [trd for trd in trades if trd[2] == 'BUY']
        sells = [trd for trd in trades if trd[2] == 'SELL']

        fig.add_trace(go.Scatter(x=[trd[0]
                                    for trd in buys], y=[trd[1] for trd in buys]))
        fig.add_trace(go.Scatter(x=[trd[0]
                                    for trd in sells], y=[trd[1] for trd in sells]))

        fig.show()

    def html(broker, traces, trades, interval, lookback):

        k = pd.DataFrame(broker.get_ohlc(interval, lookback))
        print(k)
        k['time'] = pd.to_datetime(k["time"], unit='ms')

        k = Plot.__merge_traces(k, traces)

        start = k.iloc[0]['time'].timestamp()
        trades = [trd for trd in trades if trd[0] > start]

        fig = go.Figure(data=[go.Candlestick(
            x=k['time'], open=k['open'], high=k['high'], low=k['low'], close=k['close'])])

        traced = k.loc[k['T1'] != 0]

        fig.add_trace(go.Scatter(x=traced['time'], y=traced['T1'],
                                 line=dict(color='red', dash='dot', width=1)))
        fig.add_trace(go.Scatter(x=traced['time'], y=traced['T2'],
                                 line=dict(color='red', dash='dot', width=1)))
        fig.add_trace(go.Scatter(x=traced['time'], y=traced['T3'],
                                 line=dict(color='green', dash='dot', width=1)))
        fig.add_trace(go.Scatter(x=traced['time'], y=traced['T4'],
                                 line=dict(color='green', dash='dot', width=1)))

        """buys = [trd for trd in trades if trd[2] == 'BUY']
        sells = [trd for trd in trades if trd[2] == 'SELL']

        fig.add_trace(go.Scatter(x=[trd[0]
                                    for trd in buys], y=[trd[1] for trd in buys]))
        fig.add_trace(go.Scatter(x=[trd[0]
                                    for trd in sells], y=[trd[1] for trd in sells]))"""

        fig.write_html(fm.static['graph'])

    def __trace_match(x, traces):
        if x.timestamp() in traces.keys():
            return traces[x.timestamp()]
        else:
            return [0, 0, 0, 0]

    def __merge_traces(df, traces):
        floored = (
            df['time'] - df['time'].dt.weekday.astype('timedelta64[D]')).dt.floor('1D')
        tdf = floored.apply(Plot.__trace_match, args=[traces])
        tdf = tdf.apply(pd.Series).rename(
            columns=lambda x: ['T1', 'T2', 'T3', 'T4'][x])
        return pd.concat([df, tdf], axis=1)

class Sock:

    __queries = {}
    __enabled = False
    __port = 3003
    __n = 5

    def add(query, func):
        if query != Sock.__queries.keys():
            Sock.__queries[query] = [func]
        elif func not in Sock.__queries[query]:
            Sock.__queries[query].append(func)
        else:
            return 'Already exist!'

        if not Sock.__enabled:
            listener = threading.Thread(target=Sock.__launch)
            listener.start()

    def __launch():
        Sock.__enabled = True
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', Sock.__port))
        s.listen(Sock.__n)

        while Sock.__enabled:
            c, addr = s.accept()
            threading.Thread(target=Sock.__respond, args=(c, addr)).start()

    def __respond(c, addr):

        data = c.recv(1024).decode()

        if data == '/kill':
            Sock.__enabled = False

        elif data in Sock.__queries.keys():
            resp = [func() for func in Sock.__queries[data]]
            c.send(json.dumps(resp).encode())
            time.sleep(0.1)

class Globals:
    variables = {}

    def get(key, parent=None):
        try:
            if parent == None:
                return Globals.variables[key]
            else:
                return Globals.variables[parent][key]
        except Exception as a:
            fm.log('runtime_errors', 'Globals.get key error: ' + str(a))

    def set(key, var, parent=None):
        try:
            if parent == None:
                Globals.variables[key] = var
            else:
                if parent not in Globals.variables.keys():
                    Globals.variables[parent] = {}
                Globals.variables[parent][key] = var
        except Exception as a:
            fm.log('runtime_errors', 'Globals.set key error: ' + str(a))

    def save():
        fm.save(Globals.variables, 'globals')
