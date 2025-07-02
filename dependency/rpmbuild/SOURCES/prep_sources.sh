#!/bin/bash
set -euo pipefail

# Define versions and authors
declare -A modules=(
  [Proc-Pidfile]="1.10|N/NE/NEILB"
  [Capture-Tiny]="0.50|D/DA/DAGOLDEN"
)

# Loop through and handle each module
for module in "${!modules[@]}"; do
  IFS='|' read -r version author_path <<< "${modules[$module]}"
  tarball="${module}-${version}.tar.gz"
  url="https://cpan.metacpan.org/authors/id/${author_path}/${tarball}"

  echo "Downloading ${tarball} ..."
  rm -f "${tarball}"
  wget -q "${url}" || {
    echo "Failed to download ${tarball}" >&2
    exit 1
  }
done

echo "All downloads completed successfully."
