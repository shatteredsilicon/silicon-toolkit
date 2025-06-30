#!/bin/bash

set -e

Proc_Pidfile_Version="1.10"

rm -f Proc-Pidfile-${Proc_Pidfile_Version}.tar.gz

wget https://cpan.metacpan.org/authors/id/N/NE/NEILB/Proc-Pidfile-${Proc_Pidfile_Version}.tar.gz
