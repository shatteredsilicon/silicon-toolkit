BUILDDIR	?= /tmp/ssmbuild
VERSION		?=
RELEASE		?= 1

ifeq (0, $(shell hash dpkg 2>/dev/null; echo $$?))
ARCH	:= $(shell dpkg --print-architecture)
else
ARCH	:= $(shell rpm --eval "%{_arch}")
endif

TARBALL_FILE	:= $(BUILDDIR)/tarballs/silicon-toolkit-$(VERSION)-$(RELEASE).tar.gz
SRPM_FILE		:= $(BUILDDIR)/results/SRPMS/silicon-toolkit-$(VERSION)-$(RELEASE).src.rpm
RPM_FILES		:= $(BUILDDIR)/results/RPMS/silicon-toolkit-$(VERSION)-$(RELEASE).$(ARCH).rpm $(BUILDDIR)/results/RPMS/silicon-toolkit-compat-$(VERSION)-$(RELEASE).$(ARCH).rpm

.PHONY: all
all: srpm rpm

$(TARBALL_FILE):
	mkdir -vp $(shell dirname $(TARBALL_FILE))

	GO111MODULE=on go mod vendor

	tar --exclude-vcs -czf $(TARBALL_FILE) -C $(shell dirname $(CURDIR)) --transform s/^$(shell basename $(CURDIR))/silicon-toolkit/ $(shell basename $(CURDIR))

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
rpm: $(RPM_FILES)

$(RPM_FILES): $(SRPM_FILE)
	mkdir -vp $(BUILDDIR)/mock
	mock -r ssm-9-$(ARCH) --resultdir $(BUILDDIR)/mock --rebuild $(SRPM_FILE)

	for rpm_file in $(RPM_FILES); do \
		mkdir -vp $$(dirname $${rpm_file}); \
		mv $(BUILDDIR)/mock/$$(basename $${rpm_file}) $${rpm_file}; \
	done

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/{tarballs,rpmbuild,mock,results}