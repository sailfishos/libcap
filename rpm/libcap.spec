Name: libcap
Version: 2.24
Release: 1
Summary: Library for getting and setting POSIX.1e capabilities
Source: %{name}-%{version}.tar.bz2
Patch0: libcap-2.22-buildflags.patch

URL: https://git.kernel.org/cgit/linux/kernel/git/morgan/libcap.git/
License: LGPLv2+
Group: System/Libraries
BuildRequires: libattr-devel pam-devel

%description
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package devel
Summary: Development files for libcap
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for static linking, etc) for libcap.

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install libcap-devel if you want to develop or compile applications using
libcap.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%setup -q -n %{name}-%{version}/libcap
%patch0 -p1

%build
# libcap can not be build with _smp_mflags:
make PREFIX=%{_prefix} LIBDIR=%{_libdir} SBINDIR=%{_sbindir} \
     INCDIR=%{_includedir} MANDIR=%{_mandir}

%install
rm -rf ${RPM_BUILD_ROOT}
make install RAISE_SETFCAP=no \
             PKGCONFIGDIR=${RPM_BUILD_ROOT}/%{_libdir}/pkgconfig/ \
             DESTDIR=${RPM_BUILD_ROOT} \
             LIBDIR=${RPM_BUILD_ROOT}/%{_libdir} \
             SBINDIR=${RPM_BUILD_ROOT}/%{_sbindir} \
             INCDIR=${RPM_BUILD_ROOT}/%{_includedir} \
             MANDIR=${RPM_BUILD_ROOT}/%{_mandir}/ \
             COPTFLAG="$RPM_OPT_FLAGS"
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man{2,3,8}
mv -f doc/*.3 ${RPM_BUILD_ROOT}/%{_mandir}/man3/

# remove static lib
rm ${RPM_BUILD_ROOT}/%{_libdir}/libcap.a

chmod +x ${RPM_BUILD_ROOT}/%{_libdir}/*.so.*

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}
install -m0644 -t ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version} \
        doc/capability.notes

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license License
%{_libdir}/*.so.*
%{_sbindir}/*
%{_libdir}/security/pam_cap.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcap.pc

%files doc
%defattr(-,root,root,-)
%{_mandir}/man*/*
%{_docdir}/%{name}-%{version}
