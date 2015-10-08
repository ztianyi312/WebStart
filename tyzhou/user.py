'''
Created on 2015年9月7日

@author: zhoutianji
'''
from tyzhou.orm import Model,IntegerField,StringField

class User(Model):
    '''
    classdocs
    '''
    _db="User"

    id = IntegerField('user_id', True)
    name = StringField('username')
    nickname = StringField('nickname')
    city = StringField('city')

    def updateNickname(self, userId, nickname):
        Model.update()
