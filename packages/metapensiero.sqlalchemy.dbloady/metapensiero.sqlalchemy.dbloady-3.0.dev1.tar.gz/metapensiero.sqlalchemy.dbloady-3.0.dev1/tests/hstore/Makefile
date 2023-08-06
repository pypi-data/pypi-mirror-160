# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- HSTORE functional test
# :Created:   gio 22 ott 2015 18:15:12 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016, 2017, 2019, 2021, 2022 Lele Gaifax
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
	$(VENV)/bin/dbloady -u $(SA_URI) -s state.yaml data.yaml
	$(VENV)/bin/python model.py test_1 $(SA_URI)
	$(VENV)/bin/dbloady -u $(SA_URI) -D state.yaml
	$(VENV)/bin/python model.py test_2 $(SA_URI)

$(VENV):
	python -m venv $@
	$@/bin/pip install -q sqlalchemy psycopg2
	$@/bin/pip install -q -e ../.. .

.PHONY: db
db:
	../postgresql start
	dropdb --if-exists $(DBNAME)
	createdb $(DBNAME)
	psql -c "CREATE EXTENSION hstore" $(DBNAME)
	$(VENV)/bin/python model.py setup $(SA_URI)
	rm -f state.yaml
