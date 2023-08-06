# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Adaptor functional test
# :Created:   sab 09 gen 2016 10:53:46 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2021, 2022 Lele Gaifax
#

NAME := $(notdir $(CURDIR))
VENV := $(TMPDIR)/dbloady-test-$(NAME)

.PHONY: test
test: $(VENV)
	$(VENV)/bin/python test.py

$(VENV):
	python -m venv $@
	$@/bin/pip install -q sqlalchemy
	$@/bin/pip install -q -e ../.. .
