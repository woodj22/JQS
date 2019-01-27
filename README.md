# JQS
A queue interface and filer driver that stores messages in JSON.

### Introduction
I use the AWS SQS all the time for queues. I thought i would take a deeper dive into how queues really work by building one myself as well as improving my code quality. 
I undertook this project while reading the philosphy of software design by john ousterhout. This talks about techniques that can be used to reduce complexity. 
What he believes is a measure of how good a system is. 

As a side project, below are the three goals that i set out that i believed would help me improve my understanding.

The three goals are:

1) Include an interface that would provide future developers with a model on how to build other drivers. 
  For example, a data base driver which would use a db instead of a file. 
  
2) A file driver to test the interface in goal 1 but also store messages effcieantly by understanding how filesystems work in more depth. 

3) The queue must have the ability to read messages that are currently being processed. This is something you cannot do with SQS. For good reason, but i wanted to find out why the practical way. 


### How the filesystem queue driver works

A queue is represented by a single file. A message is stored by saving a new line in the file. The new line is encoded in JSON format.
When a message is read, the first message with be at byte position 0. This then read and the byte positio of the next line is stored in a central file. 

When another message is read, it will get the next message from the byte position that is saved. 
When the message is read, the message is saved in an in_flight queue represented by another file. This means the file can be read ad all the processing messages can be viewed in that one file. 

When this message has finished be worked on, The message is deleted as it is uniquely identified by the byte position that is returned from when it is saved. 

If the job fails, it is pushed back onto the TODO queue. The retry value is evaluated to determine if it fails or is retried.
