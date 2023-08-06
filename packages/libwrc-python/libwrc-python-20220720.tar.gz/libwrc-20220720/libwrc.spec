Name: libwrc
Version: 20220720
Release: 1
Summary: Library to access the Windows Resource Compiler (WRC) format
Group: System Environment/Libraries
License: LGPLv3+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libwrc
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
                
BuildRequires: gcc                

%description -n libwrc
Library to access the Windows Resource Compiler (WRC) format

%package -n libwrc-static
Summary: Library to access the Windows Resource Compiler (WRC) format
Group: Development/Libraries
Requires: libwrc = %{version}-%{release}

%description -n libwrc-static
Static library version of libwrc.

%package -n libwrc-devel
Summary: Header files and libraries for developing applications for libwrc
Group: Development/Libraries
Requires: libwrc = %{version}-%{release}

%description -n libwrc-devel
Header files and libraries for developing applications for libwrc.

%package -n libwrc-python3
Summary: Python 3 bindings for libwrc
Group: System Environment/Libraries
Requires: libwrc = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libwrc-python3
Python 3 bindings for libwrc

%package -n libwrc-tools
Summary: Several tools for reading Windows Resource (RC) files
Group: Applications/System
Requires: libwrc = %{version}-%{release} 
 

%description -n libwrc-tools
Several tools for reading Windows Resource (RC) files

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libwrc
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libwrc-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libwrc-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libwrc.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libwrc-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libwrc-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Jul 24 2022 Joachim Metz <joachim.metz@gmail.com> 20220720-1
- Auto-generated

