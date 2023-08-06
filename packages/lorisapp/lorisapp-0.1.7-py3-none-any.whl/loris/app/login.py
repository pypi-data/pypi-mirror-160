"""Login classes
"""

from flask_login import UserMixin
import datajoint as dj
import warnings
import pymysql
import numpy as np

from loris import config
from loris.errors import LorisError


class User(UserMixin):

    def __init__(self, user_name):
        print(config['connection'])
        
        self.users = config.users_dataframe
        self.user_name = user_name
        self.user_bool = self.users[config['user_name']] == self.user_name
        self._user_exists = np.sum(self.user_bool)

        if self._user_exists > 1:
            raise LorisError('More than a single user entry')
        
    @property
    def entry(self):
        return self.users[self.user_bool].iloc[0]

    @property
    def user_exists(self):
        return self._user_exists

    def get_id(self):
        return str(self.user_name)

    @property
    def is_active(self):
        if config['user_active'] is None:
            return True
        return bool(self.entry[config['user_active']])

    @property
    def is_authenticated(self):
        return self.entry['is_authenticated']
    
    def authenticate(self):
        config.users_dataframe.loc[self.user_bool, 'is_authenticated'] = True

    def check_password(self, password):
        # check password in mysql database
        try:
            config.conn(
                user=self.user_name,
                password=password,
                reset=True
            )
            success = True
            self.authenticate()
        except Exception:
            success = False
        config.conn(reset=True)
        return success
