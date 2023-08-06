# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Dump functional test
# :Created:   gio 10 mar 2016 18:43:53 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2021, 2022 Lele Gaifax
#

NAME := $(notdir $(CURDIR))
VENV := $(TMPDIR)/dbloady-test-$(NAME)
SQLITE_DB := $(VENV)/db.sqlite

.PHONY: test
test: $(VENV) $(VENV)/first.dump $(VENV)/second.dump
	cmp $(VENV)/first.dump $(VENV)/second.dump

$(VENV):
	python -m venv $@
	$@/bin/pip install -q sqlalchemy
	$@/bin/pip install -q -e ../.. .

$(VENV)/first.dump:
	rm -f $(SQLITE_DB)
	$(VENV)/bin/python model.py setup $(SQLITE_DB)
	$(VENV)/bin/dbloady -u sqlite:///$(SQLITE_DB) data.yaml
	echo ".dump" | sqlite3 $(SQLITE_DB) > $@
	$(VENV)/bin/dbdumpy -u sqlite:///$(SQLITE_DB) spec.yaml $(VENV)/output.yaml

$(VENV)/second.dump:
	rm -f $(SQLITE_DB)
	$(VENV)/bin/python model.py setup $(SQLITE_DB)
	$(VENV)/bin/dbloady -u sqlite:///$(SQLITE_DB) $(VENV)/output.yaml
	echo ".dump" | sqlite3 $(SQLITE_DB) > $@
