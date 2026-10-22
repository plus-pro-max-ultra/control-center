#!/bin/bash
# Control-center push (agent sandbox): clones repo, copies working tree, commits, pushes. Needs the vault PAT (vocab token, must have access to control-center).
# usage: tools/push.sh "message" [version]   (run from anywhere)
set -e
O=plus-pro-max-ultra; R=control-center; W=$(cd "$(dirname "$0")/.." && pwd)
if [ -n "$2" ]; then python3 "$W/tools/build.py" "$2"; else python3 "$W/tools/build.py"; fi
tools vault write-file --name "GitHub PAT Shinnigammi-vocab" --key password --return-channel imessage --json > /tmp/wf-cc.json
P=$(jq -r .path /tmp/wf-cc.json); T=$(cat $P); rm -f $P /tmp/wf-cc.json
rm -rf /tmp/clone-cc; git clone -q https://x-access-token:$T@github.com/$O/$R.git /tmp/clone-cc 2>&1 | grep -v "empty repository" || true
rsync -a --delete --exclude .git --exclude node_modules "$W/" /tmp/clone-cc/
cd /tmp/clone-cc; git add -A; git -c user.name=maintainer -c user.email=maintainer@users.noreply.github.com commit -q -m "$1" || echo nochange
git push -q origin HEAD:main; git log --oneline -1; cd /; rm -rf /tmp/clone-cc
