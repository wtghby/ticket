# -*- coding: UTF-8 -*-
from ticket.sence.chrome import Chrome
from ticket.train.engine import Engine

# ch = Chrome()
# ch.run()

start = '重庆'
end = '成都'
date = '2018-11-28'

engine = Engine()
engine.query(start, end, date)
