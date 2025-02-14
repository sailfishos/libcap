Name: libcap
Version: 2.73
Release: 1
Summary: Library for getting and setting POSIX.1e capabilities
Source: %{name}-%{version}.tar.bz2

URL: https://github.com/sailfishos/libcap
License: BSD OR GPLv2
BuildRequires: pam-devel

%description
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package devel
Summary: Development files for libcap
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for static linking, etc) for libcap.

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install libcap-devel if you want to develop or compile applications using
libcap.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{name}-%{version}/libcap

%build
%make_build prefix=%{_prefix} lib=%{_lib} all

%install
make install RAISE_SETFCAP=no \
             PKGCONFIGDIR=%{_libdir}/pkgconfig/ \
             DESTDIR=%{buildroot} \
             LIBDIR=%{_libdir} \
             SBINDIR=%{_sbindir} \
             INCDIR=%{_includedir} \
             MANDIR=%{_mandir}

mkdir -p %{buildroot}%{_mandir}/man{2,3,8}
mv -f doc/*.3 %{buildroot}%{_mandir}/man3/

# remove static lib
rm ${RPM_BUILD_ROOT}/%{_libdir}/libcap.a
rm ${RPM_BUILD_ROOT}/%{_libdir}/libpsx.a

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
        doc/capability.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license License
%{_libdir}/*.so.*
%{_sbindir}/*
%{_libdir}/security/pam_cap.so

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcap.pc
%{_libdir}/pkgconfig/libpsx.pc

%files doc
%{_mandir}/man*/*
%{_docdir}/%{name}-%{version}
