Name:           perl-Text-Aligner
Version:        0.16
Release:        1%{?dist}
Summary:        Align text in various styles (left, right, center, etc)

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Aligner
Source0:        https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Text-Aligner-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  perl >= 0:5.008
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Term::ANSIColor) >= 2.02
BuildRequires:  perl(Test::More) >= 0.88

# Only needed on RHEL 8+, not present on RHEL 7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

Requires:       perl(Term::ANSIColor) >= 2.02
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides:       perl(Text::Aligner) = %{version}

%description
Text::Aligner exports a single function, align(), which is used to justify
strings to various alignment styles. The alignment specification is the
first argument, followed by any number of scalars which are subject to
alignment.

%prep
%setup -q -n Text-Aligner-%{version}

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
%doc Changes dist.ini LICENSE META.json README scripts
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 01 2025 Thien Nguyen <nthien86@gmail.com> 0.16-1
- Initial RPM release for Text::Aligner Perl module
