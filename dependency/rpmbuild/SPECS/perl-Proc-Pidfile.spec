Name:           perl-Proc-Pidfile
Version:        1.10
Release:        1%{?dist}
Summary:        Simple OO Perl module for maintaining a process id file for the current process

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Proc-Pidfile
Source0:        https://cpan.metacpan.org/authors/id/N/NE/NEILB/Proc-Pidfile-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  perl >= 5.006
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Test::More)

# Only needed on RHEL 8+, not present on RHEL 7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

Requires: perl
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides: perl(Proc::Pidfile) = %{version}

%description
Proc::Pidfile is a very simple OO interface which manages a pidfile for the
current process. You can pass the path to a pidfile to use as an argument
to the constructor, or you can let Proc::Pidfile choose one
("/$tmpdir/$basename", where $tmpdir is from File::Spec).

%prep
%setup -q -n Proc-Pidfile-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes dist.ini LICENSE META.json README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Jun 30 2025 Thien Nguyen <nthien86@gmail.com> 1.10-1
- Initial RPM release for Proc::Pidfile Perl module
