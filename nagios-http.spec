
%define perl_sitelib /usr/lib/perl5/site_perl

Summary: check_by_http plugin for nagios master
Name: nagios-http
Version: %{version}
Release: 1%{org_tag}%{dist}
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Application/System
Requires: nagios-http-common = %{version}, httpd
BuildRoot: %{_tmppath}/%{name}
BuildArch: noarch

%description
nagios-http provides a check_by_http nagios plugin, which can be
used to check and collate results from nagios-http-remote instances.

%package common
Summary: Common components for nagios-http
Version: %{version}
Release: 1%{org_tag}%{dist}
Group: Application/System
BuildArch: noarch

%description common
Common components (libraries) for nagios-http.

%package remote
Summary: Remote nagios-http web infrastructure and cron job helper 
Version: %{version}
Release: 1%{org_tag}%{dist}
Group: Application/System
Requires: nagios-plugins, nagios-http-common = %{version}
BuildArch: noarch

%description remote
nagios-http-remote provides the web infrastructure for remote 
nagios-http nodes, and a cron job helper for setting up cron
entries.

%prep
%setup

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mkdir -p %{buildroot}%{perl_sitelib}/Nagios/HTTP
mkdir -p %{buildroot}/usr/lib/nagios/plugins
mkdir -p %{buildroot}%{_localstatedir}/www/%{name}
install -m0644 conf/nagios-http.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/
#install -m0644 conf/nagios-http-remote.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m0644 lib/Nagios/HTTP/Util.pm %{buildroot}%{perl_sitelib}/Nagios/HTTP
install -m0755 bin/* %{buildroot}/usr/lib/nagios/plugins

%pre remote 
# Add a nagios user/group 
if ! id -u nagios >/dev/null 2>&1; then
  groupadd -r nagios && useradd -r -m -g nagios nagios
fi

%files
%config(noreplace) %{_sysconfdir}/httpd/conf.d/nagios-http.conf
/usr/lib/nagios/plugins/check_http_result
/usr/lib/nagios/plugins/check_by_http
%dir %attr(2750,nagios,apache) %{_localstatedir}/www/%{name}

%files common
%{perl_sitelib}/Nagios/HTTP/Util.pm

%files remote
/usr/lib/nagios/plugins/nagios_http_cronjob
/usr/lib/nagios/plugins/nagios_http_result

%changelog
* Tue Feb 10 2009 Gavin Carr <gavin@openfusion.com.au> 0.3-1
- Invert architecture, with the web server on the check_http_result side.

* Mon Feb 02 2009 Gavin Carr <gavin@openfusion.com.au> 0.1-1
- Initial package and release.

