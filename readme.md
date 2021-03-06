Commissioned for MozFest 2019 Accession is a collecting booth for an imaginary museum regulated entirely by AI. Visitors submit everyday items to the booth where they are photographed and subjected to a number of AI processes which describe and classify the objects submitted. Through the exhibition the digital collection grows but as it does so the AI management becomes more and more selective about what is and is not accepted, rejecting new items that are a poor fit for what is already there. 

Museum collections and AI classifiers rely on maintaining some form of status quo to make sense. A museum that collected anything would be a dumping ground with no identity, while AIs rely on training sets that have strong visual commonality. Both rely on a sense of sameness but both are subject to critical debates about diversity and representation. Accession explores this relationship by acting out a fictional but plausible scenario through commercially available AI technologies.

Installation
A spec-file.txt is included which can be used for creating a conda environment which ought to look after most of the project's dependencies. 
You'll need to install angular io cli and thus node, npm 

Running
There are 4 parts to accession: 

1. a python script which manages the interaction, runs the AI parts, sends messages to the arduino which runs the lights and motors and communicates with a webpage, sending it messages via a web socket and writing into its data structure

2. an arduino programme that controls the stepper motor for the turntable and the lights

3. a websocket server in node js socketi0 and express. This is taken direcxtly from https://github.com/Ibro/rxjs-chat 

4. a webclient in angulario. This is adapted from https://github.com/Ibro/rxjs-chat 

so, to run first set the server going by calling

cd ./server
node index.js

THEN, run the client by 

cd ./client

and either

ng serve --open
or 
ng build 

(if you build it you'll need to run the 'dist' folder from a webserver)

Then run the python script (accession.py) and cross your fingers 