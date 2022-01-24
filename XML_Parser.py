from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from lxml import etree
import os
import pandas

# Option. Available namespace styles:
# 1. full: full link will be used, e.g. <http://address.com/:tag>,
# 2. short: only the prefix will be used, e.g. <ns1:tag>,
# 3. hidden: namespaces will be ignored, e.g. <tag>.
NAMESPACE_STYLE = 'hidden'

# Option. Available output formats:
# 1. xlsx,
# 2. csv.
OUTPUT_FORMAT = 'xlsx'

# Option. Either 'True' or 'False'. Decides whether attributes will be parsed
# and included in the output file or ignored.
INCLUDE_ATTRIBUTES = True

def get_input_filepaths_from_user():
    '''
    Display a pop-out file selection dialog. The user can select one or more
    files. Return the filepaths for the selected files.
    '''

    Tk().withdraw()
    filepaths = askopenfilenames(title='Select XML file(s)')
    return filepaths

def parse_single_xml_file(filepath):
    '''
    Take a single XML file (based on the filepath provided) and parse it
    into a dictionary of xpath:text pairs. Return the dictionary.
    Requires the modify_namespaces_in_xpath function to work properly.
    '''

    result = {}

    with open(filepath, 'rb') as f:
        xml_string = f.read()

    root = etree.fromstring(xml_string)
    tree = etree.ElementTree(root)

    # For each element (tag).
    for element in root.iter():
        raw_xpath = tree.getelementpath(element)

        # Get the xpath if the element contains no children and has text.
        if len(element) == 0 and element.text != None:
            xpath = modify_namespaces_in_xpath(element, raw_xpath)
            result[xpath] = element.text

        # If INCLUDE_ATTRIBUTES is True, get the xpath if the element has
        # attributes. Seperate entry is made for each attribute.
        # The @ symbol is used instead of / to indicate it's an attribute rather
        # than a regular text value.
        if INCLUDE_ATTRIBUTES and len(element.attrib) > 0:
            for attr_key, attr_value in element.attrib.items():
                xpath = raw_xpath + '@' + attr_key
                xpath = modify_namespaces_in_xpath(element, xpath)
                result[xpath] = attr_value

    return result

def modify_namespaces_in_xpath(element, xpath):
    '''
    Function needed by the parse_single_xml_file function.
    Based on user preferance, modify namespaces within an xpath string:
    a) if the selected option is 'full', full links will be left out in the
       xpaths (no action needed because lxml uses full links by default),
    b) if option is 'prefix', the function will find the prefix used in the
       tag and replace the link with the prefix,
    c) if option is 'hidden', the function will remove the namespace
       completely.
    Returns the modified xpath.
    '''

    if NAMESPACE_STYLE == 'short':
        for prefix, link in element.nsmap.items():
            if prefix == None:
                xpath = xpath.replace('{'+ link + '}', '')
            else:
                xpath = xpath.replace(link, prefix)

    elif NAMESPACE_STYLE == 'hidden':
        while '{' in xpath:
            ns_start = xpath.index('{')
            ns_end = xpath.index('}')
            xpath = xpath[:ns_start] + xpath[ns_end+1:]

    return xpath

def parse_xml_files_and_save_results_to_df(filepaths):
    '''
    Go through all files specified in filepaths, run the parse_single_xml_file
    function on each and append the results to a list. Also, make a list of
    filenames for column headers. Finally, combine all into a pandas dataframe
    and return it.
    '''

    combined_results = []
    filenames = []
    for filepath in filepaths:
        combined_results.append(parse_single_xml_file(filepath))
        filenames.append(os.path.basename(filepath))

    # Transpose the df for better readability (we want files as columns, not
    # xpaths as columns).
    df = pandas.DataFrame(combined_results).T

    # Add column headers.
    df.columns = filenames

    return df

def add_the_diff_column(df):
    '''
    Add one more column to the end of the dataframe. The column will contain
    boolean values saying whether all the values in a row are the same (True)
    or at least one is different than the others (False).
    '''

    def all_elements_in_list_are_same(lst):
        if len(set(lst)) == 1:
            return "Match"
        else:
            return "Break"

    df['Diff'] = df.apply(all_elements_in_list_are_same, axis=1)

    return df

def generate_output_file(df):
    if OUTPUT_FORMAT == 'xlsx':
        df.to_excel('output.xlsx')

    elif OUTPUT_FORMAT == 'csv':
        df.to_csv('output.csv')

def main():
    filepaths = get_input_filepaths_from_user()
    df = parse_xml_files_and_save_results_to_df(filepaths)
    df = add_the_diff_column(df)
    generate_output_file(df)

if __name__ == '__main__':
    main()
