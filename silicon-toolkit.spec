%define debug_package   %{nil}
%define _GOPATH         %{_builddir}/go

Name:           silicon-toolkit
Summary:        Shattered Silicon Toolkit
Version:        %{_version}
Release:        %{_release}
License:        GPL-2.0
Vendor:         Shattered Silicon Ltd
URL:            https://shatteredsilicon.net
Source0:        %{name}-%{version}-%{release}.tar.gz
BuildRequires:  golang

Requires: perl-DBI, perl-DBD-MySQL, MariaDB-shared

%description
Shattered Silicon Toolkit

%prep
%setup -q -n %{name}

%build
mkdir -p %{_GOPATH}/bin
export GOPATH=%{_GOPATH}

go build -ldflags="-s -w" ./src/go/pt-mongodb-summary
%{__cp} pt-mongodb-summary %{_GOPATH}/bin
%{__cp} bin/pt-mysql-summary %{_GOPATH}/bin
%{__cp} bin/pt-summary %{_GOPATH}/bin
%{__cp} bin/pt-visual-explain %{_GOPATH}/bin
%{__cp} bin/pt-archiver %{_GOPATH}/bin

strip %{_GOPATH}/bin/* || true

%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin
install -m 0755 %{_GOPATH}/bin/pt-summary $RPM_BUILD_ROOT/usr/bin/st-summary
install -m 0755 %{_GOPATH}/bin/pt-summary $RPM_BUILD_ROOT/usr/bin/pt-summary
install -m 0755 %{_GOPATH}/bin/pt-mysql-summary $RPM_BUILD_ROOT/usr/bin/st-mysql-summary
install -m 0755 %{_GOPATH}/bin/pt-mysql-summary $RPM_BUILD_ROOT/usr/bin/pt-mysql-summary
install -m 0755 %{_GOPATH}/bin/pt-mongodb-summary $RPM_BUILD_ROOT/usr/bin/st-mongodb-summary
install -m 0755 %{_GOPATH}/bin/pt-mongodb-summary $RPM_BUILD_ROOT/usr/bin/pt-mongodb-summary
install -m 0755 %{_GOPATH}/bin/pt-visual-explain $RPM_BUILD_ROOT/usr/bin/st-visual-explain
install -m 0755 %{_GOPATH}/bin/pt-visual-explain $RPM_BUILD_ROOT/usr/bin/pt-visual-explain
install -m 0755 %{_GOPATH}/bin/pt-archiver $RPM_BUILD_ROOT/usr/bin/st-archiver
install -m 0755 %{_GOPATH}/bin/pt-archiver $RPM_BUILD_ROOT/usr/bin/pt-archiver

%clean
rm -rf $RPM_BUILD_ROOT

%postun
# uninstall
if [ "$1" = "0" ]; then
    rm -f /usr/bin/{st,pt}-summary
    rm -f /usr/bin/{st,pt}-mysql-summary
    rm -f /usr/bin/{st,pt}-mongodb-summary
    rm -f /usr/bin/{st,pt}-visual-explain
    rm -f /usr/bin/{st,pt}-archiver
    echo "Uninstall complete."
fi

%files
/usr/bin/{st,pt}-summary
/usr/bin/{st,pt}-mysql-summary
/usr/bin/{st,pt}-mongodb-summary
/usr/bin/{st,pt}-visual-explain
/usr/bin/{st,pt}-archiver
