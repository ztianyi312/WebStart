#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 2015年9月2日

@author: zhoutianji
'''
import sys
sys.path.append("/Users/zhoutianji/Documents/workspace/WebStart/tyzhou/*")
from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.web
from tornado import gen

import asyncio,logging
from tyzhou.DBUtils import dbUtils
import tyzhou.gl
logging.basicConfig(level=logging.INFO)
from tyzhou.appHandler import AppHandler

'''
def coroutine(func):
  func = asyncio.coroutine(func)
  def decorator(*args, **kwargs):
    future = tornado.concurrent.Future()
    def future_done(f):
      try:
        future.set_result(f.result())
      except Exception as e:
        future.set_exception(e)
    asyncio.async(func(*args, **kwargs)).add_done_callback(future_done)
    return future
  return decorator

def future_wrapper(f):
  future = asyncio.Future()
  def handle_future(f):
    try:
      future.set_result(f.result())
    except Exception as e:
      future.set_exception(e)
  tornado.ioloop.IOLoop.current().add_future(f, handle_future)
  return future
'''
class MainHandler(tornado.web.RequestHandler):
    #@coroutine
    @gen.coroutine
    def get(self):
        w = asyncio.async(asyncio.sleep(5))
        yield from asyncio.sleep(1)#运行结束前 后面的代码不会执行
        rs = yield from Db().select("select * from user where user_id=?", 438);
        rs2 = yield from Db().select("select * from user where user_id=?", 438);
        t1 = Db().select("select * from user where user_id=?", 438)
        t2 = Db().select("select * from user where user_id=?", 349)
        f1 = asyncio.async(t1)
        f2 = asyncio.async(t2)
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(rs)
        logging.info(rs[0])
        yield f1
        yield f2;
        logging.info(f1.result())
        logging.info(f2)
        #logging.info(next(t1))
        self.render('index.html', name='tyzhou', user=f2.result()[0])
        #return rs



class IconHandler(tornado.web.RequestHandler):
    def get(self):
        with open('/Users/zhoutianji/Downloads/favicon.ico', 'rb') as f:
            self.set_header('Content-Type', 'image/x-icon')
            self.write(f.read())

settings = {
    "template_path": "../template",
    "debug": True
}

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None
    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance

class Db(dbUtils, metaclass=Singleton):
    def __init__(self):
        loop = asyncio.get_event_loop()
        dbUtils.__init__(self, loop, host='zudiandb.mysql.rds.aliyuncs.com', port=3306, user='zudian', password='2014zudianbigger', db='zudian')




def makeApp():
    return tornado.web.Application([
    (r"/", MainHandler),
    (r"/favicon.ico", IconHandler),
    (r"/app/([0-9]+)", AppHandler),

    ], **settings)

def getDB():
    global _db
    if _db is None:
        loop = asyncio.get_event_loop()
        _db = dbUtils(loop, host='zudiantestdb.mysql.rds.aliyuncs.com', port=3306, user='zudian', password='2014zudianbigger', db='zudian')
    return _db



if __name__ == '__main__':

    AsyncIOMainLoop().install()
    application = makeApp()
    application.listen(8888)

    loop = asyncio.get_event_loop()
    #getDB()
    tyzhou.gl._db = Db()
    #Db()

    #dbUtils(loop, host='zudiandb.mysql.rds.aliyuncs.com', port=3306, user='zudian', password='2014zudianbigger', db='zudian')
    asyncio.get_event_loop().run_forever()
