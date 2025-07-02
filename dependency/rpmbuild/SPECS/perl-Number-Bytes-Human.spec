Name:           perl-Number-Bytes-Human
Version:        0.11
Release:        1%{?dist}
Summary:        Convert byte count to human readable format

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Number-Bytes-Human
Source0:        https://cpan.metacpan.org/authors/id/F/FE/FERREIRA/Number-Bytes-Human-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  perl >= 5.006
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)

# Only needed on RHEL 8+, not present on RHEL 7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

Requires:  perl
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides:  perl(Number::Bytes::Human) = %{version}

%description
Number::Bytes::Human is a Perl module that provides a simple way to convert
byte counts into human-readable format, such as "1.5M" or "2.3 GiB", and
vice versa. It is useful in applications and scripts where displaying file
sizes, memory usage, or bandwidth statistics in a user-friendly way is needed.

The module supports both decimal (SI) and binary (IEC) unit prefixes, customizable
precision, and round-trip conversions. It is a helpful utility for system monitoring
tools, report generators, and other tools that deal with byte quantities.

%prep
%setup -q -n Number-Bytes-Human-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes META.json README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 01 2025 Thien Nguyen <nthien86@gmail.com> 0.11-1
- Initial RPM release for Number::Bytes::Human Perl module
