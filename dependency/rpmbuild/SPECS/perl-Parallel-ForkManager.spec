Name:           perl-Parallel-ForkManager
Version:        2.03
Release:        1%{?dist}
Summary:        Simple parallel processing fork manager

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Parallel-ForkManager
Source0:        https://cpan.metacpan.org/authors/id/Y/YA/YANICK/Parallel-ForkManager-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  perl >= 0:5.006
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Moo) >= 1.001000
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(Test::Warn)

# Only needed on RHEL 8+, not present on RHEL 7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

Requires:       perl
Requires:       perl(Moo) >= 1.001000
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides:       perl(Parallel::ForkManager) = %{version}

%description
Parallel::ForkManager is intended for use in operations that can be done in parallel
where the number of processes to be forked off should be limited. Typical
use is a downloader which will be retrieving hundreds/thousands of files.

%prep
%setup -q -n Parallel-ForkManager-%{version}

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
%doc Changes CODE_OF_CONDUCT.md CONTRIBUTORS cpanfile doap.xml examples META.json README.mkdn
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 01 2025 Thien Nguyen <nthien86@gmail.com> 2.03-1
- Initial RPM release for Parallel::ForkManager Perl module
