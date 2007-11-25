Summary:	Linux MusE Score Typesetter
Name:		mscore
Version: 	0.7.0.1
Release:	%mkrel 1
License:	GPLv2+
Url:		http://www.gnokii.org/
Group:		Publishing
Source0:	http://www.gnokii.org/download/gnokii/%{name}-%{version}.tar.bz2
BuildRequires:	cmake libalsa-devel jackit-devel tetex
BuildRequires:	qt4-devel > 4.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
MuseScore stands for Linux MusE Score Typesetter.

Features:
      - WYSIWYG design, notes are entered on a "virtual notepaper"
      - TrueType font(s) for printing & display allows for high quality
        scaling to all sizes
      - easy & fast note entry
      - many editing functions
      - MusicXML import/export
      - Midi (SMF) import/export
      - MuseData import
      - Midi input for note entry
      - integrated sequencer and software synthesizer to
        play the score
      - print or create pdf files

%prep
%setup -q -n %{name}-0.7.0/mscore

%build
%cmake_qt4
%make

%install
rm -rf $RPM_BUILD_ROOT
cd build
%{makeinstall_std}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README
%_bindir/*
%_datadir/mscore-0.7
