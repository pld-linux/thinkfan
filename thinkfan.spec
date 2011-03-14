Summary:	ThinkPad fan control program
Name:		thinkfan
Version:	0.7.1
Release:	1
License:	GPL
Group:		Base
Source0:	http://downloads.sourceforge.net/thinkfan/%{name}-%{version}.tar.gz
# Source0-md5:	0e98ec7854edbb8186544f3aec6d95e4
Source1:	%{name}.init
URL:		http://thinkfan.sourceforge.net
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A minimalist fan control program. Supports any hardware through the
sysfs hwmon interface and most Thinkpads through /proc/acpi/ibm.

%prep
%setup -q
sed -i -e 's#gcc#%{__cc}#g' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/rc.d/init.d}

install thinkfan $RPM_BUILD_ROOT%{_sbindir}
install thinkfan.1 $RPM_BUILD_ROOT%{_mandir}/man1
install thinkfan.conf.thinkpad $RPM_BUILD_ROOT%{_sysconfdir}/thinkfan.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add thinkfan
%service thinkfan reload "thinkfan daemon"

%preun
if [ "$1" = "0" ]; then
        /sbin/chkconfig --del thinkfan
fi

%files
%defattr(644,root,root,755)
%doc NEWS README ChangeLog thinkfan.conf.sysfs
%attr(755,root,root) %{_sbindir}/thinkfan
%{_mandir}/man1/thinkfan.1*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
