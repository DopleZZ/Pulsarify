set -euo pipefail

OUT_DIR=${1:-$(pwd)/dist}
PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
VENV_DIR="$PROJECT_ROOT/.build_venv"
APP_NAME="Pulsarify"



DEVELOPER_ID=${DEVELOPER_ID:-}
ENTITLEMENTS_PATH=${ENTITLEMENTS_PATH:-}
NOTARIZE=${NOTARIZE:-0}
NOTARY_KEYFILE=${NOTARY_KEYFILE:-}
NOTARY_KEYID=${NOTARY_KEYID:-}
NOTARY_ISSUER=${NOTARY_ISSUER:-}
APPLEID=${APPLEID:-}
APP_PWD=${APP_PWD:-}

echo "Project root: $PROJECT_ROOT"
mkdir -p "$OUT_DIR"


python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r "$PROJECT_ROOT/requirements.txt"
python -m pip install pyinstaller


cd "$PROJECT_ROOT"

rm -rf build dist "${APP_NAME}.spec"


DATA_DIR="$PROJECT_ROOT/data"
SRC_DIR="$PROJECT_ROOT/src"


ADD_DATA_ARGS=(
  "${DATA_DIR}${PATHSEP:-:}:${DATA_DIR}"
  "${SRC_DIR}${PATHSEP:-:}:${SRC_DIR}"
)


pyinstaller --noconfirm --windowed --name "$APP_NAME" \
  --add-data "${PROJECT_ROOT}/data:./data" \
  --add-data "${PROJECT_ROOT}/src:./src" \
  --hidden-import PIL \
  --hidden-import PIL.Image \
  --hidden-import PIL.ImageDraw \
  --hidden-import PIL.ImageFont \
  --hidden-import PIL._imaging \
  --hidden-import PIL._imagingcms \
  --collect-all Pillow \
  --collect-submodules Pillow \
  app.py


if [ ! -d "dist/${APP_NAME}.app" ]; then
  echo "Build failed: dist/${APP_NAME}.app not found"
  exit 2
fi

APP_PATH="dist/${APP_NAME}.app"

sign_app_if_needed() {
  if [ -z "$DEVELOPER_ID" ]; then
    echo "DEVELOPER_ID not set; skipping codesign step"
    return
  fi

  echo "Codesigning app and contained binaries with identity: $DEVELOPER_ID"


  echo "Signing internal binaries..."
  find "$APP_PATH/Contents/Frameworks" -type f \( -name "*.dylib" -o -name "*.so" -o -name "*.framework" -o -perm +111 \) -print0 \
    | xargs -0 -I{} sh -c 'codesign --timestamp --sign "$DEVELOPER_ID" --force --options runtime "{}" || true'

  if [ -d "$APP_PATH/Contents/PlugIns" ]; then
    find "$APP_PATH/Contents/PlugIns" -type f -print0 \
      | xargs -0 -I{} sh -c 'codesign --timestamp --sign "$DEVELOPER_ID" --force --options runtime "{}" || true'
  fi


  if [ -f "$APP_PATH/Contents/MacOS/$APP_NAME" ]; then
    codesign --timestamp --sign "$DEVELOPER_ID" --force --options runtime "$APP_PATH/Contents/MacOS/$APP_NAME" || true
  fi


  if [ -n "$ENTITLEMENTS_PATH" ] && [ -f "$ENTITLEMENTS_PATH" ]; then
    codesign --timestamp --sign "$DEVELOPER_ID" --force --options runtime --entitlements "$ENTITLEMENTS_PATH" "$APP_PATH"
  else
    codesign --timestamp --sign "$DEVELOPER_ID" --force --options runtime "$APP_PATH"
  fi

  echo "Verifying codesign..."
  codesign --verify --deep --strict --verbose=2 "$APP_PATH" || true
  spctl -a -t exec -vv "$APP_PATH" || true
}

notarize_if_needed() {
  if [ "$NOTARIZE" != "1" ]; then
    echo "NOTARIZE not set to 1; skipping notarization"
    return
  fi

  if [ -n "$NOTARY_KEYFILE" ] && [ -n "$NOTARY_KEYID" ] && [ -n "$NOTARY_ISSUER" ]; then
    echo "Submitting for notarization via notarytool (API key)"
    ZIP_PATH="$OUT_DIR/${APP_NAME}.zip"
    (cd dist && zip -r "$ZIP_PATH" "${APP_NAME}.app")
    xcrun notarytool submit "$ZIP_PATH" --key "$NOTARY_KEYFILE" --key-id "$NOTARY_KEYID" --issuer "$NOTARY_ISSUER" --wait
    echo "Stapling notarization ticket to app"
    xcrun stapler staple "$APP_PATH"
  elif [ -n "$APPLEID" ] && [ -n "$APP_PWD" ]; then
    echo "Submitting for notarization via altool (AppleID)"
    ZIP_PATH="$OUT_DIR/${APP_NAME}.zip"
    (cd dist && zip -r "$ZIP_PATH" "${APP_NAME}.app")
    xcrun altool --notarize-app -f "$ZIP_PATH" --primary-bundle-id "com.example.${APP_NAME}" -u "$APPLEID" -p "$APP_PWD"
    echo "Note: altool requires manual checking of notarization status. Use xcrun altool --notarization-info <RequestUUID> to poll."
  else
    echo "No notarization credentials provided; skipping notarization"
  fi
}


sign_app_if_needed
notarize_if_needed


DMG_TMP="$OUT_DIR/${APP_NAME}.dmg"
rm -f "$DMG_TMP"
STAGE_DIR=$(mktemp -d)
cp -R "$APP_PATH" "$STAGE_DIR/"
hdiutil create -volname "$APP_NAME" -srcfolder "$STAGE_DIR" -ov -format UDZO "$DMG_TMP"
rm -rf "$STAGE_DIR"


deactivate || true
rm -rf "$VENV_DIR"

echo "DMG created at: $DMG_TMP"
if [ "$NOTARIZE" = "1" ]; then
  echo "If notarization was requested, ensure xcrun notarytool/altool returned success."
else
  echo "Note: app is unsigned/notarized. To distribute widely, set DEVELOPER_ID and NOTARIZE=1 and provide notary credentials. See README.md."
fi
