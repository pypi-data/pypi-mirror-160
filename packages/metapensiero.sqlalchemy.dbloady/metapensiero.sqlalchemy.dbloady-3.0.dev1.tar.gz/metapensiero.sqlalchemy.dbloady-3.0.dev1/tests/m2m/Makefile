# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- M2M functional test
# :Created:   sab 18 gen 2020, 08:30:10
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2020, 2021, 2022 Lele Gaifax
#

NAME := $(notdir $(CURDIR))
VENV := $(TMPDIR)/dbloady-test-$(NAME)
SQLITE_DB := $(VENV)/db.sqlite

.PHONY: test
test: $(VENV) db
	$(VENV)/bin/dbloady -u sqlite:///$(SQLITE_DB) data.yaml
	$(VENV)/bin/python model.py test $(SQLITE_DB)

$(VENV):
	python -m venv $@
	$@/bin/pip install -q sqlalchemy
	$@/bin/pip install -q -e ../.. .

.PHONY: db
db:
	rm -f $(SQLITE_DB)
	$(VENV)/bin/python model.py setup $(SQLITE_DB)
