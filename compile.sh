#! /bin/sh

fail() {
	[ -n "%1" ] && echo "$1" 1>&2
	exit 1
}

IWS_DIR="/Library/Application Support/Perceptive Automation/Indigo 4/IndigoWebServer/"

"$IWS_DIR"/devhelpers/indigowebstop || fail

for f in __init__.py reqhandler.py; do
	python /usr/lib/python2.6/py_compile.pyc "$f" || fail
	echo "$f compiled successfully."
done

echo "Starting IWS"
python "$IWS_DIR/IndigoWebServer.py" -i 1176 -w 8000 -cnd &
exit $?
