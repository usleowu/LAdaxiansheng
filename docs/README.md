# LAdaxiansheng 静态网页

这个目录用于承载 `LAdaxiansheng` 的 `美股盘前简报` 图片静态网页输出。

先把本地 PNG 同步进仓库：

```powershell
python .\scripts\sync_dasheng_brief_assets.py
```

再构建网页：

```powershell
python .\scripts\build_dasheng_brief_site.py --source-dir .\dasheng_brief_assets
```

本地预览：

```powershell
cd .\work\dasheng_brief_site
python -m http.server 8080
```

打开：

```text
http://127.0.0.1:8080
```

部署思路：

1. 这个仓库已经准备好了 GitHub Actions 工作流：`.github/workflows/deploy-dasheng-pages.yml`。
2. 把 `dasheng_brief_assets`、脚本和工作流推到 GitHub 的 `main` 分支。
3. 在 GitHub 仓库设置里把 Pages 的 Source 设为 `GitHub Actions`。
4. 以后新增 PNG 后，先运行同步脚本，再提交并推送，Pages 会自动更新。
