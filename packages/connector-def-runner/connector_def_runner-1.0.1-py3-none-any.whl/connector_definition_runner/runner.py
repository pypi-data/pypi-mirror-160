import os
import glob
import yaml
import chevron
import argparse
import json
import importlib.util
from requests import Session
from authenticate import Authenticate
from urllib.parse import urljoin


class Runner(Authenticate):
    def __init__(self, action_name, asset_name='asset'):
        # Load action/asset data
        self.asset_manifest, self.action_manifest = self._load_schemas(action_name, asset_name)
        self.asset, self.inputs = self._load_data()

        # Build session
        self.session = Session()
        http_proxy = os.getenv('http_proxy') or self.asset.get('http_proxy')
        self.session.proxies = {
            'http_proxy': http_proxy,
            'https_proxy': http_proxy
        }
        self.session.verify = os.getenv('verify') or self.asset.get('verify', True)

        super(Runner, self).__init__(self.session, self.asset, self.asset_manifest)

    @staticmethod
    def _load_schemas(action_name, asset_name):
        manifests = glob.glob('../**/*.yaml', recursive=True)
        asset_manifest = None
        action_manifest = None
        for manifest in manifests:
            # All Swimlane connector schemas should have schema property.
            try:
                schema = yaml.safe_load(open(manifest).read())
                schema_type = schema['schema']
                if schema_type in ['asset/1'] and schema['name'] == asset_name:
                    asset_manifest = schema

                if schema_type in ['action/1'] and schema['name'] == action_name:
                    action_manifest = schema
            except:
                pass

        return asset_manifest, action_manifest

    @staticmethod
    def _load_data():
        inputs = json.loads(os.getenv('INPUTS', '{}'))
        asset = {}
        asset_keys = os.getenv('ASSET_KEYS', '').split(',')
        for k in inputs.keys():
            if k in asset_keys:
                asset[k] = inputs[k]

        for k in asset_keys:
            del inputs[k]

        return asset, inputs

    def get_endpoint(self):
        # Mustache if available if not returns string as is.
        return chevron.render(self.action_manifest['meta']['endpoint'], self.inputs.get('path_parameters', {}))

    def get_kwargs(self):
        # todo can we handle files automatically.
        return {
            'params': self.inputs.get('query_parameters'),
            'json': self.inputs.get('json_body'),
        }

    def parse_response(self, response):
        try:
            json_body = response.json()
        except:
            json_body = {}

        # todo: can we handle files automatically?
        # todo: should we parse the raw http response? What format should we return.

        return {
            'status_code': response.status_code,
            'response_headers': response.headers,
            'data': json_body,
            'response_text': response.text,
            'raw_response': response.raw
        }

    def run(self):
        response = self.session.request(
            self.action_manifest['meta']['method'],
            urljoin(self.asset['server'], self.get_endpoint()),
            **self.get_kwargs()
        )
        return self.parse_response(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='The connector action to run')
    args = parser.parse_args()

    # check if action has an override script
    glob_path = '../**/{}.py'.format(args.action)
    action_override = glob.glob(glob_path, recursive=True)
    if action_override and len(action_override) == 1:
        spec = importlib.util.spec_from_file_location("module.name", action_override[0])
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        resp = mod.RunnerOverride(args.action).run()
    else:
        resp = Runner(args.action).run()
    print('::set-output {}'.format(resp))
    return resp


if __name__ == 'main':
    main()
