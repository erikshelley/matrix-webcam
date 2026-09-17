#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
venv_python="${script_dir}/.venv/bin/python"

if [[ ! -x "${venv_python}" ]]; then
    printf 'Could not find .venv. Run bash setup.sh first.\n' >&2
    exit 1
fi

cd "${script_dir}"
exec "${venv_python}" -m matrix_webcam "$@"