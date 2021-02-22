/*---
* Author: Liam Curtis
* Class: CSCI-3341 Intro to Operating Systems
* Professor: Dr. Hashemi
* Date: October 20, 2020
---*/

/*---
* 1.) Create Sifter Thread
*      -Turn down Invalid messages
*      -3 Chances for validity
*      -Removes Asterisk from String
*      -3 valid no-null parts
* 2.) Send to Decoder
*      -Divide message into 3
*      -Send to Substitute, Hill, and Peak
* 3.) Make placeholder thread for Testing
* 4.) Substitute Thread
*      -Replacement Algorithm:
*      -Use First character to solve for N
*      -N = [(Alphabetical Position) % 10] + 2
*      -Then Subtract N from every following character
* 5.) Hill Thread
*      -Create S and C matrices
*      -Formula:
*      -C' = (SC) % 26
*      -Repeat the process for each value for Vector C
* 6.) Peak Thread
*      -Repeat the Hill Thread Formula for 3x1 and 3x3 matrices
* 7.) Create Output Lines
*/

//Imports
#include <iostream> //might not need this
#include <vector>
#include <pthread.h>
#include <cstring>
#include <stdio.h>

//Head
using namespace std;

void * part1(void *);
void * part2(void *);
void * partSub(void *);
void * partHill(void *);
void * partPeak(void *);

//Declarations
struct args {
    char* message;
    vector<int> index;
    int counter;
};

//Main Method
int main() {
    //Parameters used in Sifter thread:
    pthread_t sifter;
    //pointer to sifter
    void* sifterPointer;
    int result;
    char * message;

    //Create Sifter Thread
    result = pthread_create(&sifter, NULL, part1, (void*)message);

    //If result = 0, thread creation was successful
    if (result != 0) {
        perror("Thread Failure");
        exit(EXIT_FAILURE);
    }
    //If result = 0, thread join was successful
    result = pthread_join(sifter, &sifterPointer);
    if(result != 0) {
        perror("Join Failure");
        exit(EXIT_FAILURE);
    }
}

//Sifter Method
void * part1(void *crypt) {
    string message;     //Input variable
    int count = 2;      //Attempt Counter
    char * cipher =  (char*) crypt;   //Character pointer
    struct args* decodeArgs = (struct args*)malloc(sizeof(struct args));    //Structure for Initialization Arguments

    //User Prompt
    do {
        cout << "Enter the message you would like deciphered, or enter EXIT to close out: " << endl;
        getline(cin, message);          //User Input
        char ciphered[message.length()+1];      //Declare Character Array = Length of message
        strcpy(ciphered, message.c_str());      //Copies String Characters to the Character Array
        //cout << message;                      //Test I/O
        cipher = ciphered;                     //Declare duplicate array for scrubbing asterisks
        vector<int> index;                //Declare Index

        //Count Asterisks
        for (int i = 0; i < message.length(); i++) {
            if (cipher[i] == '*') {
                index.push_back(i);
            }
        }

        //If 6 asterisks are found: Initialize message, index, and counter
        if (index.size() == 6) {
            decodeArgs->message = ciphered;
            decodeArgs->index = index;
            decodeArgs->counter = count+1;

            //Parameters used in Decoder Thread:
            pthread_t decoder;
            void* decoderPointer;
            int result;

            //Create Decoder Thread
            result = pthread_create(&decoder, NULL, part2, (void *)decodeArgs);

            //If result = 0, thread creation was successful
            if (result != 0) {
                perror("thread creation failed");
                exit(EXIT_FAILURE);
            }

            //If result = 0, thread join was successful
            result = pthread_join(decoder, &decoderPointer);
            if (result != 0) {
                perror("thread join failed");
                exit(EXIT_FAILURE);
            }
            //If null parts exist:
            if(count > decodeArgs->counter) {
                cout << "Invalid Message:  " << count
                     << " Attempts Remaining" << endl;
                count--;
            } else
                count = 2;

            //If message is blatantly invalid:
        } else if (message != "EXIT") {
            cout << "Invalid Message:  " << count
                 << " Attempts Remaining" << endl;
            count--;
        }
        //Reset index
        index.clear();
    } while (count >= 0 && message != "EXIT");
    //Exit program when EXIT is entered by the user
    pthread_exit(0);
}

void * part2(void* decodeArgs) {
    vector<int> index = ((struct args *) decodeArgs)->index;
    char *myMessage = ((struct args *) decodeArgs)->message;
    string str = myMessage;
    string str1, str2, str3;
    int beg1, end1, beg2, end2, beg3, end3;
    for (int i = 0; i < str.length(); i++) {
        if (myMessage[i] == '*' && myMessage[i + 1] == '*' && myMessage[i + 2] == '*') {
            //There are 3 consecutive asterisks
            i = i + 3;
            beg3 = i;
            for (int k = i + 1; k <= str.length(); k++) {
                if (myMessage[k] == '*') {
                    end3 = k;
                    break;
                } else if (k + 1 == str.length()) {
                    end3 = k+1;
                    goto end;
                }
            }
        } else if (myMessage[i] == '*' && myMessage[i + 1] == '*' && myMessage[i + 2] != '*') {
            //There are 2 consecutive asterisks
            i = i + 2;
            beg2 = i;
            for (int k = i + 1; k <= str.length(); k++) {
                if (myMessage[k] == '*') {
                    end2 = k;
                    break;
                } else if (k == str.length()) {
                    end2 = k+1;
                    goto end;
                }
            }
        } else if (myMessage[i] == '*' && myMessage[i + 1] != '*') {
            //There is 1 consecutive asterisk
            i = i + 1;
            beg1 = i;
            for (int k = i + 1; k <= str.length(); k++) {
                if (myMessage[k] == '*') {
                    end1 = k;
                    break;
                } else if (k == str.length()) {
                    end1 = k;
                    goto end;
                }
            }
        }
    }
    end:
    str1 = str.substr(beg1,end1-beg1);
    str2 = str.substr(beg2,end2-beg2);
    str3 = str.substr(beg3,end3-beg3);

    //cout << str1 << endl;
    //cout << str2 << endl;
    //cout << str3 << endl;



    //Parameters used in Substitute Thread:
    pthread_t subThread, hillThread, peakThread;
    void* subPointer;
    void* hillPointer;
    void* peakPointer;
    int result, result2, result3;
    char submsg[str1.length()+1];
    strcpy(submsg, str1.c_str());
    char hillmsg[str2.length()+1];
    strcpy(hillmsg, str2.c_str());
    char peakmsg[str3.length()+1];
    strcpy(peakmsg, str3.c_str());

    //Create Substitute Thread
    result = pthread_create(&subThread, NULL, partSub, (void *) submsg);

    //If result = 0, thread creation was successful
    if (result != 0) {
        perror("thread creation failed");
        exit(EXIT_FAILURE);
    }
    //If result = 0, thread join was successful
    result = pthread_join(subThread, &subPointer);
    if (result != 0) {
        perror("thread join failed");
        exit(EXIT_FAILURE);
    }

    //Create Hill Thread
    result2 = pthread_create(&hillThread, NULL, partHill, (void *) hillmsg);

    //If result = 0, thread creation was successful
    if (result2 != 0) {
        perror("thread creation failed");
        exit(EXIT_FAILURE);
    }
    //If result = 0, thread join was successful
    result2 = pthread_join(hillThread, &hillPointer);
    if (result2 != 0) {
        perror("thread join failed");
        exit(EXIT_FAILURE);
    }

    //Create Peak Thread
    result3 = pthread_create(&peakThread, NULL, partPeak, (void *) peakmsg);

    //If result = 0, thread creation was successful
    if (result3 != 0) {
        perror("thread creation failed");
        exit(EXIT_FAILURE);
    }
    //If result = 0, thread join was successful
    result3 = pthread_join(peakThread, &peakPointer);
    if (result3 != 0) {
        perror("thread join failed");
        exit(EXIT_FAILURE);
    }
    pthread_exit(0);
}

/* Substitute Thread:
*      -Replacement Algorithm:
*      -Use First character to solve for N
*      -N = [(Alphabetical Position) % 10] + 2
*      -Then Subtract N from every following character
*      +Errors:
*          -N is not an alphabet character
*          -The ciphered message contains a non-alphabet character
-*/

void * partSub(void * submsg) {

    string str = (char *)submsg;
    char letter;
    vector<int> key;
    char code1[str.length()+1];      //Declare Character Array = Length of message
    strcpy(code1, str.c_str());

    //Create numeric values for letters
    for (int i = 0; i < str.length(); i++) {
        letter = str.at(i);
        if (letter >= 'A' && letter <= 'Z') {
            key.push_back((int)letter - 'A');
        } else {
            key.push_back(0);
        }
    }

    //ERRORS

    //If 1st character is non-alphabet:
    if (!isalpha(code1[0])) {
        perror("First Character in Substitute Thread must be an alphabet character");
        pthread_exit(0);
    } else {
        //If message contains non-alphabet characters (excluding spaces)
        for (int j = 0; j < str.length(); j++){
            if (code1[j] == ' '){
                j++;
            }else if (!isalpha(code1[j])){
                perror("Ciphered Message in Substitute Thread must contain only alphabet characters");
                pthread_exit(0);
            }
        }
    }

    //N FORMULA: N = [(Alphabetical Position) % 10] + 2
    int N = (key.at(0) % 10) + 2;
    for (int i = 0; i <= str.length() - 1; i++) {
        key.at(i) = key.at(i) - N;
        //If the value is negative it starts over at Z
        if (key.at(i) < 0) {
            key.at(i) += 26;
        }
    }

    //Displays the actual result converted into letter
    cout << endl;
    for (int i = 2; i < str.length(); i++) {
        cout << ((char)(key.at(i) + 'A'));
    }
    cout << endl;
    return 0;
}

/*-
* 5.) Hill Thread
*      -Create S and C matrices
*      -Formula:
*      -C' = (SC) % 26
*      -Repeat the process for each value for Vector C
*      +ERRORS:
*          -Str1 contains non-alphabet characters
*          -The # of characters in str1 is not even
*          -The # of digits in str2 is not 4
*          Str2 contains non-digit characters
-*/
void * partHill(void * hillmsg) {

    string str = (char *) hillmsg;
    string str1, str2;
    char letter;
    vector<int> CKey;
    vector<int> SKey;
    vector<int> FKey;
    char code2[str.length() + 1];
    strcpy(code2, str.c_str());
    for(int i = 0; i  < str.length(); i++){
        if (code2[i] == ' '){
            str1 = str.substr(0,i);
            str2 = str.substr(i+1);
            break;
        }
    }
    //str1 == ACDUJF
    //str2 == 1 4 6 12
    int pos = str2.find(' ');
    CKey.push_back(stoi(str2.substr(pos-1)));
    CKey.push_back(stoi(str2.substr(pos)));
    CKey.push_back(stoi(str2.substr(pos+2)));
    CKey.push_back(stoi(str2.substr(pos+4)));
    //CKey == (int) 1,4,6,12

    //ERRORS

    //If str1 contains non-alphabet characters (excluding spaces)
    for (int j = 0; j < str1.length(); j++){
        if (code2[j] == ' '){
            j++;
        }else if (!isalpha(code2[j])){
            perror("First String in Hill Thread must contain only alphabet characters");
            pthread_exit(0);
        }
    }
    //If str1 does not contain an even number of characters
    if (str1.length() % 2 != 0){
        perror("First String in Hill Thread must contain an even number of characters");
    }
    //If str2 does not contain 4 digits
    int count = 0;
    for (int j = 0; j < str2.length(); j++){
        if(str2.at(j) == ' '){
            count++;
        }
        if (count > 4){
            perror("Second String in Hill Thread must contain only 4 digits");
            break;
        }
    }
    //If str2 contains non-digit characters
    for (int j = 0; j < str2.length(); j++){
        if (str2.at(j) == ' '){
            j++;
        }else if (!isdigit(str2.at(j))){
            perror("Second String in Hill Thread must contain only integer characters");
            pthread_exit(0);
        }
    }

    //Create numeric values for letters
    for (int i = 0; i < str1.length(); i++) {
        letter = str.at(i);
        if (letter >= 'A' && letter <= 'Z') {
            SKey.push_back((int)letter - 'A');
        } else {
            SKey.push_back(0);
        }
    }
    int matC[2][2] = {{CKey.at(0),CKey.at(2)},{CKey.at(1),CKey.at(3)}};
    int res[1][2];
    //cout << "String 1: " << str1 << endl << "String 2: " << str2 << endl;
    for (int i =0; i != SKey.size(); i++){
        int matS[1][2] = {SKey.at(i),SKey.at(i+1)};
        for (int j = 0; j < 2; j++){
            for (int k = 0; k < 2; k++){
                res[j][k] = 0;
                for (int m = 0; m < 2; m++){
                    res[j][k] += matS[j][m] * matC [m][k];
                }
            }
        }
        for (int j = 0; j < 1; j++) {
            for (int k = 0; k < 2; k++) {
                FKey.push_back(res[j][k] % 26);
            }
        }
        cout << "[" << ((char)(FKey.at(i) + 'A')) << ", " << ((char)(FKey.at(i+1) + 'A')) << "] ";
        i++;
    }
    cout << endl;
    return 0;
}


/* 6.) Peak Thread
*      -Create S and C matrices
*      -Formula:
*      -C' = (SC) % 26
*      -Repeat the process for each value for Vector C
*      +ERRORS:
*          -Str1 contains non-alphabet characters
*          -The # of characters in str1 is not divisble by 3
*          -The # of digits in str2 is not 9
*          Str2 contains non-digit characters
-*/
void * partPeak(void * peakmsg) {

    string str = (char *) peakmsg;
    string str1, str2;
    char letter;
    vector<int> CKey;
    vector<int> SKey;
    vector<int> FKey;
    char code2[str.length() + 1];
    strcpy(code2, str.c_str());
    for(int i = 0; i  < str.length(); i++){
        if (code2[i] == ' '){
            str1 = str.substr(0,i);
            str2 = str.substr(i+1);
            break;
        }
    }

    int pos = str2.find(' ');
    CKey.push_back(stoi(str2.substr(pos-1)));
    CKey.push_back(stoi(str2.substr(pos)));
    CKey.push_back(stoi(str2.substr(pos+2)));
    CKey.push_back(stoi(str2.substr(pos+4)));
    CKey.push_back(stoi(str2.substr(pos+6)));
    CKey.push_back(stoi(str2.substr(pos+8)));
    CKey.push_back(stoi(str2.substr(pos+10)));
    CKey.push_back(stoi(str2.substr(pos+12)));
    CKey.push_back(stoi(str2.substr(pos+14)));
    //ERRORS

    //If str1 contains non-alphabet characters (excluding spaces)
    for (int j = 0; j < str1.length(); j++){
        if (code2[j] == ' '){
            j++;
        }else if (!isalpha(code2[j])){
            perror("First String in Peak Thread must contain only alphabet characters");
            pthread_exit(0);
        }
    }
    //If str1 is not divisible by 3
    if (str1.length() % 3 != 0){
        perror("First String in Peak Thread must be divisible by 3");
    }
    //If str2 does not contain 9 digits
    int count = 1;
    for (int j = 0; j < str2.length(); j++){
        if(str2.at(j) == ' '){
            count++;
        }
    }
    if (count != 9){
        perror("Second String in Peak Thread must contain only 9 digits");
    }
    //If str2 contains non-digit characters
    for (int j = 0; j < str2.length(); j++){
        if (str2.at(j) == ' '){
            j++;
        }else if (!isdigit(str2.at(j))){
            perror("Second String in Peak Thread must contain only integer characters");
            pthread_exit(0);
        }
    }

    //Create numeric values for letters
    for (int i = 0; i < str1.length(); i++) {
        letter = str.at(i);
        if (letter >= 'A' && letter <= 'Z') {
            SKey.push_back((int)letter - 'A');
        } else {
            SKey.push_back(0);
        }
    }
    int matC[3][3] = {{CKey.at(0),CKey.at(3), CKey.at(6)},{CKey.at(1),CKey.at(4), CKey.at(7)},{CKey.at(2),CKey.at(5), CKey.at(8)}};
    int res[1][3];
    //cout << "String 1: " << str1 << endl << "String 2: " << str2 << endl;
    for (int i =0; i != SKey.size(); i++){
        int matS[1][3] = {SKey.at(i),SKey.at(i+1),SKey.at(i+2)};
        for (int j = 0; j < 3; j++){
            for (int k = 0; k < 3; k++){
                res[j][k] = 0;
                for (int m = 0; m < 3; m++){
                    res[j][k] += matS[j][m] * matC [m][k];
                }
            }
        }
        for (int j = 0; j < 1; j++) {
            for (int k = 0; k < 3; k++) {
                FKey.push_back(res[j][k] % 26);
            }
        }
        cout << "[" << ((char)(FKey.at(i) + 'A')) << ", " << ((char)(FKey.at(i+1) + 'A')) << ", " << ((char)(FKey.at(i+2) + 'A')) << "] ";
        i+=2;
    }
    cout << endl;
    return 0;
}
