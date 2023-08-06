# -*- coding: utf-8 -*-
"""
LINE Notifier

@author: Donggeun Kwon (donggeun.kwon@gmail.com)
"""

__version__ = '1.0.0'
__doc__ = 'https://notify-bot.line.me/doc/en/'

__all__ = ['__version__', 
		   '__doc__',
		   # 'get_token',
		   'notifier']

# class
from ._notify import Notify as notifier
# from ._auth import GetToken as get_token
