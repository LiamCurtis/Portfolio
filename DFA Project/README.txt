Deterministic Finite Automaton Program:
• Our purpose for creating the Deterministic Finite Automaton Program was to create a program that would accept
 the strings of the given associated language and determine if it is acceptable.

Prerequisites:
• It is recommended that the program be ran on a Mac or Windows Operating System.
• Also a DFA description data file must also be provided for correct functionality.

Getting Started:
• Executing the program from the command prompt allows the user to also feed the program a DFA description
 file written in a text file format that has been specified as a command line parameter.
• However, if the parameter when running the program is not fulfiled or seems to be missing, the user will
 be allowed to designate the file that the user would like to use when prompeted to.
• After the file containing the DFA description has been loaded by the program, the user will be allowed 
to enter consecutive strings as a test of acceptance in accordance to the language.

DFA input format:
line 1: alphabet - eg. {0,1}
line 2: states - eg. {a,b,c,d,e}
line 3: start state - eg. a
line 4: accept states - eg. {d,e}
lines 5-: transition fn - eg. (a,0)->b
			      (a,1)->c
			      etc.

Steps of Execution:
• First the program checks to see if the file name was input by the command prompt, and if not then it prompts the user to enter a file.
• Then it reads through the file line by line adding the information to the specific hashset which corresponds to line location within the document.
Note: The fourth line sets the Final States.
• After the first 4 lines have been read it then reads through the rest of the document taking those inputs as Transition Functions.
• Then the file is closed after the program no longer needs it in use.
• The program will then ask for user input of a string of numbers to test whether it is accepted by the DFA.
• The User is allowed to stop input and exit the program with the input "exit".

Expectations and Notes:
• No spaces in input.
• Alphabet at least allows {0,1}, but may have expanded past described parameters.
• States at least allows lower case letters, but may have expanded past described parameters.
• Transition functions can appear in any order in the input text file. 
• End of the input file indicates the end of transition functions.
• Note - The sample DFA-Test.txt file is a DFA that recognizes the regular
language over {0, 1} that contain the substring 001, and can be used as a starter DFA description.

Built With:
• Java related IDEs and running JDK 12.

Author and Project Members:
@author Liam Curtis
Jahmal Embden
Ashem Johnson
Chiau Wu