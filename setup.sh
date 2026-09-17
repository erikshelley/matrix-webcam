#!/usr/bin/env bash

set -euo pipefail

python_version="${PYTHON_VERSION:-3.13}"
python_command="python${python_version}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
venv_path="${script_dir}/.venv"
venv_python="${venv_path}/bin/python"

if ! command -v "${python_command}" >/dev/null 2>&1; then
    printf 'Could not find %s. Install Python %s, then run this script again.\n' \
        "${python_command}" "${python_version}" >&2
    exit 1
fi

if [[ ! -x "${venv_python}" ]]; then
    "${python_command}" -m venv "${venv_path}"
fi

if ! "${venv_python}" -c 'import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] < (3, 14) else 1)'; then
    printf '.venv must use Python 3.11, 3.12, or 3.13. Remove .venv and run this script again.\n' >&2
    exit 1
fi

"${venv_python}" -m pip install -e "${script_dir}"
printf 'Setup complete. Run bash run.sh to start matrix-webcam.\n'