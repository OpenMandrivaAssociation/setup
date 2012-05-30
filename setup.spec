Summary:	A set of system configuration and setup files
Name:		setup
Version:	2.7.18
Release:	5
License		public domain
Group:		System/Configuration/Other
Url:		http://svn.mandriva.com/svn/soft/setup/trunk
Source0:	%{name}-%{version}.tar.bz2

Requires(pre):	rpm-helper
Requires(posttrans):shadow-conv
# prevent the shell to fail running post script:
Requires(posttrans):glibc
BuildArch:	noarch

%description
The setup package contains a set of very important system
configuration and setup files, such as passwd, group,
profile and more.

You should install the setup package because you will
find yourself using its many features for system
administration.

%prep
%setup -q

%build
%make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
%makeinstall_std

find %buildroot -name "run-parts*" | xargs rm
rm -rf %{buildroot}/etc/mtab

%pre
# due to important new group additions, we need to add them manually here if they
# don't already exist because rpm will create group.rpmnew instead
if [ -f /etc/group ]; then
    grep -q '^auth:' /etc/group || %_pre_groupadd auth
    # be a little fancy here in case this is an upgrade and the user hasn't migrated to tcb yet
    if [ "`grep -q '^shadow:' /etc/group; echo $?`" == 1 ]; then
        %_pre_groupadd shadow
        if [ -f /etc/shadow ]; then
            chmod 0440 /etc/shadow && chgrp shadow /etc/shadow
        fi
    fi
    grep -q '^chkpwd:' /etc/group || %_pre_groupadd chkpwd
    grep -q '^dialout:' /etc/group || %_pre_groupadd dialout
fi

%posttrans
pwconv 2>/dev/null >/dev/null  || :
grpconv 2>/dev/null >/dev/null  || :

[ -f /var/log/lastlog ] || echo -n '' > /var/log/lastlog

if [ -x /usr/sbin/nscd ]; then
	nscd -i passwd -i group || :
fi

%triggerpostun -- setup < 2.7.8
# the files is no more in setup starting from 2.7.8, it is now in nfs-utils
if [ -e /etc/exports.rpmsave ]; then
  mv -f /etc/exports.rpmsave /etc/exports && echo "warning: /etc/exports.rpmsave restored as /etc/exports"
fi

%files
%doc NEWS
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/passwd
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/fstab
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/resolv.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/group
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts
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
