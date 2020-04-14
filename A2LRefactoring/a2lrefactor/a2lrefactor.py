"""
a2lrefactor - A2L file refactoring script for inserting Working Points definitions
==================================================================================

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

`python a2lrefactor.py -i a2l_input.a2l -o a2l_output.a2l -d xml_definition.xml -m O`

All needed element are passed as argument on the command line.

"""
import sys
import getopt
import os
from datetime import datetime
import xml.etree.ElementTree as ET


# global definitions
# log file for the program execution
now = datetime.now()
logfname = "A2LRefactor_log_{}.txt".format(now.strftime("%Y%m%d_%H%M%S"))

# the string for search absent Working Point specification within A2L tables definition records
NO_WP_DEF_STR = ""

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


# ====================================================================================================================
# # function  duplicate_a2l(a2l_input=None, a2l_output=None, mode='O'):
# #            Manages the creation of the output A2L file according to input A2L and user options
# # parameters:
# #             input A2L filename that must be physically present unless the execution of program is aborted.
# #                                             Specified with -i --ifile command line option - default None
# #             output A2L filename created if not exist.
# #                                             Specified with -o --ofile command line option  - default None
# #             overwrite mode of existing output file - 'O' overwrite , 'B' backup creation , 'M' merge nre refactor
# #                                             Specified with -m --mode command line option  - default 'O' overwrite
# # return:
# #            A2L filename (path) to be used for outputting refactor
def duplicate_a2l(a2l_input=None, a2l_output=None, mode='O'):
    """ function  duplicate_a2l(a2l_input=None, a2l_output=None, mode='O'):
    This function manages the creation of the output A2L file according to input A2L and user options

    Parameters

    :param input A2L filename:
    :type string: starting A2L filename that must be physically present unless the execution of program is aborted.

    Specified with -i --ifile command line option - default None

    :param output A2L filename:
    :type string: output A2L filename created if not exist. Specified with -o --ofile command line option - default None


    # #             overwrite mode of existing output file - 'O' overwrite , 'B' backup creation , 'M' merge nre refactor
    # #                                             Specified with -m --mode command line option  - default 'O' overwrite
    # # return:
    # #            A2L filename (path) to be used for outputting refactor
    """
    ifile_exist = os.path.isfile(a2l_input)
    ofile_exist = os.path.isfile(a2l_output)
    # instantiate the output A2L filename
    ofile2use = ''

    if not ifile_exist:
        print("input file {} not found in local directory".format(a2l_input))
        logmessage: str = "A2L input file {} not found. Execution will be terminated with status 3".format(a2l_input)
        writelog(logfname, logmessage)
        sys.exit(3)
    else:
        if ofile_exist:
            logmessage: str = 'The specified output file {} already exist:'.format(a2l_output)
            writelog(logfname, logmessage)
            print('The specified output file {} already exist:'.format(a2l_output))
            # if mode is not specified or specified incorrectly it is requested as line input stopping execution
            if not (mode.upper() in ('O', 'B', 'M')):
                # mode not specified . enter the loop for a valid mode specification by means of keyboard input
                done = False
                do_once = False
            else:
                # mode specified - loop executed once for take the correct action
                done = True
                do_once = True

            while (not done) or do_once:
                if do_once:
                    # mode specified - the answer is taken from mode
                    answer = mode
                    do_once = False
                else:
                    # mode not specified - the answer is request from keyboard input
                    answer = input("enter 'o' overwrite, 'm' keep file and merge, 'b' backup, any other key exit:  ")
                if answer.upper() in ('O', 'B'):
                    if answer.upper() == 'B':
                        # overwrite  with a backup
                        a2l_input = a2l_output
                        a2l_output += '.bak'
                        ofile2use = a2l_input
                    else:
                        # only overwrite
                        ofile2use = a2l_output
                    print('\nDuplicating A2L {} to {}'.format(a2l_input, a2l_output), end=' --> ')
                    try:
                        with open(a2l_input, 'r') as input_file:
                            with open(a2l_output, 'w') as output_file:
                                for line in input_file:
                                    output_file.write(line)
                    except FileNotFoundError:
                        logmessage = "### FATAL ERROR: Input A2L file {} NOT FOUND." \
                                     " EXECUTION ABORTED".format(a2l_input)
                        writelog(logfname, logmessage)
                        sys.exit(5)
                    print("DONE")
                    done = True
                elif answer.upper() == 'M':
                    print('\nLeaving existing {} for merging new refactor'.format(a2l_output))
                    ofile2use = a2l_output
                    done = True
                else:
                    logmessage = "Program terminated by user (key '{}' entered).".format(answer)
                    writelog(logfname, logmessage)
                    print("Program terminated by user.")
                    sys.exit(0)
        else:
            print('\nDuplicating A2L original {} to copy {}'.format(a2l_input, a2l_output), end=' --> ')
            try:
                with open(a2l_input, 'r') as input_file:
                    with open(a2l_output, 'w') as output_file:
                        for line in input_file:
                            output_file.write(line)
            except FileNotFoundError:
                logmessage = "### FATAL ERROR: Input A2L file {} NOT FOUND." \
                             " EXECUTION ABORTED".format(a2l_input)
                writelog(logfname, logmessage)
                sys.exit(5)
            print("DONE")
            logmessage = "The file '{}' ready to refactoring for WP parameters.".format(a2l_output)
            writelog(logfname, logmessage)
            ofile2use = a2l_output
    return ofile2use


# ====================================================================================================================
# function find_measurement(fname=None, measure=None, buffer_size=5000000):
#              Searches for the measurement symbol name inside the a2l file, locate the whole definition record
#
# parameters:
#             fname - A2L filename of the target A2L to be refactored - no default values
#             measure - the string representing the measure symbol name to be searched  - no default values
#             buffer_size - the length in bytes of the file lines to be read in one shot - default 5000000
# return:
#             integer - number of the line in A2L file where the symbol record start
def find_measurement(fname=None, measure=None, buffer_size=5000000):
    found = False
    # open the target A2L file
    with open(fname, 'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for measure by name iterating through the whole read lines
        for line_number, line in enumerate(lines):
            if (measure in line) and (DECLARATION_BEGIN_STR in line):
                line_position = line_number
                # if measure is found, verify the correct syntax of the a2l line
                syntax_verified = False
                # split the line into single text words for reading and check the right syntax
                for word_position, word in enumerate(line.lstrip(' ').split(' ')):
                    if word_position == 0:
                        # omitting the trailing blanks the keyword DECLARATION_BEGIN_STR
                        # must be first meta-command in line
                        syntax_verified = syntax_verified or (word == DECLARATION_BEGIN_STR)
                    elif syntax_verified and (word_position == 1):
                        # the keyword SYMBOL_DECLARATION_STR must be before the measure in the line
                        syntax_verified = syntax_verified and (word == MEASUREMENT_DECLARATION_STR)
                    elif syntax_verified and (word_position == 2):
                        # the measure name must be the third element of the first row
                        syntax_verified = syntax_verified and (word == measure)
                        found = True
                        break

                    else:
                        found = False
                        line_position = -1
                        break

                break

        # if measure found and syntax verified the positive check recorded into log file
        # otherwise a warning is arisen
        if (not found) or (not syntax_verified):
            line_position = -1
    # return the first line position in A2L file
    return line_position


# ====================================================================================================================
# function find_symbol(fname=None, symbol= None, buffer_size= 5000000):
#              Searches for the table (MAP or CURVE) symbol inside the a2l file, locate the whole definition record,
#                     build a dictionary as buffer with all rows included into definition record
# parameters:
#             fname - A2L filename of the target A2L to be refactored - no default values
#             symbol - the string representing the symbol to be searched  - no default values
#             buffer_size - the length in bytes of the file lines to be read in one shot - default 5000000
# return:
#             integer - number of the line in A2L file where the symbol record start
#             dictionary -  buffer of line of the complete symbol definition
def find_symbol(fname=None, symbol=None, buffer_size=5000000):
    found = False
    # open the target A2L file
    with open(fname, 'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for symbol by symbol iterating through the whole read lines
        for line_number, line in enumerate(lines):
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
        for line_number, line in enumerate(lines):
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


# ====================================================================================================================
# function apply_changes2file(edit_file=None, def_buffer= None):
#              Searches for the line number in MAP or CURVE identified in the modified buffer
#                     replace the lines with those included in the buffer 
# parameters:
#             fname - A2L filename of the target A2L to be refactored - no default values
#             dictionary - the buffer containing the modified lines - no default values
# return:
#             boolean - the result of the file save after changing are applied
def apply_changes2file(edit_file=None, def_buffer=None):
    # the buffer is a dictionary whose keys are the line number position in A2L file
    # the line replacing is done in absolute (the modified lines are placed in the same positions of original ones) 
    # since no alteration of line number is required by change for WP
    lines2change_keys = def_buffer.keys()
    lines2change = []
    # a sorted list is created from dictionary keys to be sure of sequentially access the lines in A2L file
    for key in lines2change_keys:
        lines2change.append(int(key))
    lines2change.sort()
    # operates the line substitution after open and globally read the A2L file
    # the write is done on a temporary file buffer
    with open('a2ltemp.tmp', "w+") as fpo:  # the temporary file opened for write
        fpi = open(edit_file, "r")  # the target file to be modified opened for read
        lines = fpi.readlines()
        fpi.close()
        # lines from 0 to the n-1 line where n is the position of the first line to be replaced are merely copied
        # the index 0 of the list contains n
        for i in range(lines2change[0]):
            fpo.write(lines[i])
        # the loop of insertion of the buffer
        for i in range(lines2change[0], lines2change[-1] + 1, 1):
            line = " ".join(def_buffer[str(i)])  # complete line is rebuilt starting from all words saved in dict.
            fpo.write(line)
        del line
        restart_i = i + 1
        # remaining line after buffer position are merely copied
        for i in range(restart_i, len(lines), 1):
            fpo.write(lines[i])
    # once finished the lines substitution the original not modified file is deleted
    os.remove(edit_file)
    # the modified copy of the A2L is renamed according to target filename 
    os.rename('a2ltemp.tmp', edit_file)
    # the correct operation is asserted by the verification that the target file is checked by OS 
    result = os.path.isfile(edit_file)
    return result


def read_att(attr_dict,element,attribute):
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
        value =attr_dict[element][attribute]
        status = 1
        e = None
    except KeyError:
        value = None
        status = 0
        e = "not present."

    if value == '':
        value == None
        status = 0
        e = "missing value."

    return value, status , e





# =====================================================================================================================
# =====================================================================================================================
# Application main function
def main(argv, name):
    logmessage = "{} - Execution started ########################################################".format(name)
    writelog(logfname, logmessage)

    # instantiates empty command line arguments parameters
    definitions_xmlfile: str = ''
    input_a2lfile = ''
    output_a2lfile = ''
    write_mode = ''

    # reading the command line arguments
    try:
        opts, args = getopt.getopt(argv, "hd:i:o:m:", ["dfile=", "ifile=", "ofile=", "mode"])
    except getopt.GetoptError:
        print('{} -d <xml_definitionsfile> -i <a2l_inputfile> -o <a2l_outputfile>'.format(name))
        sys.exit(2)
    opt_string = ""
    for opt, arg in opts:
        opt_string += " {} {}".format(opt, arg)
        if opt == '-h':
            print('USAGE: python {} -d <fname> -i <fname> -o <fname> -m <char>'.format(name).split('/')[-1])
            print('\t\t-d\t--dfile\t > \t wp definitions xml filename.xml')
            print('\t\t-i\t--ifile\t > \t starting a2l file w/o wp definitions')
            print('\t\t-o\t--ofile\t > \t target a2l file with wp definitions')
            print('\t\t-m\t--mode\t > \t write mode for target a2l:')
            print('\t\t\t\t\t >> \t O,o - overwrite existing file')
            print('\t\t\t\t\t >> \t M,m - merge changes in existing file')
            print('\t\t\t\t\t >> \t B,b - create a backup copy (.bak)of existing file before overwrite')
            sys.exit()
        elif opt in ("-d", "--dfile"):
            definitions_xmlfile = arg
        elif opt in ("-i", "--ifile"):
            input_a2lfile = arg
        elif opt in ("-o", "--ofile"):
            output_a2lfile = arg
        elif opt in ("-m", "--mode"):
            write_mode = arg

    # log record the argument received from command line
    logmessage = "{} {}".format(name, opt_string)
    del opt_string
    writelog(logfname, logmessage)

    # define the target a2l file to be refactored for including wp parameters setting
    edit_file = duplicate_a2l(input_a2lfile, output_a2lfile, write_mode)

    # log record the defined target file
    logmessage = "defined target file: {}".format(edit_file)
    writelog(logfname, logmessage)

    # read the xml definition file
    # if file not found execution is aborted
    try:
        wp_tree = ET.parse(definitions_xmlfile)
        wp_root = wp_tree.getroot()
    except FileNotFoundError:
        logmessage = "Error: xml definition file '{}' NOT FOUND.\n" \
                     "Possibly misspelled filename or wrong path\n" \
                     "NOTHING TO DO. Execution aborted with status(5)".format(definitions_xmlfile)
        writelog(logfname, logmessage)
        print(logmessage)
        sys.exit(5)

    # read the strings of declarations keyword to be used for search into A2L file from XML root attributes
    global NO_WP_DEF_STR
    NO_WP_DEF_STR = wp_root.attrib['nowpdefstring']

    global DECLARATION_BEGIN_STR
    DECLARATION_BEGIN_STR = wp_root.attrib['declaration_prefix']

    global DECLARATION_END_STR
    DECLARATION_END_STR = wp_root.attrib['declaration_suffix']

    global SYMBOL_DECLARATION_STR
    SYMBOL_DECLARATION_STR = wp_root.attrib['symbol_prefix']

    global AXIS_PTS_DECLARATION_STR
    AXIS_PTS_DECLARATION_STR = wp_root.attrib['axis_pts_prefix']

    global MEASUREMENT_DECLARATION_STR
    MEASUREMENT_DECLARATION_STR = wp_root.attrib['measure_prefix']

    # instantiate the errors and warning counters
    error_counter = 0
    warning_counter = 0
    # wp_root contains all the element <table> in the opened xml configuration file
    # main iteration through Working Points definitions
    for table in wp_root:
        # log the symbol under process
        logmessage = "Processing Element '{}' that is a {}: ".format(table.attrib['symbol'], table.attrib['type'])
        writelog(logfname, logmessage)
        error_counter_old = error_counter
        warning_counter_old = warning_counter
        if table.attrib['type'].upper() in ('MAP', 'CURVE'):

            # search the symbol under process:

            result, symbol_def_buffer = find_symbol(edit_file, table.attrib['symbol'], 5000000)
            if result < 0:
                warning_counter += 1
                logmessage = "\t!!! WARNING: Element '{}' NOT found. " \
                             "Nothing to do. Skipping.".format(table.attrib['symbol'])
                enable_process = False
            else:
                logmessage = "\tElement '{}' found at row number" \
                             " {} of {}".format(table.attrib['symbol'], result, edit_file)
                enable_process = True
            # log the result of the search
            writelog(logfname, logmessage)
            if enable_process:
                # instantiate the parameters to be changed
                a2l_changes = {}
                for a2l_element in table:
                    # print('\t\t\t\t', a2l_element.tag, a2l_element.attrib)
                    a2l_changes[a2l_element.tag] = a2l_element.attrib
                    # print()

                # modify the buffer to introduce wp parameters for table symbol
                # ===============================================================
                # 1st part of 3 - Change the Record of Main Element (the table itself) definition in A2L
                # operates on the axis references definitions
                symbol_change_done = [False, False]
                xaxis_done = False
                yaxis_done = False
                isMAP = table.attrib['type'].upper() == 'MAP'
                for key, line in symbol_def_buffer.items():
                    if not xaxis_done:
                        # Search the keyword defined as WP absent specification (from XML)
                        if NO_WP_DEF_STR in line:
                            line[line.index(NO_WP_DEF_STR)] = a2l_changes['xinput']['symbol']
                            symbol_change_done[0] = False
                            xaxis_done = True

                        elif a2l_changes['xinput']['symbol'] in line:
                            symbol_change_done[0] = True
                            xaxis_done = True

                    elif isMAP and xaxis_done and (not yaxis_done):
                        if NO_WP_DEF_STR in line:
                            line[line.index(NO_WP_DEF_STR)] = a2l_changes['yinput']['symbol']
                            symbol_change_done[1] = False
                            break
                        elif a2l_changes['yinput']['symbol'] in line:
                            symbol_change_done[1] = True
                            break

                # modify the file at buffer lines locations if required
                if not symbol_change_done[0] and not symbol_change_done[1]:
                    result = apply_changes2file(edit_file, symbol_def_buffer)
                    if result:
                        logmessage = "\t Changes applied to a2l file for symbol definition record of Element "
                        writelog(logfname, logmessage)
                else:
                    logmessage = "\t Changes not needed to a2l file for symbol definition record of Element "
                    writelog(logfname, logmessage)

                # search the axis definition
                axis_pts, valid, e = read_att(a2l_changes,'xaxis','symbol')
                if not valid==1:
                    logmessage = "### UNRECOVERABLE ERROR for {}: 'xaxis'," \
                                 "'symbol' {}".format(table.attrib['symbol'], e)
                    writelog(logfname, logmessage)
                    error_counter += 1
                    continue
                result, axis_def_buffer = find_axis_pts(edit_file, axis_pts, 5000000)
                if result > 0:
                    # modify the buffer to introduce wp parameters for x axis
                    # x axis is common to MAP and CURVE types
                    xaxis_change_done = False
                    for key, line in axis_def_buffer.items():
                        if NO_WP_DEF_STR in line:
                            line[line.index(NO_WP_DEF_STR)] = a2l_changes['xinput']['symbol']
                            xaxis_change_done = False
                            break
                        elif a2l_changes['xinput']['symbol'] in line:
                            xaxis_change_done = True
                            break
                    # modify the file at buffer lines locations
                    if not xaxis_change_done:
                        result = apply_changes2file(edit_file, axis_def_buffer)
                        if result:
                            logmessage = "\t Changes applied to a2l file for xAXIS_PTS for Element "
                            writelog(logfname, logmessage)
                    else:
                        logmessage = "\t Changes not needed to a2l file for xAXIS_PTS for Element "
                        writelog(logfname, logmessage)
                else:
                    error_counter += 1
                    logmessage = "### ERROR : '{}' X AXIS_PTS NOT FOUND: " \
                                 "declaration not modifies for WP!".format(axis_pts)
                    writelog(logfname, logmessage)

                # if element is a MAP the y axis must be processed as well
                if isMAP:
                    # axis_pts = a2l_changes['yaxis']['symbol']
                    axis_pts, valid, e = read_att(a2l_changes, 'yaxis', 'symbol')
                    if not valid == 1:
                        logmessage = "### UNRECOVERABLE ERROR for {}: 'yaxis'," \
                                     "'symbol' {}".format(table.attrib['symbol'], e)
                        writelog(logfname, logmessage)
                        error_counter += 1
                        continue
                    result, axis_def_buffer = find_axis_pts(edit_file, axis_pts, 5000000)
                    if result > 0:
                        # modify the buffer to introduce wp parameters for y axis
                        # y axis is for MAP only types
                        yaxis_change_done = False
                        for key, line in axis_def_buffer.items():
                            if NO_WP_DEF_STR in line:
                                line[line.index(NO_WP_DEF_STR)] = a2l_changes['yinput']['symbol']
                                yaxis_change_done = False
                                break
                            elif a2l_changes['yinput']['symbol'] in line:
                                yaxis_change_done = True
                                break
                        # modify the file at buffer lines locations
                        if not yaxis_change_done:
                            result = apply_changes2file(edit_file, axis_def_buffer)
                            if result:
                                logmessage = "\t Changes applied to a2l file for yAXIS_PTS for Element "
                                writelog(logfname, logmessage)
                        else:
                            logmessage = "\t Changes not needed to a2l file for yAXIS_PTS for Element "
                            writelog(logfname, logmessage)
                    else:
                        error_counter += 1
                        logmessage = "### ERROR : '{}' Y AXIS_PTS NOT FOUND:" \
                                     " declaration not modifies for WP!".format(axis_pts)
                        writelog(logfname, logmessage)

                # verifies the correct definition of inputs measurements. Can raise only warnings:
                # the measurements can be not declared in A2L since they can be defined as internal
                # calculation of Canape / Inca applications.
                # x_measure = a2l_changes['xinput']['symbol']
                x_measure, valid, e = read_att(a2l_changes,'xinput','symbol')
                if not valid==1:
                    logmessage = "### UNRECOVERABLE ERROR for {}: 'xinput'," \
                                 "'symbol' {}".format(table.attrib['symbol'], e)
                    writelog(logfname, logmessage)
                    error_counter += 1
                    continue
                result = find_measurement(edit_file, x_measure)
                if result > 0:
                    logmessage = "Measurement symbol '{}' as x input found in A2L" \
                                 " at line {}.".format(x_measure, result)
                else:
                    warning_counter += 1
                    logmessage = "!!! WARNING. Measurement symbol '{}' as x input NOT found in A2L".format(x_measure)
                writelog(logfname, logmessage)

                if isMAP:
                    # y_measure = a2l_changes['yinput']['symbol']
                    y_measure, valid, e = read_att(a2l_changes, 'yinput', 'symbol')
                    if not valid == 1:
                        logmessage = "### UNRECOVERABLE ERROR for {}: 'yinput'," \
                                     "'symbol' {}".format(table.attrib['symbol'], e)
                        writelog(logfname, logmessage)
                        error_counter += 1
                        continue
                    result = find_measurement(edit_file, y_measure)
                    if result > 0:
                        logmessage = "Measurement symbol '{}' as y input found in A2L" \
                                     " at line {}.".format(y_measure, result)
                    else:
                        warning_counter += 1
                        logmessage = "!!! WARNING. Measurement symbol '{}' as y input NOT found" \
                                     " in A2L".format(y_measure)
                    writelog(logfname, logmessage)

        logmessage = "END Processing Element '{}' with {} Errors and {} Warnings.\n".format(table.attrib['symbol'],
                                                                                            error_counter - error_counter_old,
                                                                                            warning_counter - warning_counter_old)
        writelog(logfname, logmessage)

    logmessage = "{} - Execution ended \n" \
                 "\t\t\twith {} Errors and {} Warnings.\n " \
                 "######################################################".format(name, error_counter, warning_counter)
    writelog(logfname, logmessage)

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:], sys.argv[0])
