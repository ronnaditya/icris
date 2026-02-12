"""
This module defines classes based on the Page Object Model that represent
different parts of the ICRIS website. Each class accepts a Selenium
WebDriver instance as an argument and wraps the associated methods
around it. This makes the program more robust and stable when reloading
the page.

"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    import credentials
    from navigation import scroll_to_element
except Exception:
    from . import credentials

class ICRISEntryPage(object):
    """
    Class representing the ICRIS entry page.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver
        A Selenium WebDriver instance

    Attributes
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The associated Selenium WebDriver instance
    wait : selenium.webdriver.supoport.wait.WebDriverWait
        The associated Selenium WebDriverWait instance
    registered_user_xpath : str
        XPath representing the `Registered User` radio button
    temporary_message_xpath : str
        XPath representing the temporary `Click Here` link which will
        be discarded on 12/01/2020selenium.webdriver.remote.webelement.WebElement
    REGISTERED_USER_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance representing the
        `Registered User` radio button
    TEMPORARY_MESSAGE_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance representing the
        temporary `Click Here` link which will be discarded on 12/01/2020

    """

    url = 'https://www.icris.cr.gov.hk/csci/'

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 30)

        self.registered_user_xpath = "//img[@src='images/registered_01.gif']"
        self.temporary_message_xpath = "//a[@href='normal.html']" # Remove after 12/01/2020

        self.REGISTERED_USER_BUTTON = lambda: self.browser.find_element_by_xpath(self.registered_user_xpath)
        self.TEMPORARY_MESSAGE_BUTTON = lambda: self.browser.find_element_by_xpath(self.temporary_message_xpath)

    def launch_icris(self):
        """Open the `url` and dismiss all initial messages"""

        self.browser.get(self.url)

        self.TEMPORARY_MESSAGE_BUTTON().click() # Temporary message which will last till 12/01/2020
        main_window = self.browser.current_window_handle
        self.browser.switch_to.window(self.browser.window_handles[1])

        self.browser.close()
        self.browser.switch_to.window(main_window)

    def navigate_to_login(self):
        """Navigate to the login page"""

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.registered_user_xpath)))

        self.REGISTERED_USER_BUTTON().click()
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

class LoginPage(object):
    """
    Class representing the login page.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver
        A Selenium WebDriver instance

    Attributes
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The associated Selenium WebDriver instance
    wait : selenium.webdriver.supoport.wait.WebDriverWait
        The associated Selenium WebDriverWait instance
    username_xpath : str
        XPath representing the `Username` field
    password_xpath : str
        XPath representing the `Password` field
    submit_xpath : str
        XPath representing the `Submit` button
    check_box_xpath : str
        XPath representing checkboxes, uses string formatting with %
    USERNAME_FIELD : lambda function
        Lambda function returning a Selenium WebElement instance representing 
        the `Username` field
    PASSWORD_FIELD : lambda function
        Lambda function returning a Selenium WebElement instance representing 
        the `Password` field
    SUBMIT_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance representing 
        the `Submit` button
    CHECKBUTTONS : list
        List of Selenium WebElement instances representing each checkbox
        button

    """

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 30)

        self.username_xpath = "//input[@name='username']"
        self.password_xpath = "//input[@name='password']"
        self.submit_xpath = "//input[@value='Accept, Submit & Login']"
        self.check_box_xpath = "//input[@id='CHKBOX_0%s']"

        self.USERNAME_FIELD = lambda: self.browser.find_element_by_xpath(self.username_xpath)
        self.PASSWORD_FIELD = lambda: self.browser.find_element_by_xpath(self.password_xpath)
        self.SUBMIT_BUTTON = lambda: self.browser.find_element_by_xpath(self.submit_xpath)
        self.CHECKBUTTONS = lambda: [self.browser.find_element_by_xpath(
            self.check_box_xpath % (i + 1)) for i in range(9)]

    def login(self):
        """Login to ICRIS using variables defined in the `credentials` module"""

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.username_xpath)))

        self.USERNAME_FIELD().send_keys(credentials.username)
        self.PASSWORD_FIELD().send_keys(credentials.password)

        for checkbutton in self.CHECKBUTTONS():
            checkbutton.click()

        self.SUBMIT_BUTTON().click()

class MainMenu(object):
    """
    Class representing the Main Menu.

    This class is the parent class of every class defined after this class
    as the main menu is available on every page after login.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver
        A Selenium WebDriver instance

    Attributes
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The associated Selenium WebDriver instance
    wait : selenium.webdriver.supoport.wait.WebDriverWait
        The associated Selenium WebDriverWait instance
    search_xpath : str
        XPath representing the `Search` menu
    image_record_xpath : str
        XPath representing the `Image Record` option under the
        `Search` menu
    shopping_xpath : str
        XPath representing the `Shopping` menu
    check_out_xpath : str
        XPath representing the `Check Out` option under the `Shopping` menu
    logout_xpath : str
        XPath representing the `Logout` button
    SEARCH_MENU : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Search` menu
    IMAGE_RECORD_OPTION : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Image Record` option under the `Search` menu
    SHOPPING_MENU : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Shopping` menu
    CHECK_OUT_OPTION : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Check Out`
        option under the `Shopping` menu
    LOGOUT_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Logout` button

   """

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 30)

        self.search_xpath = "//div[@class='m0l0i'][contains(translate(., '\u00A0', ' '), 'Search')]"
        self.image_record_xpath = "//div[@class='m0l1i'][contains(translate(., '\u00A0', ' '), 'Image Record (including Document Index)')]"
        self.shopping_xpath = "//div[@class='m0l0i'][contains(translate(., '\u00A0', ' '), 'Shopping')]"
        self.check_out_xpath = "//div[@class='m0l1i'][contains(translate(., '\u00A0', ' '), 'Check out Shopping Cart')]"
        self.logout_xpath = "//div[@class='m0l0i'][contains(translate(., '\u00A0', ' '), 'Logout')]"

        self.SEARCH_MENU = lambda: self.browser.find_element_by_xpath(self.search_xpath)
        self.IMAGE_RECORD_OPTION = lambda: self.browser.find_element_by_xpath(self.image_record_xpath)
        self.SHOPPING_MENU = lambda: self.browser.find_element_by_xpath(self.shopping_xpath)
        self.CHECK_OUT_OPTION = lambda: self.browser.find_element_by_xpath(self.check_out_xpath)
        self.LOGOUT_BUTTON = lambda: self.browser.find_element_by_xpath(self.logout_xpath)
    
    def navigate_to_search_page(self):
        """Navigate to the search page"""

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.search_xpath)))

        scroll_to_element(self.browser, self.SEARCH_MENU())
        ActionChains(self.browser).move_to_element(self.SEARCH_MENU()).click(self.IMAGE_RECORD_OPTION()).perform()

    def navigate_to_shopping_cart(self):
        """Navigate to the shopping cart page"""

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.shopping_xpath)))
        
        scroll_to_element(self.browser, self.SHOPPING_MENU())
        ActionChains(self.browser).move_to_element(self.SHOPPING_MENU()).click(self.CHECK_OUT_OPTION()).perform()

    def logout(self):
        """Log out of ICRIS"""
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.logout_xpath)))
        scroll_to_element(self.browser, self.LOGOUT_BUTTON())
        self.LOGOUT_BUTTON().click()

        self.wait.until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()
        self.browser.close()

class SearchPage(MainMenu):
    """
    Class representing the search page.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver
        A Selenium WebDriver instance

    Attributes
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The associated Selenium WebDriver instance
    wait : selenium.webdriver.supoport.wait.WebDriverWait
        The associated Selenium WebDriverWait instance
    name_button_xpath : str
        XPath representing the `Search` menu
    crNo_button_xpath : str
        XPath representing the `Image Record` option under the
        `Search` menu
    name_search_xpath : str
        XPath representing the `Shopping` menu
    crNo_search_xpath : str
        XPath representing the `Check Out` option under the `Shopping` menu
    submit_xpath : str
        XPath representing the `Logout` button
    NAME_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance representing the `Search` menu
    CRNO_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance representing the `Image Record`
        option under the `Search` menu
    NAME_SEARCH : lambda function
        Lambda function returning a Selenium WebElement instance representing the `Shopping` menu
    CRNO_SEARCH : lambda function
        Lambda function returning a Selenium WebElement instance representing the `Check Out`
        option under the `Shopping` menu
    SUBMIT : lambda function
        Lambda function returning a Selenium WebElement instance representing the `Logout` button

   """

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 30)
        super().__init__(self.browser)

        self.name_button_xpath = "//input[@name='radioButton'][@value='BYNAME']"
        self.crNo_button_xpath = "//input[@name='radioButton'][@value='BYCRNO']"
        self.name_search_xpath = "//input[@type='text'][@name='companyName']"
        self.crNo_search_xpath = "//input[@type='text'][@name='CRNo']"
        self.submit_xpath = "//input[@type='button'][@value='Search']"

        self.NAME_BUTTON = lambda: self.browser.find_element_by_xpath("//input[@name='radioButton'][@value='BYNAME']")
        self.CRNO_BUTTON = lambda: self.browser.find_element_by_xpath("//input[@name='radioButton'][@value='BYCRNO']")
        self.NAME_SEARCH = lambda: self.browser.find_element_by_xpath("//input[@type='text'][@name='companyName']")
        self.CRNO_SEARCH = lambda: self.browser.find_element_by_xpath("//input[@type='text'][@name='CRNo']")
        self.SUBMIT_BUTTON = lambda: self.browser.find_element_by_xpath("//input[@type='button'][@value='Search']")        

    def name_search(self, name):
        """
        Search for a company based on its registered name.
        
        Parameters
        ----------
        name : str
            Registered name of the company
        
        """

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.name_button_xpath)))

        self.NAME_BUTTON().click()
        self.NAME_SEARCH().send_keys(name)
        self.SUBMIT_BUTTON().click()

    def crNo_search(self, number):
        """
        Search for a company based on its Companies Registry Number.
        
        Parameters
        ----------
        number : str
            Companies Registry Number of the company
        
        """

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.crNo_button_xpath)))

        self.CRNO_BUTTON().click()
        self.CRNO_SEARCH().send_keys(number)
        self.SUBMIT_BUTTON().click()

class CompaniesIndexPage(MainMenu):
    """
    Class representing the companies index page.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver
        A Selenium WebDriver instance

    Attributes
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The associated Selenium WebDriver instance
    wait : selenium.webdriver.supoport.wait.WebDriverWait
        The associated Selenium WebDriverWait instance
    table_xpath : str
        XPath representing the table listing matched companies
    no_matches_xpath : str
        XPath representing the message when no matches are found
    TABLE : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the table listing matched companies
    NO_MATCHES : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the element of the message when no matches are found
    CONTENT : list
        List of Selenium WebElement instances representing each row of the
        table listing matched companies
    COMPANY_BUTTON : lambda function
        Lambda function that accepts the index of the relevant company row and 
        returns a Selenium WebDriver instance representing the link to the 
        document index page of that 

    """

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 5)
        super().__init__(self.browser)

        self.table_xpath = "//table[@class='data']"
        self.no_matches_xpath = "//font[@class='sameasbody'][contains(translate(., '\u00A0', ' '), 'NO MATCHING RECORD FOUND FOR THE SEARCH INFORMATION INPUT!')]"

        self.TABLE = lambda: self.browser.find_element_by_xpath(self.table_xpath)
        self.NO_MATCHES = lambda: self.browser.find_element_by_xpath(self.no_matches_xpath)
        self.CONTENT = lambda: [row for row in self.TABLE().find_elements_by_tag_name('tr')[1:]]
        self.COMPANY_BUTTON = lambda company: company_element.find_elements_by_tag_name('td')[2].find_element_by_tag_name('a')
    
    @staticmethod
    def companies_indexer(content, identifier):
        """
        Index the table listing.

        Parameters
        ----------
        content : list
            List of Selenium WebElement instances representing each row of the
            table listing matched companies
        identifier : str
            Registered name or the Companies Registry Number of the company
        
        Returns
        -------
        live_matches : list
            List of indices of matches of companies that are still active
        dissolved_matches : list
            List of indices of matches of companies that are dissolved
        
        """

        live_matches = []
        dissolved_matches = []

        # Check if identifier is a name or a C.R.No.
        # and index accordingly
        if identifier.isdigit():
            for (count, row) in enumerate(content[:-1]):
                data = row.find_elements_by_tag_name('td')

                crNo = data[1].text.strip()  
                company_status = data[5].text.strip()

                if identifier == crNo:
                    if company_status == 'Live':
                        live_matches.append(count)
                    else:
                        dissolved_matches.append(count)
        else:
            for (count, row) in enumerate(content[:-1]):
                data = row.find_elements_by_tag_name('td')

                title = data[2].text.strip()
                company_status = data[5].text.strip()

                if identifier == title:
                    if company_status == 'Live':
                        live_matches.append(count)
                    else:
                        dissolved_matches.append(count)

        return live_matches, dissolved_matches
            
    def choose_name(self, name):
        """
        Choose the first match of an active company based on its registered name
        if a live match was found. If no live matches were found, raise exceptions
        based on whether dissolved matches were found.

        Parameter
        ---------
        name : str
            Registered name of the company

        """

        assert name.isalpha(), '`name` must be a reistered company name'

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.table_xpath)))

        live_matches, dissolved_matches = self.companies_indexer(self.CONTENT(), name)

        if len(live_matches) > 0:
            company = content[live_matches[0]]
            COMPANY_BUTTON(company_element).click()

        elif len(dissolved_matches) > 0:
            raise Exception("The company has been dissolved")

        else:
            raise Exception(f"No matches found for company name: {name}")
        
    def choose_number(self, crNo):
        """
        Choose the first match of an active company based on its Companies Registry Number
        if a live match was found. If no live matches were found, raise exceptions
        based on whether dissolved matches were found.

        Parameter
        ---------
        name : str
            Registered name of the company

        """


        assert name.isdigit(), '`crNo` must be a Companies Registry Number'

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.table_xpath)))

        live_matches, dissolved_matches = self.companies_indexer(self.CONTENT(), crNo)

        if len(live_matches) > 0:
            company_element = content[live_matches[0]]
            COMPANY_BUTTON(company_element).click()

        elif len(dissolved_matches) > 0:
            raise Exception("The company has been dissolved")

        else:
            raise Exception(f"No matches found for Companies Registry Number: {crNo}")

class CompanyInformationPage(MainMenu):
    """
    Class representing the ICRIS entry page.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver
        A Selenium WebDriver instance

    Attributes
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The associated Selenium WebDriver instance
    wait : selenium.webdriver.supoport.wait.WebDriverWait
        The associated Selenium WebDriverWait instance
    proceed_button_xpath : str
        XPath representing the `Proceed` button
    PROCEED_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance representing the
        `Proceed` button

    """

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 30)
        super().__init__(self.browser)

        self.proceed_button_xpath = "//input[@type='submit'][@value='Proceed to Document Index']"

        self.PROCEED_BUTTON = lambda: self.browser.find_element_by_xpath(self.proceed_button_xpath)

    def proceed(self):
        """Proceed to the document index page"""

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.proceed_button_xpath)))
        self.PROCEED_BUTTON().click()

class DocumentIndexPage(MainMenu):
    """
    Class representing the check out pages.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver
        A Selenium WebDriver instance

    Attributes
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The associated Selenium WebDriver instance
    wait : selenium.webdriver.supoport.wait.WebDriverWait
        The associated Selenium WebDriverWait instance
    filing_year_menu_xpath : str
        XPath representing the `Filing Year` menu
    show_all_option_xpath : str
        XPath representing the `Show All` option under the 
        `Filing Year` menu
    table_xpath : str
        XPath representing the table listing all documents
        on the current page
    pages_menu_xpath : str
        XPath representing the menu listing pages
    go_buttons_xpath : str
        XPath representing the `Go` buttons.
        There are two go buttons with the same XPath.
    option_tag : str
        String representing the HTML tag of the options under
        the `Pages` men 
    cart_ok_button_xpath : str
        XPath representing the `OK` button which carts documents
    FILING_YEAR_MENU : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the `Filing Year` menu
    SHOW_ALL_OPTION : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the `Show All` option under the
        `Filing Year` menu
    TABLE : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the table listing all documents
        on the current page
    PAGES_MENU : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the menu listing pages
    PAGES : list
        List of Selenium WebElement instances representing different options
        under the `Pages` menu
    FILING_YEAR_GO_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the `Go` button of the `Filing Year` menu
    PAGES_MENU_GO_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the `Go` button of the `Pages` menu
    CART_OK_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance
        representing the `OK` button which carts documents
    CART_BUTTON : lambda function
        Lambda function returning a Selenium WebDriver instance
        representing the row of the document to be carted, accepts
        a Selenium WebDriver element representing the link
        of the document to be carted
    CONTENT : list
        List containing Selenium WebDriver instances representing
        rows on the document index

   """

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 30)
        super().__init__(self.browser)

        self.filing_year_menu_xpath = "//select[@name='filing_year']"
        self.show_all_option_xpath = "//option[@value='all']"
        self.table_xpath = "//table[@dwcopytype='CopyTableRow']"
        self.pages_menu_xpath = "//select[@name='SelectPage']"
        self.go_buttons_xpath = "//input[@type='submit'][@value='GO']"
        self.option_tag = 'option'
        self.cart_ok_button_xpath = "//input[@type='button'][@value='OK']"

        self.FILING_YEAR_MENU = lambda: self.browser.find_element_by_xpath(self.filing_year_menu_xpath)
        self.SHOW_ALL_OPTION = lambda: self.browser.find_elements_by_xpath(self.show_all_option_xpath)[1]
        self.TABLE = lambda: self.browser.find_element_by_xpath(self.table_xpath)
        self.PAGES_MENU = lambda: self.browser.find_element_by_xpath(self.pages_menu_xpath)
        self.PAGES = lambda: self.PAGES_MENU().find_elements_by_tag_name(self.option_tag)
        self.FILING_YEAR_GO_BUTTON = lambda: self.browser.find_elements_by_xpath(self.go_buttons_xpath)[0]
        self.PAGES_MENU_GO_BUTTON = lambda: self.browser.find_elements_by_xpath(self.go_buttons_xpath)[1]
        self.CART_OK_BUTTON = lambda: self.browser.find_element_by_xpath(self.cart_ok_button_xpath)
        self.CART_BUTTON = lambda document_row: document_row.find_elements_by_tag_name('td')[0].find_element_by_tag_name('a')
        self.CONTENT = lambda: self.TABLE().find_elements_by_tag_name('tr')[2:]
        
    def list_documents(self):
        """List all documents of the company"""

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.show_all_option_xpath)))

        self.SHOW_ALL_OPTION().click()
        self.FILING_YEAR_GO_BUTTON().click()

    def navigate_to_page(self, page_number):
        """
        Navigate to the specified page on the document index.
        
        Parameters
        ----------
        page_number : int
            The order of the page to navigate to

        """

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.pages_menu_xpath)))
        scroll_to_element(self.browser, self.PAGES_MENU())
        self.PAGES()[page_number].click()
        self.PAGES_MENU_GO_BUTTON().click()

    def check_purchase_status(self, document_row):
        """
        Check the purchase status of a given document.

        Parameters
        ----------
        document_row : selenium.webdriver.remote.webelement.WebElement
            A Selenium WebElement instance representing the HTML element of 
            the row of the document for which the purchase status is to be
            checked
        
        Returns
        -------
        purchase_status : bool
            Boolean specifying whether the documents were purchased before

        """
        # Add check for blue line
        purchase_status = False
        return purchase_status

    def return_doc_row(self, document_index, page_number = 1):
        """
        Return a Seleniu WebDriver instance representing the document
        corresponding to the passed parameters.

        Parameters
        ----------
        document_index : int
            Order of the document on the page from which the relevant document
            is to be processed
        page_number : int
            The page number of the page on which the document is listed
        
        Returns
        ----------
        document_row : selenium.webdriver.remote.webelement.WebElement
            A Selenium WebElement instance representing the HTML element of 
            the row of the document for which the purchase status is to be
            checked
        
        """

        if page_number != 1:
            self.PAGES()[page_number].click()
            self.PAGES_MENU_GO_BUTTON().click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.table_xpath)))
        document_row = self.TABLE().find_elements_by_tag_name('tr')[2:][document_index]

        return document_row

    def cart_document(self, document_row):
        """
        Cart document.

        Parameters
        ----------
        document_row : selenium.webdriver.remote.webelement.WebElement
            A Selenium WebElement instance representing the HTML element of 
            the row of the document for which the purchase status is to be
            checked

        Returns
        -------
        cart_status : bool
            Boolean specifying whether the carting operation was successful
        
        """

        cart_result = False 
        main_window = self.browser.current_window_handle

        try:
            self.CART_BUTTON(document_row).click()

            self.browser.switch_to.window(self.browser.window_handles[1])

            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.cart_ok_button_xpath)))
            scroll_to_element(self.browser, self.CART_OK_BUTTON())
            self.CART_OK_BUTTON().click()

            self.browser.switch_to.window(main_window)

            cart_result = True

        except:
            cart_result = False

        return cart_result

    def index_and_cart(self, document_type, num_doc = 1):
        """
        Index and cart documents.
        
        Prameters
        ---------
        document_type : str
            Type of the document to be carted
        num_doc : int, optional
            Number of documents to be carted, default 1
        
        Returns
        -------
        cart_status : bool
            Boolean specifying whether any documents were carted
        doc_count : int
            Number of documents carted

        """

        assert type(document_type) == str, 'Must specify the type of document to be indexed'

        doc_count = 0
        request_regex = re.compile(rf'{document_type}')

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.pages_menu_xpath)))

        num_pages = len(self.PAGES())
        cart_status = False

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.table_xpath)))

        if num_pages > 1:
            for page_count in range(num_pages):
                
                if doc_count >= num_doc:
                    break
                
                self.navigate_to_page(page_count)

                self.wait.until(EC.element_to_be_clickable((By.XPATH, self.table_xpath)))
                
                for (row_count, row) in enumerate(self.CONTENT()):
                    data = row.find_elements_by_tag_name('td')
                    
                    if len(data) > 3: # Check if row is empty
                        doc_name = str(data[4].text.strip())

                        if bool(request_regex.search(doc_name)):
                            document_row = self.return_doc_row(row_count)

                            if not self.check_purchase_status(document_row):
                                cart_status = self.cart_document(document_row)
                                doc_count += 1
                                if doc_count == num_doc:
                                    break

        elif num_pages == 1:
                
            for (row_count, row) in enumerate(self.CONTENT()):
                data = row.find_elements_by_tag_name('td')
                
                if len(data) > 3:
                    doc_name = str(data[4].text.strip())

                    if bool(request_regex.search(doc_name)):
                        document_row = self.return_doc_row(row_count)

                        if not self.check_purchase_status(document_row):
                            cart_status = self.cart_document(document_row)
                            doc_count += 1

                            if num_doc == doc_count:
                                break

        return cart_status, doc_count

class CheckOutPages(MainMenu):
    """
    Class representing the check out pages.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver
        A Selenium WebDriver instance

    Attributes
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        The associated Selenium WebDriver instance
    wait : selenium.webdriver.supoport.wait.WebDriverWait
        The associated Selenium WebDriverWait instance
    save_and_checkout_xpath : str
        XPath representing the `Save and Checkout` button
    delete_all_button_xpath : str
        XPath representing the `Delete All` checkbutton
    proceed_to_charge_xpath : str
        XPath representing the `Proceed to charge` button
    deduct_from_account_xpath : str
        XPath representing the `Deduct from Account` button
    select_all_button_name : str
        XPath representing the `Select All` checkbutton
    check_box_buttons_xpath : str
        XPath representing the checkbuttons for selecting 
        each document, uses string formatting
    SAVE_AND_CHECKOUT_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Search` menu
    DELETE_ALL_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Image Record` option under the `Search` menu
    PROCEED_TO_CHARGE_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Shopping` menu
    DEDUCT_FROM_ACCOUNT_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Check Out`
        option under the `Shopping` menu
    SELECT_ALL_BUTTON : lambda function
        Lambda function returning a Selenium WebElement instance 
        representing the `Logout` button

   """

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 30)
        super().__init__(self.browser)

        self.save_and_checkout_xpath = "//input[@type='submit'][@value='Save and Checkout']"
        self.delete_all_button_xpath = "//div[@align='right']"
        self.proceed_to_charge_xpath = "//input[@type='button'][@value='Proceed to Charge']"
        self.deduct_from_account_xpath = "//input[@name='Button'][@value='Deduct from Account']"
        self.select_all_button_name = "selectAll"
        self.check_box_buttons_xpath = "//input[@name='selectcheckout_%d']"

        self.SAVE_AND_CHECKOUT_BUTTON = lambda: self.browser.find_element_by_xpath(self.save_and_checkout_xpath)
        self.DELETE_ALL_BUTTON = lambda: self.browser.find_element_by_xpath(self.delete_all_button_xpath).find_element_by_tag_name('a')
        self.PROCEED_TO_CHARGE_BUTTON = lambda: self.browser.find_element_by_xpath(self.proceed_to_charge_xpath)
        self.DEDUCT_FROM_ACCOUNT_BUTTON = lambda: self.browser.find_element_by_xpath(self.deduct_from_account_xpath)
        self.SELECT_ALL_BUTTON = lambda: self.browser.find_element_by_name(self.select_all_button_name)
        # self.CHECK_BOX_BUTTON will be instantiated within fucntion calls as a different number is required for each check box

    def checkout(self):
        """Click on the `Save and Checkout` button"""

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.save_and_checkout_xpath)))
        scroll_to_element(self.browser, self.SAVE_AND_CHECKOUT())
        self.SAVE_AND_CHECKOUT().click()
    
    def delete_all_items(self):
        """Click on the `Delete All` button"""

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.delete_all_button_xpath)))
        scroll_to_element(self.browser, self.DELETE_ALL_BUTTON())
        self.DELETE_ALL_BUTTON().click()
        self.browser.switch_to.alert.accept()

    def deselect_all_items(self):
        """Deselect all items in the shopping cart"""

        self.wait.until(EC.element_to_be_clickable((By.NAME, self.select_all_button_name)))

        if not self.SELECT_ALL_BUTTON().is_selected():
            scroll_to_element(self.browser, self.SELECT_ALL_BUTTON())
            self.SELECT_ALL_BUTTON().click() # Invoked twice to ensure that all documents
            self.SELECT_ALL_BUTTON().click() # are deselected
        else:
            scroll_to_element(self.browser, self.SELECT_ALL_BUTTON())
            self.SELECT_ALL_BUTTON().click()

    def select_in_batch(self, batch_size = 10):
        """
        Select a batch of given size from the document listing in the shopping cart

        Parameters
        ----------
        batch_size : int
            Size of batch    
        
        """

        for check_box_button_rank in range(1, batch_size + 1, 1):
            try:
                CHECK_BOX_BUTTON = self.browser.find_element_by_xpath(self.check_box_buttons_xpath % check_box_button_rank)
                scroll_to_element(self.browser, CHECK_BOX_BUTTON)
                CHECK_BOX_BUTTON.click()
            except:
                pass

    def proceed(self):
        """Proceed to the final page of the purchasing process"""

        self.wait.until(EC.element_to_be_clickable((By.NAME, self.proceed_to_charge_xpath)))
        self.PROCEED_TO_CHARGE().click()

    def deduct_from_account(self):
        """
        Purchase selected documents

        =======
        WARNING
        =======
        This function purchases selected documents and, hence, leads 
        to a deduction in the wallet.

        """

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.deduct_from_account_xpath)))
        self.DEDUCT_FROM_ACCOUNT.click()
