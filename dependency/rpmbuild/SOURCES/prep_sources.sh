#!/bin/bash
set -euo pipefail

# Define versions and authors
declare -A modules=(
  [Proc-Pidfile]="1.10|N/NE/NEILB"
  [Config-IniFiles]="3.000003|S/SH/SHLOMIF"
  [Text-Table]="1.135|S/SH/SHLOMIF"
  [Capture-Tiny]="0.50|D/DA/DAGOLDEN"
  [Number-Bytes-Human]="0.11|F/FE/FERREIRA"
  [Text-Aligner]="0.16|S/SH/SHLOMIF"
  [Scalar-List-Utils]="1.69|P/PE/PEVANS"
  [Parallel-ForkManager]="2.03|Y/YA/YANICK"
  [Moo]="2.005005|H/HA/HAARG"
  [Class-XSAccessor]="1.19|S/SM/SMUELLER"
  [Role-Tiny]="2.002004|H/HA/HAARG"
  [Class-Method-Modifiers]="2.15|E/ET/ETHER"
  [Sub-Quote]="2.006008|H/HA/HAARG"
  [XString]="0.005|A/AT/ATOOMIC"
  [Test-Warn]="0.37|B/BI/BIGJ"
  [Sub-Uplevel]="0.2800|D/DA/DAGOLDEN"
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
