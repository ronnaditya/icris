"""
icris_automation - an automation framework for carrying out tasks on the
Hong Kong government's ICRIS website.

**icris_automation** provides convenient classes based on the 
Page Object Model to make redundant tasks such as document purchasing
from the ICRIS website convenient and simple. The framework is highly
modularized, making it easy to modify and extend the functionality 
provided. In the context of this project, an `identifier` is a company name
or a Companies Registry Number through which a coporate entity in Hong
Kong can be identified.

When imported into Python Interactive, all functions defined in the modules
`navigation`, `website_layout`, and `data_processing` are made available to the
user.

Usage
-----
>>> companies_list = ['Company X', 'Company Y']
>>> browser = init_icris(init_browser(headless=False))
>>> status_df = process_requests(companies_list, 'Annual Return', 3)

"""

from .data_processing import *
from .navigation import *
from .website_layout import *
