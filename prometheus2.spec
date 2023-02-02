%define debug_package %{nil}

Name:    prometheus2
Version: 2.20.0
Release: 4
Summary: The Prometheus 2.x monitoring system and time series database.
License: ASL 2.0
URL:     https://prometheus.io
Conflicts: prometheus

Source0: prometheus-%{version}.linux-arm64.tar.gz
Source1: prometheus-%{version}.linux-amd64.tar.gz
Source2: prometheus.service
Source3: prometheus.default

BuildRequires: systemd
%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus is a systems and service monitoring system. It collects metrics from
configured targets at given intervals, evaluates rule expressions, displays the
results, and can trigger alerts if some condition is observed to be true.

%prep
%ifarch aarch64
%setup -q -b 0 -n prometheus-%{version}.linux-arm64
%endif

%ifarch x86_64
%setup -q -b 1 -n prometheus-%{version}.linux-amd64
%endif

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 prometheus %{buildroot}%{_bindir}/prometheus
install -D -m 755 promtool %{buildroot}%{_bindir}/promtool
install -D -m 755 tsdb %{buildroot}%{_bindir}/tsdb
for dir in console_libraries consoles; do
  for file in ${dir}/*; do
    install -D -m 644 ${file} %{buildroot}%{_datarootdir}/prometheus/${file}
  done

done
install -D -m 644 prometheus.yml %{buildroot}%{_sysconfdir}/prometheus/prometheus.yml
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/prometheus.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/default/prometheus

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post prometheus.service

%preun
%systemd_preun prometheus.service

%postun
%systemd_postun prometheus.service

%files
%defattr(-,root,root,-)
%{_bindir}/prometheus
%{_bindir}/promtool
%{_bindir}/tsdb
%config(noreplace) %{_sysconfdir}/prometheus/prometheus.yml
%{_datarootdir}/prometheus
%{_unitdir}/prometheus.service
%config(noreplace) %{_sysconfdir}/default/prometheus
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus

%changelog
* Mon Jan 09 2023 tianhang <tian_hang@hoperun.com> - 2.20.0-4
- cherry pick commit c18e334 to fix compilation failure

- Thu Mar 24 2022 yaoxin <yaoxin30@huawei.com> - 2.20.0-3
- Delete release %{?dist}

* Mon Feb 28 2022 wulei <wulei80@huawei.com> - 2.20.0-2
- Fix %{_unitdir} not identified

* Tue Aug 11 2020 houjian <houjian@kylinos.cn> - 2.20.0-1
- Init project prometheus
