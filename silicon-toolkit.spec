%define debug_package   %{nil}

Name:           silicon-toolkit
Summary:        Shattered Silicon Toolkit
Version:        %{_version}
Release:        %{_release}
License:        GPL-2.0
Vendor:         Shattered Silicon Ltd
URL:            https://shatteredsilicon.net
Source0:        %{name}-%{version}-%{release}.tar.gz

# Build dependencies
BuildRequires:  perl
BuildRequires:  systemd

# These packages only exist on RHEL/OL 8 and later
%if 0%{?rhel} >= 8
BuildRequires:  perl-generators
BuildRequires:  systemd-rpm-macros
%endif

# Required Perl modules
Requires: perl
Requires: perl(Capture::Tiny)
Requires: perl(Config::IniFiles)
Requires: perl(DBD::mysql)
Requires: perl(JSON)
Requires: perl(Number::Bytes::Human)
Requires: perl(Parallel::ForkManager)
Requires: perl(Proc::Pidfile)
Requires: perl(Text::Table)

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
Silicon Toolkit is a collection of advanced command-line tools used by
Shattered Silicon (https://shatteredsilicon.net/) support staff to perform
a variety of MySQL and system tasks that are too difficult or complex
to perform manually.

These tools are ideal alternatives to private or "one-off" scripts because
they are professionally developed, formally tested, and fully documented.
They are also fully self-contained, so installation is quick and easy and
no libraries are installed.

Silicon Toolkit is developed and supported by Shattered Silicon.  For more
information and other free, open-source software developed by Shattered Silicon,
visit https://github.com/shatteredsilicon.

%prep
%setup -q -n %{name}

%install
install -d -m 0755 %{buildroot}%{_bindir}
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0755 bin/* %{buildroot}%{_bindir}/
install -m 0644 config/systemd/*.service %{buildroot}%{_unitdir}/

%post
%systemd_post st-sideload-relay.service
%systemd_post st-prioritizer.service

%preun
%systemd_preun st-sideload-relay.service
%systemd_preun st-prioritizer.service

%postun
%systemd_postun st-sideload-relay.service
%systemd_postun st-prioritizer.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/*
%config %{_unitdir}/*.service
