# INECO Core Methods

This module contains the core methods of the INECO library.


## **Installation**

    pip install inecocores

## **Usage**
    
    form inecocores.core import Service
    s = Service()
    s.check_report(customerId='1', reportId="123", parameters={"a": 1, "b": 2, "c": 3})
    sample_parameter = {
        'js_parameter_name': 'IDS',
        'js_parameter_value': 'sale_order.id = 32069',
    }
    result = s.call_report(customerId='1', reportId="123", parameters=sample_parameter)