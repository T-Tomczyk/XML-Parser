## Introduction
Merge_XMLs is a tool for transforming data from one or more .xml files into a single .csv or .xlsx file.

This tool is particularly useful when working with many XML files that are similar to each other in terms of their structures while the main differences between them lie in the text and attributes' values.

The above is not a requirement though, the tool will work with all XML files and any number of them.

## Transformation example
Given ex1.xml:
'''xml

'''

and ex2.xml:
'''xml

'''

the script produces the follwing output.xlsx:
[]()

## Details of how it works


## Usage as a standalone package
If you don't know which method to choose, go with this one.
This method only works on Windows.
1. Download the .exe file.
2. Double-click on the downloaded .exe file.
3. Windows might ask for your permission to open the application. Grant it.
4. In the pop-up window select the XML file(s) you want to transform.
5. The script will produce an output file in the same location as the .exe file.

## Usage as a Python script
1. Download the "XML_Parser.py" file. You can do it using your browser or from command line using git:
2. In your command line go to the location of the downloaded file.
3. Run "python XML_Parser.py".
4. Select the XML file(s).
5. The script will produce an output file in the same location as the .py file.

The script has the following dependancies:
- Python 3
- pandas module ("pip install pandas")
- lxml module ("pip install lxml")

## Credits and license
