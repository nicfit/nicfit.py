PHONY: test clean

PRE_GEN_SCRIPT = hooks/pre_gen_project.py
PRE_GEN_SCRIPT_IN = ${PRE_GEN_SCRIPT}.in

all: ${PRE_GEN_SCRIPT}

${PRE_GEN_SCRIPT}: cookiecutter.json ${PRE_GEN_SCRIPT_IN}
	mkpregen.py cookiecutter.json ${PRE_GEN_SCRIPT_IN} >| $@

clean:

test:
	rm -rf sampleproject
	cookiecutter -o sampleproject -f --no-input .
