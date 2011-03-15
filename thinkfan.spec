Summary:	ThinkPad fan control program
Name:		thinkfan
Version:	0.7.1
Release:	1
License:	GPL
Group:		Base
Source0:	http://downloads.sourceforge.net/thinkfan/%{name}-%{version}.tar.gz
# Source0-md5:	0e98ec7854edbb8186544f3aec6d95e4
Source1:	%{name}.init
URL:		http://thinkfan.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A minimalist fan control program. Supports any kind of system via the
sysfs hwmon interface (/sys/class/hwmon). It is designed to eat as
little CPU power as possible. The development was inspired by the
excellent work people have done on thinkwiki.org.

%prep
%setup -q
sed -i -e 's#gcc#%{__cc}#g' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/rc.d/init.d}

install -p thinkfan $RPM_BUILD_ROOT%{_sbindir}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p thinkfan.conf.sysfs $RPM_BUILD_ROOT%{_sysconfdir}/thinkfan.conf
cp -p thinkfan.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add thinkfan
%service thinkfan restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del thinkfan
	%service thinkfan stop
fi

%files
%defattr(644,root,root,755)
%doc NEWS README ChangeLog thinkfan.conf.thinkpad
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/thinkfan
%{_mandir}/man1/thinkfan.1*
