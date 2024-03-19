BUILDDIR	?= /tmp/ssmbuild
VERSION		?= 3.5.7.1
RELEASE		?= 1

ifeq (0, $(shell hash dpkg 2>/dev/null; echo $$?))
ARCH	:= $(shell dpkg --print-architecture)
else
ARCH	:= $(shell rpm --eval "%{_arch}")
endif

TARBALL_FILE	:= $(BUILDDIR)/tarballs/silicon-toolkit-$(VERSION)-$(RELEASE).tar.gz
SRPM_FILE		:= $(BUILDDIR)/results/SRPMS/silicon-toolkit-$(VERSION)-$(RELEASE).src.rpm
RPM_FILE		:= $(BUILDDIR)/results/RPMS/silicon-toolkit-$(VERSION)-$(RELEASE).$(ARCH).rpm

.PHONY: all
all: srpm rpm

$(TARBALL_FILE):
	mkdir -vp $(shell dirname $(TARBALL_FILE))

	GO111MODULE=on go mod vendor

	tar -czf $(TARBALL_FILE) -C $(shell dirname $(CURDIR)) --transform s/^$(shell basename $(CURDIR))/silicon-toolkit/ $(shell basename $(CURDIR))

.PHONY: srpm
srpm: $(SRPM_FILE)

$(SRPM_FILE): $(TARBALL_FILE)
	mkdir -vp $(BUILDDIR)/rpmbuild/{SOURCES,SPECS,BUILD,SRPMS,RPMS}
	mkdir -vp $(shell dirname $(SRPM_FILE))

	cp silicon-toolkit.spec $(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec
	sed -i "s/%{_version}/$(VERSION)/g" "$(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec"
	sed -i "s/%{_release}/$(RELEASE)/g" "$(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec"
	cp $(TARBALL_FILE) $(BUILDDIR)/rpmbuild/SOURCES/
	spectool -C $(BUILDDIR)/rpmbuild/SOURCES/ -g $(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec
	rpmbuild -bs --define "debug_package %{nil}" --define "_topdir $(BUILDDIR)/rpmbuild" $(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec
	mv $(BUILDDIR)/rpmbuild/SRPMS/$(shell basename $(SRPM_FILE)) $(SRPM_FILE)

.PHONY: rpm
rpm: $(RPM_FILE)

$(RPM_FILE): $(SRPM_FILE)
	mkdir -vp $(BUILDDIR)/mock $(shell dirname $(RPM_FILE))
	mock -r ssm-9-$(ARCH) --resultdir $(BUILDDIR)/mock --rebuild $(SRPM_FILE)
	mv $(BUILDDIR)/mock/$(shell basename $(RPM_FILE)) $(RPM_FILE)

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/{tarballs,rpmbuild,mock,results}