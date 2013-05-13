#!/bin/sh

if [ ! $# -eq 3 ]; then
	cat <<-EOF
	Usage: $0 filename.desktop entryname exec
EOF
	exit 1
fi

cat <<-EOF > $1
	[Desktop Entry]
	Version=1.0
	Name=$2
	Exec=$3
	Icon=
	Terminal=false
	Type=Application
	Categories=AudioVideo;Player; // Applications -> Sound & Video ->
	Categories=Game; // Applications -> Games ->
	Categories=Application;Network; // Applications -> Internet ->
	Categories=Utility; // Applications -> Accessories ->
	Categories=Application;Development; // Applications -> Programming ->
	Categories=Application;Graphics;Viewer; // Applications -> Graphics ->
	Categories=Office; // Applications -> Office ->
	Categories=System; // Applications -> System Tools ->
	Categories=Education; // Applications -> Education ->
	Categories=Science; // Applications -> Science ->
EOF

gedit $1
