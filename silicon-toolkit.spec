%define debug_package   %{nil}

Name:           silicon-toolkit
Summary:        Shattered Silicon Toolkit
Version:        %{_version}
Release:        %{_release}
License:        GPL-2.0
Vendor:         Shattered Silicon Ltd
URL:            https://shatteredsilicon.net
Source0:        %{name}-%{version}-%{release}.tar.gz

Requires: perl-DBI, perl-DBD-MySQL, MariaDB-shared

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
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin
install -m 0755 -d $RPM_BUILD_ROOT/lib/systemd/system
install -m 0755 bin/* $RPM_BUILD_ROOT/usr/bin/
install -m 0644 config/systemd/*.service $RPM_BUILD_ROOT/lib/systemd/system/

%post
%systemd_post st-sideload-relay.service

%preun
%systemd_preun st-sideload-relay.service

%postun
%systemd_postun st-sideload-relay.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/*
%config /lib/systemd/system/*
