# Silicon Toolkit
Silicon Toolkit is a collection of advanced command-line tools used by
Shattered Silicon (https://shatteredsilicon.net/) support staff to perform
a variety of MySQL and system tasks that are too time consuming or complex
to perform manually.

These tools are ideal alternatives to private or "one-off" scripts because
they are professionally developed, formally tested, and fully documented.
They are also fully self-contained, so installation is quick and easy and
no libraries are installed.

Silicon Toolkit is developed and supported by Shattered Silicon.  For more
information and other free, open-source software developed by Shattered Silicon,
visit https://github.com/shatteredsilicon.

## Setting up the CentOS 6 environment with Docker and build

Use Docker to setting up a CentOS 6 environemnt with following command:

```
docker run -it -d --privileged library/centos:6.10 bash
```

And run following commands inside the container:

```
rm -f /etc/yum.repos.d/*.repo

cat << 'EOF' > /etc/yum.repos.d/CentOS-Base.repo
[base]
name=CentOS-6.10 - Base Archive
baseurl=https://archive.kernel.org/centos-vault/6.10/os/x86_64/
gpgcheck=1
gpgkey=https://archive.kernel.org/centos-vault/RPM-GPG-KEY-CentOS-6
enabled=1

[updates]
name=CentOS-6.10 - Updates Archive
baseurl=https://archive.kernel.org/centos-vault/6.10/updates/x86_64/
gpgcheck=1
gpgkey=https://archive.kernel.org/centos-vault/RPM-GPG-KEY-CentOS-6
enabled=1

[extras]
name=CentOS-6.10 - Extras Archive
baseurl=https://archive.kernel.org/centos-vault/6.10/extras/x86_64/
gpgcheck=1
gpgkey=https://archive.kernel.org/centos-vault/RPM-GPG-KEY-CentOS-6
enabled=1
EOF

yum install -y git tar rpmdevtools epel-release
yum install -y mock

cat << 'EOF' > /etc/mock/centos-6-x86_64.cfg
config_opts['root'] = 'centos-6-x86_64'
config_opts['target_arch'] = 'x86_64'
config_opts['legal_host_arches'] = ('x86_64',)

config_opts['package_manager'] = 'yum'
config_opts['use_bootstrap'] = False
config_opts['environment']['OPENSSL_ENABLE_SHA1_SIGNATURES'] = '1'

config_opts['chroot_setup_cmd'] = 'install bash bzip2 coreutils cpio diffutils findutils gawk grep gzip info make patch sed shadow-utils tar unzip xz yum rpmdevtools'
config_opts['dist'] = 'el6'
config_opts['releasever'] = '6'
config_opts['dnf_warning'] = False

config_opts['yum.conf'] = """
[main]
assumeyes=1
reposdir=/dev/null

[base]
name=CentOS-6.10 - Base Archive
baseurl=https://archive.kernel.org/centos-vault/6.10/os/x86_64/
gpgcheck=1
gpgkey=https://archive.kernel.org/centos-vault/RPM-GPG-KEY-CentOS-6
enabled=1

[updates]
name=CentOS-6.10 - Updates Archive
baseurl=https://archive.kernel.org/centos-vault/6.10/updates/x86_64/
gpgcheck=1
gpgkey=https://archive.kernel.org/centos-vault/RPM-GPG-KEY-CentOS-6
enabled=1

[extras]
name=CentOS-6.10 - Extras Archive
baseurl=https://archive.kernel.org/centos-vault/6.10/extras/x86_64/
gpgcheck=1
gpgkey=https://archive.kernel.org/centos-vault/RPM-GPG-KEY-CentOS-6
enabled=1
"""
EOF

git clone -b el6 https://github.com/shatteredsilicon/silicon-toolkit.git ~/silicon-toolkit && cd ~/silicon-toolkit
BUILDDIR=~/rpmbuild make
```

And finally the result packages should be located in `~/rpmbuild/results/RPMS/` if all these preceding commands were executed successfully.
The following result packages are dependencies for the silicon-toolkit package in EL6.

- perl-Capture-Tiny
- perl-Proc-Pidfile
- perl-Text-Table+Aligner
