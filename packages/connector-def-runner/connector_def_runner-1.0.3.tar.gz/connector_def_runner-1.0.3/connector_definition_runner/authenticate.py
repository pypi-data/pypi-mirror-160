
class Authenticate:
    def __init__(self, session, asset, asset_manifest):
        self.session = session
        self.asset_manifest = asset_manifest
        self.asset = asset

        self.authentication_handler()

    def authentication_handler(self):
        security = self.asset_manifest['meta']['security']
        auth_map = {
            'apiKey': self.apikey_auth,
        }

        auth_map[security['type']]()

        return self.session

    def apikey_auth(self):
        security = self.asset_manifest['meta']['security']
        switcher = {
            'header': self.session.headers.update({
                security['name']: self.asset[security['name']]
            }),
            'cookie': NotImplementedError,
            'query': NotImplementedError,
        }

        switch = switcher[security['in']]

        # todo: remove this once all switches are implemented
        if callable(switch):
            raise switch()

        return self.session

    def http_auth(self):
        raise NotImplementedError()

    def oauth2(self):
        raise NotImplementedError()
