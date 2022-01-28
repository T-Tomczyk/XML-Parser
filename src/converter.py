import os
import pandas
from lxml import etree

def parse_single_xml_file(filepath, include_attr, namespaces_style):
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
            xpath = modify_namespaces_in_xpath(
                element,
                raw_xpath,
                namespaces_style
                )
            result[xpath] = element.text

        # If include_attr is 'yes' and if the element has attributes,
        # get the xpath. Seperate entry in output df is made for each attribute.
        # In final xpath '@' is used instead of '/' to indicate it's an
        # attribute rather than a regular text value.
        if include_attr == 'yes' and len(element.attrib) > 0:
            for attr_key, attr_value in element.attrib.items():
                xpath = raw_xpath + '@' + attr_key
                xpath = modify_namespaces_in_xpath(
                    element,
                    xpath,
                    namespaces_style
                    )
                result[xpath] = attr_value

    return result

def modify_namespaces_in_xpath(element, xpath, namespaces_style):
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

    if namespaces_style == 'prefixes':
        for prefix, link in element.nsmap.items():
            if prefix == None:
                xpath = xpath.replace('{'+ link + '}', '')
            else:
                xpath = xpath.replace(link, prefix)

    elif namespaces_style == 'hidden':
        while '{' in xpath:
            ns_start = xpath.index('{')
            ns_end = xpath.index('}')
            xpath = xpath[:ns_start] + xpath[ns_end+1:]

    return xpath

def parse_xmls_and_save_to_df(filepaths, include_attr, namespaces_style):
    '''
    Go through all files specified in filepaths, run the parse_single_xml_file
    function on each and append the results to a list. Also, make a list of
    filenames for column headers. Finally, combine all into a pandas dataframe
    and return it.
    '''

    combined_results = []
    filenames = []
    for filepath in filepaths:
        parsed = parse_single_xml_file(filepath, include_attr, namespaces_style)
        combined_results.append(parsed)
        filenames.append(os.path.basename(filepath))

    # Transpose the df for better readability (we want files as columns, not
    # xpaths as columns).
    df = pandas.DataFrame(combined_results).T

    # Add column headers.
    df.columns = filenames

    # Add the diff column.
    df = add_the_diff_column(df)

    return df

def add_the_diff_column(df):
    '''
    Add one more column to the end of the dataframe. The column will contain
    information saying whether all the values in a row are the same (Match)
    or at least one is different than the others (Break).
    '''

    def all_elements_in_list_are_same(lst):
        if len(set(lst)) == 1:
            return "Match"
        else:
            return "Break"

    df['Diff'] = df.apply(all_elements_in_list_are_same, axis=1)

    return df

def generate_output_file(source_df, output_format):
    '''
    Generates either a csv or an xlsx file based on user preferance.

    Before saving the file, checks if the output_filename is available. If not,
    adds a numerical suffix to the filename. Initial target filename is simply
    xml_parser_output.csv (or xml_parser_output.xlsx), then
    # xml_parser_output.csv, then xml_parser_output.csv and so on.
    '''
    output_filename = 'xml_parser_output.' + output_format

    suffix = 1
    while output_filename in os.listdir():
        output_filename = 'xml_parser_output' + str(suffix) + '.' + output_format
        suffix += 1

    if output_format == 'xlsx':
        source_df.to_excel(output_filename)

    elif output_format == 'csv':
        source_df.to_csv(output_filename)
