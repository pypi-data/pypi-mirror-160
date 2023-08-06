import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

"""
LINE Notify API

Copyright © LINE Corporation
"""


class Notify:
    def __init__(self, token):
        self.token = token
        self.tokens = {self.token:0} # token list which used
        self.retries =  Retry(total=3,
                              backoff_factor=1,
                              status_forcelist=[500, 502, 503, 504])
        self.headers={'Authorization': 'Bearer ' + self.token}
        self.api_url = 'https://notify-api.line.me/api/notify'
        self.start_msg = None
        self.end_msg = 'End, this msg is sent from Line token "' + self.token + '".'

    def deco(self, func):
        return self._sender(self, func)

    class _sender(object):
        def __init__(self, outer, func):
            self.func = func
            self.smsg = outer.start_msg
            self.emsg = outer.end_msg
            self.noti = outer.notify
        
        def __call__(self, *args, **kwargs):
            if self.smsg is not None: self.noti(self.smsg)
            ret = self.func(*args, **kwargs)
            if self.emsg is not None: self.noti(self.emsg)
            
            return ret 

    def set_msg(self, start_msg, end_msg):
        '''
        if start_msg(or end_msg) is None,
            then it will not notify 
        '''
        self.start_msg = start_msg
        self.end_msg = end_msg

        return None

    def notify(self, msg, img_path=None, limit=False):
        import warnings

        if limit and self.tokens[self.token] > 1000:
            warnings.warn("Limit count: change the token, use 'change_token()'", Warning)
            return False, self.tokens[self.token]

        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=self.retries))
		
        if img_path == None:
            response = session.post(url=self.api_url,
                                    data={'message': msg}, #1000 characters max
                                    headers=self.headers,
                                    timeout=3)
        else:
            try:
                with open(img_path, 'rb') as fd:
                    response = session.post(url=self.api_url, 
                                            data={'message': msg},
                                            headers=self.headers,
                                            files={'imageFile': fd},
                                            timeout=3)
            except:
                warnings.warn("Error: Sending Image file is failed", Warning)
				
                response = session.post(url=self.api_url,
                                        data={'message': 'Image Failed, '+msg},
                                        headers=self.headers,
                                        timeout=3)
                
        """
            Response Headers status
            
            200: Success
            400: Bad request
            401: Invalid access token
            500: Failure due to server error
        """
        if response.status_code!=200:
            warnings.warn("LINE Notify Request Failed", Warning)
            return response
        
        self.tokens[self.token] += 1
        
        return self.tokens[self.token]
        
    def change_token(self, token):
        if self.tokens.get(token) is None:
            self.token = token
            self.tokens[self.token] = 0
            self.headers={'Authorization': 'Bearer ' + self.token}
        else:
            import warnings 
            warnings.warn(str(token)+' is already used ' + str(self.tokens[token]), Warning)
            self.token = token

        return True
