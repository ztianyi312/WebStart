'''
Created on 2015年9月2日

@author: zhoutianji
'''

import tornado.web
from tornado import gen
from tyzhou.user import User

class AppHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, userId):
        user=yield from User.find(userId)
        
        #u = User(name=123131, nickname='asdqweweq', id=23923)
        #yield from u.save()
        #print(u.id)
        
        self.render("user.html", user=user)