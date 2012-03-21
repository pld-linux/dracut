Summary:	Initramfs generator using udev
Name:		dracut
Version:	017
Release:	0.5
License:	GPL v2+
Group:		Base
Source0:	ftp://www.kernel.org/pub/linux/utils/boot/dracut/%{name}-%{version}.tar.xz
# Source0-md5:	8c966954cd973b5abbd7193368f1d5cc
Source1:	pld.conf
Patch0:		no-rh.patch
Patch1:		create-target-dir-for-symlink.patch
Patch2:		bash-sh.patch
URL:		https://dracut.wiki.kernel.org/
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt-progs
Requires:	bash
Requires:	coreutils
Requires:	cpio
Requires:	filesystem >= 2.1.0
Requires:	findutils
Requires:	grep
Requires:	gzip
Requires:	hardlink
Requires:	module-init-tools >= 3.7-9
Requires:	sed
Requires:	systemd-units
Requires:	udev
Requires:	util-linux >= 2.20
Suggests:	dash
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dracutlibdir	%{_prefix}/lib/dracut

%description
Dracut contains tools to create a bootable initramfs for 2.6 Linux
kernels. Unlike existing implementations, dracut does hard-code as
little as possible into the initramfs. Dracut contains various modules
which are driven by the event-based udev. Having root on MD, DM, LVM2,
LUKS is supported as well as NFS, iSCSI, NBD, FCoE with the
dracut-network package.

%package network
Summary:	Dracut modules to build a dracut initramfs with network support
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description network
This package requires everything which is needed to build a generic
all purpose initramfs with network support with dracut.

%package fips
Summary:	Dracut modules to build a dracut initramfs with an integrity check
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	hmaccalc
Requires:	nss-softokn-freebl

%description fips
This package requires everything which is needed to build an all
purpose initramfs with dracut, which does an integrity check.

This package requires everything which is needed to build an all
purpose initramfs with dracut, which does an integrity check.

%package fips-aesni
Summary:	Dracut modules to build a dracut initramfs with an integrity check with aesni-intel
Group:		Base
Requires:	%{name}-fips = %{version}-%{release}

%description fips-aesni
This package requires everything which is needed to build an all
purpose initramfs with dracut, which does an integrity check and adds
the aesni-intel kernel module.

%package caps
Summary:	Dracut modules to build a dracut initramfs which drops capabilities
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	libcap

%description caps
This package requires everything which is needed to build an all
purpose initramfs with dracut, which drops capabilities.

%package tools
Summary:	Dracut tools to build the local initramfs
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description tools
This package contains tools to assemble the local initrd and host
configuration.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/boot/dracut,/etc/logrotate.d,/sbin} \
	$RPM_BUILD_ROOT/var/{log,lib/{dracut/overlay,initramfs}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_prefix}/lib \
	bindir=%{_bindir} \
	systemdsystemunitdir=%{systemdunitdir} \
	sysconfdir=%{_sysconfdir} \
	mandir=%{_mandir}

echo %{name}-%{version}-%{release} > $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/10rpmversion/dracut-version

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/dracut.conf.d/01-dist.conf
install -p dracut.conf.d/fips.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/dracut.conf.d/40-fips.conf
install -p dracut.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/dracut_log

# create compat symlink
ln -s %{_bindir}/dracut $RPM_BUILD_ROOT/sbin/dracut

# remove gentoo specific modules
%{__rm} -r $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/50gensplash

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README HACKING TODO COPYING AUTHORS NEWS dracut.html dracut.png dracut.svg
%dir %{_sysconfdir}/dracut.conf.d
%config(noreplace) %{_sysconfdir}/dracut.conf
%config(noreplace) %{_sysconfdir}/dracut.conf.d/01-dist.conf
%config(noreplace) /etc/logrotate.d/dracut_log
# compat symlink
%attr(755,root,root) /sbin/dracut
%attr(755,root,root) %{_bindir}/dracut
%attr(755,root,root) %{_bindir}/mkinitrd
%attr(755,root,root) %{_bindir}/lsinitrd
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%attr(755,root,root) %{dracutlibdir}/dracut-functions.sh
%attr(755,root,root) %{dracutlibdir}/dracut-functions
%attr(755,root,root) %{dracutlibdir}/dracut-logger.sh
%attr(755,root,root) %{dracutlibdir}/dracut-initramfs-restore
%dir %{dracutlibdir}/modules.d/00bootchart
%attr(755,root,root) %{dracutlibdir}/modules.d/00bootchart/*.sh
%dir %{dracutlibdir}/modules.d/00dash
%attr(755,root,root) %{dracutlibdir}/modules.d/00dash/*.sh
%dir %{dracutlibdir}/modules.d/01bash
%attr(755,root,root) %{dracutlibdir}/modules.d/01bash/*.sh
%dir %{dracutlibdir}/modules.d/05busybox
%attr(755,root,root) %{dracutlibdir}/modules.d/05busybox/*.sh
%dir %{dracutlibdir}/modules.d/10i18n
%{dracutlibdir}/modules.d/10i18n/README
%{dracutlibdir}/modules.d/10i18n/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/10i18n/*.sh
%dir %{dracutlibdir}/modules.d/10rpmversion
%{dracutlibdir}/modules.d/10rpmversion/dracut-version
%attr(755,root,root) %{dracutlibdir}/modules.d/10rpmversion/*.sh
%dir %{dracutlibdir}/modules.d/30convertfs
%attr(755,root,root) %{dracutlibdir}/modules.d/30convertfs/*.sh
%dir %{dracutlibdir}/modules.d/45url-lib
%attr(755,root,root) %{dracutlibdir}/modules.d/45url-lib/*.sh
%dir %{dracutlibdir}/modules.d/50plymouth
%attr(755,root,root) %{dracutlibdir}/modules.d/50plymouth/*.sh
%dir %{dracutlibdir}/modules.d/90btrfs
%{dracutlibdir}/modules.d/90btrfs/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/90btrfs/*.sh
%dir %{dracutlibdir}/modules.d/90crypt
%attr(755,root,root) %{dracutlibdir}/modules.d/90crypt/*.sh
%dir %{dracutlibdir}/modules.d/90dm
%{dracutlibdir}/modules.d/90dm/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/90dm/*.sh
%dir %{dracutlibdir}/modules.d/90dmraid
%{dracutlibdir}/modules.d/90dmraid/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/90dmraid/*.sh
%dir %{dracutlibdir}/modules.d/90dmsquash-live
%attr(755,root,root) %{dracutlibdir}/modules.d/90dmsquash-live/*.sh
%dir %{dracutlibdir}/modules.d/90kernel-modules
%attr(755,root,root) %{dracutlibdir}/modules.d/90kernel-modules/*.sh
%dir %{dracutlibdir}/modules.d/90lvm
%{dracutlibdir}/modules.d/90lvm/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/90lvm/*.sh
%dir %{dracutlibdir}/modules.d/90mdraid
%{dracutlibdir}/modules.d/90mdraid/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/90mdraid/*.sh
%dir %{dracutlibdir}/modules.d/90multipath
%attr(755,root,root) %{dracutlibdir}/modules.d/90multipath/*.sh
%dir %{dracutlibdir}/modules.d/91crypt-gpg
%attr(755,root,root) %{dracutlibdir}/modules.d/91crypt-gpg/*.sh
%dir %{dracutlibdir}/modules.d/95debug
%attr(755,root,root) %{dracutlibdir}/modules.d/95debug/*.sh
%dir %{dracutlibdir}/modules.d/95resume
%attr(755,root,root) %{dracutlibdir}/modules.d/95resume/*.sh
%dir %{dracutlibdir}/modules.d/95rootfs-block
%attr(755,root,root) %{dracutlibdir}/modules.d/95rootfs-block/*.sh
%dir %{dracutlibdir}/modules.d/95dasd
%attr(755,root,root) %{dracutlibdir}/modules.d/95dasd/*.sh
%dir %{dracutlibdir}/modules.d/95dasd_mod
%attr(755,root,root) %{dracutlibdir}/modules.d/95dasd_mod/*.sh
%dir %{dracutlibdir}/modules.d/95fstab-sys
%attr(755,root,root) %{dracutlibdir}/modules.d/95fstab-sys/*.sh
%dir %{dracutlibdir}/modules.d/95zfcp
%{dracutlibdir}/modules.d/95zfcp/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/95zfcp/*.sh
%dir %{dracutlibdir}/modules.d/95terminfo
%attr(755,root,root) %{dracutlibdir}/modules.d/95terminfo/*.sh
%dir %{dracutlibdir}/modules.d/95udev-rules
%{dracutlibdir}/modules.d/95udev-rules/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/95udev-rules/*.sh
%dir %{dracutlibdir}/modules.d/96securityfs
%attr(755,root,root) %{dracutlibdir}/modules.d/96securityfs/*.sh
%dir %{dracutlibdir}/modules.d/97biosdevname
%attr(755,root,root) %{dracutlibdir}/modules.d/97biosdevname/*.sh
%dir %{dracutlibdir}/modules.d/97masterkey
%{dracutlibdir}/modules.d/97masterkey/README
%attr(755,root,root) %{dracutlibdir}/modules.d/97masterkey/*.sh
%dir %{dracutlibdir}/modules.d/98ecryptfs
%{dracutlibdir}/modules.d/98ecryptfs/README
%attr(755,root,root) %{dracutlibdir}/modules.d/98ecryptfs/*.sh
%dir %{dracutlibdir}/modules.d/98integrity
%{dracutlibdir}/modules.d/98integrity/README
%attr(755,root,root) %{dracutlibdir}/modules.d/98integrity/*.sh
%dir %{dracutlibdir}/modules.d/98selinux
%attr(755,root,root) %{dracutlibdir}/modules.d/98selinux/*.sh
%dir %{dracutlibdir}/modules.d/98syslog
%{dracutlibdir}/modules.d/98syslog/README
%{dracutlibdir}/modules.d/98syslog/rsyslog.conf
%attr(755,root,root) %{dracutlibdir}/modules.d/98syslog/*.sh
%dir %{dracutlibdir}/modules.d/98usrmount
%attr(755,root,root) %{dracutlibdir}/modules.d/98usrmount/*.sh
%dir %{dracutlibdir}/modules.d/99base
%attr(755,root,root) %{dracutlibdir}/modules.d/99base/*.sh
%dir %{dracutlibdir}/modules.d/99fs-lib
%attr(755,root,root) %{dracutlibdir}/modules.d/99fs-lib/*.sh
%dir %{dracutlibdir}/modules.d/99img-lib
%attr(755,root,root) %{dracutlibdir}/modules.d/99img-lib/*.sh
%dir %{dracutlibdir}/modules.d/99shutdown
%attr(755,root,root) %{dracutlibdir}/modules.d/99shutdown/*.sh
%dir /var/lib/initramfs
%{systemdunitdir}/*.service
%{systemdunitdir}/*/*.service
%{_mandir}/man8/dracut.8*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man5/dracut.conf.5*

%files network
%defattr(644,root,root,755)
%dir %{dracutlibdir}/modules.d/40network
%{dracutlibdir}/modules.d/40network/dhclient.conf
%attr(755,root,root) %{dracutlibdir}/modules.d/40network/*.sh
%dir %{dracutlibdir}/modules.d/95fcoe
%attr(755,root,root) %{dracutlibdir}/modules.d/95fcoe/*.sh
%dir %{dracutlibdir}/modules.d/95iscsi
%attr(755,root,root) %{dracutlibdir}/modules.d/95iscsi/*.sh
%dir %{dracutlibdir}/modules.d/90livenet
%attr(755,root,root) %{dracutlibdir}/modules.d/90livenet/*.sh
%dir %{dracutlibdir}/modules.d/95nbd
%attr(755,root,root) %{dracutlibdir}/modules.d/95nbd/*.sh
%dir %{dracutlibdir}/modules.d/95nfs
%attr(755,root,root) %{dracutlibdir}/modules.d/95nfs/*.sh
%dir %{dracutlibdir}/modules.d/95ssh-client
%attr(755,root,root) %{dracutlibdir}/modules.d/95ssh-client/*.sh
%dir %{dracutlibdir}/modules.d/45ifcfg
%attr(755,root,root) %{dracutlibdir}/modules.d/45ifcfg/*.sh
%dir %{dracutlibdir}/modules.d/95znet
%attr(755,root,root) %{dracutlibdir}/modules.d/95znet/*.sh

%files fips
%defattr(644,root,root,755)
%{dracutlibdir}/modules.d/01fips
%config(noreplace) %{_sysconfdir}/dracut.conf.d/40-fips.conf

%files fips-aesni
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{dracutlibdir}/modules.d/02fips-aesni/*.sh

%files caps
%defattr(644,root,root,755)
%{dracutlibdir}/modules.d/02caps/README
%attr(755,root,root) %{dracutlibdir}/modules.d/02caps/*.sh

%files tools
%defattr(644,root,root,755)
%{_mandir}/man8/dracut-gencmdline.8*
%{_mandir}/man8/dracut-catimages.8*
%attr(755,root,root) %{_bindir}/dracut-gencmdline
%attr(755,root,root) %{_bindir}/dracut-catimages
%dir /boot/dracut
%dir /var/lib/dracut
%dir /var/lib/dracut/overlay
