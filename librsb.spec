%define ver %(echo %{version}-rc7)

%define major 0
%define libname %mklibname rsb %{major}
%define devname %mklibname rsb -d

%bcond_with	octave

Summary:	A parallel matrix computations library for the Recursive Sparse Blocks format
Name:		librsb
Version:	1.2.0
Release:	0
License:	LGPLv3
Group:		System/Libraries
URL:		http://librsb.sourceforge.net
Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{ver}.tar.gz
Source100:	%{name}.rpmlintrc

BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(hwloc)
BuildRequires:	pkgconfig(libpapi)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	doxygen
BuildRequires:	graphviz
%if %{with octave}
BuildRequires:	octave-devel
%endif
BuildRequires:	gcc-gfortran
BuildRequires:	openmp-devel
BuildRequires:	help2man

%description
librsb is a library for sparse matrix computations featuring the Recursive
Sparse Blocks (RSB) matrix format. This format allows cache efficient and
multi-threaded (that is, shared memory parallel) operations on large sparse
matrices. The most common operations necessary to iterative solvers are
available, e.g.: matrix-vector multiplication, triangular solution,
rows/columns scaling, diagonal extraction / setting, blocks extraction, norm
computation, formats conversion. The RSB format is especially well suited
for symmetric and transposed multiplication variants. Most numerical kernels
code is auto generated, and the supported numerical types can be chosen by
the user at build time.

librsb implements the Sparse BLAS standard, as specified in the BLAS Forum
documents.

%files
%{_bindir}/%{name}-config
%{_bindir}/rsbench
%{_mandir}/man1/%{name}-config.1*
%{_mandir}/man1/rsbench.1*
%doc COPYING

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	A parallel matrix computations library for the Recursive Sparse Blocks format
Group:		System/Libraries

%description -n %{libname}
librsb is a library for sparse matrix computations featuring the Recursive
Sparse Blocks (RSB) matrix format. This format allows cache efficient and
multi-threaded (that is, shared memory parallel) operations on large sparse
matrices. The most common operations necessary to iterative solvers are
available, e.g.: matrix-vector multiplication, triangular solution,
rows/columns scaling, diagonal extraction / setting, blocks extraction, norm
computation, formats conversion. The RSB format is especially well suited
for symmetric and transposed multiplication variants. Most numerical kernels
code is auto generated, and the supported numerical types can be chosen by
the user at build time.

librsb implements the Sparse BLAS standard, as specified in the BLAS Forum
documents.

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%doc COPYING

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	A parallel matrix computations library for the Recursive Sparse Blocks format
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Headers and development files for %{name}.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/rsb-examples.3*
%{_mandir}/man3/rsb-spblas.h.3*
%{_mandir}/man3/rsb.h.3*
%doc examples
%doc README
%doc AUTHORS
#doc ChangeLog
%doc COPYING

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{ver}

# remove pre-built documentation
rm -fr doc/{html,man}/*

# fix file-not-utf8
for f in README
do
  iconv -f iso8859-15 -t utf8 ${f} > ${f}.tmp
  touch -r ${f} ${f}.tmp
  mv -f ${f}.tmp ${f}
done

%build
export CFLAGS=" -D_DEFAULT_SOURCE=1"
export LDFLAGS=" `pkg-config --libs libtirpc`"

# configure
autoreconf -fiv
%configure	\
	--disable-c-examples			\
	--disable-fortran-examples		\
	--enable-doc-build			\
	--enable-fortran-module-install		\
	--enable-librsb-stats			\
	--enable-matrix-types=all		\
	--enable-matrix-ops=all			\
%if %{with octave}
	--enable-octave-testing			\
%endif
	--enable-pkg-config-install		\
	--enable-zero-division-checks-on-solve	\
	--with-hwloc				\
	--with-rpc				\
	--with-zlib				\
	%{nil}

# update doxygen configuration file
pushd doc
doxygen -u
popd

# build
%make

%check
%make qqtests

%install
%makeinstall_std

