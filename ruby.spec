%global ruby_major_version 1.9
%global ruby_version %{ruby_major_version}.2
%global ruby_patch_level 290

%global ruby_abi %{ruby_major_version}.1

%global ruby_archive %{name}-%{ruby_version}-p%{ruby_patch_level}

Summary: An interpreter of object-oriented scripting language
Name: ruby
Version: %{ruby_version}.%{ruby_patch_level}
Release: 1%{?dist}
Group: Development/Languages
License: Ruby or GPLv2
URL: http://ruby-lang.org/
Source0: ftp://ftp.ruby-lang.org/pub/%{name}/%{ruby_major_version}/%{ruby_archive}.tar.gz
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

%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


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
%{_libdir}/libruby-static.a
%{_libdir}/ruby

%changelog

