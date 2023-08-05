from binpan import binpan


a = binpan.Symbol(symbol='btcusdt',
                  tick_interval='1m',
                  time_zone='Europe/Madrid',
                  limit=2000,
                  closed=True,
                  from_redis=True)
print(a.df['Open timestamp'].diff().value_counts())
print(a)

b = binpan.Symbol(symbol='ethusdt',
                  tick_interval='1m',
                  start_time='2022-07-13 01:00:00',
                  end_time='2022-07-14 17:00:00',
                  time_zone=None,
                  closed=True,
                  from_redis=True)
print(b.df['Open timestamp'].diff().value_counts())
print(b)

c = binpan.Symbol(symbol='btcusdt',
                  tick_interval='1m',
                  start_time='2022-07-13 18:00:00',
                  time_zone='Europe/Madrid',
                  closed=True,
                  limit=5000,
                  from_redis=True)
print(c.df['Open timestamp'].diff().value_counts())
print(c)
