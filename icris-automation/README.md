# icris_automation

**icris_automation** is a Python automation tool aimed at carrying out tasks such as document purchasing on the Hong Kong government's ICRIS website with convenience and efficiency.

The package is highly modularized, making it easy to modify and extend the functionality provided. Different parts of the ICRIS website are represented as classes--based on the Page-Object Model--in the `website_layout` module; functions associated with navigating the website and carrying out tasks across multiple pages are defined in the `navigation` module; and functions related to managing data are defined in the `data_processing` module. In the context of this project, an `identifier` is a registered company name or a Companies Registry Number through which a coporate entity in Hong Kong can be identified independently.

## Installation

The package relies on the Python bindings of Selenium. [Here](https://selenium-python.readthedocs.io/installation.html) are the installation instructions. Currently, the project supports bindings for Firefox  and PhantomJS for visible and headless operation respectively (see the function `init_browser` in the `navigation` module for more details).

The package itself can be installed by following the instructions detailed [here](https://cets.seas.upenn.edu/answers/install-python-module.html).

## Usage

The tool can be imported into the Python interpreter as a package and be used from the command line. 

Running it in from the Python interpreter:
```Python
>>> from icris_automation import *
>>> companies_list = ['Company X', 'Company Y']
>>> browser = init_browser(headless=False) # Open Firefox
>>> browser = init_icris(browser)
>>> # Cart documents and return a dataframe containing information about the process
>>> status_df = process_requests(
...                            companies_list,
...                            browser,
...                            document_type='Annual Return',
...                            num_doc=3,
...                            )
```

Running it from the command line:
```Bash
$ python -m icris_automation entities.txt Annual\ Return 3 -p
```

## License

This project is distributed under the [MIT](https://github.com/adityaverma415/icris_automation/blob/master/LICENSE) license. 
