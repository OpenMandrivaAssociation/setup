Summary:	A set of system configuration, setup files and directories
Name:		setup
Version:	2.8.1
Release:	1
License:	Public Domain
Group:		System/Base
Url:		https://abf.rosalinux.ru/software/setup
Source0:	%{name}-%{version}.tar.xz
Source1:	setup.rpmlintrc

Requires(posttrans):	nscd

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

%posttrans
[ -f /var/log/lastlog ] || echo -n '' > /var/log/lastlog

if [ -x /usr/sbin/nscd ]; then
	nscd -i passwd -i group || :
fi

%files
%doc NEWS
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/passwd
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/shadow
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/fstab
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/resolv.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/group
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/gshadow
%config(noreplace) %{_sysconfdir}/services
%config(noreplace) %{_sysconfdir}/inputrc
%config(noreplace) %{_sysconfdir}/filesystems
%config(noreplace) %{_sysconfdir}/host.conf
%config(noreplace) %{_sysconfdir}/hosts.allow
%config(noreplace) %{_sysconfdir}/hosts.deny
%config(noreplace) %{_sysconfdir}/motd
%config(noreplace) %{_sysconfdir}/printcap
%config(noreplace) %{_sysconfdir}/profile
%config(noreplace) %{_sysconfdir}/shells
%config(noreplace) %{_sysconfdir}/protocols
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/securetty
%config(noreplace) %{_sysconfdir}/csh.login
%config(noreplace) %{_sysconfdir}/csh.cshrc
%ghost %verify(not md5 size mtime) /var/log/lastlog
