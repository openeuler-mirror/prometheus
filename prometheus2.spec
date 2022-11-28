%define    debug_package %{nil}

Name:      prometheus2
Version:   2.20.0
Release:   4
Summary:   The Prometheus 2.x monitoring system and time series database.
License:   ASL 2.0
URL:       https://prometheus.io
Conflicts: prometheus


BuildRequires: systemd

Source0:   prometheus-%{version}.linux-arm64.tar.gz
Source1:   prometheus-%{version}.linux-amd64.tar.gz
Source2:   prometheus.service
Source3:   prometheus.default
Source4:   prometheus-%{version}.linux-riscv64.tar.gz

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

%ifarch riscv64
%setup -q -b 4 -n prometheus-%{version}.linux-riscv64
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
* Thu Nov 24 2022 misaka00251 <liuxin@iscas.ac.cn> - 2.20.0-4
- Fix changelog & Add riscv64 support

* Wed Apr 20 2022 zhuang.li <zhuang.li@turbolinux.com.cn> - 2.20.0-3
- Modify the schema judgment, resulting in compilation failure

* Tue Dec 14 2021 konglidong <konglidong@uniontech.com> - 2.20.0-2
- modify format and delete %dist

* Tue Aug 11 2020 houjian <houjian@kylinos.cn> - 2.20.0-1
- Init project prometheus
