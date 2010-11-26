#! /bin/sh

fail() {
	[ -n "%1" ] && echo "$1" 1>&2
	exit 1
}

[ -f __init__.py ] || fail "Could not get version number."

PACKAGE_DIR="packages"
VER=`cat __init__.py | grep -e '^__version__' | cut -d \' -f 2`

PLUGIN_NAME="hvac-plot"
PLUGIN_ARCHIVE="$PLUGIN_NAME-$VER.tgz"
PLUGIN_FILES="LICENSE ChangeLog __init__.py __init__.pyc reqhandler.py reqhandler.pyc css images js"

SCRIPT_NAME="hvac-track"
SCRIPT_ARCHIVE="$SCRIPT_NAME-$VER.tgz"
SCRIPT_FILES="attachments/"

cd `dirname "$0"`

mkdir "$PACKAGE_DIR" > /dev/null 2>&1

if [ -f "$PACKAGE_DIR/$PLUGIN_ARCHIVE" ]; then
	printf "Overwrite $PACKAGE_DIR/$PLUGIN_ARCHIVE? [y/N] "
	read yn < /dev/tty
else
	yn=y
fi
if [ "x$yn" = "xy" -o "x$yn" = "xY" ]; then
	rm -rf "$PACKAGE_DIR/$PLUGIN_NAME" > /dev/null 2>&1
	mkdir "$PACKAGE_DIR/$PLUGIN_NAME" || fail
	cp -a $PLUGIN_FILES "$PACKAGE_DIR/$PLUGIN_NAME" || fail
	tar cfz "$PACKAGE_DIR/$PLUGIN_ARCHIVE" -C "$PACKAGE_DIR" --exclude ".git" "$PLUGIN_NAME"
	rm -rf "$PACKAGE_DIR/$PLUGIN_NAME" > /dev/null 2>&1
else
	exit 1
fi

if [ -f "$PACKAGE_DIR/$SCRIPT_ARCHIVE" ]; then
	printf "Overwrite $PACKAGE_DIR/$SCRIPT_ARCHIVE? [y/N] "
	read yn < /dev/tty
else
	yn=y
fi
if [ "x$yn" = "xy" -o "x$yn" = "xY" ]; then
	rm -rf "$PACKAGE_DIR/$SCRIPT_NAME" > /dev/null 2>&1
	mkdir "$PACKAGE_DIR/$SCRIPT_NAME" || fail
	cp -a $SCRIPT_FILES "$PACKAGE_DIR/$SCRIPT_NAME" || fail
	tar cfz "$PACKAGE_DIR/$SCRIPT_ARCHIVE" -C "$PACKAGE_DIR" --exclude ".git" "$SCRIPT_NAME"
	rm -rf "$PACKAGE_DIR/$SCRIPT_NAME" > /dev/null 2>&1
else
	exit 1
fi
