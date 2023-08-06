# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- JSON functional test
# :Created:   mar 08 nov 2016 09:48:18 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2021, 2022 Lele Gaifax
#

export PGHOST := localhost
export PGPORT := 65432
export PGUSER := dbloady

NAME := $(notdir $(CURDIR))
VENV := $(TMPDIR)/dbloady-test-$(NAME)
DBNAME := dbloady
SA_URI := postgresql://localhost:$(PGPORT)/$(DBNAME)

.PHONY: test
test: $(VENV) db
	$(VENV)/bin/dbloady -u $(SA_URI) data.yaml
	$(VENV)/bin/python model.py test $(SA_URI)

$(VENV):
	python -m venv $@
	$@/bin/pip install -q sqlalchemy psycopg2
	$@/bin/pip install -q -e ../.. .

.PHONY: db
db:
	../postgresql start
	dropdb --if-exists $(DBNAME)
	createdb $(DBNAME)
	$(VENV)/bin/python model.py setup $(SA_URI)
