# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Pre/post scripts test
# :Created:   gio 14 gen 2016 11:28:44 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2021, 2022 Lele Gaifax
#

NAME := $(notdir $(CURDIR))
VENV := $(TMPDIR)/dbloady-test-$(NAME)
SQLITE_DB := $(VENV)/db.sqlite

.PHONY: test
test: $(VENV) db
	$(VENV)/bin/dbloady -u sqlite:///$(SQLITE_DB) -p preload.py -P postload.py data.yaml
	$(VENV)/bin/python model.py test $(SQLITE_DB)

$(VENV):
	python -m venv $@
	$@/bin/pip install -q sqlalchemy
	$@/bin/pip install -q -e ../.. .

.PHONY: db
db:
	rm -f $(SQLITE_DB)
	$(VENV)/bin/python model.py setup $(SQLITE_DB)
