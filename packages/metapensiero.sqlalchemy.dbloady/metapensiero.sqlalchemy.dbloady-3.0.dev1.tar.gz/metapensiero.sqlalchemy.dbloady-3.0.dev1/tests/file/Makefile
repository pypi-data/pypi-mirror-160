# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- File functional test
# :Created:   dom 08 apr 2018 13:57:32 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018, 2019, 2021, 2022 Lele Gaifax
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
