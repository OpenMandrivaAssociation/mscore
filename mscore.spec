Summary:	Linux MusE Score Typesetter
Name:		mscore
Version: 	0.9.3
Release:	%mkrel 3
License:	GPLv2
Url:		http://mscore.sourceforge.net/
Group:		Publishing
Source0:	http://ovh.dl.sourceforge.net/sourceforge/mscore/%{name}-%{version}.tar.bz2
Patch0:		mscore-0.9.3-fix-underlink.patch
Patch1:		mscore-0.9.3-disable-uitools.patch
Patch2:		mscore-0.9.3-only-install-qm.patch
BuildRequires:	cmake
BuildRequires:	libalsa-devel
BuildRequires:	jackit-devel
Buildrequires:	fluidsynth-devel
BuildRequires:	portaudio-devel
BuildRequires:	tetex-latex
BuildRequires:	qt4-devel > 4.4
BuildRequires:	qt4-linguist
Requires:	qtscriptbindings
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
%patch1 -p0
%patch2 -p0 -b .locale

%build
%cmake_qt4 -DUSE_GLOBAL_FLUID=ON -DBUILD_SCRIPT_INTERFACE=OFF
%make
make lupdate
make lrelease

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std} -C build

# conflicts with qtscriptbindings
rm -f %buildroot%qt4plugins/script/*

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README
%_bindir/*
%_datadir/mscore*
%_datadir/applications/*.desktop
%_datadir/pixmaps/*
%qt4plugins/designer/libawlplugin.so
