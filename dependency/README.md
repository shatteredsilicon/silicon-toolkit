# Prepare dependencies

The `dependency/rpmbuild/` directory contains SPEC files and patches for building missing Perl modules.

~~~~ {.bash}
$ cd /path/to/rpmbuild/SOURCES
$ ./prep_sources.sh
~~~~

This will download sources

* Proc-Pidfile

For example: build Proc-Pidfile

~~~~ {.bash}
$ cd /path/to/rpmbuild
$ rpmbuild -bs SPECS/perl-Proc-Pidfile.spec
$ mock -r alma+epel-8-x86_64 rebuild SRPMS/perl-Proc-Pidfile-1.10-1.el8.src.rpm
~~~~

**NOTES:** If there is no available `src.rpm` file for a Perl module from the [Fedora Project](https://src.fedoraproject.org/), build a `.spec` file from scratch using the `cpanspec` tool, as shown in the following example.

~~~~ {.bash}
#!/bin/bash

set -e

# Check if cpanspec is installed
if ! command -v cpanspec &> /dev/null; then
    echo "cpanspec is not installed. Installing..."
    sudo dnf install -y cpanspec
fi

AUTHOR="Thien Nguyen <nthien86@gmail.com>"
Proc_Pidfile_Version="1.10"

mkdir -p {BUILD,RPMS,SOURCES,SPECS,SRPMS}

wget https://cpan.metacpan.org/authors/id/N/NE/NEILB/Proc-Pidfile-${Proc_Pidfile_Version}.tar.gz
cpanspec -v --force \
         --add-provides "perl(Proc::Pidfile) = ${Proc_Pidfile_Version}" \
         --packager "${AUTHOR}" \
         Proc-Pidfile-${Proc_Pidfile_Version}.tar.gz

mv *.spec SPECS/
mv *.tar.gz SOURCES/
~~~~
