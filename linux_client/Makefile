SHELL = /bin/bash

compile:
	sudo cp ./spc /usr/local/bin/
	sudo cp ./spc.py /usr/local/bin/
	sudo cp ./spc_functions.py /usr/local/bin/
	sudo chown root: /usr/local/bin/spc
	sudo chmod 755 /usr/local/bin/spc
	sudo mkdir /usr/local/man/man1
	sudo cp manpage /usr/local/man/man1/spc.1
	sudo gzip /usr/local/man/man1/spc.1

