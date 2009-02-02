
Summary: check_by_http plugin for nagios master
Name: nagios-http
Version: %{version}
Release: 1%{org_tag}%{dist}
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Application/System
Requires: nagios
BuildRoot: %{_tmppath}/%{name}

%description
nagios-http provides a check_by_http nagios plugin, which can be
used to check and collate results from nagios-http-remote instances.

%package remote
Summary: Remote nagios-http web infrastructure and cron job helper 
Version: %{version}
Release: 1%{org_tag}%{dist}
Group: Application/System
Requires: nagios-plugins, httpd

%description remote
nagios-http-remote provides the web infrastructure for remote 
nagios-http nodes, and a cron job helper for setting up cron
entries.

%prep
%setup

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mkdir -p %{buildroot}/usr/lib/nagios/plugins
mkdir -p %{buildroot}%{_localstatedir}/www/%{name}
install -m0644 conf/%{name}.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -m0755 bin/nagios_http_cronjob %{buildroot}/usr/lib/nagios/plugins

%files

%files remote
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
/usr/lib/nagios/plugins/nagios_http_cronjob
%dir %attr(0755,nagios,nagios) %{_localstatedir}/www/%{name}

%changelog
* Mon Feb 02 2009 Gavin Carr <gavin@openfusion.com.au> 0.1-1
- Initial package and release.

