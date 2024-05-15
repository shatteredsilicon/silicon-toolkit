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

go install -ldflags="-s -w" ./src/go/...
%{__cp} bin/* %{_GOPATH}/bin

strip %{_GOPATH}/bin/* || true

%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin
for file in %{_GOPATH}/bin/*
do
    cp $file $RPM_BUILD_ROOT/usr/bin/
    st_basename=$(basename $file)
    if [ " st-sideload-relay st-int-capacity-checker st-unused-key-checker st-oversized-blobs " == *" $st_basename "* ]; then
        continue
    fi
    cp $file $RPM_BUILD_ROOT/usr/bin/pt${st_basename#st}
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/st-*


%package compat
Summary:        Shattered Silicon Toolkit (compat)

%description compat
Shattered Silicon Toolkit (compat)

%files compat
/usr/bin/{st,pt}-*
