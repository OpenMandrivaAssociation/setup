Summary:	A set of system configuration, setup files and directories
Name:		setup
Version:	2.9.4
Release:	2
License:	Public Domain
Group:		System/Base
Url:		https://github.com/OpenMandrivaSoftware/setup
Source0:	https://github.com/OpenMandrivaSoftware/setup/archive/refs/tags/%{version}.tar.gz
Source1:	setup.rpmlintrc
Requires(meta):	system-release
OrderWithRequires:	filesystem
BuildArch:	noarch

%description
The setup package contains a set of very important system configuration, setup 
files and directories, such as passwd, group, profile, basic directory layout
for a Linux system and more.

The filesystem is one of the basic packages that is installed on a Linux
system.  Filesystem  contains the basic directory layout for a Linux operating
system, including the correct permissions for the directories.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install
touch %{buildroot}%{_sysconfdir}/fstab

%files
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/passwd
%verify(not md5 size mtime) %attr(0440,root,shadow) %config(noreplace,missingok) %{_sysconfdir}/shadow
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/group
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts
%verify(not md5 size mtime) %attr(0440,root,shadow) %config(noreplace,missingok) %{_sysconfdir}/gshadow
%config(noreplace) %{_sysconfdir}/services
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/inputrc
%config(noreplace) %{_sysconfdir}/filesystems
%config(noreplace) %{_sysconfdir}/host.conf
%config(noreplace) %{_sysconfdir}/hosts.allow
%config(noreplace) %{_sysconfdir}/hosts.deny
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/motd
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/motd-ssh
%config(noreplace) %{_sysconfdir}/printcap
%config(noreplace) %{_sysconfdir}/profile
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/shells
%config(noreplace) %{_sysconfdir}/ethertypes
%config(noreplace) %{_sysconfdir}/protocols
%config(noreplace) %{_sysconfdir}/csh.login
%config(noreplace) %{_sysconfdir}/csh.cshrc
%dir %{_sysconfdir}/profile.d
%{_sysconfdir}/profile.d/*.csh
%{_sysconfdir}/profile.d/*.sh
%ghost %attr(0644,root,root) %verify(not md5 size mtime) %{_logdir}/lastlog
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %{_sysconfdir}/fstab
