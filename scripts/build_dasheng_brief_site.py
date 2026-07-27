from __future__ import annotations

import argparse
import html
import json
import shutil
from dataclasses import dataclass
from pathlib import Path


SITE_TITLE = "LAdaxiansheng | 美股盘前简报"
SITE_SUBTITLE = "LAdaxiansheng 的每日盘前简报与专题图归档"


@dataclass
class BriefImage:
    file_name: str
    title: str
    date: str
    category: str


def parse_brief(path: Path) -> BriefImage:
    stem = path.stem
    parts = stem.split("-", 1)
    if len(parts) == 2:
        date, title = parts
    else:
        date, title = "", stem

    category = "专题"
    if "美股盘前信息简报" in title:
        category = "日常版"
    elif "研报" in title:
        category = "研报"

    return BriefImage(
        file_name=path.name,
        title=title,
        date=date,
        category=category,
    )


def copy_images(items: list[BriefImage], source_dir: Path, image_dir: Path) -> None:
    image_dir.mkdir(parents=True, exist_ok=True)
    for item in items:
        shutil.copy2(source_dir / item.file_name, image_dir / item.file_name)


def render_html(items: list[BriefImage]) -> str:
    latest = items[0] if items else None
    items_json = json.dumps(
        [
            {
                "fileName": item.file_name,
                "title": item.title,
                "date": item.date,
                "category": item.category,
            }
            for item in items
        ],
        ensure_ascii=False,
        indent=2,
    )

    latest_block = ""
    if latest:
        latest_block = f"""
        <section class="hero-card">
          <div class="hero-copy">
            <div class="eyebrow">最新更新</div>
            <h2>{html.escape(latest.title)}</h2>
            <p>{html.escape(latest.date)} 发布，适合直接发给团队做盘前同步。</p>
            <div class="hero-actions">
              <a class="btn primary" href="./images/{html.escape(latest.file_name)}" target="_blank" rel="noreferrer">查看原图</a>
              <a class="btn" href="#archive">浏览全部</a>
            </div>
          </div>
          <a class="hero-preview" href="./images/{html.escape(latest.file_name)}" target="_blank" rel="noreferrer">
            <img src="./images/{html.escape(latest.file_name)}" alt="{html.escape(latest.title)}" loading="eager" />
          </a>
        </section>
        """

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{SITE_TITLE}</title>
  <style>
    :root {{
      --bg: #efe8dc;
      --paper: #f9f4eb;
      --ink: #18324b;
      --muted: #64707a;
      --line: #d4cab8;
      --accent: #b88a3b;
      --teal: #0f7b83;
      --shadow: 0 20px 50px rgba(24, 50, 75, 0.12);
      --radius: 22px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
      background:
        radial-gradient(circle at top right, rgba(184, 138, 59, 0.16), transparent 20%),
        linear-gradient(180deg, #f6f0e5 0%, var(--bg) 52%, #e8e0d2 100%);
      color: var(--ink);
    }}
    .shell {{
      width: min(1180px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 32px 0 56px;
    }}
    .topbar {{
      display: grid;
      gap: 20px;
      grid-template-columns: 1.4fr 0.8fr;
      align-items: stretch;
    }}
    .masthead, .meta {{
      background: rgba(249, 244, 235, 0.82);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(24, 50, 75, 0.08);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }}
    .masthead {{
      padding: 28px;
      position: relative;
      overflow: hidden;
    }}
    .masthead::before {{
      content: "";
      position: absolute;
      inset: 0 auto 0 0;
      width: 10px;
      background: linear-gradient(180deg, var(--accent), #dfb76a);
    }}
    .masthead h1 {{
      margin: 0;
      font-size: clamp(28px, 4vw, 44px);
      line-height: 1.08;
    }}
    .masthead p {{
      margin: 12px 0 0;
      font-size: 16px;
      color: var(--muted);
    }}
    .meta {{
      padding: 24px 26px;
      display: grid;
      gap: 14px;
      align-content: center;
    }}
    .stat-label {{
      font-size: 12px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--teal);
      font-weight: 700;
    }}
    .stat-value {{
      font-size: 26px;
      font-weight: 700;
    }}
    .hero-card {{
      margin-top: 26px;
      display: grid;
      grid-template-columns: 0.95fr 1.05fr;
      gap: 18px;
      padding: 18px;
      border-radius: 28px;
      background: linear-gradient(135deg, rgba(24, 50, 75, 0.97), rgba(23, 68, 85, 0.94));
      color: #fff;
      box-shadow: var(--shadow);
    }}
    .hero-copy {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .eyebrow {{
      color: #d9b56d;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    .hero-copy h2 {{
      margin: 12px 0;
      font-size: clamp(24px, 3.2vw, 40px);
      line-height: 1.12;
    }}
    .hero-copy p {{
      margin: 0;
      color: rgba(255,255,255,0.78);
      font-size: 16px;
      line-height: 1.65;
    }}
    .hero-actions {{
      display: flex;
      gap: 12px;
      margin-top: 22px;
      flex-wrap: wrap;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 44px;
      padding: 0 18px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.2);
      color: #fff;
      text-decoration: none;
      font-weight: 700;
    }}
    .btn.primary {{
      background: linear-gradient(135deg, #d4a047, #bf7c29);
      border-color: transparent;
      color: #172837;
    }}
    .hero-preview {{
      display: block;
      min-height: 100%;
      border-radius: 20px;
      overflow: hidden;
      background: rgba(255,255,255,0.08);
    }}
    .hero-preview img {{
      display: block;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
    }}
    .archive-header {{
      margin-top: 34px;
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 18px;
      flex-wrap: wrap;
    }}
    .archive-header h3 {{
      margin: 0;
      font-size: 28px;
    }}
    .archive-header p {{
      margin: 8px 0 0;
      color: var(--muted);
    }}
    .toolbar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .chip {{
      border: 1px solid var(--line);
      background: rgba(249, 244, 235, 0.85);
      color: var(--ink);
      border-radius: 999px;
      padding: 10px 14px;
      font-weight: 700;
      cursor: pointer;
    }}
    .chip.active {{
      background: var(--ink);
      color: #fff;
      border-color: var(--ink);
    }}
    .grid {{
      margin-top: 18px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 18px;
    }}
    .card {{
      display: flex;
      flex-direction: column;
      background: rgba(249, 244, 235, 0.92);
      border: 1px solid rgba(24, 50, 75, 0.08);
      border-radius: 22px;
      overflow: hidden;
      box-shadow: var(--shadow);
      min-height: 100%;
    }}
    .thumb {{
      display: block;
      aspect-ratio: 4 / 5;
      overflow: hidden;
      background: #ddd1bf;
    }}
    .thumb img {{
      display: block;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
      transition: transform 180ms ease;
    }}
    .card:hover .thumb img {{
      transform: scale(1.03);
    }}
    .card-body {{
      display: grid;
      gap: 10px;
      padding: 18px;
    }}
    .badge {{
      display: inline-flex;
      width: fit-content;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(15, 123, 131, 0.1);
      color: var(--teal);
      font-weight: 700;
      font-size: 12px;
    }}
    .card-body h4 {{
      margin: 0;
      font-size: 20px;
      line-height: 1.3;
    }}
    .card-body p {{
      margin: 0;
      color: var(--muted);
    }}
    .card-actions {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 2px;
    }}
    .link {{
      color: var(--ink);
      font-weight: 700;
      text-decoration: none;
    }}
    footer {{
      margin-top: 34px;
      padding-top: 18px;
      border-top: 1px solid rgba(24, 50, 75, 0.12);
      color: var(--muted);
      font-size: 14px;
    }}
    @media (max-width: 920px) {{
      .topbar, .hero-card {{
        grid-template-columns: 1fr;
      }}
      .hero-preview {{
        max-height: 520px;
      }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="topbar">
      <div class="masthead">
        <h1>{SITE_TITLE}</h1>
        <p>{SITE_SUBTITLE}</p>
      </div>
      <div class="meta">
        <div>
          <div class="stat-label">内容总数</div>
          <div class="stat-value">{len(items)} 张</div>
        </div>
        <div>
          <div class="stat-label">分享方式</div>
          <div class="stat-value">静态网页</div>
        </div>
      </div>
    </section>
    {latest_block}
    <section id="archive">
      <div class="archive-header">
        <div>
          <h3>内容归档</h3>
          <p>支持按类型筛选，点击卡片直接打开原图。</p>
        </div>
        <div class="toolbar">
          <button class="chip active" data-filter="全部">全部</button>
          <button class="chip" data-filter="日常版">日常版</button>
          <button class="chip" data-filter="专题">专题</button>
          <button class="chip" data-filter="研报">研报</button>
        </div>
      </div>
      <div class="grid" id="grid"></div>
    </section>
    <footer>
      页面由本地图片目录自动生成。后续新增 PNG 后重新运行构建脚本即可刷新站点。
    </footer>
  </main>
  <script>
    const items = {items_json};
    const grid = document.getElementById("grid");
    const chips = Array.from(document.querySelectorAll(".chip"));

    function render(filter) {{
      grid.innerHTML = "";
      const visible = items.filter(item => filter === "全部" || item.category === filter);
      for (const item of visible) {{
        const card = document.createElement("article");
        card.className = "card";
        card.innerHTML = `
          <a class="thumb" href="./images/${{item.fileName}}" target="_blank" rel="noreferrer">
            <img src="./images/${{item.fileName}}" alt="${{item.title}}" loading="lazy" />
          </a>
          <div class="card-body">
            <span class="badge">${{item.category}}</span>
            <h4>${{item.title}}</h4>
            <p>${{item.date || "未标日期"}}</p>
            <div class="card-actions">
              <a class="link" href="./images/${{item.fileName}}" target="_blank" rel="noreferrer">查看原图</a>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }}
    }}

    for (const chip of chips) {{
      chip.addEventListener("click", () => {{
        for (const other of chips) other.classList.remove("active");
        chip.classList.add("active");
        render(chip.dataset.filter);
      }});
    }}

    render("全部");
  </script>
</body>
</html>
"""


def build_site(source_dir: Path, output_dir: Path) -> None:
    source_dir = source_dir.resolve()
    output_dir = output_dir.resolve()
    image_dir = output_dir / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = sorted(source_dir.glob("*.png"), reverse=True)
    items = [parse_brief(path) for path in image_paths]
    copy_images(items, source_dir, image_dir)
    (output_dir / "index.html").write_text(render_html(items), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a static website for Dasheng Caijing brief images.")
    parser.add_argument(
        "--source-dir",
        default=r"C:\Users\mufeng\Documents\大先生财经\美股盘前简报",
        help="Directory that contains the PNG brief images.",
    )
    parser.add_argument(
        "--output-dir",
        default=r"C:\Users\mufeng\Documents\Codex\2026-06-05\analyze-a-public-company-pull-the\work\dasheng_brief_site",
        help="Directory where the static site will be written.",
    )
    args = parser.parse_args()
    build_site(Path(args.source_dir), Path(args.output_dir))


if __name__ == "__main__":
    main()
