%define srcname MuseScore

Summary:    Linux MusE Score Typesetter
Name:       mscore
Version:    0.9.5
Release:    %mkrel 3
License:    GPLv2
Url:        http://mscore.sourceforge.net/
Group:      Publishing
Source0:    http://downloads.sourceforge.net/project/mscore/mscore/%{name}-%{version}/%{srcname}-%{version}.tar.bz2
Patch0:     mscore-0.9.5-fix-underlink.patch
Patch1:     mscore-0.9.5-disable-uitools.patch
BuildRequires:  cmake
BuildRequires:  libalsa-devel
BuildRequires:  jackit-devel
BuildRequires:  fluidsynth-devel
BuildRequires:  portaudio-devel
BuildRequires:  tetex-latex
BuildRequires:  qt4-devel > 4.4
BuildRequires:  qt4-linguist
Requires:   qtscriptbindings
Provides:   musescore-%{version}
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
# only install .qm files
perl -pi -e 's,.*.ts\n,,g' share/locale/CMakeLists.txt

%build
%cmake_qt4 -DUSE_GLOBAL_FLUID=ON -DBUILD_SCRIPT_INTERFACE=OFF
%make
make lupdate
make lrelease

%install
rm -rf %{buildroot}
%{makeinstall_std} -C build

# conflicts with qtscriptbindings
rm -f %{buildroot}%{qt4plugins}/script/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README
%{_bindir}/%{name}
%{_datadir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{qt4plugins}/designer/libawlplugin.so
