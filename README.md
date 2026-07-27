# LAdaxiansheng

Public GitHub Pages site for `LAdaxiansheng | 美股盘前简报`.

## Update flow

1. Generate new PNG brief images into `C:\Users\mufeng\Documents\大先生财经\美股盘前简报`.
2. Sync those PNG assets into this repo:

```powershell
python .\scripts\sync_dasheng_brief_assets.py
```

3. Rebuild the static site:

```powershell
python .\scripts\build_dasheng_brief_site.py --source-dir .\dasheng_brief_assets --output-dir .\work\dasheng_brief_site
```

4. Sync the built site into `docs`:

```powershell
Remove-Item -Recurse -Force .\docs -ErrorAction SilentlyContinue
Copy-Item -Recurse .\work\dasheng_brief_site .\docs
```

5. Commit and push to `main`. GitHub Pages publishes from `/docs`.
