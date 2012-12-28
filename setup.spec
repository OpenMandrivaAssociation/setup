Summary:	A set of system configuration and setup files
Name:		setup
Version:	2.7.21
Release:	3
License:	Public Domain
Group:		System/Configuration/Other
Url:		http://svn.mandriva.com/svn/soft/setup/trunk
Source0:	%{name}-%{version}.tar.xz

Requires(pre):	rpm-helper
Requires(posttrans):	shadow-conv
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
%make

%install
%makeinstall_std

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


%changelog
* Sun Sep 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.7.21-2
+ Revision: 816563
- drop dependency on run-parts, we haven't shipped it as part of this package
  for a while, so no sense in adding a dependency on it for legacy compatibility
- new version:
  	o don't create /etc/mtab
  	o remove run-parts from this package, it's packaged separately
  	o update /etc/protocols and /etc/services from debian package
  	  netbase 4.47
- drop redundant glibc dependency
- fix license tag
- drop redundant buildroot cleaning
- cosmetics
- change buildarch to noarch
- add Requires(pre): rpm-helper

* Tue May 29 2012 Guilherme Moro <guilherme@mandriva.com> 2.7.18-5
+ Revision: 801039
- Remove mtab, owned by util-linux now

* Sun Dec 11 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.7.18-4
+ Revision: 740166
- cleaned up spec
- removed defattr, clean section, BuildRoot, mkrel
- changed req for shadow-utils to shadow-conv
- (recently split to avoid dep loop)
- removed pre 2007 Conflicts
- removed reqs for run-parts

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.7.18-3
+ Revision: 669970
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.7.18-2mdv2011.0
+ Revision: 607533
- rebuild

* Thu Dec 31 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.18-1mdv2010.1
+ Revision: 484524
- new version

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.7.17-2mdv2010.0
+ Revision: 427069
- rebuild

* Sat Apr 11 2009 Gustavo De Nardin <gustavodn@mandriva.com> 2.7.17-1mdv2009.1
+ Revision: 366419
- 2.7.17
  - stop csh from sourcing /etc/profile.d/* on non-interactive shells
    (bug #49407, comment 6)

* Fri Jan 09 2009 Frederic Crozat <fcrozat@mandriva.com> 2.7.16-1mdv2009.1
+ Revision: 327455
- Release 2.7.16 :
 - add dialout group, needed by latest udev, replace uucp group for serial stuff, just like Debian

* Wed Jan 07 2009 Pixel <pixel@mandriva.com> 2.7.15-1mdv2009.1
+ Revision: 326531
- 2.7.15: handle control + left/right arrow in gnome-terminal (#36287)

* Wed Dec 17 2008 Frederic Crozat <fcrozat@mandriva.com> 2.7.14-1mdv2009.1
+ Revision: 315121
- Release 2.7.14 :
 - fix warning in run-parts
 - configure inputrc to add trailing / to directories symlink (instead of patching bash)

* Sat Jul 12 2008 Olivier Thauvin <nanardon@mandriva.org> 2.7.13-1mdv2009.0
+ Revision: 234201
- 2.7.13: add tty0 to securetty for uml

* Thu May 22 2008 Vincent Danen <vdanen@mandriva.com> 2.7.12-3mdv2009.0
+ Revision: 210051
- use %%_pre_groupadd instead of groupadd directly to dynamically assign gid's on upgrades, since those gid's may already have been taken

* Sun May 18 2008 Vincent Danen <vdanen@mandriva.com> 2.7.12-2mdv2009.0
+ Revision: 208736
- create shadow, chkpwed, and auth groups in %%pre if they don't already exist in the system

* Wed May 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.12-1mdv2009.0
+ Revision: 207315
- new version

* Fri Mar 28 2008 Pixel <pixel@mandriva.com> 2.7.11-3mdv2008.1
+ Revision: 190933
- require run-parts for backward compatibility until other packages correctly
  require it directly

* Fri Mar 28 2008 Pixel <pixel@mandriva.com> 2.7.11-2mdv2008.1
+ Revision: 190867
- run-parts is moved to package run-parts

* Mon Jan 28 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 2.7.11-1mdv2008.1
+ Revision: 159330
- New upstream: 2.7.11. Closes: #34841
- Update URL tag.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.10-1mdv2008.1
+ Revision: 119058
- new version

* Tue Sep 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2.7.9-2mdv2008.0
+ Revision: 84515
- rebuild

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - new release

