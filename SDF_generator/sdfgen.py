"""
sdfgen - A2L file parser to locate diagnosis symbols and .par parser to locate values
=====================================================================================

This script allows the user to change the Mathworks Tool Chain Automatically Generated A2L file, that are not
provided with definition of Working Points for Vector Canape or ETAS Inca, adding the information needed.

This tool needs command line arguments:
---------------------------------------

    -i arg  a2lfilename: the starting A2L, usually generated automatically by the SW development toolchain

    -o arg  a2lfilename: the target refactored (the output) A2L file

    -d arg  xmlfilename: an xml file with information to be included in origin A2L to get the target one

    -m arg  mode: an overwrite mode specification in case of already existing output a2lfilename

:return: sys exit mode
:rtype: int

:example:

`python sdfgen.py -i a2l_input.a2l -o a2l_output.a2l -d xml_definition.xml -m O`

All needed element are passed as argument on the command line.

"""
import sys
import getopt
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import re

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import red, black, white, green, grey

# global definitions
# log file for the program execution
now = datetime.now()
logfname = "sdfgen_log_{}.txt".format(now.strftime("%Y%m%d_%H%M%S"))

# the string for search parameters declaration begin in A2L record
DECLARATION_BEGIN_STR = ""

# the string for search parameters declaration end in A2L record
DECLARATION_END_STR = ""

# the string for search symbols (MAP and CURVE) name into declaration in A2L record
SYMBOL_DECLARATION_STR = ""

# the string for search axis_pts name into declaration in A2L record
AXIS_PTS_DECLARATION_STR = ""

# the string for search measurement name into declaration in A2L record
MEASUREMENT_DECLARATION_STR = ""


# read the xml gsec  data xml file
# if file not found execution is aborted
def gsec_parse(fname='gsec.xml'):
    try:
        gsec_data_tree = ET.parse(fname)
        gsec_data_root = gsec_data_tree.getroot()
        gsec_dict = {'hw_version': gsec_data_root.attrib['hw_version'],
                     'sw_release': gsec_data_root.attrib['sw_release']}
        for i, dsrx in enumerate(gsec_data_root):
            gsec_dict[dsrx.attrib['name']] = {}
            gsec_dict[dsrx.attrib['name']]['type'] = dsrx.attrib['type']
            gsec_dict[dsrx.attrib['name']]['byte'] = dsrx.attrib['byte']
            gsec_dict[dsrx.attrib['name']]['bit'] = dsrx.attrib['bit']
            for element in dsrx:
                gsec_dict[dsrx.attrib['name']][element.tag] = element.attrib
        del gsec_data_root, gsec_data_tree, dsrx, element
    except FileNotFoundError:
        logmessage = "Error: xml gsec data file '{}' NOT FOUND.\n" \
                     "Possibly misspelled filename or wrong path\n" \
                     "NOTHING TO DO. Execution aborted with status(5)".format(fname)
        writelog(logfname, logmessage)
        print(logmessage)
        sys.exit(5)

    return gsec_dict


# ====================================================================================================================
# function find_symbol_on_a2l(fname=None, symbol= None, buffer_size= 5000000):
#              Searches for the table (MAP or CURVE) symbol inside the a2l file, locate the whole definition record,
#                     build a dictionary as buffer with all rows included into definition record
# parameters:
#             fname - A2L filename of the target A2L to be refactored - no default values
#             symbol - the string representing the symbol to be searched  - no default values
#             buffer_size - the length in bytes of the file lines to be read in one shot - default 5000000
# return:
#             integer - number of the line in A2L file where the symbol record start
#             dictionary -  buffer of line of the complete symbol definition
def find_symbol_on_a2l(fname=None, symbol=None, buffer_size=5000000):
    found = False
    # open the target A2L file
    with open(fname, 'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for symbol by symbol iterating through the whole read lines
        for line_number, line_raw in enumerate(lines):
            # remove the description string that may include the symbol TEXT    2020/08/05 beppe.miletto@gmail.com
            line = re.sub(r"\".*\"", 'comment symbol', line_raw)
            if (symbol in line) and (DECLARATION_BEGIN_STR in line):
                line_position = line_number
                # if symbol is found, verify the correct syntax of the a2l line
                syntax_verified = False
                # split the line into single text words for reading and check the right syntax
                for word_position, word in enumerate(line.lstrip(' ').split(' ')):
                    if word_position == 0:
                        # omitting the trailing blanks the keyword DECLARATION_BEGIN_STR
                        # must be first meta-command in line
                        syntax_verified = syntax_verified or (word == DECLARATION_BEGIN_STR)
                    elif syntax_verified and (word_position == 1):
                        # the keyword SYMBOL_DECLARATION_STR must be before the symbol in the line
                        syntax_verified = syntax_verified and (word == SYMBOL_DECLARATION_STR)
                    elif syntax_verified and (word_position == 2):
                        # the symbol name must be the third element of the first row
                        syntax_verified = syntax_verified and (word == symbol)
                        found = True
                        break

                    else:
                        found = False
                        line_position = -1
                        break

                break

        # if symbol found and syntax verified a buffer with the symbol complete definition is created
        # buffer includes the lines of A2L file
        # 1st starting with /begin CHARACTERISTIC
        # last starting with /end CHARACTERISTIC syntax
        if found and syntax_verified:
            symbol_def_buffer = {str(line_position): lines[line_position].split(' ')}
            symbol_def_line_count = 1
            end = False
            while not end:
                line = lines[line_position + symbol_def_line_count].split(' ')
                symbol_def_buffer[str(line_position + symbol_def_line_count)] = line
                if (DECLARATION_END_STR in line) and (
                        (SYMBOL_DECLARATION_STR in line) or (SYMBOL_DECLARATION_STR + '\n' in line)):
                    end = True
                else:
                    symbol_def_line_count += 1
        else:
            line_position = -1
            symbol_def_buffer = None
            # logmessage = "#### ERROR = Symbol'{}' NOT FOUND. Check Either The XML definition file or A2L " \
            #              "for misspelled name".format(symbol)
            # writelog(logfname, logmessage)
    # return the first line position in A2L file and the complete buffer of symbol definition
    return line_position, symbol_def_buffer


# ====================================================================================================================
# function find_symbol_on_par(fname=None, symbol= None, buffer_size= 5000000):
#              Searches for the table (MAP or CURVE) symbol inside the a2l file, locate the whole definition record,
#                     build a dictionary as buffer with all rows included into definition record
# parameters:
#             fname - A2L filename of the target A2L to be refactored - no default values
#             symbol - the string representing the symbol to be searched  - no default values
#             buffer_size - the length in bytes of the file lines to be read in one shot - default 5000000
# return:
#             integer - number of the line in A2L file where the symbol record start
#             dictionary -  buffer of line of the complete symbol definition
def find_symbol_on_par(fname=None, symbol=None, buffer_size=5000000):
    # open the target A2L file
    with open(fname, 'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for symbol by symbol iterating through the whole read lines
        for line_number, line_raw in enumerate(lines):
            # remove the description string that may include the symbol TEXT    2020/08/05 beppe.miletto@gmail.com
            line = re.sub(r"\".*\"", 'comment symbol', line_raw)
            if symbol in line:
                line_position = line_number
                # if symbol is found, verify the correct syntax of the a2l line
                # split the line into single text words for reading and check the right syntax
                for word_position, word in enumerate(line.lstrip(' ').split(' ')):
                    if word_position == 3:
                        diag_enabled = word == '1'

                break

    return line_position, diag_enabled


# ====================================================================================================================
# function find_scalar_value(fname=None, symbol= None, buffer_size= 5000000):
#              Searches for the table (MAP or CURVE) symbol inside the a2l file, locate the whole definition record,
#                     build a dictionary as buffer with all rows included into definition record
# parameters:
#             fname - A2L filename of the target A2L to be refactored - no default values
#             symbol - the string representing the symbol to be searched  - no default values
#             buffer_size - the length in bytes of the file lines to be read in one shot - default 5000000
# return:
#             integer - number of the line in A2L file where the symbol record start
#             dictionary -  buffer of line of the complete symbol definition
def find_scalar_value(fname=None, symbol=None, buffer_size=5000000):
    # open the target A2L file
    scalar_value = ''
    with open(fname, 'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for symbol by symbol iterating through the whole read lines
        for line_number, line_raw in enumerate(lines):
            # remove the description string that may include the symbol TEXT    2020/08/05 beppe.miletto@gmail.com
            line = re.sub(r"\".*\"", 'comment symbol', line_raw)
            if symbol in line:
                # if symbol is found, verify the correct syntax of the a2l line
                # split the line into single text words for reading and check the right syntax
                for word_position, word in enumerate(line.lstrip(' ').split(' ')):
                    if word_position == 5:
                        scalar_value = word
                break
    # print(scalar_value)
    return scalar_value


# ====================================================================================================================
# function find_table_value(fname=None, symbol= None, buffer_size= 5000000):
#              Searches for the table (MAP or CURVE) symbol inside the a2l file, locate the whole definition record,
#                     build a dictionary as buffer with all rows included into definition record
# parameters:
#             fname - A2L filename of the target A2L to be refactored - no default values
#             symbol - the string representing the symbol to be searched  - no default values
#             buffer_size - the length in bytes of the file lines to be read in one shot - default 5000000
# return:
#             integer - number of the line in A2L file where the symbol record start
#             dictionary -  buffer of line of the complete symbol definition
def find_table_value(fname=None, symbol=None, buffer_size=5000000):
    # open the target A2L file
    table_value = ''
    with open(fname, 'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for symbol by symbol iterating through the whole read lines
        for line_number, line_raw in enumerate(lines):
            # remove the description string that may include the symbol TEXT    2020/08/05 beppe.miletto@gmail.com
            line = re.sub(r"\".*\"", 'comment symbol', line_raw)
            if symbol in line:
                # if symbol is found, verify the correct syntax of the a2l line
                # split the line into single text words for reading and check the right syntax
                words = line.replace('  ', ' ').split()
                t_format = words[1]
                format_s = ''
                data_size = 0
                table_size = (0, 0)
                for i, char in enumerate(t_format):
                    if char in '[]()':
                        continue
                    elif char.isalpha() and i < 7:
                        format_s += char
                    elif char.isdigit() and i > 6:
                        table_size_string = t_format[-7:-1].strip()
                        if table_size_string[0] == '(' and table_size_string[-1] == ')':
                            table_size = eval(table_size_string)
                            table_value = {}
                            for row_number in range(table_size[1]):
                                data_row = lines[line_number + row_number]
                                data_string = data_row.rstrip('\n').split('  ')[-1]
                                table_value[row_number] = int(data_string.split(';')[-1])

                break
    # print(table_value)
    return table_value


# ====================================================================================================================
# function find_axis_pts(fname=None, axis_pts= None, buffer_size= 5000000):
#              Searches for the table's (MAP or CURVE) axis_pts inside the a2l file, locate the whole definition record,
#                     build a dictionary as buffer with all rows included into definition record
# parameters:
#             fname - A2L filename of the target A2L to be refactored - no default values
#             axis_pts - the string representing the axis_pts to be searched  - no default values
#             buffer_size - the length in bytes of the file lines to be read in one shot - default 5000000
# return:
#             integer - number of the line in A2L file where the axis_pts record start
#             dictionary -  buffer of line of the complete axis_pts definition
def find_axis_pts(fname=None, axis_pts=None, buffer_size=5000000):
    found = False
    # open the target A2L file to be queried and edited and read all lines
    with open(fname, 'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for axis_pts by axis_pts label (the symbol)
        for line_number, line_raw in enumerate(lines):
            # remove the description string that may include the symbol TEXT    2020/08/05 beppe.miletto@gmail.com
            line = re.sub(r"\".*\"", 'comment axis', line_raw)
            if (axis_pts in line) and (DECLARATION_BEGIN_STR in line):
                line_position = line_number
                # if axis_pts is found, verify the correct syntax of the a2l line
                syntax_verified = False
                for word_position, word in enumerate(line.lstrip(' ').split(' ')):
                    if word_position == 0:
                        # omitting the trailing blanks the keyword DECLARATION_BEGIN_STR must be first meta-command in line
                        syntax_verified = syntax_verified or (word == DECLARATION_BEGIN_STR)
                    elif syntax_verified and (word_position == 1):
                        # the keyword AXIS_PTS_DECLARATION_STR must be before the axis_pts in the line
                        syntax_verified = syntax_verified and (word == AXIS_PTS_DECLARATION_STR)
                    elif syntax_verified and (word_position == 2):
                        # the axis_pts name must be the third element of the first row
                        syntax_verified = syntax_verified and (word == axis_pts)
                        found = True
                        break

                    else:
                        found = False
                        line_position = -1
                        break

                break

        # if axis_pts found and syntax verified a buffer with the axis_pts complete definition is created
        if found and syntax_verified:
            axis_pts_def_buffer = {str(line_position): lines[line_position].split(' ')}
            axis_pts_def_line_count = 1
            end = False
            while not end:
                line = lines[line_position + axis_pts_def_line_count].split(' ')
                axis_pts_def_buffer[str(line_position + axis_pts_def_line_count)] = line
                if (DECLARATION_END_STR in line) and (
                        (AXIS_PTS_DECLARATION_STR in line) or (AXIS_PTS_DECLARATION_STR + '\n' in line)):
                    end = True
                else:
                    axis_pts_def_line_count += 1
        else:
            line_position = -1
            axis_pts_def_buffer = None
            # logmessage = "#### ERROR = AXIS_PTS symbol'{}' NOT FOUND. Check Either The XML definition file or A2L " \
            #              "for misspelled name".format(axis_pts)
            # writelog(logfname, logmessage)
    return line_position, axis_pts_def_buffer


# ------------------------------------------------------------------------------------------------------------
# function writelog(logfname, message):
# write a message to the log file leaded by the timestamp 
# parameters:
#              fname   - the log filename where write the message
#              message - the log message to be written
# return none
def writelog(log_fname, message):
    now_here = datetime.now()
    with open(log_fname, "a+") as lfp:
        lfp.write("{}\t-\t{}\n".format(now_here, message))


def read_att(attr_dict, element, attribute):
    """
    function read_att(attr_dict,element,attribute)
    safe reads the attribute from xml definition file

    :param attr_dict: the dictionary including the attribute key and value

    :param element: string value of parent element of attribute

    :param attribute: string tag of attribute (dict key) to read

    :return value: string <the attribute value if normal, None if error found>
    :return status: bool <true if normal, false if errors found>
    :return e: string <None if normal, Description of error if errors found>
    """
    try:
        value = attr_dict[element][attribute]
        status = 1
        e = None
    except KeyError:
        value = None
        status = 0
        e = "not present."

    if value == '':
        value = None
        status = 0
        e = "missing value."

    return value, status, e


def framePage(canvas, top=10 * mm, bottom=10 * mm, left=10 * mm, right=10 * mm):
    canvas.setStrokeColor(black)
    canvas.setLineWidth(1)
    canvas.setDash()
    # object dimensions : or:(originX,originY), dim : ( Width, Height) , vertex clockwise from bottom left [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
    big_rect = {'or': (left, bottom), 'dim': (WIDTH - (left + right), HEIGHT - (bottom + top)),
                'vert': [(left, bottom), (left, HEIGHT - top), (WIDTH - right, HEIGHT - top), (WIDTH - right, bottom)]}
    # the main frame big rectangle
    canvas.rect(big_rect['or'][0], big_rect['or'][1], big_rect['dim'][0], big_rect['dim'][1], stroke=1, fill=0)


def myFirstPage(canvas, doc):
    canvas.saveState()
    framePage(canvas, top=78, bottom=30, left=45.5, right=45.5)


def myLaterPages(canvas, doc):
    canvas.saveState()
    framePage(canvas, top=30, bottom=30, left=45.5, right=45.5)
    canvas.setFillColor(red)
    canvas.setFont('Helvetica', 9)
    canvas.drawString(0.6 * inch, 0.29 * inch, "Page {}  - {}".format(doc.page, DOCTYPE))
    canvas.drawString(0.6 * inch, HEIGHT - 0.35 * inch, "Page {}  - {}".format(doc.page, DOCTYPE))
    canvas.restoreState()


# =====================================================================================================================
# =====================================================================================================================
# Application main function
def main(argv, name):
    logmessage = "{} - Execution started ########################################################".format(name)
    writelog(logfname, logmessage)

    # instantiates empty command line arguments parameters
    definitions_xmlfile: str = ''
    custdata_xmlfile = ''
    input_a2lfile = ''
    input_parfile = ''
    output_pdffile = ''

    # reading the command line arguments
    try:
        opts, args = getopt.getopt(argv, "hd:c:a:p:o:", ["dfile=", "cfile", "afile=", "pfile=", "ofile"])
    except getopt.GetoptError:
        print('{} -d <xml_definitionsfile> -a <a2l_inputfile> -p <par_inputfile> -o <pdf_outfile>'.format(name))
        sys.exit(2)
    # if no option on the command line found print the help message (simulate option -h)
    if len(opts) < 1:
        opts.append(('-h', ''))

    opt_string = ""
    for opt, arg in opts:
        opt_string += " {} {}".format(opt, arg)
        if opt == '-h':
            print('USAGE: python {} -d <fname> -a <fname> -p <fname> -o <fname>'.format(name).split('/')[-1])
            print('\t\t-d\t--dfile\t > \t diag definitions xml filename.xml')
            print('\t\t-c\t--cfile\t > \t customer definitions xml filename.xml')
            print('\t\t-a\t--afile\t > \t input a2l file ')
            print('\t\t-p\t--pfile\t > \t input par calibration file')
            print('\t\t-o\t--ofile\t > \t output pdf file')
            sys.exit()
        elif opt in ("-d", "--dfile"):
            definitions_xmlfile = arg
        elif opt in ("-c", "--cfile"):
            custdata_xmlfile = arg
        elif opt in ("-a", "--afile"):
            input_a2lfile = arg
        elif opt in ("-p", "--pfile"):
            input_parfile = arg
        elif opt in ("-o", "--ofile"):
            output_pdffile = arg

    # log record the argument received from command line
    logmessage = "{} {}".format(name, opt_string)
    del opt_string
    writelog(logfname, logmessage)

    # log record the defined target file
    logmessage = "defined target file: {}".format(input_a2lfile)
    writelog(logfname, logmessage)

    # read the xml customer data xml file
    # if file not found execution is aborted
    try:
        customer_data_tree = ET.parse(custdata_xmlfile)
        customer_data_root = customer_data_tree.getroot()
        engine_manufacturer = customer_data_root.attrib['engine_manufacturer']
        engine = customer_data_root.attrib['engine']
        description = customer_data_root.attrib['description']
        app_vehicles = []
        for i, vehicle in enumerate(customer_data_root):
            app_vehicles.append({'customer': vehicle.attrib['customer'], 'type': vehicle.attrib['type'],
                                 'model': vehicle.attrib['model']})
            # print(app_vehicles[i])
        del customer_data_root, customer_data_tree, custdata_xmlfile
    except FileNotFoundError:
        logmessage = "Error: xml customer data file '{}' NOT FOUND.\n" \
                     "Possibly misspelled filename or wrong path\n" \
                     "NOTHING TO DO. Execution aborted with status(5)".format(definitions_xmlfile)
        writelog(logfname, logmessage)
        print(logmessage)
        sys.exit(5)

    # read the xml definition file
    # if file not found execution is aborted
    try:
        diag_tree = ET.parse(definitions_xmlfile)
        diag_root = diag_tree.getroot()
    except FileNotFoundError:
        logmessage = "Error: xml definition file '{}' NOT FOUND.\n" \
                     "Possibly misspelled filename or wrong path\n" \
                     "NOTHING TO DO. Execution aborted with status(5)".format(definitions_xmlfile)
        writelog(logfname, logmessage)
        print(logmessage)
        sys.exit(5)

    # read the strings of declarations keyword to be used for search into A2L file from XML root attributes

    SYMBOL_PREFIX = "CHARACTERISTIC"
    DECLARATION_PREFIX = "/begin"
    DECLARATION_SUFFIX = "/end"

    global HW_VERSION
    HW_VERSION = diag_root.attrib['hw_version']

    global SW_RELEASE
    SW_RELEASE = diag_root.attrib['sw_release']

    global GENERAL_DIAG_SEEK_PATTERN
    GENERAL_DIAG_SEEK_PATTERN = diag_root.attrib['general_diag_seek_pattern']

    global SYMBOL_DECLARATION_STR
    SYMBOL_DECLARATION_STR = diag_root.attrib['symbol_prefix']

    global DECLARATION_BEGIN_STR
    DECLARATION_BEGIN_STR = diag_root.attrib['declaration_prefix']

    global DECLARATION_END_STR
    DECLARATION_END_STR = diag_root.attrib['declaration_suffix']

    # instantiate the errors and warning counters
    error_counter = 0
    warning_counter = 0

    element2change = len(diag_root)
    print("Read '{}': found {} entities to be described in SDF document.".format(definitions_xmlfile, element2change))

    # open the document Story in the reportlab Platypus Simplestyle
    # Write the first page
    global DOC_FORMAT
    DOC_FORMAT = A4

    global WIDTH
    global HEIGHT

    WIDTH, HEIGHT = DOC_FORMAT

    doc = SimpleDocTemplate(output_pdffile, pagesize=DOC_FORMAT, rightMargin=72, leftMargin=72, topMargin=18,
                            bottomMargin=18, author=os.getlogin())
    Story = []

    # Define the big table on Cover Page
    global DOCTYPE
    DOCTYPE = "Metatron HDS9 - Finalized Diagnostic Specification"
    DOCTYPE_HEADER = "Metatron HDS9 <br/> Finalized Diagnostic Specification"

    global COMPANY
    COMPANY = 'Metatron Research Center'

    global DEPARTMENT
    DEPARTMENT = 'Powertrain Application Department'
    Story = []
    imlogo = Image('./static/metatronlogo.png', 0.75 * inch, 0.75 * 54 / 220 * inch, hAlign='LEFT')
    style = ParagraphStyle(name='Heading1', fontName='Helvetica-Bold', fontSize=16, textColor=grey, spaceAfter=6)
    p_doctype = Paragraph(DOCTYPE_HEADER, style)
    style = ParagraphStyle(name='Heading1', fontName='Helvetica', fontSize=8, textColor=grey, spaceAfter=8)
    p_generatedby = Paragraph('Generated by {}'.format(name), style)
    style = ParagraphStyle(name='Heading1', fontName='Helvetica', fontSize=8, textColor=grey, spaceAfter=8)
    p_ecusetup = Paragraph(
        "ECU setup: [HW version: {} ] - [SW release: {} ] - [Calibration dataset: {}]".format(HW_VERSION, SW_RELEASE,
                                                                                              input_parfile), style)
    s = Spacer(0.5 * inch, 0.05 * inch, True)
    data = [[imlogo, COMPANY, (p_doctype, s)],
            [DEPARTMENT, '11', '12', '13', '14'],
            ['Date: {:%d, %b %Y}'.format(now), '21', p_generatedby, '23', '24'],
            [p_ecusetup, '31', '32', '33', '34']]
    t = Table(data, colWidths=[1 * inch, 2 * inch, 2 * inch, 1 * inch, 1 * inch])
    t.setStyle(TableStyle([('SPAN', (0, 1), (1, 1)),  # Powertrain Application Department
                           ('SPAN', (2, 0), (4, 1)),  # DOCTYPE
                           ('SPAN', (0, 2), (1, 2)),  # date
                           ('SPAN', (2, 2), (-1, 2)),  # generated by
                           ('SPAN', (0, 3), (-1, 3)),  # ECU configuration
                           ('BACKGROUND', (0, 0), (-1, -1), white),
                           ('TEXTCOLOR', (0, 0), (-1, -1), grey),
                           ('GRID', (0, 0), (-1, -1), 0.25, green),
                           ('BOX', (0, 0), (-1, -1), 0.5, black)]))

    Story.append(t)
    del p_generatedby, p_ecusetup, t
    # Define the Text of the Cover page
    s = Spacer(0.5 * inch, 1.5 * inch, True)
    Story.append(s)
    style = ParagraphStyle(name='Heading1', fontName='Helvetica-Bold', fontSize=16, textColor=black, spaceAfter=6)
    eng_man_p = Paragraph('Engine manufacturer: {}'.format(engine_manufacturer), style)
    Story.append(eng_man_p)
    s = Spacer(0.5 * inch, 1 * inch, True)
    style = ParagraphStyle(name='Heading1', fontName='Helvetica-Bold', fontSize=24, textColor=black, spaceAfter=6)
    eng_p = Paragraph('Engine model: {}'.format(engine), style)
    style = ParagraphStyle(name='Heading1', fontName='Helvetica-Bold', fontSize=16, textColor=black, spaceAfter=6)
    engversion_p = Paragraph('        version: {}'.format(description), style)
    Story.append(s)
    Story.append(eng_p)
    Story.append(Spacer(0.5 * inch, 0.25 * inch, True))
    Story.append(engversion_p)
    Story.append(Spacer(0.5 * inch, 1.0 * inch, True))
    if len(app_vehicles) > 0:
        style = ParagraphStyle(name='Heading1', fontName='Helvetica', fontSize=12, textColor=black, spaceAfter=12)
        if len(app_vehicles) > 1:
            Story.append(Paragraph("for following vehicles:", style))
            Story.append(Spacer(0.5 * inch, 0.5 * inch, True))
            vehicles_s = ''
            for vehicle in app_vehicles:
                vehicles_s += '<br/> Type: {} - Customer: {} -  Model: {} <br/>'.format(vehicle['type'],
                                                                                        vehicle['customer'],
                                                                                        vehicle['model'])
        if len(app_vehicles) == 1:
            Story.append(Paragraph("for following vehicle:", style))
            vehicles_s = 'Type: {} - Customer: {} -  Model: {} '.format(app_vehicles[0]['type'],
                                                                        app_vehicles[0]['customer'],
                                                                        app_vehicles[0]['model'])

        vehicles_p = Paragraph(vehicles_s, style)
        Story.append(vehicles_p)
        Story.append(Spacer(0.5 * inch, 1 * inch))

    style = ParagraphStyle(name='Heading1', fontName='Helvetica', fontSize=12, textColor=black, spaceAfter=12)
    p = Paragraph("Approved by:   _________________________", style)
    Story.append(p)
    Story.append(PageBreak())

    Story.append(vehicles_p)

    # GSEC parser
    gsec = gsec_parse()

    # diag_root contains all the element <table> in the opened xml configuration file
    # main iteration through Working Points definitions
    dd = {}  # the big data dictionary that contains all diagnostic data to be formatted and printed
    for diag in diag_root:
        # log the symbol under process
        logmessage = "Processing Element '{}' that is a {}: ".format(diag.attrib['line_seek_pattern'],
                                                                     diag.attrib['type'])
        print("\t ->{}".format(logmessage))
        writelog(logfname, logmessage)
        error_counter_old = error_counter
        warning_counter_old = warning_counter
        if diag.attrib['type'].upper() in ('STD', 'CURVE'):
            diag_els = {}
            diag_els['type'] = diag.attrib['type']
            diag_els['line_seek_pattern'] = diag.attrib['line_seek_pattern']
            # search the symbol under process:
            symbol = 'ds{}{}'.format(diag.attrib['line_seek_pattern'], GENERAL_DIAG_SEEK_PATTERN)
            result, symbol_a2l_buffer = find_symbol_on_a2l(input_a2lfile, symbol, 5000000)
            if result < 0:
                warning_counter += 1
                logmessage = "\t!!! WARNING: Element '{}' NOT found in A2L. " \
                             "Nothing to do. Skipping.".format(diag.attrib['symbol'])
                enable_process = False
            else:
                logmessage = "\tElement '{}' found at row number of A2L" \
                             " {} of {}".format(symbol, result + 1, input_a2lfile)
                found_in_par, diag_enabled = find_symbol_on_par(input_parfile, symbol, 5000000)

                if found_in_par > 0:
                    enable_process = True
                    if diag_enabled:
                        diag_els['enabled'] = True
                        logmessage += "\t Found in par at row {} and Diag. Enabled".format(found_in_par + 1)
                    else:
                        diag_els['enabled'] = False
                        logmessage += "\t Found in par at row {} and Diag. NOT Enabled".format(found_in_par + 1)
                else:
                    logmessage += "\t NOT Found in par."
                    error_counter += 1
            # log the result of the search
            writelog(logfname, logmessage)
            if enable_process:
                # instantiate the parameters to be changed
                for element in diag:

                    diag_els[element.tag] = element.attrib
                    # print(diag_els[element.tag])
                    if element.tag == 'DTC':
                        for symptom in element:
                            symptom_code = symptom.attrib['FMI_UDS']
                            diag_els[element.tag][symptom_code] = symptom.attrib
                            for symptom_element in symptom:
                                diag_els[element.tag][symptom_code][symptom_element.tag] = symptom_element.attrib
                                if symptom_element.tag == 'fault_check_test':
                                    threshold_symbol = symptom_element.attrib['threshold_par']
                                    if symptom_element.attrib['type'] == 'scalar':
                                        # reading scalar type threshold
                                        threshold_value = find_scalar_value(input_parfile, threshold_symbol, 5000000)
                                        diag_els[element.tag][symptom_code][symptom_element.tag][
                                            'threshold_value'] = threshold_value

                        # Reading Automa values from par
                        if 'conf2dev_seek' in diag_els['automa']:
                            symbol = diag_els['line_seek_pattern'] + diag_els['automa']['conf2dev_seek']
                            diag_els['automa']['conf2dev_value'] = find_scalar_value(input_parfile, symbol).strip()

                        if 'deb2conf_seek' in diag_els['automa']:
                            symbol = diag_els['line_seek_pattern'] + diag_els['automa']['deb2conf_seek']
                            diag_els['automa']['deb2conf_value'] = find_scalar_value(input_parfile, symbol).strip()

                        if 'filt2conf_seek' in diag_els['automa']:
                            symbol = diag_els['line_seek_pattern'] + diag_els['automa']['filt2conf_seek']
                            diag_els['automa']['filt2conf_value'] = find_scalar_value(input_parfile, symbol).strip()

                        if 'inconfold_seek' in diag_els['automa']:
                            symbol = diag_els['line_seek_pattern'] + diag_els['automa']['inconfold_seek']
                            diag_els['automa']['inconfold_value'] = find_scalar_value(input_parfile, symbol).strip()

                        if 'wuccntinit_seek' in diag_els['automa']:
                            symbol = diag_els['line_seek_pattern'] + diag_els['automa']['wuccntinit_seek']
                            diag_els['automa']['wuccntinit_value'] = find_scalar_value(input_parfile, symbol).strip()

                        if 'step_seek' in diag_els['automa']:
                            symbol = diag_els['line_seek_pattern'] + diag_els['automa']['step_seek']
                            diag_els['automa']['step_value'] = find_scalar_value(input_parfile, symbol).strip()

                        # Reading Adia Conf Word
                        if 'adia_seek' in diag_els['adia']:
                            symbol = diag_els['line_seek_pattern'] + diag_els['adia']['adia_seek']
                            diag_els['adia']['adia_value'] = find_scalar_value(input_parfile, symbol).strip()

                        # Reading the GSEC config table

                        if 'gsec_seek' in diag_els['gsec']:
                            symbol = diag_els['line_seek_pattern'] + diag_els['gsec']['gsec_seek']
                            diag_els['gsec']['gsec_value'] = find_table_value(input_parfile, symbol)

                        try:
                            if 'vssymbol' in diag_els['vs']:
                                if diag_els['vs']['vssymbol'] != 'na':
                                    symbol = diag_els['vs']['vssymbol']
                                    diag_els['vs']['vs_value'] = find_scalar_value(input_parfile, symbol).strip()
                                else:
                                    diag_els['vs']['vssymbol'] = 'na'
                                    diag_els['vs']['vs_value'] = 'na'
                        except:
                            diag_els['vs']['vssymbol'] = 'na'
                            diag_els['vs']['vs_value'] = 'na'

        dd[diag_els['line_seek_pattern']] = diag_els
        del diag_els
        logmessage = "END Processing Element '{}' that is a {}: error found {} - warnings found {}  ".format(
            diag.attrib['line_seek_pattern'], diag.attrib['type'],
            error_counter - error_counter_old,
            warning_counter - warning_counter_old)
        writelog(logfname, logmessage)
        print("\t ->{}".format(logmessage))

    logmessage = "{} - Execution ended \n" \
                 "\t\t\twith {} Errors and {} Warnings.\n " \
                 "######################################################".format(name, error_counter, warning_counter)
    writelog(logfname, logmessage)
    print(logmessage)

    # PDF Document writing final statement
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:], sys.argv[0])
