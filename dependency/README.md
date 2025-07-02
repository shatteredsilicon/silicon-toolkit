#  Prepare Perl Module Dependencies

The `dependency/rpmbuild/` directory contains `.spec` files and patch files used to build missing Perl modules required for packaging.

## Step 1: Download Sources

~~~~ {.bash}
$ cd /path/to/rpmbuild/SOURCES
$ ./prep_sources.sh
~~~~

This script downloads source archives for the following modules:

* Proc-Pidfile
* Scalar-List-Utils
* Config-IniFiles
* Text-Aligner
* Text-Table
* Capture-Tiny
* Number-Bytes-Human
* Parallel-ForkManager
* Moo
* Class::XSAccessor
* Role::Tiny
* XString
* Sub::Quote
* Class::Method::Modifiers
* Sub::Uplevel
* Test::Warn

## Step 2: Build and Install Modules (in order)

To satisfy interdependencies, build and install the modules in the following order:

1. `Proc-Pidfile`
2. `Capture-Tiny`
3. `Number-Bytes-Human`
4. `Text-Aligner`
5. `Text-Table`
6. `Scalar-List-Utils`
7. `Config-IniFiles`
8. `Class-XSAccessor`
9. `Class-Method-Modifiers`
10. `Role-Tiny`
11. `XString`
12. `Sub-Quote`
13. `Moo`
14. `Sub-Uplevel`
15. `Test-Warn`
16. `Parallel-ForkManager`

**On EL8 and newer:** Only `Proc-Pidfile` needs to be packaged, as the remaining modules are already provided by the system Perl distribution or `perl-core`.

**On EL7:** All of the above modules must be built and installed manually, as they are not included in the base repositories.

## Example: Building `Proc-Pidfile`

~~~~ {.bash}
$ cd /path/to/rpmbuild
$ rpmbuild -bs SPECS/perl-Proc-Pidfile.spec
$ mock -r alma+epel-8-x86_64 rebuild SRPMS/perl-Proc-Pidfile-1.10-1.el8.src.rpm
~~~~

# Building Missing Modules via `cpanspec`

If a `.src.rpm` for a module is not available from the [Fedora Project](https://src.fedoraproject.org/), you can build it from scratch using [`cpanspec`](https://pagure.io/cpanspec).

## Example: Generate `.spec` Files for All Modules

~~~~ {.bash}
#!/bin/bash

set -e

# Author Info
AUTHOR="Thien Nguyen <nthien86@gmail.com>"

# Ensure cpanspec is installed
if ! command -v cpanspec &> /dev/null; then
    echo "cpanspec is not installed. Installing..."
    sudo dnf install -y cpanspec
fi

# Create required directories
mkdir -p {BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Perl modules and their versions (Name|Version|CPAN Path|Provides)
MODULES=(
  "Proc-Pidfile|1.10|N/NE/NEILB|Proc::Pidfile"
  "Config-IniFiles|3.000003|S/SH/SHLOMIF|Config::IniFiles"
  "Text-Table|1.135|S/SH/SHLOMIF|Text::Table"
  "Parallel-ForkManager|2.03|Y/YA/YANICK|Parallel::ForkManager"
  "Capture-Tiny|0.50|D/DA/DAGOLDEN|Capture::Tiny"
  "Number-Bytes-Human|0.11|F/FE/FERREIRA|Number::Bytes::Human"
  "Text-Aligner|0.16|S/SH/SHLOMIF|Text::Aligner"
  "Scalar-List-Utils|1.69|P/PE/PEVANS|List::Util"
  "Moo|2.005005|H/HA/HAARG|Moo"
  "Class-XSAccessor|1.19|S/SM/SMUELLER|Class::XSAccessor"
  "Role-Tiny|2.002004|H/HA/HAARG|Role::Tiny"
  "Class-Method-Modifiers|2.15|E/ET/ETHER|Class::Method::Modifiers"
  "Sub-Quote|2.006008|H/HA/HAARG|Sub::Quote"
  "XString|0.005|A/AT/ATOOMIC|XString"
  "Test-Warn|0.37|B/BI/BIGJ|Test::Warn"
  "Sub-Uplevel|0.2800|D/DA/DAGOLDEN|Sub::Uplevel"
)

# Function to download and generate .spec using cpanspec
generate_spec() {
  local name=$1
  local version=$2
  local cpan_path=$3
  local provides=$4

  local archive="${name}-${version}.tar.gz"
  local url="https://cpan.metacpan.org/authors/id/${cpan_path}/${archive}"

  echo "Processing ${name}..."

  wget -q "$url" -O "$archive"
  cpanspec -v --force \
           --add-provides "perl(${provides}) = ${version}" \
           --packager "${AUTHOR}" \
           "$archive"
}

# Process all modules
for module in "${MODULES[@]}"; do
  IFS='|' read -r name version path provides <<< "$module"
  generate_spec "$name" "$version" "$path" "$provides"
done

# Move generated files
mv -v *.spec SPECS/
mv -v *.tar.gz SOURCES/
~~~~
