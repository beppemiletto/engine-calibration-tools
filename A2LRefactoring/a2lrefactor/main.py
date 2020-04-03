import sys, getopt, os
from datetime import datetime
import xml.etree.ElementTree as ET

# global definitions
# log file for the program execution
now = datetime.now()
logfname = "A2LRefactor_log_{}.txt".format(now.strftime("%Y%m%d_%H%M%S"))
# the string for search absent Working Point specification within A2L tables definition records
NO_WP_DEF_STR = ""


# function  duplicate_a2l(a2l_input=None, a2l_output=None, mode='O'):
#            manage the creation of the output A2L file accrding to input A2L and user options
# parameters:
#             input A2L filename that must be phisycally present unless the execution of program is aborted.
#                                             Specified with -i --ifile command line option - default None
#             output A2L filename created if not exist.
#                                             Specified with -o --ofile command line option  - default None
#             overwrite mode of existing output file - 'O' overwrite , 'B' backup creation , 'M' merge nre refactor
#                                             Specified with -m --mode command line option  - default 'O' overwrite
# return:
#            A2L filename (path) to be used for outputting refactor
def duplicate_a2l(a2l_input=None, a2l_output=None, mode='O'):
    ifile_exist = os.path.isfile(a2l_input)
    ofile_exist = os.path.isfile(a2l_output)
    #instantiate the output A2L filename
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
            if not( mode.upper() in ('O', 'B', 'M')):
                # mode not specified . enter the loop for a valid mode specification by means of keyboard input
                done= False
                do_once = False
            else:
                # mode specified - loop executed once for take the correct action
                done = True
                do_once = True

            while (not done) or do_once :
                if do_once:
                    # mode specified - the answer is taken from mode
                    answer = mode
                    do_once = False
                else:
                    # mode not specified - the answer is request from keyboard input
                    answer = input("enter 'o' overwrite, 'm' keep file and merge, 'b' backup, any other key for exit:  ")
                if answer.upper() in ('O', 'B'):
                    if  answer.upper() == 'B':
                        # overwrite  with a backup
                        a2l_input = a2l_output
                        a2l_output += '.bak'
                        ofile2use = a2l_input
                    else:
                        # only overwrite
                        ofile2use = a2l_output
                    print('\nDuplicating A2L {} to {}'.format(a2l_input, a2l_output),end=' --> ')
                    try:
                        with open(a2l_input, 'r') as input_file:
                            with open(a2l_output, 'w') as output_file:
                                for line in input_file:
                                    output_file.write(line)
                    except:
                        pass
                    print("DONE")
                    done=True
                elif answer.upper() =='M':
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
            except:
                pass
            print("DONE")
            logmessage = "The file '{}' ready to refactoring for WP parameters.".format(a2l_output)
            writelog(logfname, logmessage)
            ofile2use = a2l_output
    return ofile2use

## find_symbol:
# search for the symbol inside the a2l file
# return:
#        line number of symbol record
#        dictionary as buffer of line of the complete symbol definition)
def find_symbol(fname=None, symbol= None, buffer_size= 5000000):
    found = False
    # open the file to be queried and edited and read all lines
    with open(fname,'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for symbol by symbol
        for line_number , line in enumerate(lines):
            if symbol in line:
                line_position = line_number
                # if symbol is found, verify the correct syntax of the a2l line
                syntax_verified = False
                for word_position, word in enumerate(line.lstrip(' ').split(' ')):
                    if (word_position == 0) :
                        # omitting the trailing blanks the keyword '/begin' must be first meta-command in line
                        syntax_verified = (syntax_verified) or (word == '/begin')
                    elif (syntax_verified) and (word_position == 1):
                        # the keyword 'CHARACTERISTIC' must be before the symbol in the line
                        syntax_verified = (syntax_verified) and (word == 'CHARACTERISTIC')
                    elif (syntax_verified) and (word_position == 2):
                        # the symbol name must be the third element of the first row
                        syntax_verified = (syntax_verified) and (word == symbol)
                        found = True
                        break

                    else:
                        found = False
                        line_position = -1
                        break

                break

        # if symbol found and syntax verified a buffer with the symbol complete definition is created
        if found and syntax_verified:
            symbol_def_buffer = {}
            syntax_verified = False
            symbol_def_buffer[str(line_position)] = lines[line_position].split(' ')
            symbol_def_line_count = 1
            end = False
            while not end:
                line = lines[line_position+ symbol_def_line_count].split(' ')
                symbol_def_buffer[str(line_position+ symbol_def_line_count)] = line
                if ('/end' in line) and (('CHARACTERISTIC' in line) or ('CHARACTERISTIC\n' in line)):
                    end = True
                else:
                    symbol_def_line_count +=1
    return line_position, symbol_def_buffer

## find_axis_pts:
# search for the axis_pts inside the a2l file
# return:
#        line number of axis_pts record
#        dictionary as buffer of line of the complete axis_pts definition)
def find_axis_pts(fname=None, axis_pts= None, buffer_size= 5000000):
    found = False
    # open the file to be queried and edited and read all lines
    with open(fname,'r') as fp:
        lines = fp.readlines(buffer_size)
        # search for axis_pts by axis_pts
        for line_number , line in enumerate(lines):
            if axis_pts in line:
                line_position = line_number
                # if axis_pts is found, verify the correct syntax of the a2l line
                syntax_verified = False
                for word_position, word in enumerate(line.lstrip(' ').split(' ')):
                    if (word_position == 0) :
                        # omitting the trailing blanks the keyword '/begin' must be first meta-command in line
                        syntax_verified = (syntax_verified) or (word == '/begin')
                    elif (syntax_verified) and (word_position == 1):
                        # the keyword 'AXIS_PTS' must be before the axis_pts in the line
                        syntax_verified = (syntax_verified) and (word == 'AXIS_PTS')
                    elif (syntax_verified) and (word_position == 2):
                        # the axis_pts name must be the third element of the first row
                        syntax_verified = (syntax_verified) and (word == axis_pts)
                        found = True
                        break

                    else:
                        found = False
                        line_position = -1
                        break

                break

        # if axis_pts found and syntax verified a buffer with the axis_pts complete definition is created
        if found and syntax_verified:
            axis_pts_def_buffer = {}
            syntax_verified = False
            axis_pts_def_buffer[str(line_position)] = lines[line_position].split(' ')
            axis_pts_def_line_count = 1
            end = False
            while not end:
                line = lines[line_position+ axis_pts_def_line_count].split(' ')
                axis_pts_def_buffer[str(line_position+ axis_pts_def_line_count)] = line
                if ('/end' in line) and (('AXIS_PTS' in line) or ('AXIS_PTS\n' in line)):
                    end = True
                else:
                    axis_pts_def_line_count +=1
    return line_position, axis_pts_def_buffer



def writelog(logfname, message):
    now = datetime.now()
    with open(logfname,"a+") as lfp:
        lfp.write("{}\t-\t{}\n".format(now,message))


def apply_changes2file(edit_file=None, def_buffer= None):
    lines2change_keys  = def_buffer.keys()
    lines2change = []
    for key in lines2change_keys:
        lines2change.append(int(key))
    lines2change.sort()
    with open('a2ltemp.tmp', "w+") as fpo:
        fpi = open(edit_file, "r")
        lines = fpi.readlines()
        fpi.close()

        for i in range(lines2change[0]):
            fpo.write(lines[i])
        for i in range(lines2change[0], lines2change[-1]+1, 1):
            line = " ".join(def_buffer[str(i)])
            fpo.write(line)
        del line
        restart_i = i+1
        for i in range(restart_i, len(lines), 1):
            fpo.write(lines[i])
    os.remove(edit_file)
    os.rename('a2ltemp.tmp', edit_file)
    result = os.path.isfile(edit_file)
    return result


def main(argv,name):


    logmessage = "{} - Execution started ########################################################".format(name)
    writelog(logfname,logmessage)


    # instantiates empty command line arguments parameters
    definitions_xmlfile = ''
    input_a2lfile = ''
    output_a2lfile = ''
    write_mode = ''

    # reading the command line arguments
    try:
        opts, args = getopt.getopt(argv, "hd:i:o:m:", ["dfile=", "ifile=", "ofile=", "mode"])
    except getopt.GetoptError:
        print ('{} -d <xml_definitionsfile> -i <a2l_inputfile> -o <a2l_outputfile>'.format(name))
        sys.exit(2)
    opt_string = ""
    for opt, arg in opts:
        opt_string += " {} {}".format(opt,arg)
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
    logmessage = "{} {}".format(name,opt_string)
    del opt_string
    writelog(logfname,logmessage)

    # define the target a2l file to be refactored for including wp parameters setting
    edit_file = duplicate_a2l(input_a2lfile, output_a2lfile, write_mode)

    # log record the defined target file
    logmessage = "defined target file: {}".format(edit_file)
    writelog(logfname,logmessage)

    wp_tree = ET.parse(definitions_xmlfile)
    wp_root = wp_tree.getroot()

    # read the NO WP defintion keyword to be used for search
    global NO_WP_DEF_STR
    NO_WP_DEF_STR = wp_root.attrib['nowpdefstring']

    # open the xml configuration file
    for table in wp_root:
        # log the symbol under process
        logmessage = "Processing Element '{}' that is a {}: ".format(table.attrib['symbol'], table.attrib['type'])
        writelog(logfname, logmessage)
        if table.attrib['type'].upper() in ('MAP', 'CURVE'):

            # search the symbol under process:

            result, symbol_def_buffer = find_symbol(edit_file,table.attrib['symbol'], 5000000)
            if result < 0:
                logmessage= "\tElement '{}' not found. Nothing to do.".format(table.attrib['symbol'])
                enable_process = False
            else:
                logmessage = "\tElement '{}' found at row number {} of {}".format(table.attrib['symbol'], result, edit_file)
                enable_process = True
            # log the result of the search
            writelog(logfname, logmessage)
            if enable_process:
                # instantiate the parameters to be changed
                a2l_changes = {}
                for a2l_element in table:
                    print('\t\t\t\t', a2l_element.tag, a2l_element.attrib)
                    a2l_changes[a2l_element.tag] = a2l_element.attrib
                    print()

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
                            yaxis_done = True
                            break
                        elif a2l_changes['yinput']['symbol'] in line:
                            symbol_change_done[1] = True
                            yaxis_done = True
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
                axis_pts = a2l_changes['xaxis']['symbol']
                result, axis_def_buffer = find_axis_pts(edit_file, axis_pts, 5000000)
                if result >0 :
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

                # if element is a MAP the y axis must be processed as well
                if isMAP:
                    axis_pts = a2l_changes['yaxis']['symbol']
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


    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:], sys.argv[0])


