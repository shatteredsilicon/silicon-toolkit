Name:           perl-Capture-Tiny
Version:        0.50
Release:        1%{?dist}
Summary:        Capture STDOUT and STDERR from Perl, XS or external programs

License:        Apache Software License
URL:            https://metacpan.org/dist/Capture-Tiny
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Capture-Tiny-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  perl >= 5.006
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More) >= 0.62
BuildRequires:  perl(Scalar::Util)

# Only needed on RHEL 8+, not present on RHEL 7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

Requires:       perl
Requires:       perl(Scalar::Util)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides:       perl(Capture::Tiny) = %{version}

%description
Capture::Tiny provides a simple, portable way to capture almost anything
sent to STDOUT or STDERR, regardless of whether it comes from Perl, from XS
code or from an external program. Optionally, output can be teed so that it
is captured while being passed through to the original filehandles. Yes, it
even works on Windows (usually). Stop guessing which of a dozen capturing
modules to use in any particular situation and just use this one.

%prep
%setup -q -n Capture-Tiny-%{version}

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
%doc Changes CONTRIBUTING.mkdn cpanfile dist.ini LICENSE META.json perlcritic.rc README Todo
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 01 2025 Thien Nguyen <nthien86@gmail.com> 0.50-1
- Initial RPM release for Capture::Tiny Perl module
