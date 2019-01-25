SHELL := /bin/bash


setup: # install os and python requirements
	sudo apt-get install $(cat requirements/requirements.os.txt | xargs)
	pip3 install -r requirements/requirements.py.txt
	make logfiles
	make secret
	make key


logfiles: # create log files
	touch logs/tagbox.log
	touch logs/error.log


clean_log: # empty log files
	> logs/tagbox.log
	> logs/error.log

test:
	PASSWORD ?= $(shell stty -echo; read -p "Password: " pwd; stty echo; echo $$pwd)


credentials: # set Tagbox API credentials
	make secret
	make key


secret: # set Tagbox API secret as env variable
	@read -p "Type or paste your Tagbox secret: " TAGBOX_SECRET; export $$TAGBOX_SECRET;


key: # set Tagbox API key as env variable
	TAGBOX_KEY ?= $(shell bash -c "read -s -p 'Type or paste your Tagbox key: ' TAGBOX_KEY; echo $$TAGBOX_KEY")


