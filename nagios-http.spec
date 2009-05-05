
%define perl_sitelib /usr/lib/perl5/site_perl

Summary: check_by_http plugin for nagios master
Name: nagios-http-master
Version: %{version}
Release: 1%{org_tag}
Source0: nagios-http-%{version}.tar.gz
License: GPL
Group: Application/System
Requires: nagios-http-common = %{version}, httpd
BuildRoot: %{_tmppath}/%{name}
BuildArch: noarch
Obsoletes: nagios-http
Provides: nagios-http

%description
nagios-http provides a check_by_http nagios plugin, which can be
used to check and collate results from nagios-http-remote instances.

%package -n nagios-http-common
Summary: Common components for nagios-http
Version: %{version}
Release: 1%{org_tag}
Group: Application/System
BuildArch: noarch

%description -n nagios-http-common
Common components (libraries) for nagios-http.

%package -n nagios-http-remote
Summary: Remote nagios-http web infrastructure and cron job helper 
Version: %{version}
Release: 1%{org_tag}
Group: Application/System
Requires: perl-suidperl, nagios-plugins, nagios-http-common = %{version}, perl-Crypt-SSLeay
BuildArch: noarch

%description -n nagios-http-remote
nagios-http-remote provides the web infrastructure for remote 
nagios-http nodes, and a cron job helper for setting up cron
entries.

%prep
%setup -n nagios-http-%{version}

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

%pre -n nagios-http-remote 
# Add a nagios user/group 
if ! id -u nagios >/dev/null 2>&1; then
  groupadd -r nagios && useradd -r -m -g nagios nagios
fi

%files
%config(noreplace) %{_sysconfdir}/httpd/conf.d/nagios-http.conf
/usr/lib/nagios/plugins/check_http_result
/usr/lib/nagios/plugins/check_by_http
%dir %attr(2750,nagios,apache) %{_localstatedir}/www/%{name}

%files -n nagios-http-common
%{perl_sitelib}/Nagios/HTTP/Util.pm

%files -n nagios-http-remote
# nagios_http_cronjob needs to be setuid, to create jobs in /etc/cron.d
%attr(4750,root,nagios) /usr/lib/nagios/plugins/nagios_http_cronjob
%attr(0755,root,root) /usr/lib/nagios/plugins/nagios_http_result

%changelog
* Tue May 05 2009 Gavin Carr <gavin@openfusion.com.au> 0.5-1
- Remove remote_hostname from check_http_result, and just pass -H hostname.

* Sat Feb 28 2009 Gavin Carr <gavin@openfusion.com.au> 0.4-1
- Make nagios_http_cronjob root setuid, instead of having to setup sudo.
- Add remote_hostname argument check_http_result.

* Tue Feb 10 2009 Gavin Carr <gavin@openfusion.com.au> 0.3-1
- Invert architecture, with the web server on the check_http_result side.

* Mon Feb 02 2009 Gavin Carr <gavin@openfusion.com.au> 0.1-1
- Initial package and release.

