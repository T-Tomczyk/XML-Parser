about_msg_content = '''XML Parser
Version 1.0
Copyright (c) 2022 Tomasz Tomczyk

This product is licensed under GNU GENERAL PUBLIC LICENSE.

To read the license, click Help -> Read License.'''

help_msg_content = '''XML Parser is a tool for transforming data from one or more .xml files into a tabular format (.csv or .xlsx).

---

Usage:
1. adjust the settings to your preference and click "Continue",
2. select one or more XML files for conversion,
3. the tool will create an output file in the same location as the "XML Parser.exe" file.

---

Explanation of the available settings:
1. Output format: output can be exported to either .csv or .xlsx (Excel) file.

2. Namespaces style. If an XML file starts with the following lines:
    <xsl xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:table>
then in the output file you will receive the following:
    a) if style is set to Hidden: table/...
    b) if style is set to Prefixes: {xsl}table/...
    c) if style is set to Full links: {http://www.w3.org/1999/XSL/Transform}table/...

3. Attributes. If an XML file includes the following line:
    <name style="First Last">Alan Turing</name>
and if Attributes are set to be included, then in the output file you will receive the following:
    name          Alan Turing
    name@style    First Last
Otherwise the name@style line will not be displayed in the results.

---

For a more detailed guide, source code and other information visit the tool's repository on GitHub by clicking Help -> Visit GitHub.'''
