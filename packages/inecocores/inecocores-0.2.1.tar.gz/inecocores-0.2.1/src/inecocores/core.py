#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests


class Service:
    server = 'https://dev.ineco.co.th'

    def check_report(self, customerId, reportId, parameters):
        """
        Check report existing
        :param customerId:
        :param reportId:
        :param parameters:
        :return: {'parameters': {'a': 1, 'b': 2, 'c': 3}, 'path': '/path/name/', 'status': 'ok'}
        """
        data = {
            'customerId': customerId,
            'reportId': reportId,
            'parameters': parameters
        }
        r = requests.post(Service.server + '/status', json=data)
        result = r.json()
        return result

    def call_report(self, customerId, reportId, parameters):
        """
        Check report existing
        :param customerId:
        :param reportId:
        :param parameters:
        :return: {'status': 'ok', 'output': 'base64format', 'type':'ineco'}
        """
        data = {
            'customerId': customerId,
            'reportId': reportId,
            'parameters': parameters
        }
        r = requests.post(Service.server + '/callreport', json=data)
        result = r.json()
        return result

    def get_youtube(self, version, model, viewtype):
        data = {
            'version': version,
            'model': model,
            'viewtype': viewtype
        }
        r = requests.post(Service.server + '/youtube', json=data)
        result = r.json()
        return result


# if __name__ == "__main__":
#     s = Service()
#     s.check_report(customerId='1', reportId="123", parameters={"a": 1, "b": 2, "c": 3})
#     sample_parameter = {
#         'js_parameter_name': 'IDS',
#         'js_parameter_value': 'sale_order.id = 32069',
#     }
#     result = s.call_report(customerId='1', reportId="123", parameters=sample_parameter)
#     print(result['output'])
