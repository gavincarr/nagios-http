
%define perl_sitelib %(eval "`perl -V:installsitelib`"; echo $installsitelib)
%define version 0.7.11

Summary: check_http_result plugin for nagios master
Name: nagios-http-master
Version: %{version}
Release: 1%{org_tag}%{dist}
Source0: nagios-http-%{version}.tar.gz
License: GPL
Group: Application/System
Requires: nagios-http-common = %{version}, httpd
BuildRoot: %{_tmppath}/nagios-http
BuildArch: noarch
Obsoletes: nagios-http
Provides: nagios-http
# This requires shouldn't be necessary, but there are bogus packages around
# (rpmforge perl-Test-Mock-LWP) that claim to provide perl(LWP::UserAgent) etc.

%description
nagios-http-master provides a check_http_result nagios plugin, which can 
be used to check and collate results from nagios-http-remote instances.

%package -n nagios-http-common
Summary: Common components for nagios-http
Version: %{version}
Release: 1%{org_tag}%{dist}
Group: Application/System
BuildArch: noarch

%description -n nagios-http-common
Common components (libraries) for nagios-http.

%package -n nagios-http-remote
Summary: Remote nagios-http web infrastructure and cron job helper 
Version: %{version}
Release: 1%{org_tag}%{dist}
Group: Application/System
Requires: nagios-plugins, nagios-http-common = %{version}
%if %{rhel} < 6
Requires: perl-suidperl
%endif
BuildArch: noarch
Requires: perl-libwww-perl

%description -n nagios-http-remote
nagios-http-remote provides the web infrastructure for remote 
nagios-http nodes, and a cron job helper for setting up cron
entries.

%prep
%setup -n nagios-http-%{version}

%build
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT

%install
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mkdir -p %{buildroot}%{perl_sitelib}/Nagios/HTTP
mkdir -p %{buildroot}/usr/lib/nagios/plugins
mkdir -p %{buildroot}%{_localstatedir}/www/nagios-http
install -m0644 conf/nagios-http.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/
#install -m0644 conf/nagios-http-remote.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m0644 lib/Nagios/HTTP/Util.pm %{buildroot}%{perl_sitelib}/Nagios/HTTP
install -m0755 bin/* %{buildroot}/usr/lib/nagios/plugins

%pre -n nagios-http-remote 
# Add a nagios user/group 
if ! id -u nagios >/dev/null 2>&1; then
  getent group nagios || groupadd -r nagios
  useradd -r -g nagios nagios
fi

%files
%config(noreplace) %{_sysconfdir}/httpd/conf.d/nagios-http.conf
/usr/lib/nagios/plugins/check_http_result
%dir %attr(2750,nagios,apache) %{_localstatedir}/www/nagios-http

%files -n nagios-http-common
%{perl_sitelib}/Nagios/HTTP/Util.pm

%files -n nagios-http-remote
# nagios_http_cronjob needs to be setuid, to create jobs in /etc/cron.d
%attr(4750,root,nagios) /usr/lib/nagios/plugins/nagios_http_cronjob
%attr(0755,root,root) /usr/lib/nagios/plugins/nagios_http_result

%changelog
* Mon May 30 2011 Gavin Carr <gavin@openfusion.com.au> 0.7.11-1
- Add explicit requires on perl-libwww-perl to workaround problems.

* Mon May 30 2011 Gavin Carr <gavin@openfusion.com.au> 0.7.10-1
- More perl_sitelib fixes for rhel6.

* Mon May 30 2011 Gavin Carr <gavin@openfusion.com.au> 0.7.9-1
- Add %dist to release to support diff rhel6 site_perl, bump to 0.7.9.

* Mon May 09 2011 Gavin Carr <gavin@openfusion.com.au> 0.7.8-1
- Tweak %pre script to handle case where nagios group exists but user doesn't.

* Tue Mar 22 2011 Gavin Carr <gavin@openfusion.com.au> 0.7.7-1
- Tweak verbose logger sub to avoid readonly-variable-modification warning.

* Fri Feb 12 2010 Gavin Carr <gavin@openfusion.com.au> 0.7.6-1
- Add UA use_env to nagios_http_result to support proxies.
- Add support to nagios_http_result for readings args and env variables from a config.

* Thu Jan 07 2010 Gavin Carr <gavin@openfusion.com.au> 0.7.5-1
- Allow hyphens in hostnames in nagios_http_cronjob.

* Wed Nov 18 2009 Gavin Carr <gavin@openfusion.com.au> 0.7.4-1
- Add '|' to valid cmd characters in nagios_http_cronjob.

* Wed Sep 09 2009 Gavin Carr <gavin@openfusion.com.au> 0.7.2-1
- Add /sbin and /usr/sbin to $cronjob_path in nagios_http_cronjob.

* Wed Jul 01 2009 Gavin Carr <gavin@openfusion.com.au> 0.7-1
- Add --report-hostname support to check_http_result and nagios_http_cronjob.

* Tue May 19 2009 Gavin Carr <gavin@openfusion.com.au> 0.6.1-1
- Add --log syslog support to check_http_result.

* Tue May 19 2009 Gavin Carr <gavin@openfusion.com.au> 0.6-1
- Add --env support to check_http_result and nagios_http_cronjob.

* Tue May 05 2009 Gavin Carr <gavin@openfusion.com.au> 0.5-1
- Remove remote_hostname from check_http_result, and just pass -H hostname.

* Sat Feb 28 2009 Gavin Carr <gavin@openfusion.com.au> 0.4-1
- Make nagios_http_cronjob root setuid, instead of having to setup sudo.
- Add remote_hostname argument check_http_result.

* Tue Feb 10 2009 Gavin Carr <gavin@openfusion.com.au> 0.3-1
- Invert architecture, with the web server on the check_http_result side.

* Mon Feb 02 2009 Gavin Carr <gavin@openfusion.com.au> 0.1-1
- Initial package and release.

