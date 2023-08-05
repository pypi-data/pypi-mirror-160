#! /usr/bin/python

# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""This class implements a BASIC interpreter that
presents a prompt to the user. The user may input
program statements, list them and run the program.
The program may also be saved to disk and loaded
again.

"""

from basictoken import BASICToken as Token
from lexer import Lexer
from program import Program
from sys import stderr,implementation
from os import listdir,rename,remove
import gc
try:
    from pydos_ui import input
except:
    pass

if implementation.name.upper() == 'MICROPYTHON':
    from sys import print_exception

gc.collect()
if 'threshold' in dir(gc):
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

def main():

    banner = (
"""
     PPPP   Y   Y  BBBB    AAA    SSSS   I    CCC
     P   P   Y Y   B   B  A   A  S       I   C
     P   P   Y Y   B   B  A   A  S       I   C
     PPPP     Y    BBBB   AAAAA  SSSS    I   C
u  u P        Y    B   B  A   A      S   I   C
u  u P        Y    B   B  A   A      S   I   C
uuuu P        Y    BBBB   A   A  SSSS    I    CCC
                    microPyBasic
""")

    print(banner)

    lexer = Lexer()
    program = Program()

    fOpened = False
    #initialize and open temporary file
    tmpfile = open('_pybTmp.tmp','w+')
    infile = tmpfile

    #Attempting memory pre-allocation to prepare for large Basic programs
    if implementation.name.upper() in ['MICROPYTHON','CIRCUITPYTHON']:
        gc.collect()
        for i in range(1600):
            if i % 100 == 0:
                print(".",end="")
            try:
                program.__program[i] = i
            except:
                print("\nMemory pre-allocation limit reached at ",i)
                break
        print()
        program.__program.clear()

    if passedIn != "":
        infile = program.load(passedIn,tmpfile)
        program.execute(infile,tmpfile)

    # Continuously accept user input and act on it until
    # the user enters 'EXIT'
    while True:

        # kfw stmt = input_keyboard(': ')
        stmt = input(': ')

        try:
        #if True:
            tokenlist = lexer.tokenize(stmt)

            # Execute commands directly, otherwise
            # add program statements to the stored
            # BASIC program

            if len(tokenlist) > 0:

                # remove blank tokens
                i = 0
                iend = len(tokenlist)
                for _ in range(iend):
                    if i>0 and tokenlist[i].lexeme.strip() == "" and tokenlist[i].category != Token.STRING:
                        tokenlist.pop(i)
                    else:
                        i+=1

                # Exit the interpreter
                if tokenlist[0].category == Token.EXIT:
                    if fOpened:
                        infile.close()
                    tmpfile.close()
                    remove('_pybTmp.tmp')
                    break

                # Add a new program statement, beginning
                # a line number
                elif tokenlist[0].category == Token.UNSIGNEDINT\
                     and len(tokenlist) > 1:
                    program.add_stmt(tokenlist,-1,tmpfile)

                # Delete a statement from the program
                elif tokenlist[0].category == Token.UNSIGNEDINT \
                        and len(tokenlist) == 1:
                    program.delete_statement(int(tokenlist[0].lexeme))

                # Execute the program
                elif tokenlist[0].category == Token.RUN:
                    try:
                        program.execute(infile,tmpfile)

                    except KeyboardInterrupt:
                        print("Program terminated")

                # List the program
                elif tokenlist[0].category == Token.LIST:
                    if len(tokenlist) == 2:
                        program.list(int(tokenlist[1].lexeme),int(tokenlist[1].lexeme),infile,tmpfile)
                    elif len(tokenlist) == 3:
                        program.list(int(tokenlist[1].lexeme),int(tokenlist[2].lexeme),infile,tmpfile)
                    elif len(tokenlist) == 4:
                        program.list(int(tokenlist[1].lexeme),int(tokenlist[3].lexeme),infile,tmpfile)
                    else:
                        program.list(-1,-1,infile,tmpfile)

                # Save the program to disk
                elif tokenlist[0].category == Token.SAVE:
                    if len(tokenlist) <= 1:
                        print("No filename specified")
                    elif "/" in tokenlist[1].lexeme or "\\" in tokenlist[1].lexeme or ":" in tokenlist[1].lexeme:
                        print("Can only save to current directory")
                    else:
                        if tokenlist[1].lexeme.split(".")[-1].upper() == "PGM":
                            filename = tokenlist[1].lexeme+".BAS"
                            if filename in listdir():
                                remove(filename)
                        else:
                            filename = tokenlist[1].lexeme

                        if program.save(filename,infile,tmpfile):
                            # Since we are running the program from the disk file "in place"
                            # the current program listing is contained only on disk in the
                            # loaded file (if one has been loaded) and the _pYbTmp.tmp working file
                            # the program.save function has to save the file to a temporary filename
                            # and we now have to replace the specified output filename with that
                            # temporary file. Finally we need to reload the saved file to initialize
                            # the in place files and index
                            #
                            # PGM files are worse since we use the internal file index keys we have to
                            # first save as a normal BAS file and reaload to eliminate all code from
                            # the temporary file
                            program.delete()
                            if fOpened:
                                infile.close()

                            if filename in listdir():
                                remove(filename)

                            rename(filename+".pYb",filename)

                            tmpfile.close()
                            tmpfile = open('_pybTmp.tmp','w+')
                            infile = program.load(filename,tmpfile)
                            if infile != None:

                                if tokenlist[1].lexeme.split(".")[-1].upper() == "PGM":

                                    filename = tokenlist[1].lexeme
                                    if program.save(filename,infile,tmpfile):

                                        if filename in listdir():
                                            remove(filename)

                                        rename(filename+".pYb",filename)

                                        #.PGM.BAS file now being used, need to close .PGM.BAS and reload .pgm file
                                        program.delete()
                                        infile.close()
                                        infile = program.load(filename,tmpfile)
                                        if infile != None:
                                            remove(filename+".BAS")
                                            fOpened = True
                                            print("Program written to file")
                                        else:
                                            # This should never happen, but just in case...
                                            fOpened = False
                                            print("Program saved but lost from active memory, ",end="")
                                            print("enter load command to re-load saved work")
                                else:
                                    fOpened = True
                                    print("Program written to file")
                            else:
                                # This should never happen, but just in case...
                                fOpened = False
                                if tokenlist[1].lexeme.split(".")[-1].upper() == "PGM":
                                    rename(filename,tokenlist[1].lexeme+".BAS")
                                    print("Texed program saved as "+tokenlist[1].lexeme+".BAS but lost from active memory, ",end="")
                                else:
                                    print("Program saved but lost from active memory, ",end="")
                                print("enter load command to re-load saved work")


                # Load the program from disk and/or delete the program from memory
                elif tokenlist[0].category == Token.LOAD or tokenlist[0].category == Token.NEW:
                    program.delete()
                    if fOpened:
                        infile.close()
                    fOpened = False

                    tmpfile.close()
                    tmpfile = open('_pybTmp.tmp','w+')

                    if tokenlist[0].category == Token.LOAD:

                        if len(tokenlist) > 1:
                            infile = program.load(tokenlist[1].lexeme,tmpfile)
                            if infile != None:
                                fOpened = True
                                print("Program read from file")
                            else:
                                fOpened = False
                        else:
                            print("Program file not found")

                # Unrecognised input
                else:
                    print("Unrecognized input")
                    for token in tokenlist:
                        token.print_lexeme()
                    print("")

        # Trap all exceptions so that interpreter
        # keeps running
        except Exception as e:
            if implementation.name.upper() == 'MICROPYTHON':
                #### print(e)
                print_exception(e)
            else:
                print(e)

if __name__ != "PyDOS":
    passedIn = ""

main()
