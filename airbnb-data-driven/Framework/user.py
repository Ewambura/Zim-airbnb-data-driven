
from pathlib import Path
import pymysql
import datetime
import hashlib
from baseObject import baseObject

class user(baseObject):
    def __init__(self, config_path='config.yml'):
        self.setup(config_path)
        print(type(self).__name__)
        self.roles=[{'value':'guest','text':'Guest'},{'value':'owner','text':'Property Owner'},{'value':'admin','text':'Admin'}]

    def verify_new(self):
        self.errors = []
        
        if '@' not in self.data[0]['email']:
            self.errors.append('Email must contain @')
        if self.data[0]['role'] not in self.rolelist():
            self.errors.append('Role does not exist')
        if len(self.data[0]['password']) < 3:
            self.errors.append('Password must be at least 3 characters long')
        if self.data[0]['password2']!=self.data[0]['password']:
            self.errors.append('Password and Password2 must match')
        self.data[0]['password'] = self.hashpassword(self.data[0]['password'])
        u = user(self.config_path)
        u.getByField('email',self.data[0]['email'])
        if len(u.data) > 0:
            self.errors.append(f"Email address is already in use. ({self.data[0]['email']})")
        
        if len(self.errors) == 0:
            return True
        else:
            return False
    def verify_update(self):
        self.errors = []
        if '@' not in self.data[0]['email']:
            self.errors.append('Email must contain @')
        if self.data[0]['role'] not in self.rolelist():
            self.errors.append('Role does not exist')
        if 'password2' in self.data[0]:
            if len(self.data[0]['password']) < 3:
                self.errors.append('Password must be at least 3 characters long')
            if self.data[0]['password2'] != self.data[0]['password']:
                self.errors.append('Password and Password2 must match')
            if len(self.errors) == 0:
                self.data[0]['password'] = self.hashpassword(self.data[0]['password'])
        if len(self.errors) == 0:
            return True
        else:
            return False

    def tryLogin(self,un, pw):
        self.data = []
        pw=self.hashpassword(pw)
        print()
        sql = f'''SELECT * FROM `{self.tn}` WHERE `email` = %s AND `password` = %s;'''
        self.cur.execute(sql,[un,pw])    
        for row in self.cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        return False

    def rolelist(self):  
        rolelists= []
        for item in self.roles:
            rolelists.append((item['value']))
        return rolelists
    
    def hashpassword(self,password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()