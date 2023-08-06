
class Authenticate:
    def __init__(self, session, asset, security):
        self.session = session
        self.security = security
        self.asset = asset
        self.params = {}

        self.authentication_handler()

    def authentication_handler(self):
        auth_map = {
            'apiKey': self.apikey_auth,
        }

        auth_map[self.security['type']]()

        return self.session

    def apikey_auth(self):
        switcher = {
            'header': self.session.headers.update({
                self.security['name']: self.asset[self.security['name']]
            }),
            'cookie': NotImplementedError,
            'query': self.params.update({
                self.security['name']: self.asset[self.security['name']]
            }),
        }

        switch = switcher[self.security['in']]

        # todo: remove this once all switches are implemented
        if callable(switch):
            raise switch()

        return self.session

    def http_auth(self):
        raise NotImplementedError()

    def oauth2(self):
        raise NotImplementedError()
