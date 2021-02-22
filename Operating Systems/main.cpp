/*---
* Author: Liam Curtis
* Class: CSCI-3341 Intro to Operating Systems
* Professor: Dr. Hashemi
* Date: October 20, 2020
*/


//Imports
#include <pthread.h>
#include<cstdlib>
#include <stdio.h>
#include <semaphore.h>
#include <unistd.h>

#define SIZE 3
#define FULL 0
#define EMPTY 0
char buffer[SIZE];
int nextIn = 0;
int nextOut = 0;

sem_t producerSemaphore; //producer semaphore
sem_t consumerSemaphore; //consumer semaphore

void Produce(char item, int n)
{
    int value;
    sem_wait(&producerSemaphore); //get the mutex to fill the buffer

    if(n==26){
        n = 1;
    }else{
        n=n+1;
    }
    buffer[nextIn] = item;
    nextIn = (nextIn + 1) % SIZE;
    if (nextIn ==1){
        printf("\nProducer (n = %d): %c ",n,item);
    }else {

        printf("%c ", item);
    }
    if(nextIn==FULL)
    {
        sem_post(&consumerSemaphore);
        sleep(1);
    }
    sem_post(&producerSemaphore);

}

void * Producer() {
    for(;;) {
        srand(time(NULL));
        int i;
        int n = rand() % 26 + 1;
        for (i = 0; i < 3; i++) {
            Produce((char) ('A' + (n - 1) % 26), n);
            n++;
        }
    }
}

int Consume(int vowelCount)
{
    int item;
    sem_wait(&consumerSemaphore); // gain the mutex to consume from buffer

    item = buffer[nextOut];
    nextOut = (nextOut + 1) % SIZE;
    if(item ==65 || item ==69 || item ==73 || item ==79 || item ==85){
        vowelCount++;
    }
    if (nextOut ==1){
        printf("\nConsumer: %c ",item);
    }else {
        printf("%c ", item);
    }
    if(nextOut==EMPTY) //its empty
    {
        printf("\n# of Vowels: %d\n",vowelCount);
        sleep(1);
    }

    sem_post(&consumerSemaphore);
    return vowelCount;
}

void * Consumer(){
    for(;;) {

        int i;
        int vC = 0;
        for (i = 0; i < 3; i++) {
            if (i % 3 == 0) {
                vC = 0;
            }
            vC = Consume(vC);
        }
    }

}

int main()
{
    pthread_t prodThread,conThread;
    //initialize the semaphores
        sem_init(&producerSemaphore, 0, 100);
        sem_init(&consumerSemaphore, 0, 0);

        //creating producer and consumer threads


        if (pthread_create(&prodThread, NULL, reinterpret_cast<void *(*)(void *)>(Producer), NULL)) {
            printf("\n ERROR creating thread 1");
            exit(EXIT_FAILURE);
        }

        if (pthread_create(&conThread, NULL, reinterpret_cast<void *(*)(void *)>(Consumer), NULL)) {
            printf("\n ERROR creating thread 2");
            exit(EXIT_FAILURE);
        }

        if (pthread_join(prodThread, NULL)) /* wait for the producer to finish */
        {
            printf("\n ERROR joining thread");
            exit(EXIT_FAILURE);
        }

        if (pthread_join(conThread, NULL)) /* wait for consumer to finish */
        {
            printf("\n ERROR joining thread");
            exit(EXIT_FAILURE);
        }


        sem_destroy(&producerSemaphore);
        sem_destroy(&consumerSemaphore);


    //exit the main thread

    pthread_exit(NULL);
    return 1;
}