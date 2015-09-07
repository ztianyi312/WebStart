'''
Created on 2015年9月2日

@author: zhoutianji
'''

import tornado.web

class baseHandler(tornado.web.RequestHandler):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        pass

    def get_current_user(self):
        userId = self.get_query_arguments('userId', False);
        return tornado.web.RequestHandler.get_current_user(self)