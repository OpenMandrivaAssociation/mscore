Summary:	Linux MusE Score Typesetter
Name:		mscore
Version: 	0.8.0
Release:	%mkrel 1
License:	GPLv2+
Url:		http://mscore.sourceforge.net/
Group:		Publishing
Source0:	http://ovh.dl.sourceforge.net/sourceforge/mscore/%{name}-%{version}.tar.bz2
Patch0:		mscore-0.8.0-fix-desktop-file.patch
BuildRequires:	cmake libalsa-devel jackit-devel texlive-texmf-context
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
%setup -q -n %{name}-%{version}/mscore
%patch0 -p0

%build
%cmake_qt4
make

%install
rm -rf $RPM_BUILD_ROOT
cd build
%{makeinstall_std}

%post
%update_menus

%postun
%clean_menus

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README
%_bindir/*
%_datadir/mscore*
%_datadir/applications/*.desktop
%_datadir/pixmaps/*.png
