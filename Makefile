BUILDDIR	?= /tmp/ssmbuild
VERSION		?=
RELEASE		?= 1

.PHONY: all
all:

ifeq (0, $(shell hash dpkg 2>/dev/null; echo $$?))
ARCH	:= $(shell dpkg --print-architecture)
all: sdeb deb
else
ARCH	:= $(shell rpm --eval "%{_arch}")
all: srpm rpm
endif

TARBALL_FILE	:= $(BUILDDIR)/tarballs/silicon-toolkit-$(VERSION)-$(RELEASE).tar.gz
SRPM_FILE		:= $(BUILDDIR)/results/SRPMS/silicon-toolkit-$(VERSION)-$(RELEASE).src.rpm $(BUILDDIR)/results/SRPMS/perl-Capture-Tiny-0.50-1.src.rpm $(BUILDDIR)/results/SRPMS/perl-Proc-Pidfile-1.10-1.src.rpm 
RPM_FILES		:= $(BUILDDIR)/results/RPMS/silicon-toolkit-$(VERSION)-$(RELEASE).$(ARCH).rpm $(BUILDDIR)/results/RPMS/perl-Capture-Tiny-0.50-1.noarch.rpm $(BUILDDIR)/results/RPMS/perl-Proc-Pidfile-1.10-1.noarch.rpm
SDEB_FILES		:= $(BUILDDIR)/results/SDEBS/silicon-toolkit_$(VERSION)-$(RELEASE).dsc $(BUILDDIR)/results/SDEBS/silicon-toolkit_$(VERSION)-$(RELEASE).tar.gz
DEB_FILES		:= $(BUILDDIR)/results/DEBS/silicon-toolkit_$(VERSION)-$(RELEASE)_$(ARCH).deb $(BUILDDIR)/results/DEBS/silicon-toolkit_$(VERSION)-$(RELEASE)_$(ARCH).changes

$(TARBALL_FILE):
	mkdir -vp $(shell dirname $(TARBALL_FILE))

	tar --exclude-vcs -czf $(TARBALL_FILE) -C $(shell dirname $(CURDIR)) --transform s/^$(shell basename $(CURDIR))/silicon-toolkit/ $(shell basename $(CURDIR))

.PHONY: srpm
srpm: $(SRPM_FILE)

$(SRPM_FILE):
	mkdir -vp $(BUILDDIR)/rpmbuild/{SOURCES,SPECS,BUILD,SRPMS,RPMS}
	mkdir -vp $(shell dirname $(SRPM_FILE))

	# prepare and build silicon-toolkit
	tar --exclude-vcs -czf $(BUILDDIR)/rpmbuild/SOURCES/$(shell basename $(TARBALL_FILE)) -C $(shell dirname $(CURDIR)) --transform s/^$(shell basename $(CURDIR))/silicon-toolkit/ $(shell basename $(CURDIR))
	cp silicon-toolkit.spec $(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec
	sed -i "s/%{_version}/$(VERSION)/g" "$(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec"
	sed -i "s/%{_release}/$(RELEASE)/g" "$(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec"
	spectool -C $(BUILDDIR)/rpmbuild/SOURCES/ -g $(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec
	rpmbuild -bs --define "debug_package %{nil}" --define "_topdir $(BUILDDIR)/rpmbuild" $(BUILDDIR)/rpmbuild/SPECS/silicon-toolkit.spec

	# prepare and build dependencies
	cd $(BUILDDIR)/rpmbuild/SOURCES && source $(CURDIR)/dependency/rpmbuild/SOURCES/prep_sources.sh
	cp dependency/rpmbuild/SPECS/perl-Capture-Tiny.spec $(BUILDDIR)/rpmbuild/SPECS/
	cp dependency/rpmbuild/SPECS/perl-Proc-Pidfile.spec $(BUILDDIR)/rpmbuild/SPECS/
	sed -i '/^\s*Requires:\s*perl(:MODULE_COMPAT_/d' $(BUILDDIR)/rpmbuild/SPECS/perl-Capture-Tiny.spec
	sed -i '/^\s*Requires:\s*perl(:MODULE_COMPAT_/d' $(BUILDDIR)/rpmbuild/SPECS/perl-Proc-Pidfile.spec
	rpmbuild -bs --define "debug_package %{nil}" --define "_topdir $(BUILDDIR)/rpmbuild" --define 'dist %{nil}' $(BUILDDIR)/rpmbuild/SPECS/perl-Capture-Tiny.spec
	rpmbuild -bs --define "debug_package %{nil}" --define "_topdir $(BUILDDIR)/rpmbuild" --define 'dist %{nil}' $(BUILDDIR)/rpmbuild/SPECS/perl-Proc-Pidfile.spec

	for srpm_file in $(SRPM_FILE); do \
		mv $(BUILDDIR)/rpmbuild/SRPMS/$$(basename $${srpm_file}) $${srpm_file}; \
	done

.PHONY: rpm
rpm: $(RPM_FILES)

$(RPM_FILES): $(SRPM_FILE)
	mkdir -vp $(BUILDDIR)/mock

	for srpm_file in $(SRPM_FILE); do \
		mock -r oraclelinux-7-$(ARCH) --resultdir $(BUILDDIR)/mock --define 'dist %{nil}' --rebuild $${srpm_file}; \
	done

	for rpm_file in $(RPM_FILES); do \
		mkdir -vp $$(dirname $${rpm_file}); \
		mv $(BUILDDIR)/mock/$$(basename $${rpm_file}) $${rpm_file}; \
	done

.PHONY: sdeb
sdeb: $(SDEB_FILES)

$(SDEB_FILES): $(TARBALL_FILE)
	mkdir -vp $(BUILDDIR)/debbuild/SDEB/silicon-toolkit-$(VERSION)-$(RELEASE)
	cp -r config/deb $(BUILDDIR)/debbuild/SDEB/silicon-toolkit-$(VERSION)-$(RELEASE)/debian
	cp $(TARBALL_FILE) $(BUILDDIR)/debbuild/SDEB/silicon-toolkit-$(VERSION)-$(RELEASE)

	cd $(BUILDDIR)/debbuild/SDEB/silicon-toolkit-$(VERSION)-$(RELEASE)/; \
		sed -i "s/%{_version}/$(VERSION)/g"  debian/control; \
		sed -i "s/%{_release}/$(RELEASE)/g"  debian/control; \
		sed -i "s/%{_version}/$(VERSION)/g"  debian/rules; \
		sed -i "s/%{_release}/$(RELEASE)/g"  debian/rules; \
		sed -i "s/%{_version}/$(VERSION)/g"  debian/changelog; \
		sed -i "s/%{_release}/$(RELEASE)/g"  debian/changelog; \
		dpkg-buildpackage -S -us

	for sdeb_file in $(SDEB_FILES); do \
		mkdir -vp $$(dirname $${sdeb_file}); \
		mv -f $(BUILDDIR)/debbuild/SDEB/$$(basename $${sdeb_file}) $${sdeb_file}; \
	done

.PHONY: deb
deb: $(DEB_FILES)

$(DEB_FILES): $(SDEB_FILES)
	mkdir -vp $(BUILDDIR)/debbuild/DEB/silicon-toolkit-$(VERSION)-$(RELEASE)
	for sdeb_file in $(SDEB_FILES); do \
		cp -r $${sdeb_file} $(BUILDDIR)/debbuild/DEB/silicon-toolkit-$(VERSION)-$(RELEASE)/; \
	done

	cd $(BUILDDIR)/debbuild/DEB/silicon-toolkit-$(VERSION)-$(RELEASE)/; \
		rm -rf silicon-toolkit-$(VERSION); \
		dpkg-source -x -sp silicon-toolkit_$(VERSION)-$(RELEASE).dsc; \
		cd silicon-toolkit-$(VERSION); \
			dpkg-buildpackage -b -uc

	for deb_file in $(DEB_FILES); do \
		mkdir -vp $$(dirname $${deb_file}); \
		mv -f $(BUILDDIR)/debbuild/DEB/silicon-toolkit-$(VERSION)-$(RELEASE)/$$(basename $${deb_file}) $${deb_file}; \
	done

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/{tarballs,rpmbuild,mock,results}