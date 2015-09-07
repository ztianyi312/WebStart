'''
Created on 2015年9月6日

@author: zhoutianji
'''

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web
from tyzhou.DBUtils import dbUtils
from jinja2 import Template,Environment, PackageLoader

@asyncio.coroutine
def user(request):
    id = request.match_info['id']
    rs = yield from __db.select("select * from user where user_id=?", id);
    template = __env.get_template('index.html')
    return web.Response(body=template.render(name='tyzhou', user=rs[0]).encode('utf-8'))
    #return web.Response(body=b'<h1>Index</h1>')
    
@asyncio.coroutine
def hello(request):
    return web.Response(body=b'<h1>hello</h1>')

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/user/{id}', user)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = yield from loop.create_server(app.make_handler(), 'localhost', 8888)
    
    global __env 
    __env = Environment(loader=PackageLoader('template', ''))
    
    print('Server started at http://127.0.0.1:8000...')
    return srv


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    global __db
    __db=dbUtils(loop, host='zudiantestdb.mysql.rds.aliyuncs.com', port=3306, user='zudian', password='2014zudianbigger', db='zudian')
    loop.run_until_complete(init(loop))
    loop.run_forever()
