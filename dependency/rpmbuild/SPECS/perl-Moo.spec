Name:           perl-Moo
Version:        2.005005
Release:        1%{?dist}
Summary:        Minimalist Object Orientation (with Moose compatibility)

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/pod/Moo
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Moo-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  perl >= 5.006
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Class::Method::Modifiers) >= 1.10
BuildRequires:  perl(Class::XSAccessor) >= 1.18
BuildRequires:  perl(Role::Tiny) >= 2.002003
BuildRequires:  perl(Scalar::Util) >= 1.00
BuildRequires:  perl(Sub::Defer) >= 2.006006
BuildRequires:  perl(Sub::Quote) >= 2.006006
BuildRequires:  perl(Sub::Util)
BuildRequires:  perl(Test::More)

# Only needed on RHEL 8+, not present on RHEL 7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

Requires:       perl
Requires:       perl(Class::Method::Modifiers) >= 1.10
Requires:       perl(Class::XSAccessor) >= 1.18
Requires:       perl(Role::Tiny) >= 2.002003
Requires:       perl(Scalar::Util) >= 1.00
Requires:       perl(Sub::Defer) >= 2.006006
Requires:       perl(Sub::Quote) >= 2.006006
Requires:       perl(Sub::Util)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides:       perl(Moo) = %{version}


%description
Moo is an extremely light-weight Object Orientation system. It allows one
to concisely define objects and roles with a convenient syntax that avoids
the details of Perl's object system. Moo contains a subset of Moose and is
optimised for rapid startup.

%prep
%setup -q -n Moo-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -name perllocal.pod -delete
find %{buildroot} -name .packlist -delete

find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes LICENSE META.json README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 01 2025 Thien Nguyen <nthien86@gmail.com> 2.005005-1
- Initial RPM release for Moo Perl module
