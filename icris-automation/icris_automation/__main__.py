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

Usage
-----
$ python icris_automation Companies.docx Annual\ Return 2 -e -p -l -d 

"""

import argparse

import pandas as pd
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException

from data_processing import create_generator, export_final_df
from navigation import init_icris, init_browser, clear_cart, process_requests
from website_layout import MainMenu

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help='File containing company names or companies registry numbers')
    parser.add_argument('document_type', help='Type of document to be purchased')
    parser.add_argument('num_doc', default=1, type=int , help='Number of documents to be purchased')
    parser.add_argument('-e','--excel', help='Export purchase results data to Excel file', action="store_true")
    parser.add_argument('-p', '--purchase', help='Purchase documents in batches of 10', action="store_true")
    parser.add_argument('-l', '--logout', help='Do not logout after processing documents', action="store_true")
    parser.add_argument('-d', '--delete', help='Delete items in shopping cart', action="store_true")
    parser.add_argument('-b', '--browser', help='Do not run the operations in a headless browser', action="store_true")

    args = parser.parse_args()

    identifier_generator = create_generator(args.input) # Instantiate a generator for yielding identifiers in batches

    if args.browser:
        browser = init_icris(init_browser(headless=False))
    else:
        browser = init_icris(init_browser())
    final_df = pd.DataFrame()

    for identifier_list in identifier_generator: # Process documents in batches
        final_df = process_requests(identifier_list, 
                                    args.document_type, 
                                    browser, 
                                    args.num_doc, 
                                    final_df
                                    )
        if args.purchase: # Purchase documents in batches
            try:
                purchase_documents(browser)
            except NoSuchElementException:
                pass
            except:
                print(f'\n\n\t\t****Could not purchase documents for sequence beginning with {identifier_list[0]}****')

    if not args.delete:
        try:
            clear_cart(browser)
        except Exception as e:
            print(f"\n\n\t\t****Previous documents could not be deleted****\n\t\t\n> Traceback:\n\n" + e)

    if not args.logout:
        try:
            MainMenu(browser).logout()
        except Exception as exception:
            print("\n\n\t\t****Could not logout****\n\n\t\tTraceback> " + exception)

    if args.excel:
        try:
            export_final_df(final_df)
        except Exception as exception:
            print("\n\n\t\t****Could not write to excel file****\n\n\t\tTraceback> " + exception)

    print('\n\n\t\t****Document processing complete****')
    print(final_df)

main()
