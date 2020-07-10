#!/bin/sh
cd /data/workflow-prospectusextract-etl
LOGS_DIR=logs

if [ ! -d "${LOGS_DIR}" ]
then
  mkdir "${LOGS_DIR}"
fi

python3 workflow-prospectusextract-etl.py workflow-prospectusextract-etl.conf $python_env

echo $python_env
echo "workflow-annualreportextractsub-etl.py starting..."
