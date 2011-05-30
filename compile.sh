#! /bin/sh

fail() {
	[ -n "%1" ] && echo "$1" 1>&2
	exit 1
}

cd `dirname "$0"`

IWS_DIR="/Library/Application Support/Perceptive Automation/Indigo 5/IndigoWebServer/"
SCRIPT_DIR="$IWS_DIR/../Scripts/Attachments"

PY_FILES="__init__.py reqhandler.py"

echo "# ######################################################################### #"
echo "# Stopping IndigoWebServer"
"$IWS_DIR"/devhelpers/indigowebstop || fail
echo "# ######################################################################### #"
echo ""

echo "# ######################################################################### #"
echo "# Cleaning development tree"
git clean -X -f || fail
echo "# ######################################################################### #"
echo ""

echo "# ######################################################################### #"
echo "# Compiling Plugin"
for f in $PY_FILES; do
	python /usr/lib/python2.6/py_compile.pyc "$f" || fail
	echo "# $f compiled successfully."
done
echo "# ######################################################################### #"
echo ""

echo "# ######################################################################### #"
echo "# Updating Script Attachments"
pushd attachments > /dev/null 2>&1
for f in *.scpt; do
	if [ "$f" -nt "$SCRIPT_DIR/$f" ]; then
		WARN_RELOAD_SCRIPTS=1
		cp -v "$f" "$SCRIPT_DIR/$f"
	fi
done
popd > /dev/null 2>&1
[ -n "$WARN_RELOAD_SCRIPTS" ] && echo "# SCRIPT ATTACHMENTS UPDATED -- RELOAD SCRIPT ATTACHMENTS IN INDIGO."
echo "# ######################################################################### #"
echo ""

echo "Press enter to restart IndigoWebServer"
read foo < /dev/tty

echo "# ######################################################################### #"
echo "# Starting IndigoWebServer"
python "$IWS_DIR/IndigoWebServer.py" -i 1176 -w 8000 -cnd &
exit 0
