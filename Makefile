#############################################################
##### Makefile for Python-Project-Template Cookiecutter #####
#############################################################

#######
## Init
#######
init:
	@cookiecutter . --output-dir ./cookiecutter-temp
	@find ./ -maxdepth 1 ! -name '.git' ! -name 'cookiecutter-temp' !  -name '.' ! -exec rm -rf {} +
	@rsync -r ./cookiecutter-temp/*/ . && rm -rf ./cookiecutter-temp

######
## Tag 
######
tag:
ifdef version
	@git tag -a v${version} -m "Python-Project-Template v${version}"
else
	@git push origin --tags
endif
