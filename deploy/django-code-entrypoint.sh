#!/bin/bash

cd /app/code
python manage.py collectstatic --no-input

python manage.py migrate --no-input

data_loaded=$(psql -qtAX -h db -U smrpo -d smrpo -c "SELECT count(*) FROM (SELECT 1 FROM auth_group LIMIT 1) AS t")
if [ $data_loaded -eq 0 ]
then
    echo "Loading fixtures ..."
    python manage.py loaddata -i /fixtures/groups.json
else
    echo "Fixtures already loaded"
fi