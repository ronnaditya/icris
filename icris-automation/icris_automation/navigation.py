"""
This module defines convenient functions to automate navigation of 
the ICRIS website and carry out tasks such as purchasing documents 
and clearing the shopping cart.

"""

import traceback

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException
from selenium.webdriver.common.action_chains import ActionChains

try:
    from .website_layout import *
except:
    from website_layout import *

def scroll_to_element(browser, element):
    """
    Scroll to the the element on the passed browser.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver.Webdriver
        An instance of the Selenium Webdriver object representing the
        browser of the element
    element : selenium-webdriver.WebElement
        Element to scroll to

    """

    x = element.location['x']
    y = element.location['y']
    scroll_by_coord = f'window.scrollTo({x},{y});'
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    browser.execute_script(scroll_by_coord)
    browser.execute_script(scroll_nav_out_of_way)

def init_browser(headless=True):
    """
    Open a browser for web surfing.

    Parameters
    ----------
    headless : bool, optional
        Specify whether to make the browser visible, default `True`
    
    Returns
    -------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        A selenium WebDriver instance

    """

    if headless:
        browser = webdriver.PhantomJS()     
    else:
        browser = webdriver.Firefox()
    return browser

def init_icris(browser):
    """
    Open the ICRIS website and navigate to the home page.
    
    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        A Selenium WebDriver instance
    
    Returns
    -------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The final active browser instance after completing the login procedure

    """

    entry = ICRISEntryPage(browser)
    login = LoginPage(browser)

    entry.launch_icris()
    entry.navigate_to_login()
    login.login()

    return browser

def init_webpages(browser):
    """
    Instantiate website objects for various parts of the ICRIS website 
    linked to the passed Selenium WebDriver instance. 
    
    Methods of the returned class instances are wrapped around the passed
    Selenium WebDriver instance and can be called to navigate 
    the ICRIS website as required.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        A Selenium WebDriver instance

    Returns
    -------
    main_menu : class instance
        Object with wrapped methods to interact with the main menu,
        which can be accessed from all pages of the ICRIS website
    search : class instance
        Object with wrapped methods to navigate the search page
    companies : class instance
        Object with wrapped methods to navigate the companies index page
    info : class instance
        Object with wrapped methods to navigate the companies information page
    doc_index : class instance
        Object with wrapped methods to navigate the document index page

    """

    main_menu = MainMenu(browser)
    search = SearchPage(browser)
    companies = CompaniesIndexPage(browser)
    info = CompanyInformationPage(browser)
    doc_index = DocumentIndexPage(browser)

    return main_menu, search, companies, info, doc_index

def purchase_documents(browser):
    """
    Purchase documents in the cart.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        A Selenium WebDriver instance

    """

    main_menu, check_out = MainMenu(browser), CheckOutPages(browser)
    main_menu.navigate_to_shopping_cart()
    check_out.deselect_all_items()
    check_out.select_in_batch()
    check_out.checkout()
    check_out.proceed()
    ActionChains(browser).move_to_element(check_out.DEDUCT_FROM_ACCOUNT_BUTTON()).perform()
    # check_out.DEDUCT_FROM_ACCOUNT().click() # The final button to purchase documents

def clear_cart(browser):
    """
    Empty cart.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        A Selenium WebDriver instance

    """
    main_menu, check_out = MainMenu(browser), CheckOutPages(browser)
    main_menu.navigate_to_shopping_cart()
    check_out.delete_all_items()

def process_request(identifier, browser, document_type='Annual Return', num_doc=1, status_df=None):
    """
    Search ICRIS for the passed identifier, analyze the returned documents, 
    and cart the documents depending on whether we purchased 
    the document before.

    Parameters
    ----------

    identifier : str
        Name or Companies Registry Number of the company to 
        purchase documents for
    browser : selenium.webdriver.remote.webdriver.WebDriver
        An instance of Selenium WebDriver
    document_type : str, optional
        Type of document to be purchased, default `Annual Return`
    num_doc : int, optional
        Number of documents of type `document_type` to be purchased
    status_df : pandas.DataFrame
        Dataframe object to append data related to the status of the
        operations to

    Returns
    -------
    status_df : pandas.DataFrame
        Dataframe object containing information about the status of
        the carting operations with the following columns

    """

    if status_df is None:
        status_df = pd.DataFrame()

    cart_number = 0

    try:
        try: # Check if there were no matches for the passed identifier
            companies = CompaniesIndexPage(browser)
            companies.NO_MATCHES()
            raise Exception(f"No matches found for identifier: {identifier}")
        except NoSuchElementException:
            pass

        main_menu, search, companies, info, doc_index = init_webpages(browser)
        exception = 'None'

        main_menu.navigate_to_search_page()
        
        if identifier.isdigit():
            search.crNo_search(identifier)
        else:
            search.name_search(identifier)

        if identifier.isdigit():
            try:
                companies.choose_number(identifier)
            except TimeoutError:
                raise Exception(f"No companies found for company number {identifier}")
        else:
            try:
                companies.choose_name(identifier)
            except TimeoutError:
                raise Exception(f"No companies found for company name {identifier}")

        info.proceed()
        doc_index.list_documents()
        cart_status, cart_number = doc_index.index_and_cart(document_type, num_doc)

        row = pd.Series([identifier,document_type, str(cart_status).upper(), cart_number, exception])
        status_df = status_df.append(row, ignore_index = True)

        return status_df

    except Exception:
        exception = traceback.format_exc(7)

        try:
            cart_status 
        except NameError:
            cart_status  = False

        row = pd.Series([identifier, document_type, str(cart_status).upper(), cart_number, exception])
        status_df = status_df.append(row, ignore_index = True)

        return status_df

def process_requests(identifier_list, browser, document_type='Annual Return', num_doc=1, status_df=None):
    """
    Search ICRIS for the passed identifiers, analyze the returned documents, 
    and cart the documents depending on whether we purchased 
    the document before.

    Parameters
    ----------

    identifier_list : list
        List containing names or Companies Registry Numbers of the 
        companies to purchase documents for
    browser : selenium.webdriver.remote.webdriver.WebDriver
        An instance of Selenium WebDriver
    document_type : str, optional
        Type of document to be purchased, default `Annual Return`
    num_doc : int, optional
        Number of documents of type `document_type` to be purchased
    status_df : pandas.DataFrame
        Dataframe object to append data related to the status of the
        operations to

    Returns
    -------
    status_df : pandas.DataFrame
        Dataframe object containing information about the status of
        the carting operations with the following columns:
        `identifier`, `document_type`, `purchase_status`, 
        `document_count`, `traceback`

    """

    if status_df is None: # Instantiate a dataframe object if one was not passed
        status_df = pd.DataFrame()

    assert isinstance(identifier_list, list), "The first argument must be a list"

    print("\n\n\t\t****Processing documents...****\n\n")

    for count, identifier in enumerate(identifier_list):
        try:
            identifier = identifier.decode() # Convert binary data
        except:
            pass

        status_df = process_request(identifier, document_type, browser, num_doc, status_df)
        status_df.columns = ['identifier', 'document_type', 'purchase_status', 'document_count','traceback']

        print(f"\n\n\t\t****{str(count + 1)} out of {str(len(identifier_list))} documents processed****")
    
    print("\n\n\t\t****Document processing complete****\n\n")

    return status_df
