#!/bin/bash
# usage: ./run_test_connection.sh <recipe-id> <datahub-version> <plugins-required> <tmp-dir> <report-file>

set -euo pipefail
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR" || exit


venv_dir="$4/venv-$3-$2"
SECONDS=0
# Create tmp file to store requirements using provided recipe id. 
req_file="$4/requirements-$1.txt"
touch "$req_file"
if [ "$2" == "latest" ]; then
    echo "Latest version will be installed"
    echo "acryl-datahub[$3]" > "$req_file"
else
    echo "acryl-datahub[$3]==$2" > "$req_file"
fi
if [ ! -d "$venv_dir" ]; then
  echo "venv doesn't exist.. minting.."
  python3 -m venv $venv_dir
  source "$venv_dir/bin/activate"
  pip install --upgrade pip wheel setuptools
  pip install -r $req_file
else
    if [ "$2" == "latest" ]; then
        # in case we are installing latest, we want to always re-install in case latest has changed
        source "$venv_dir/bin/activate"
        pip install --upgrade -r $req_file
    fi
fi
rm $req_file
echo "Elapsed seconds = $SECONDS"
echo "recipe is at $4/$1.yml"
if (datahub ingest run --help | grep test-source-connection); then
  echo "Success"
  rm -f "$5"
  # Execute DataHub recipe, based on the recipe id. 
  if (python3 -m datahub ingest -c "$4/$1.yml" --test-source-connection --report-to "$5"); then
    exit 0
   else
    exit 1
fi
else
  echo "datahub ingest doesn't seem to have test_connection feature. You are likely running an old version"
  cat << EOF > "$5"
{
  "internal_failure": True,
  "internal_failure_reason": "datahub library doesn't have test_connection feature. You are likely running an old version."
}
EOF
  exit 0 # success here means we have succeeded at trying and we know why we failed
fi
