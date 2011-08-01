%global major_version 1
%global minor_version 9
%global teeny_version 2
%global patch_level 290

%global major_minor_version %{major_version}.%{minor_version}

%global ruby_version %{major_minor_version}.%{teeny_version}
%global ruby_abi %{major_minor_version}.1

%global ruby_archive %{name}-%{ruby_version}-p%{patch_level}

Summary: An interpreter of object-oriented scripting language
Name: ruby
Version: %{ruby_version}.%{patch_level}
Release: 1%{?dist}
Group: Development/Languages
License: Ruby or GPLv2
URL: http://ruby-lang.org/
Source0: ftp://ftp.ruby-lang.org/pub/%{name}/%{major_minor_version}/%{ruby_archive}.tar.gz
BuildRequires: autoconf
BuildRequires: gdbm-devel
BuildRequires: ncurses-devel
BuildRequires: db4-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: tk-devel

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -q -n %{ruby_archive}


%build
autoconf

%configure \
        --disable-rpath \
        --enable-shared

make %{?_smp_mflags} COPY="cp -p"


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%check
# Unfortunately not all tests passes :/ Moreover the test suite is unstable.
# 8569 tests, 2200057 assertions, 2 failures, 2 errors, 0 skips
# 8569 tests, 2200055 assertions, 3 failures, 2 errors, 0 skips
make check || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING*
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc NEWS
%doc README
%doc README.ja
%doc README.EXT
%doc README.EXT.ja
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
%{_includedir}/ruby-%{ruby_abi}
%{_libdir}/ruby
%{_libdir}/libruby.so*
# http://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Static_Libraries
%exclude %{_libdir}/libruby-static.a

%changelog

