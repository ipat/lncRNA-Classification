# lncRNA families classifier

lncRNA (Long non-coding RNA) families classifier is the tool that used to classify the input DNA or RNA sequences to identify family that those sequences. The method behind this classifier is the Hidden-Markov-Model. The classifier composed of 217 HMM models which contain characteristics of each lncRNA family.

## Setup
This project has 2 components that have to be done. 
#### 1. Start the classifier module
The classifier module used for classifying the family. The classifier module communicates with the front-end website via socket.
To start the module use the command below:
```sh
$ cd bio_web/bio_web
$ python testRNA.py
```
To remind you, the script is in bio_web/bio_web directory not the outside one.

#### 2. Start client web server
The web server itself was developed by Django. To start the web server use the command below:
```sh
$ cd bio_web/bio_web
$ python manage.py runserver [IP address]:[port]
```
The classifier and the web server will connect automatically via the selected IP address and port which you can reconfig it in the future. 

## Tools and references

* [Promeganate](https://github.com/jmschrei/pomegranate) -  a package for graphical models and Bayesian statistics for Python.
* [Rfam](http://rfam.xfam.org/) - a database is a collection of RNA families.
* [HMM tutorial](https://www.cs.princeton.edu/~mona/Lecture/HMM1.pdf) - a HMM tutorial by Princeton University which cover the HMM with insertion and deletion.
* [Django](https://www.djangoproject.com/) - high-level Python Web framework
