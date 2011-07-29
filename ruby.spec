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
%doc



%changelog

