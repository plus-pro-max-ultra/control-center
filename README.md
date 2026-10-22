# 控制中心（Control Center）

MM 與 Instinct 之間的最高長期規則文件與狀態頁。

- `CONTROL.md` — 規則的唯一來源（六個區塊）。編輯此檔即修改規則。
- `CHANGELOG.md` — 更新紀錄。
- `site/` — 頁面模板與樣式。
- `tools/build.py` — 將 CONTROL.md + CHANGELOG.md 渲染為 `index.html`。
- `tools/push.sh` — 建置、提交、推送（需要有 repo 權限的 PAT）。

每次推送版本時，於同一提交更新 CONTROL.md 的「目前狀態」與 CHANGELOG.md。
