Summary:	ThinkPad fan control program
Summary(pl.UTF-8):	Program do sterowania wiatraczkiem w ThinkPadach
Name:		thinkfan
Version:	1.3.1
Release:	2
License:	GPL v3+
Group:		Applications/System
#Source0Download: https://github.com/vmatare/thinkfan/releases
# TODO:
#Source0:	https://github.com/vmatare/thinkfan/archive/%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/vmatare/thinkfan/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	8f7cdec0a524ed99fe6836f95d749da1
Source1:	%{name}.init
URL:		https://github.com/vmatare/thinkfan
BuildRequires:	cmake >= 3.0
BuildRequires:	libatasmart-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-devel
BuildRequires:	yaml-cpp-devel >= 0.5.4
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

%build
install -d build
cd build
%cmake \
	..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT{%{systemdunitdir},%{_sysconfdir}/systemd/system}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Packaged by %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/{COPYING,README.md,thinkfan.yaml}

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p examples/thinkfan.yaml $RPM_BUILD_ROOT%{_sysconfdir}/thinkfan.yaml
%{__mv} $RPM_BUILD_ROOT%{_prefix}%{systemdunitdir}/*.service $RPM_BUILD_ROOT%{systemdunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add thinkfan
%service thinkfan restart
%systemd_post thinkfan.service

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del thinkfan
	%service thinkfan stop
fi
%systemd_preun thinkfan.service

%postun
%systemd_reload

%triggerpostun -- %{name} < 5.42-5
%systemd_trigger smartd.service

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.yaml
%dir %{_sysconfdir}/systemd/system/thinkfan.service.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system/thinkfan.service.d/override.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/thinkfan
%doc COPYING README.md examples/thinkfan.yaml
%{_mandir}/man1/thinkfan.1*
%{_mandir}/man5/thinkfan.conf.5*
%{_mandir}/man5/thinkfan.conf.legacy.5*
%{systemdunitdir}/%{name}.service
%{systemdunitdir}/%{name}-sleep.service
%{systemdunitdir}/%{name}-wakeup.service
