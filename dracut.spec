Summary:	Initramfs generator using udev
Summary(pl.UTF-8):	Generator initramfs wykorzystujący udev
Name:		dracut
Version:	103
Release:	1
License:	GPL v2+
Group:		Base
Source0:	https://github.com/dracut-ng/dracut-ng/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0fad536babb3cb764eaa8f3fc7eadba4
Source1:	pld.conf
Patch0:		plymouth-libdir.patch
Patch2:		arch-libdir.patch
Patch3:		systemd-paths.patch
Patch4:		cryptsetup.patch
Patch5:		bash.patch
URL:		https://github.com/dracut-ng/dracut-ng/wiki
BuildRequires:	asciidoc
BuildRequires:	dash
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	kmod-devel >= 23
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
Requires:	bash
Requires:	coreutils
Requires:	cpio
Requires:	filesystem
Requires:	findutils
Requires:	glibc-misc
Requires:	grep
Requires:	gzip
Requires:	hardlink
Requires:	kmod >= 23
Requires:	sed
Requires:	systemd-units
Requires:	udev
Requires:	util-linux >= 2.22.2-3
Requires:	vim-rt
Requires:	vim-static
Requires:	virtual(module-tools)
# disabled due to angry (bug)reports, because it changes well known
# net device names from ethX to emX or pXpY
#Suggests:	biosdevname
Suggests:	btrfs-progs
Suggests:	busybox
Suggests:	bzip2
Suggests:	cryptsetup
Suggests:	dash
Suggests:	device-mapper
Suggests:	dmraid
Suggests:	e2fsprogs
Suggests:	gnupg
Suggests:	kbd
Suggests:	keyutils
Suggests:	libselinux-utils
Suggests:	losetup
Suggests:	lvm2
Suggests:	mdadm
Suggests:	multipath-tools
Suggests:	plymouth
Suggests:	suspend-utils
Suggests:	syslogdaemon
Suggests:	xfsprogs
Suggests:	xz
Conflicts:	kmod < 6
Conflicts:	plymounth < 0.9.3-1
Conflicts:	systemd < 1:199
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dracutlibdir	%{_prefix}/lib/dracut

%description
Dracut contains tools to create a bootable initramfs for 2.6 Linux
kernels. Unlike existing implementations, dracut does hard-code as
little as possible into the initramfs. Dracut contains various modules
which are driven by the event-based udev. Having root on MD, DM, LVM2,
LUKS is supported as well as NFS, iSCSI, NBD, FCoE with the
dracut-network package.

%description -l pl.UTF-8
Dracut zawiera narzędzia do tworzenia uruchamialnych obrazów initramfs
dla jąder Linuksa 2.6. W przeciwieństwie do wcześniejszych
implementacji, dracut zaszywa możliwie najmniej stałych w initramfs.
Zawiera różne moduły sterowane w oparciu o zdarzenia udev. Obsługiwane
jest przechowywanie głównego systemu plików na urządzeniach MD, DM,
LVM2, LUKS, a po doinstalowaniu pakietu dracut-network także poprzez
NFS, iSCSI, NBD, FCoE.

%package network
Summary:	Dracut modules to build a dracut initramfs with network support
Summary(pl.UTF-8):	Moduły Dracuta do tworzenia initramfs z obsługą sieci
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	bridge-utils
Requires:	dhcp-client
Requires:	iproute2
Requires:	iputils-arping
Requires:	nbd
Requires:	net-tools
Requires:	nfs-utils-clients
Requires:	open-iscsi
Requires:	openssh-clients
Requires:	ping
Requires:	rpcbind
Suggests:	curl

%description network
This package requires everything which is needed to build a generic
all purpose initramfs with network support with dracut.

%description network -l pl.UTF-8
Ten pakiet zawiera wszystko, co potrzebne do tworzenia przy użyciu
dracuta zwykłych obrazów initramfs dowolnego przeznaczenia z obsługą
sieci.

%package fips
Summary:	Dracut modules to build a dracut initramfs with an integrity check
Summary(pl.UTF-8):	Moduły Dracuta do tworzenia initramfs z kontrolą spójności
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	hmaccalc
Requires:	nss-softokn-freebl
Obsoletes:	dracut-fips-aesni < 048

%description fips
This package requires everything which is needed to build an all
purpose initramfs with dracut, which does an integrity check.

%description fips -l pl.UTF-8
Ten pakiet zawiera wszystko, co potrzebne do tworzenia przy użyciu
dracuta obrazów initramfs dowolnego przeznaczenia, wykonujących
kontrolę własnej spójności.

%package caps
Summary:	Dracut modules to build a dracut initramfs which drops capabilities
Summary(pl.UTF-8):	Moduły Dracuta do tworzenia initramfs zrzucającego uprawnienia
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	libcap

%description caps
This package requires everything which is needed to build an all
purpose initramfs with dracut, which drops capabilities.

%description caps -l pl
Ten pakiet zawiera wszystko, co potrzebne do tworzenia przy użyciu
dracuta obrazów initramfs dowolnego przeznaczenia zrzucających
uprawnienia.

%package tools
Summary:	Dracut tools to build the local initramfs
Summary(pl.UTF-8):	Narzędzia Dracuta do tworzenia lokalnych initramfs
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description tools
This package contains tools to assemble the local initrd and host
configuration.

%description tools -l pl.UTF-8
Ten pakiet zawiera narzędzia do łączenia lokalnych initrd oraz
konfiguracji maszyn.

%package -n bash-completion-dracut
Summary:	bash-completion for dracut
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla polecenia dracut
Group:		Applications/Shells
Requires:	%{name} = %{version}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-dracut
bash-completion for dracut.

%description -n bash-completion-dracut -l pl.UTF-8
Bashowe dopełnianie składni dla polecenia dracut.

%prep
%setup -q -n dracut-ng-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%{__sed} -i -e 's,@libexecdir@,%{_libexecdir},g' modules.d/50plymouth/module-setup.sh
%{__sed} -i -e 's,@lib@,%{_lib},g' modules.d/95resume/module-setup.sh
find modules.d -name '*.orig' | xargs -r %{__rm}

%build
# not autoconf generated
./configure \
	--sysconfdir=%{_sysconfdir} \
	--systemdsystemunitdir=%{systemdunitdir}

%{__make} all doc \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/boot/dracut,/sbin} \
	$RPM_BUILD_ROOT/var/{log,lib/{dracut/overlay,initramfs}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/dracut.conf.d/01-dist.conf
install -p dracut.conf.d/50-fips.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/dracut.conf.d/40-fips.conf

echo "DRACUT_VERSION=%{version}-%{release}" >$RPM_BUILD_ROOT%{dracutlibdir}/dracut-version.sh

# create compat symlink
ln -s %{_bindir}/dracut $RPM_BUILD_ROOT/sbin/dracut

# remove foreign arch modules
%ifnarch ppc ppc64
%{__rm} -r $RPM_BUILD_ROOT%{dracutlibdir}/modules.d/90ppcmac
%endif

# modules used by dracut tests
%{__rm} -r $RPM_BUILD_ROOT%{dracutlibdir}/modules.d/80test{,-makeroot,-root}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS.md README.md docs/HACKING.md dracut.html docs/dracut.png docs/dracut.svg
%dir %{_sysconfdir}/dracut.conf.d
%config(noreplace) %{_sysconfdir}/dracut.conf
%config(noreplace) %{_sysconfdir}/dracut.conf.d/01-dist.conf
# compat symlink
%attr(755,root,root) /sbin/dracut
%attr(755,root,root) %{_bindir}/dracut
%attr(755,root,root) %{_bindir}/lsinitrd
%dir %{dracutlibdir}
%dir %{dracutlibdir}/dracut.conf.d
%attr(755,root,root) %{dracutlibdir}/dracut-install
%attr(755,root,root) %{dracutlibdir}/dracut-util
%dir %{dracutlibdir}/modules.d
%attr(755,root,root) %{dracutlibdir}/dracut-functions.sh
%attr(755,root,root) %{dracutlibdir}/dracut-functions
%attr(755,root,root) %{dracutlibdir}/dracut-init.sh
%attr(755,root,root) %{dracutlibdir}/dracut-logger.sh
%attr(755,root,root) %{dracutlibdir}/dracut-initramfs-restore
%dir %{dracutlibdir}/modules.d/00bash
%attr(755,root,root) %{dracutlibdir}/modules.d/00bash/module-setup.sh
%dir %{dracutlibdir}/modules.d/00dash
%attr(755,root,root) %{dracutlibdir}/modules.d/00dash/*.sh
%dir %{dracutlibdir}/modules.d/00mksh
%attr(755,root,root) %{dracutlibdir}/modules.d/00mksh/module-setup.sh
%dir %{dracutlibdir}/modules.d/00systemd
%attr(755,root,root) %{dracutlibdir}/modules.d/00systemd/module-setup.sh
%dir %{dracutlibdir}/modules.d/00warpclock
%attr(755,root,root) %{dracutlibdir}/modules.d/00warpclock/*.sh
%dir %{dracutlibdir}/modules.d/01systemd-ac-power
%{dracutlibdir}/modules.d/01systemd-ac-power/99-initrd-power-targets.rules
%{dracutlibdir}/modules.d/01systemd-ac-power/initrd-on-ac-power.target
%{dracutlibdir}/modules.d/01systemd-ac-power/initrd-on-battery-power.target
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-ac-power/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-ask-password
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-ask-password/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-bsod
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-bsod/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-coredump
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-coredump/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-creds
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-creds/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-hostnamed
%{dracutlibdir}/modules.d/01systemd-hostnamed/99-systemd-networkd-dracut.conf
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-hostnamed/module-setup.sh
%{dracutlibdir}/modules.d/01systemd-hostnamed/org.freedesktop.hostname1_dracut.conf
%{dracutlibdir}/modules.d/01systemd-hostnamed/systemd-hostname-dracut.conf
%dir %{dracutlibdir}/modules.d/01systemd-initrd
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-initrd/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-integritysetup
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-integritysetup/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-journald
%{dracutlibdir}/modules.d/01systemd-journald/initrd.conf
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-journald/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-ldconfig
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-ldconfig/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-modules-load
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-modules-load/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-pcrphase
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-pcrphase/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-portabled
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-portabled/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-pstore
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-pstore/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-repart
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-repart/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-sysctl
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-sysctl/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-sysext
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-sysext/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-sysusers
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-sysusers/module-setup.sh
%{dracutlibdir}/modules.d/01systemd-sysusers/sysusers-dracut.conf
%dir %{dracutlibdir}/modules.d/01systemd-timedated
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-timedated/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-tmpfiles
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-tmpfiles/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-udevd
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-udevd/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-veritysetup
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-veritysetup/module-setup.sh
%dir %{dracutlibdir}/modules.d/03modsign
%attr(755,root,root) %{dracutlibdir}/modules.d/03modsign/*.sh
%dir %{dracutlibdir}/modules.d/03rescue
%attr(755,root,root) %{dracutlibdir}/modules.d/03rescue/module-setup.sh
%dir %{dracutlibdir}/modules.d/04watchdog
%attr(755,root,root) %{dracutlibdir}/modules.d/04watchdog/*.sh
%dir %{dracutlibdir}/modules.d/04watchdog-modules
%attr(755,root,root) %{dracutlibdir}/modules.d/04watchdog-modules/module-setup.sh
%dir %{dracutlibdir}/modules.d/05busybox
%attr(755,root,root) %{dracutlibdir}/modules.d/05busybox/*.sh
%dir %{dracutlibdir}/modules.d/06dbus-broker
%attr(755,root,root) %{dracutlibdir}/modules.d/06dbus-broker/module-setup.sh
%dir %{dracutlibdir}/modules.d/06dbus-daemon
%attr(755,root,root) %{dracutlibdir}/modules.d/06dbus-daemon/module-setup.sh
%dir %{dracutlibdir}/modules.d/06rngd
%attr(755,root,root) %{dracutlibdir}/modules.d/06rngd/module-setup.sh
%{dracutlibdir}/modules.d/06rngd/rngd.service
%dir %{dracutlibdir}/modules.d/09dbus
%attr(755,root,root) %{dracutlibdir}/modules.d/09dbus/module-setup.sh
%dir %{dracutlibdir}/modules.d/10i18n
%{dracutlibdir}/modules.d/10i18n/README
%{dracutlibdir}/modules.d/10i18n/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/10i18n/*.sh
%dir %{dracutlibdir}/modules.d/30convertfs
%attr(755,root,root) %{dracutlibdir}/modules.d/30convertfs/*.sh
%dir %{dracutlibdir}/modules.d/50drm
%attr(755,root,root) %{dracutlibdir}/modules.d/50drm/module-setup.sh
%dir %{dracutlibdir}/modules.d/50plymouth
%attr(755,root,root) %{dracutlibdir}/modules.d/50plymouth/*.sh
%dir %{dracutlibdir}/modules.d/62bluetooth
%attr(755,root,root) %{dracutlibdir}/modules.d/62bluetooth/module-setup.sh
%dir %{dracutlibdir}/modules.d/80cms
%attr(755,root,root) %{dracutlibdir}/modules.d/80cms/*.sh
%dir %{dracutlibdir}/modules.d/80lvmmerge
%{dracutlibdir}/modules.d/80lvmmerge/README.md
%attr(755,root,root) %{dracutlibdir}/modules.d/80lvmmerge/*.sh
%dir %{dracutlibdir}/modules.d/80lvmthinpool-monitor
%attr(755,root,root) %{dracutlibdir}/modules.d/80lvmthinpool-monitor/*.sh
%{dracutlibdir}/modules.d/80lvmthinpool-monitor/start-thinpool-monitor.service
%dir %{dracutlibdir}/modules.d/81cio_ignore
%attr(755,root,root) %{dracutlibdir}/modules.d/81cio_ignore/*.sh
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
%dir %{dracutlibdir}/modules.d/90dmsquash-live-autooverlay
%attr(755,root,root) %{dracutlibdir}/modules.d/90dmsquash-live-autooverlay/*.sh
%{dracutlibdir}/modules.d/90dmsquash-live/checkisomd5@.service
%dir %{dracutlibdir}/modules.d/90dmsquash-live-ntfs
%attr(755,root,root) %{dracutlibdir}/modules.d/90dmsquash-live-ntfs/*.sh
%dir %{dracutlibdir}/modules.d/90kernel-modules
%attr(755,root,root) %{dracutlibdir}/modules.d/90kernel-modules/*.sh
%dir %{dracutlibdir}/modules.d/90kernel-modules-extra
%attr(755,root,root) %{dracutlibdir}/modules.d/90kernel-modules-extra/*.sh
%dir %{dracutlibdir}/modules.d/90lvm
%{dracutlibdir}/modules.d/90lvm/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/90lvm/*.sh
%dir %{dracutlibdir}/modules.d/90mdraid
%{dracutlibdir}/modules.d/90mdraid/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/90mdraid/*.sh
%dir %{dracutlibdir}/modules.d/90multipath
%attr(755,root,root) %{dracutlibdir}/modules.d/90multipath/*.service
%attr(755,root,root) %{dracutlibdir}/modules.d/90multipath/*.sh
%dir %{dracutlibdir}/modules.d/90numlock
%attr(755,root,root) %{dracutlibdir}/modules.d/90numlock/module-setup.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90numlock/numlock.sh
%dir %{dracutlibdir}/modules.d/90nvdimm
%attr(755,root,root) %{dracutlibdir}/modules.d/90nvdimm/module-setup.sh
%dir %{dracutlibdir}/modules.d/90overlayfs
%attr(755,root,root) %{dracutlibdir}/modules.d/90overlayfs/*.sh
%dir %{dracutlibdir}/modules.d/90pcmcia
%attr(755,root,root) %{dracutlibdir}/modules.d/90pcmcia/module-setup.sh
%dir %{dracutlibdir}/modules.d/90qemu
%attr(755,root,root) %{dracutlibdir}/modules.d/90qemu/*.sh
%dir %{dracutlibdir}/modules.d/90systemd-cryptsetup
%attr(755,root,root) %{dracutlibdir}/modules.d/90systemd-cryptsetup/module-setup.sh
%dir %{dracutlibdir}/modules.d/91crypt-gpg
%{dracutlibdir}/modules.d/91crypt-gpg/README
%attr(755,root,root) %{dracutlibdir}/modules.d/91crypt-gpg/*.sh
%dir %{dracutlibdir}/modules.d/91crypt-loop
%attr(755,root,root) %{dracutlibdir}/modules.d/91crypt-loop/*.sh
%dir %{dracutlibdir}/modules.d/91fido2
%attr(755,root,root) %{dracutlibdir}/modules.d/91fido2/module-setup.sh
%dir %{dracutlibdir}/modules.d/91pcsc
%attr(755,root,root) %{dracutlibdir}/modules.d/91pcsc/module-setup.sh
%{dracutlibdir}/modules.d/91pcsc/pcscd.service
%{dracutlibdir}/modules.d/91pcsc/pcscd.socket
%dir %{dracutlibdir}/modules.d/91pkcs11
%attr(755,root,root) %{dracutlibdir}/modules.d/91pkcs11/module-setup.sh
%dir %{dracutlibdir}/modules.d/91tpm2-tss
%attr(755,root,root) %{dracutlibdir}/modules.d/91tpm2-tss/module-setup.sh
%dir %{dracutlibdir}/modules.d/91zipl
%attr(755,root,root) %{dracutlibdir}/modules.d/91zipl/*.sh
%dir %{dracutlibdir}/modules.d/95dcssblk
%attr(755,root,root) %{dracutlibdir}/modules.d/95dcssblk/*.sh
%dir %{dracutlibdir}/modules.d/95debug
%attr(755,root,root) %{dracutlibdir}/modules.d/95debug/*.sh
%dir %{dracutlibdir}/modules.d/95hwdb
%attr(755,root,root) %{dracutlibdir}/modules.d/95hwdb/module-setup.sh
%dir %{dracutlibdir}/modules.d/95lunmask
%attr(755,root,root) %{dracutlibdir}/modules.d/95lunmask/*.sh
%dir %{dracutlibdir}/modules.d/95resume
%attr(755,root,root) %{dracutlibdir}/modules.d/95resume/*.sh
%dir %{dracutlibdir}/modules.d/95rootfs-block
%attr(755,root,root) %{dracutlibdir}/modules.d/95rootfs-block/*.sh
%dir %{dracutlibdir}/modules.d/95dasd
%attr(755,root,root) %{dracutlibdir}/modules.d/95dasd/*.sh
%dir %{dracutlibdir}/modules.d/95dasd_mod
%attr(755,root,root) %{dracutlibdir}/modules.d/95dasd_mod/*.sh
%dir %{dracutlibdir}/modules.d/95fcoe-uefi
%attr(755,root,root) %{dracutlibdir}/modules.d/95fcoe-uefi/*.sh
%dir %{dracutlibdir}/modules.d/95fstab-sys
%attr(755,root,root) %{dracutlibdir}/modules.d/95fstab-sys/*.sh
%dir %{dracutlibdir}/modules.d/95nvmf
%attr(755,root,root) %{dracutlibdir}/modules.d/95nvmf/*.sh
%{dracutlibdir}/modules.d/95nvmf/95-nvmf-initqueue.rules
%dir %{dracutlibdir}/modules.d/95virtiofs
%attr(755,root,root) %{dracutlibdir}/modules.d/95virtiofs/*.sh
%dir %{dracutlibdir}/modules.d/95zfcp
%attr(755,root,root) %{dracutlibdir}/modules.d/95zfcp/*.sh
%dir %{dracutlibdir}/modules.d/95terminfo
%attr(755,root,root) %{dracutlibdir}/modules.d/95terminfo/*.sh
%dir %{dracutlibdir}/modules.d/95udev-rules
%{dracutlibdir}/modules.d/95udev-rules/*.rules
%attr(755,root,root) %{dracutlibdir}/modules.d/95udev-rules/*.sh
%dir %{dracutlibdir}/modules.d/95virtfs
%attr(755,root,root) %{dracutlibdir}/modules.d/95virtfs/*.sh
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
%dir %{dracutlibdir}/modules.d/98pollcdrom
%attr(755,root,root) %{dracutlibdir}/modules.d/98pollcdrom/*.sh
%dir %{dracutlibdir}/modules.d/98selinux
%attr(755,root,root) %{dracutlibdir}/modules.d/98selinux/*.sh
%dir %{dracutlibdir}/modules.d/98syslog
%{dracutlibdir}/modules.d/98syslog/README
%{dracutlibdir}/modules.d/98syslog/rsyslog.conf
%attr(755,root,root) %{dracutlibdir}/modules.d/98syslog/*.sh
%dir %{dracutlibdir}/modules.d/98dracut-systemd
%{dracutlibdir}/modules.d/98dracut-systemd/dracut-tmpfiles.conf
%{dracutlibdir}/modules.d/98dracut-systemd/*.service
%attr(755,root,root) %{dracutlibdir}/modules.d/98dracut-systemd/*.sh
%doc %{dracutlibdir}/modules.d/98dracut-systemd/*.8*
%dir %{dracutlibdir}/modules.d/98usrmount
%attr(755,root,root) %{dracutlibdir}/modules.d/98usrmount/*.sh
%dir %{dracutlibdir}/modules.d/99base
%attr(755,root,root) %{dracutlibdir}/modules.d/99base/*.sh
%dir %{dracutlibdir}/modules.d/99fs-lib
%attr(755,root,root) %{dracutlibdir}/modules.d/99fs-lib/*.sh
%dir %{dracutlibdir}/modules.d/99img-lib
%attr(755,root,root) %{dracutlibdir}/modules.d/99img-lib/*.sh
%dir %{dracutlibdir}/modules.d/99memstrack
%attr(755,root,root) %{dracutlibdir}/modules.d/99memstrack/*.sh
%{dracutlibdir}/modules.d/99memstrack/memstrack.service
%dir %{dracutlibdir}/modules.d/99shutdown
%attr(755,root,root) %{dracutlibdir}/modules.d/99shutdown/*.sh
%dir %{dracutlibdir}/modules.d/99squash
%attr(755,root,root) %{dracutlibdir}/modules.d/99squash/*.sh
%dir %{dracutlibdir}/modules.d/99uefi-lib
%attr(755,root,root) %{dracutlibdir}/modules.d/99uefi-lib/*.sh
%attr(755,root,root) %{dracutlibdir}/dracut-version.sh
%attr(755,root,root) %{dracutlibdir}/skipcpio

%dir /var/lib/initramfs

%{systemdunitdir}/dracut-*.service
%{systemdunitdir}/initrd.target.wants/dracut-*.service
%{systemdunitdir}/sysinit.target.wants/dracut-shutdown.service

%{_npkgconfigdir}/dracut.pc

%{_mandir}/man1/lsinitrd.1*
%{_mandir}/man5/dracut.conf.5*
%{_mandir}/man7/dracut.bootup.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.modules.7*
%{_mandir}/man8/dracut.8*
%{_mandir}/man8/dracut-cmdline.service.8*
%{_mandir}/man8/dracut-initqueue.service.8*
%{_mandir}/man8/dracut-mount.service.8*
%{_mandir}/man8/dracut-pre-mount.service.8*
%{_mandir}/man8/dracut-pre-pivot.service.8*
%{_mandir}/man8/dracut-pre-trigger.service.8*
%{_mandir}/man8/dracut-pre-udev.service.8*
%{_mandir}/man8/dracut-shutdown.service.8*

#/usr/lib/kernel/install.d/50-dracut.install
#/usr/lib/kernel/install.d/51-dracut-rescue.install

%files network
%defattr(644,root,root,755)
%dir %{dracutlibdir}/modules.d/00systemd-network-management
%attr(755,root,root) %{dracutlibdir}/modules.d/00systemd-network-management/module-setup.sh
%dir %{dracutlibdir}/modules.d/01systemd-networkd
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-networkd/*.sh
%{dracutlibdir}/modules.d/01systemd-networkd/99-default.network
%{dracutlibdir}/modules.d/01systemd-networkd/99-wait-online-dracut.conf
%dir %{dracutlibdir}/modules.d/01systemd-resolved
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-resolved/module-setup.sh
%{dracutlibdir}/modules.d/01systemd-resolved/resolved-tmpfile-dracut.conf
%dir %{dracutlibdir}/modules.d/01systemd-timesyncd
%attr(755,root,root) %{dracutlibdir}/modules.d/01systemd-timesyncd/module-setup.sh
%{dracutlibdir}/modules.d/01systemd-timesyncd/timesyncd-tmpfile-dracut.conf
%dir %{dracutlibdir}/modules.d/35connman
%attr(755,root,root) %{dracutlibdir}/modules.d/35connman/*.sh
%{dracutlibdir}/modules.d/35connman/cm-initrd.service
%{dracutlibdir}/modules.d/35connman/cm-wait-online-initrd.service
%dir %{dracutlibdir}/modules.d/35network-legacy
%{dracutlibdir}/modules.d/35network-legacy/dhclient.conf
%attr(755,root,root) %{dracutlibdir}/modules.d/35network-legacy/*.sh
%dir %{dracutlibdir}/modules.d/35network-manager
%attr(755,root,root) %{dracutlibdir}/modules.d/35network-manager/*.sh
%{dracutlibdir}/modules.d/35network-manager/initrd-no-auto-default.conf
%{dracutlibdir}/modules.d/35network-manager/nm-initrd.service
%{dracutlibdir}/modules.d/35network-manager/nm-wait-online-initrd.service
%dir %{dracutlibdir}/modules.d/40network
%attr(755,root,root) %{dracutlibdir}/modules.d/40network/*.sh
%dir %{dracutlibdir}/modules.d/45ifcfg
%attr(755,root,root) %{dracutlibdir}/modules.d/45ifcfg/*.sh
%dir %{dracutlibdir}/modules.d/45net-lib
%attr(755,root,root) %{dracutlibdir}/modules.d/45net-lib/*.sh
%dir %{dracutlibdir}/modules.d/45url-lib
%attr(755,root,root) %{dracutlibdir}/modules.d/45url-lib/*.sh
%dir %{dracutlibdir}/modules.d/90kernel-network-modules
%attr(755,root,root) %{dracutlibdir}/modules.d/90kernel-network-modules/module-setup.sh
%dir %{dracutlibdir}/modules.d/90livenet
%attr(755,root,root) %{dracutlibdir}/modules.d/90livenet/*.sh
%ifarch ppc ppc64
%dir %{dracutlibdir}/modules.d/90ppcmac
%attr(755,root,root) %{dracutlibdir}/modules.d/90ppcmac/*.sh
%endif
%dir %{dracutlibdir}/modules.d/90qemu-net
%attr(755,root,root) %{dracutlibdir}/modules.d/90qemu-net/*.sh
%dir %{dracutlibdir}/modules.d/95cifs
%attr(755,root,root) %{dracutlibdir}/modules.d/95cifs/*.sh
%dir %{dracutlibdir}/modules.d/95fcoe
%attr(755,root,root) %{dracutlibdir}/modules.d/95fcoe/*.sh
%dir %{dracutlibdir}/modules.d/95iscsi
%attr(755,root,root) %{dracutlibdir}/modules.d/95iscsi/*.sh
%dir %{dracutlibdir}/modules.d/95nbd
%attr(755,root,root) %{dracutlibdir}/modules.d/95nbd/*.sh
%dir %{dracutlibdir}/modules.d/95nfs
%attr(755,root,root) %{dracutlibdir}/modules.d/95nfs/*.sh
%dir %{dracutlibdir}/modules.d/95ssh-client
%attr(755,root,root) %{dracutlibdir}/modules.d/95ssh-client/*.sh
%dir %{dracutlibdir}/modules.d/95znet
%attr(755,root,root) %{dracutlibdir}/modules.d/95znet/*.sh

%files fips
%defattr(644,root,root,755)
%dir %{dracutlibdir}/modules.d/01fips
%attr(755,root,root) %{dracutlibdir}/modules.d/01fips/*.sh
%config(noreplace) %{_sysconfdir}/dracut.conf.d/40-fips.conf

%files caps
%defattr(644,root,root,755)
%{dracutlibdir}/modules.d/02caps/README
%dir %{dracutlibdir}/modules.d/02caps
%attr(755,root,root) %{dracutlibdir}/modules.d/02caps/*.sh

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dracut-catimages
%{_mandir}/man8/dracut-catimages.8*
%dir /boot/dracut
%dir /var/lib/dracut
%dir /var/lib/dracut/overlay

%files -n bash-completion-dracut
%defattr(644,root,root,755)
%{_datadir}/bash-completion/completions/dracut
%{_datadir}/bash-completion/completions/lsinitrd
