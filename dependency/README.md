#  Prepare Perl Module Dependencies

The `dependency/rpmbuild/` directory contains `.spec` files and patch files used to build missing Perl modules required for packaging.

## Step 1: Download Sources

~~~~ {.bash}
$ cd /path/to/rpmbuild/SOURCES
$ ./prep_sources.sh
~~~~

This script downloads source archives for the following modules:

* Proc-Pidfile
* Capture-Tiny

## Step 2: Build and Install Modules (in order)

To satisfy interdependencies, build and install the modules in the following order:

1. `Proc-Pidfile`
2. `Capture-Tiny`

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
  "Capture-Tiny|0.50|D/DA/DAGOLDEN|Capture::Tiny"
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
