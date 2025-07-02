Name:           perl-Config-IniFiles
Version:        3.000003
Release:        1%{?dist}
Summary:        Module for reading .ini-style configuration files

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Config-IniFiles
Source0:        https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Config-IniFiles-%{version}.tar.gz

BuildArch:      noarch

# Build dependencies
BuildRequires:  perl >= 0:5.008
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Test::More) >= 0.88

# Only needed on RHEL 8+, not present on RHEL 7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

# Runtime dependencies
Requires:       perl(IO::Scalar)
Requires:       perl(List::Util) >= 1.33
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides:       perl(Config::IniFiles) = %{version}

%description
Config::IniFiles provides a way to have readable configuration files
outside your Perl script. Configurations can be imported (inherited,
stacked,...), sections can be grouped, and settings can be accessed from a
tied hash.

%prep
%setup -q -n Config-IniFiles-%{version}

%build
%{__perl} Build.PL --installdirs=vendor
./Build

%install
rm -rf %{buildroot}

./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
./Build test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes dist.ini LICENSE META.json OLD-Changes.txt README scripts weaver.ini
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 01 2025 Thien Nguyen <nthien86@gmail.com> 3.000003-1
- Initial RPM release for Config::IniFiles Perl module
