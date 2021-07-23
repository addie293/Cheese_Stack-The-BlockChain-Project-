# Overview

The basic elements of the cheese stack are working fine. The main objective of the project was to implement a basic working module and thereafter add on improvements if we have time. Even though there was a paucity of time due to various problems within the group (details in Retrospective.md), we were able to successfully implement the basic element and also further add on improvements. In this case, we have reached the main goal of our project.

## Time spent by each member on the project (in hours)

| Member Name     | Time|
| ----------- | ----------- |
| Aditya Das   | 55       |
| Md Nur Amin   | 50        |
| Erblin Berisha| 45|

## Task Assignment Between Members

| Member Name     | Task(s) Assigned|
| ----------- | ----------- |
| Aditya Das   | Design of Protocol and Integration, Design and coding implementation of member.py, Testing and Validating the prototype, proof of work implementation       |
| Md Nur Amin   | Design and Coding Implementation of cheesestack.py, Creation and Implementating cheese.py, Testing and Validating the Prototype       |
| Erblin Berisha| Coding the tracker|

## Objectives Implemented

In our implementation, the following objectives were fulfilled:<br><br>
1. Minning cheeses and validating the mined cheeses are working fine.<br><br>
2. Communication between the members and between a member and a tracker is working. Multiple members can communicate with the tracker.<br><br>
3.  The members also exchange a set of “recent transactions” that are transactions that are not yet written into a block. When mining, the member tries to mine a block containing all the current transactions.<br><br>
4. Cheeses are used to store money transactions (multiple ones per block), allowing the miner to get some credit.<br><br>
5. Members can check if the cheese stack is valid by sending a nounce to other members.

## Objectives Not-Implemented

Unfortunately, the following objective(s) were not implemented in the prototype.<br><br>
1. We did not implement a Graphical User Interface (GUI).<br><br>
2. The notion of members 'complaining' to the tracker has not been included.

## Comparison to Initial Objective

All the basic elements of the cheese stack were implemented. All of them are working fine. Since that was also the initial objective, the current and the initial objectives remain the same.

# Adherence to Good Development Practices

We tried adhering to good development practices as far as possible. The following is the details of the those practices.

## About the Document

| Practice Stated     | Outcome|
| ----------- | ----------- |
| The Use of Markup   | Positive|

## About git

| Stated Practice    | Outcome|
| ----------- | ----------- |
| Commit only Source and Configuration   | Positive       |
|Use .gitignore file(s) so that git status shows up clean| Positive|
|Do not use git just to store a zip of your project| Positive|
|Commit and Push often| Negative|
|Provide good commit messages| Positive|
|Use of English for all commit messages| Positive|

## About the Code

| Stated Practice    | Outcome|
| ----------- | ----------- |
| Write your code in English  | Positive       |
|Indent and Format your code properly| Positive|
|Learn to use your editor| Positive|
|Avoid mixing spaces| Positive|
|Keep your code clean| Positive|

## About the Testing Mechanism

| Stated Practice    | Outcome|
| ----------- | ----------- |
| Test a lot and often  | Positive       |
| Have Stress Tests| Negative|
| Have tests for bad behavoiur from other peers| Negative|
|Document how to build, compile and test your project| Positive|
|Document how to understand and continue your project| Positive|





