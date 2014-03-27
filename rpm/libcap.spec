Name: libcap
Version: 2.22
Release: 1
Summary: Library for getting and setting POSIX.1e capabilities
Source: http://mirror.linux.org.au/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.bz2
Patch0: libcap-2.22-buildflags.patch
Patch1: libcap-2.22-signed-sizeof-compare.patch

URL: http://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.6/
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# libcap can not be build with _smp_mflags:
make PREFIX=%{_prefix} LIBDIR=%{_libdir} SBINDIR=%{_sbindir} \
     INCDIR=%{_includedir} MANDIR=%{_mandir}

%install
rm -rf ${RPM_BUILD_ROOT}
make install RAISE_SETFCAP=no \
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_sbindir}/*
%{_mandir}/man8/*
%{_libdir}/security/pam_cap.so
%doc doc/capability.notes License

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man1/*
%{_mandir}/man3/*

