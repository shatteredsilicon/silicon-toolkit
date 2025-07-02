Name:           perl-Scalar-List-Utils
Version:        1.69
Release:        1%{?dist}
Summary:        Distribution of general-utility subroutines

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/pod/List::Util
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Scalar-List-Utils-%{version}.tar.gz

BuildRequires:  perl >= 0:5.006
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)

# Only needed on RHEL 8+, not present on RHEL 7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

Requires:       perl
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides:       perl(List::Util) = %{version}
Provides:       perl(List::Util::XS) = %{version}
Provides:       perl(Scalar::Util) = %{version}
Provides:       perl(Sub::Util) = %{version}
Provides:       perl(Sub::Identify) = %{version}


%description
Scalar::List::Utils does nothing on its own. It is packaged with several
useful modules.

%prep
%setup -q -n Scalar-List-Utils-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes META.json README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/List*
%{perl_vendorarch}/Scalar*
%{perl_vendorarch}/Sub*
%{_mandir}/man3/*

%changelog
* Tue Jul 01 2025 Thien Nguyen <nthien86@gmail.com> 1.69-1
- Initial RPM release for Scalar::List::Utils Perl module
