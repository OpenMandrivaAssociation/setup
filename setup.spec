Summary:	A set of system configuration, setup files and directories
Name:		setup
Version:	2.8.8
Release:	9
License:	Public Domain
Group:		System/Base
Url:		https://abf.io/software/setup
Source0:	%{name}-%{version}.tar.xz
Source1:	setup.rpmlintrc
BuildArch:	noarch

%description
The setup package contains a set of very important system configuration, setup 
files and directories, such as passwd, group, profile, basic directory layout
for a Linux system and more.

The filesystem is one of the basic packages that is installed on a Linux 
system.  Filesystem  contains the basic directory layout for a Linux operating 
system, including the correct permissions for the directories.

%prep
%setup -q

%build
%make

%install
%makeinstall_std

# (tpg) versioned pre/post trans are here to keep backup of
# already existing /etc/shadow and /etc/gshadow to
# keep them away from being rewriten by new files with this rpm
# and finally allow user to login with his old passwords
%pretrans
if [ -e /etc/shadow ]; then
	mv -f /etc/shadow /etc/shadow.backup
fi

if [ -e /etc/gshadow ]; then
	mv -f /etc/gshadow /etc/gshadow.backup
fi

%posttrans
if [ -e /etc/shadow.backup ]; then
	mv -f /etc/shadow.bak /etc/shadow
    rm -rf /etc/shadow.backup
fi

if [ -e /etc/gshadow.backup ]; then
	mv -f /etc/gshadow.backup /etc/gshadow
    rm -rf /etc/gshadow.backup
fi

%triggerposttransun -- setup < 2.8.8-4
sed -i -e "s,/bin/nologin,/sbin/nologin,g" /etc/shells ||:
sed -i -e "s,/sbin:/sbin/halt,/bin:/bin/halt,g" /etc/passwd ||:

%files
%doc NEWS
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/passwd
%verify(not md5 size mtime) %attr(0440,root,root) %config(noreplace,missingok) %{_sysconfdir}/shadow
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/fstab
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/resolv.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/group
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts
%verify(not md5 size mtime) %attr(0440,root,root) %config(noreplace,missingok) %{_sysconfdir}/gshadow
%config(noreplace) %{_sysconfdir}/services
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/inputrc
%config(noreplace) %{_sysconfdir}/filesystems
%config(noreplace) %{_sysconfdir}/host.conf
%config(noreplace) %{_sysconfdir}/hosts.allow
%config(noreplace) %{_sysconfdir}/hosts.deny
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/motd
%config(noreplace) %{_sysconfdir}/printcap
%config(noreplace) %{_sysconfdir}/profile
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/shells
%config(noreplace) %{_sysconfdir}/protocols
%config(noreplace) %{_sysconfdir}/csh.login
%config(noreplace) %{_sysconfdir}/csh.cshrc
%dir %{_sysconfdir}/profile.d
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %{_logdir}/lastlog
