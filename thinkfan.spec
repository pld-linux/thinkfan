Summary:	ThinkPad fan control program
Summary(pl.UTF-8):	Program do sterowania wiatraczkiem w ThinkPadach
Name:		thinkfan
Version:	0.9.1
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/thinkfan/%{name}-%{version}.tar.gz
# Source0-md5:	a981142f2c52ee4b0af69d5abbe03ced
Source1:	%{name}.init
URL:		http://thinkfan.sourceforge.net/
BuildRequires:	cmake >= 2.6
BuildRequires:	libatasmart-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A minimalist fan control program. Supports any kind of system via the
sysfs hwmon interface (/sys/class/hwmon). It is designed to eat as
little CPU power as possible. The development was inspired by the
excellent work people have done on thinkwiki.org.

%description -l pl.UTF-8
Minimalistyczny program do sterowania wiatraczkiem. Obsługuje dowolny
system poprzez interfejs sysfs hwmon (/sys/class/hwmon). Został tak
zaprojektowany, aby obciążać procesor w najmniejszym możliwym stopniu.
Stworzenie tego narzędzia zostało zainspirowane wspaniałą pracą
wykonaną przez ludzi na thinkwiki.org.

%prep
%setup -q

%{__sed} -i -e 's#bin#sbin#g' -e 's#man/man1#share/man/man1#g' CMakeLists.txt

%build
install -d build
cd build
%{cmake} \
	-DUSE_ATASMART=1 \
	..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p examples/thinkfan.conf.simple $RPM_BUILD_ROOT%{_sysconfdir}/thinkfan.conf

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
%doc NEWS README examples/thinkfan.conf.*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/thinkfan
%{_mandir}/man1/thinkfan.1*
