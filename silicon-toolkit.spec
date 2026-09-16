%define debug_package   %{nil}

Name:           silicon-toolkit
Summary:        Shattered Silicon Toolkit
Version:        %{_version}
Release:        %{_release}%{?dist}
License:        GPL-2.0
Vendor:         Shattered Silicon Ltd
URL:            https://shatteredsilicon.net
Source0:        %{name}-%{version}-%{_release}.tar.gz

Requires: initscripts, chkconfig

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
install -m 0755 -d $RPM_BUILD_ROOT/etc/init.d/
install -m 0755 bin/* %{buildroot}%{_bindir}/
install -m 0755 config/init.d/* $RPM_BUILD_ROOT/etc/init.d/

%post
for service in st-{prioritizer,sideload-relay}; do
    /sbin/chkconfig --add "$service" || :
done

%preun
# uninstall
if [ "$1" = "0" ]; then
    for service in st-{prioritizer,sideload-relay}; do
        /sbin/service "$service" stop || :
        /sbin/chkconfig --del "service" || :
    done
fi

%postun


%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/*
%config /etc/init.d/st-prioritizer
%config /etc/init.d/st-sideload-relay
