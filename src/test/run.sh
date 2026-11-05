#!/usr/bin/env bash
# 브라우저 회귀. 크로미움이 필요하다.
#   npm i playwright && node src/test/run.sh        (또는 bash src/test/run.sh)
# 한 개만 돌리려면: node src/test/pwdark.js
set -u
cd "$(dirname "$0")/../.."
echo "── 데이터·생성기 검사"
node src/check.js || exit 1
echo
if ! node -e "require('playwright')" 2>/dev/null; then
  echo "playwright가 없다. 먼저 설치한다:  npm install --no-save playwright"
  exit 1
fi
echo "── 브라우저 회귀"
fail=0
for f in src/test/pw*.js; do
  case "$f" in *pwupd.js|*pwcache.js) continue;; esac   # http 가 필요해 아래에서 따로 돌린다
  printf '%-22s ' "$(basename "$f")"
  if timeout 240 node "$f" >/tmp/$(basename "$f").log 2>&1; then echo "통과"
  else echo "★ 실패 (/tmp/$(basename "$f").log)"; fail=1; fi
done
printf '%-22s ' "test_sheet.js"
node src/test/test_sheet.js >/tmp/test_sheet.log 2>&1 && echo "통과" || { echo "★ 실패"; fail=1; }

# ── http 가 있어야 도는 것들 (서비스 워커·새 버전 알림) ──
echo
echo "── 서비스 워커 · 새 버전 알림 (http)"
PORT=8778
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null' EXIT
sleep 2
for f in src/test/pwcache.js src/test/pwupd.js; do
  [ -f "$f" ] || continue
  printf '%-22s ' "$(basename "$f")"
  if VOCA_HTTP="http://127.0.0.1:$PORT/index.html" timeout 240 node "$f" >/tmp/$(basename "$f").log 2>&1
  then echo "통과"; else echo "★ 실패 (/tmp/$(basename "$f").log)"; fail=1; fi
done
kill $SRV 2>/dev/null

exit $fail
