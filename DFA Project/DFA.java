/*
CSCI 3236
Theoretical Foundations
DFA Assignment
November 21, 2019
*/

/*
@author Liam Curtis
Authorized by:
Liam Curtis
Jahmal Embden
Ashem Johnson
Chiau Wu
*/

package TheoreticalFoundationsDFA;

//Imports
import java.util.Scanner;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.Optional;
import java.util.Queue;
import java.util.Set;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Objects;

public class DFA {
    
    //Declare Data References
    private static Set<Integer> language = new HashSet<Integer>();
    private static Set<State> states = new HashSet<State>();
    private static State sState;
    private static Set<Transition> transitionFn = new HashSet<Transition>();
    private static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        String fileName = null;
        //Check to see if the file name was input by the command prompt
        if (args.length != 0) {
            fileName = args[0];
        } else {
            System.out.println("Input the name of the DFA file:");
            fileName = sc.nextLine();
        }

        File file = new File("src/TheoreticalFoundationsDFA/" + fileName);
                file.getAbsolutePath();
        try {
            BufferedReader buffRead = new BufferedReader(new InputStreamReader(new FileInputStream(file)));

            // Read line 1 (Alphabet)
            //Add to Alphabet Hashset
            String text = null;
            text = buffRead.readLine();
            text = text.substring(1, text.length()-1);
            String[] alphabets = text.split(",");
            for (String x: alphabets) {
                addToLanguage(Integer.parseInt(x));
            }

            // Read line 2 (States)
            // Add to state hashset
            text = buffRead.readLine();
            text = text.substring(1, text.length()-1);
            String[] stateNames = text.split(",");
            for (String x: stateNames) {
                State state = new State(x.charAt(0));
                state.setAState(true);
                addToStates(state);
            }

            // Read line 3 (Start State)
            text = buffRead.readLine();
            sState = getStatebyName(text.charAt(0));

            // Read line 4 (Final States)
            // Set Final States
            text = buffRead.readLine();
            text = text.substring(1, text.length()-1);
            String[] aStateNames = text.split(",");
            for (String x: aStateNames) {
                char name = x.charAt(0);
                states.stream().filter(state -> state.getName() == name).forEach(state -> setFinalState(state));
            }

            //Read the remaining lines (Transition Functions)
            text = buffRead.readLine();
            while(text!=null){
                String pattern = "\\((\\w),(\\w)\\)(\\W*)(\\w)";
                Pattern r = Pattern.compile(pattern);
                Matcher m = r.matcher(text);
                while (m.find()) {  
                    Transition transition = new Transition(getStatebyName(m.group(1).charAt(0)), Integer.parseInt(m.group(2)), getStatebyName(m.group(4).charAt(0)));
                    addTransition(transition);
                }
                text = buffRead.readLine();

            }          
            //Close file reader
            buffRead.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        String input;
        while (true) {
            System.out.println("Enter a string of numbers to test or exit to stop");
            input = sc.nextLine();
            if ("exit".equals(input)){
                break;
            } else {
                String[] inputArray = input.split("");
                LinkedList<Integer> inputList = new LinkedList<>();
                for (String s: inputArray) {
                    //Wrong character condition
                    if (!isInteger(s)) {
                        System.out.println("Rejected");
                        break;
                    }
                    inputList.add(Integer.parseInt(s));
                }

                if (isCompatible(sState, inputList)) {
                    System.out.println("Accepted\n");
                }

                else {
                    System.out.println("Rejected\n");
                }
            }
        }
    }

    //Checks to make sure input is only integer characters: 0 - 9
    private static boolean isInteger(String s) {
        char c = s.charAt(0);
        return (c >= 48 && c <= 57);
    }

    //Accesors + Mutators
    private static void setFinalState(State state) {
        state.setFState(true);
    }

    private static State getStatebyName(char name) {
        return states.stream().filter(s -> s.getName() == name).findFirst().get();
    }
    
    //Adds Characters to Language
    public static void addToLanguage(Integer symbol) {
        language.add(symbol);
    }
    
    //Adds States to State class
    public static void addToStates(State state){
        states.add(state);
    }

    //Adds Transitions to Transition class
    public static void addTransition(Transition transition) throws IllegalArgumentException{
    // Checks for duplicate states
        if(transitionFn.stream().noneMatch(t -> t.getState1().equals(transition.getState1()) && Objects.equals(t.getSymbol(), transition.getSymbol()))){
            transitionFn.add(transition);
        } else {
            throw new IllegalArgumentException();
        }
    }
    
    //Checks to see if user input is accepted by the DFA
    public static boolean isCompatible(State state, Queue<Integer> symbol) {
        if(symbol.isEmpty() && state.isFState()){
            return true;
        } if(!language.contains(symbol.peek())){
        return false;
        }
        Optional<State> nextState = getNextState(state, symbol.poll());
        if(nextState.isPresent()){
            return isCompatible(nextState.get(), symbol);
        }
        return false;
    }
    //Returns Next State
    private static Optional<State> getNextState(State state, Integer alphabet){
        return transitionFn.stream().filter(t -> t.getState1().equals(state) && Objects.equals(t.getSymbol(), alphabet)).map(t -> t.getState2()).findFirst();
    }
}

class Transition {
    
    //Declare Data References
    State state1;
    Integer num;
    State state2;
    
    //Constructors
    public Transition(State state1, Integer symbol, State state2){
        this.state1 = state1;
        this.num = symbol;
        this.state2 = state2;
    }
    
    //Accessors + Mutators
    public State getState1() {
        return state1;
    }

    public Integer getSymbol() {
        return num;
    }

    public State getState2() {
        return state2;
    }
}

class State {
    
    //Declare Data References
    private char name;
    private boolean fState = false;
    private boolean aState = false;
   
    //Constructors
    public State(char name) {
        this.name = name;
        }
    
    //Accessors + Mutators
    public char getName() {
        return name;
    }

    public void setName(char name) {
        this.name = name;
    }

    public boolean isFState() {
        return fState;
    }
    public void setFState(boolean finalState) {
        this.fState = finalState;
    }
    public boolean isAState() {
        return aState;
    }
    public void setAState(boolean acceptState) {
        this.aState = acceptState;
    }
}