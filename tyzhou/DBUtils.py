#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 2015年9月2日

@author: zhoutianji
'''

import asyncio, logging
logging.basicConfig(level=logging.INFO)
import aiomysql


def log(sql, args=()):
    logging.info('SQL: %s' % sql)

class dbUtils(object):
    
    
    def __init__(self, loop, **kw):
        self.loop = loop
        self.kw = kw
        f= self.create_pool(loop, **kw)
        loop.run_until_complete(f)
        dbUtils.db = self
        logging.info('database connection pool created')
        logging.info(type(self.pool))
    '''
    classdocs
    '''
    @asyncio.coroutine
    def create_pool(self, loop, **kw):
        logging.info('create database connection pool...')
        self.pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
        )
        
    @asyncio.coroutine
    def select(self, sql, args, size=None):
        log(sql, args)
        #logging.info(type((yield from self.pool)))
        with (yield from self.pool) as conn:
            cur = yield from conn.cursor(aiomysql.DictCursor)
            yield from cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = yield from cur.fetchmany(size)
            else:
                rs = yield from cur.fetchall()
            yield from cur.close()
            logging.info('rows returned: %s' % len(rs))
            return rs
    
    @asyncio.coroutine
    def execute(self, sql, args, autocommit=True):
        log(sql)
        with (yield from self.pool) as conn:
            if not autocommit:
                yield from conn.begin()
            try:
                cur = yield from conn.cursor()
                yield from cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
                yield from cur.close()
                if not autocommit:
                    yield from conn.commit()
            except BaseException as e:
                if not autocommit:
                    yield from conn.rollback()
                raise
            return affected
        
    @asyncio.coroutine
    def insert(self, sql, args, autocommit=True):
        log(sql)
        with (yield from self.pool) as conn:
            if not autocommit:
                yield from conn.begin()
            try:
                cur = yield from conn.cursor()
                yield from cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
                lastId = cur.lastrowid
                yield from cur.close()
                if not autocommit:
                    yield from conn.commit()
            except BaseException as e:
                if not autocommit:
                    yield from conn.rollback()
                raise
            return affected,lastId
        
@asyncio.coroutine
def testAsync(db):
    rs = yield from db.select("select * from user where user_id=?", 1);
    logging.info(type(rs))
    logging.info(rs[0])
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    db=dbUtils(loop, host='zudiantestdb.mysql.rds.aliyuncs.com', port=3306, user='zudian', password='2014zudianbigger', db='zudian')
    
    
    loop.run_until_complete(testAsync(db))
    
    
    
    