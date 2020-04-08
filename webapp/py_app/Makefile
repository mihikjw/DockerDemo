
all:
	$(MAKE) install test success || $(MAKE) failure

install:
	pip3 install -r requirements.txt

test:
	coverage run --source="." -m unittest discover
	coverage html --omit="*/tests/*.py,*__init__.py,main.py"

success:
	@printf "\n\e[1;32mBuild Succesful\e[0m\n"

failure:
	@printf "\n\e[1;31mBuild Failed\e[0m\n"
	exit 1

clean:
	find . -type f -name '*.pyc' -delete
	if [ -f ./coverage ]; then rm ./coverage; fi;
	if [ -d ./htmlcov ]; then rm -r ./htmlcov; fi;