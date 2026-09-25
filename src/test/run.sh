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
  case "$f" in *pwupd.js) continue;; esac      # http 서버가 필요해 따로 돌린다
  printf '%-22s ' "$(basename "$f")"
  if timeout 240 node "$f" >/tmp/$(basename "$f").log 2>&1; then echo "통과"
  else echo "★ 실패 (/tmp/$(basename "$f").log)"; fail=1; fi
done
printf '%-22s ' "test_sheet.js"
node src/test/test_sheet.js >/tmp/test_sheet.log 2>&1 && echo "통과" || { echo "★ 실패"; fail=1; }
echo
echo "새 버전 알림(pwupd)은 http가 필요하다:"
echo "  python3 -m http.server 8778 & node src/test/pwupd.js"
exit $fail
