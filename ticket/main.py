# -*- coding: UTF-8 -*-
from ticket.sence.chrome import Chrome
from ticket.train.engine import Engine
from ticket.resolve.resolver import Resolver

# ch = Chrome()
# ch.run()

start = '重庆'
end = '成都'
date = '2018-11-28'

engine = Engine()
no = True
while no:
    try:
        results = engine.query(start, end, date)
        resolver = Resolver()
        has = resolver.left_ticket(results)
        if has:
            print("已经有余票，请尽快购买！")
            no = False
    except Exception as ex:
        ch = Chrome()
        ch.run()
