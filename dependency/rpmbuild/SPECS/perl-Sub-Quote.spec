Name:           perl-Sub-Quote
Version:        2.006008
Release:        8%{?dist}
Summary:        Efficient generation of subroutines via string eval
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Sub-Quote
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Sub-Quote-%{version}.tar.gz

BuildArch:      noarch

# Base build tools
BuildRequires:  coreutils
BuildRequires:  make

# Perl environment and toolchain
BuildRequires:  perl >= 5.006
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)

# Only on RHEL 8+, not present on EL7
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
%endif

# Non-core or versioned modules needed at build/run-time
BuildRequires:  perl(XString) >= 0.003
BuildRequires:  perl(Test::More) >= 0.94

# Runtime requirements
Requires:       perl(XString) >= 0.003

# Compatibility handling
Conflicts:      perl-Moo < 2.003000

# Provides declarations
Provides:       perl(Sub::Quote) = %{version}
Provides:       perl(Sub::Defer) = %{version}

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(ErrorLocation\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(InlineModule\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Sub::Name\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(ThreadsCheck\\)

%description
This package provides performant ways to generate subroutines from strings.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Sub-Quote-%{version}

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}

# Clean up unnecessary files
find %{buildroot} -name perllocal.pod -delete
find %{buildroot} -name .packlist -delete

%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -r -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Thu Jul 03 2025 Thien Nguyen <nthien86@gmail.com> - 2.006008-8
- Added provides

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.006008-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.006008-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.006008-5
- Filter perl(Sub::Name) from tests

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.006008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.006008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.006008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 24 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.006008-1
- 2.006008 bump
- Package tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.006006-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.006006-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.006006-9
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.006006-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.006006-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.006006-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.006006-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.006006-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.006006-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.006006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.006006-1
- 2.006006 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.006003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.006003-2
- Perl 5.30 rebuild

* Mon Mar 11 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.006003-1
- 2.006003 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.005001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.005001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.005001-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.005001-1
- 2.005001 bump

* Wed Feb 07 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.005000-1
- 2.005000 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.004000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.004000-1
- 2.004000 bump

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.003001-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.003001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.003001-1
- Initial release
