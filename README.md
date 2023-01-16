# Couveflow

Ongoig project.

Couveflow aims to be a assets monitoring system composed by a central passive server and a rules engine that receives requests from active client. It is a proof of concept of applying formal languages and a IoT system architecture based on plug&play devices. It is not granted to be reliable and does not intend to be used in realtime systems.

## Logic summary

Making it simple, Couveflow works as a dialog between the server and the cliens.

A client can ask Couveflow to be registered, explanning what are it's actions and when they should be activated, through expressions using the language described [here](couveflow/core/guidelines/evaluator.py). The client then can ping the server asking for his next action (if there is one), and the server evaluate the expressions to get what it should tell client to do.