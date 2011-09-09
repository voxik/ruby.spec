%global major_version 1
%global minor_version 9
%global teeny_version 3
# TODO: This is small hack, but works as long as the package is not official.
%global patch_level review1

%global major_minor_version %{major_version}.%{minor_version}

%global ruby_version %{major_minor_version}.%{teeny_version}
%global ruby_abi %{major_minor_version}.1

%global ruby_archive %{name}-%{ruby_version}-p%{patch_level}

%global ruby_libdir %{_datadir}/%{name}
%global ruby_libarchdir %{_libdir}/%{name}

# This is the local lib/arch and should not be used for packaging.
%global ruby_sitedir site_ruby
%global ruby_sitelibdir %{_prefix}/local/share/ruby/%{ruby_sitedir}
%global ruby_sitearchdir %{_prefix}/local/%{_lib}/ruby/%{ruby_sitedir}

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the Fedora repositories.
%global ruby_vendordir vendor_ruby
%global ruby_vendorlibdir %{_datadir}/ruby/%{ruby_vendordir}
%global ruby_vendorarchdir %{_libdir}/ruby/%{ruby_vendordir}

Summary: An interpreter of object-oriented scripting language
Name: ruby
Version: %{ruby_version}.%{patch_level}
Release: 1%{?dist}
Group: Development/Languages
License: Ruby or BSD
URL: http://ruby-lang.org/
Source0: ftp://ftp.ruby-lang.org/pub/%{name}/%{major_minor_version}/%{ruby_archive}.tar.gz

# http://redmine.ruby-lang.org/issues/5231
Patch0: ruby-1.9.3-disable-versioned-paths.patch
# TODO: Should be submitted upstream?
Patch1: ruby-1.9.3-arch-specific-dir.patch
# http://redmine.ruby-lang.org/issues/5281
Patch2: ruby-1.9.3-added-site-and-vendor-arch-flags.patch

BuildRequires: autoconf
BuildRequires: gdbm-devel
BuildRequires: ncurses-devel
BuildRequires: db4-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: tk-devel
# Needed to pass test_set_program_name(TestRubyOptions)
BuildRequires: procps

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package devel
Summary:    A Ruby development environment
Group:      Development/Languages
# Requires:   %{name}-libs = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Provides:   ruby(devel) = %{major_minor_version}
Provides:   ruby(devel) = %{ruby_version}

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.

%prep
%setup -q -n %{ruby_archive}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoconf

%configure \
        --with-rubylibprefix='%{ruby_libdir}' \
        --with-archdir='%{ruby_libarchdir}' \
        --with-sitedir='%{ruby_sitelibdir}' \
        --with-sitearchdir='%{ruby_sitearchdir}' \
        --with-vendordir='%{ruby_vendorlibdir}' \
        --with-vendorarchdir='%{ruby_vendorarchdir}' \
        --with-rubyhdrdir='%{_includedir}' \
        --disable-rpath \
        --enable-shared \
        --disable-versioned-paths

make %{?_smp_mflags} COPY="cp -p"


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%check
# Unfortunately not all tests passes :/ Moreover the test suite is unstable.
# 10089 tests, 2208914 assertions, 3 failures, 0 errors, 45 skips
# 10089 tests, 2208922 assertions, 7 failures, 0 errors, 45 skips
make check || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc NEWS
%doc README
%lang(ja) %doc README.ja
%doc ToDo
%doc doc/ChangeLog-*
%doc doc/NEWS-*
%{_bindir}/erb
%{_bindir}/gem
%{_bindir}/irb
%{_bindir}/rake
%{_bindir}/rdoc
%{_bindir}/ri
%{_bindir}/ruby
%{_bindir}/testrb
%{_mandir}/man1/erb*
%{_mandir}/man1/irb*
%{_mandir}/man1/rake*
%{_mandir}/man1/ri*
%{_mandir}/man1/ruby*
%{_datadir}/ri
%{_libdir}/libruby.so*
%{ruby_libdir}
%{ruby_libarchdir}
# http://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Static_Libraries
%exclude %{_libdir}/libruby-static.a

%files devel
%doc COPYING*
%doc GPL
%doc LEGAL
%doc README.EXT
%lang(ja) %doc README.EXT.ja

%{_includedir}/ruby.h
%{_includedir}/ruby
%dir %{_includedir}/%{_target}
%{_includedir}/%{_target}/ruby

%{_libdir}/libruby.so
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/ruby-1.9.pc

%changelog

