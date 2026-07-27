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
    daily_count = sum(1 for item in items if item.category == "日常版")
    special_count = sum(1 for item in items if item.category == "专题")
    report_count = sum(1 for item in items if item.category == "研报")
    recent_list = "".join(
        f'<li><span>{html.escape(item.date or "未标日期")}</span><strong>{html.escape(item.title)}</strong></li>'
        for item in items[:3]
    )
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
            <div class="eyebrow">Latest Drop</div>
            <h2>{html.escape(latest.title)}</h2>
            <p>{html.escape(latest.date)} 发布。这个版本适合直接转给团队做晨会同步、盘前讨论或客户群展示。</p>
            <div class="hero-actions">
              <a class="btn primary" href="./images/{html.escape(latest.file_name)}" target="_blank" rel="noreferrer">打开最新原图</a>
              <a class="btn" href="#archive">查看全部归档</a>
            </div>
            <ul class="recent-list">
              {recent_list}
            </ul>
          </div>
          <a class="hero-preview" href="./images/{html.escape(latest.file_name)}" target="_blank" rel="noreferrer">
            <img src="./images/{html.escape(latest.file_name)}" alt="{html.escape(latest.title)}" loading="eager" />
            <span class="preview-label">最新封面预览</span>
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
      --bg: #ede4d4;
      --paper: rgba(255, 251, 245, 0.88);
      --paper-strong: #f8f1e6;
      --ink: #16324e;
      --muted: #607080;
      --line: rgba(22, 50, 78, 0.1);
      --accent: #c89137;
      --accent-strong: #a86d1d;
      --teal: #187f84;
      --navy: #11283e;
      --shadow: 0 24px 80px rgba(17, 40, 62, 0.12);
      --radius: 28px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(200, 145, 55, 0.22), transparent 18%),
        radial-gradient(circle at 90% 15%, rgba(24, 127, 132, 0.12), transparent 16%),
        linear-gradient(180deg, #f7f1e8 0%, var(--bg) 54%, #e6dbc7 100%);
      color: var(--ink);
      min-height: 100vh;
    }}
    .shell {{
      width: min(1280px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 28px 0 64px;
    }}
    .hero-shell {{
      display: grid;
      gap: 22px;
      grid-template-columns: minmax(0, 1.3fr) minmax(320px, 0.7fr);
      align-items: start;
    }}
    .masthead, .sidepanel, .archive-panel {{
      background: var(--paper);
      backdrop-filter: blur(10px);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }}
    .masthead {{
      min-height: 100%;
      padding: 34px;
      position: relative;
      overflow: hidden;
    }}
    .masthead::before {{
      content: "";
      position: absolute;
      inset: 0 0 auto 0;
      height: 160px;
      background:
        radial-gradient(circle at 15% 25%, rgba(200, 145, 55, 0.22), transparent 28%),
        linear-gradient(135deg, rgba(17, 40, 62, 0.98), rgba(24, 82, 95, 0.92));
      z-index: 0;
    }}
    .masthead > * {{
      position: relative;
      z-index: 1;
    }}
    .brand-kicker {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 8px 14px;
      border-radius: 999px;
      color: #fff;
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255,255,255,0.16);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    .brand-kicker::before {{
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: linear-gradient(135deg, #f0c66d, #ce8a26);
    }}
    .masthead h1 {{
      margin: 72px 0 0;
      max-width: 100%;
      font-size: clamp(30px, 4.1vw, 46px);
      line-height: 1.04;
      letter-spacing: -0.02em;
    }}
    .title-brand {{
      display: inline;
      white-space: nowrap;
    }}
    .title-divider {{
      display: inline;
      margin: 0 0.16em;
      color: #244b70;
    }}
    .title-main {{
      display: block;
      margin-top: 4px;
    }}
    .masthead p {{
      margin: 16px 0 0;
      max-width: 46em;
      font-size: 17px;
      line-height: 1.8;
      color: var(--muted);
    }}
    .masthead strong {{
      color: var(--navy);
    }}
    .masthead-note {{
      margin-top: 26px;
      padding-top: 18px;
      border-top: 1px solid rgba(22, 50, 78, 0.12);
      color: var(--muted);
      line-height: 1.75;
      font-size: 15px;
    }}
    .sidepanel {{
      padding: 22px;
      display: grid;
      gap: 16px;
    }}
    .metric-grid {{
      display: grid;
      gap: 14px;
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
    .metric {{
      padding: 18px;
      border-radius: 20px;
      background: linear-gradient(180deg, rgba(255,255,255,0.85), rgba(247, 238, 225, 0.95));
      border: 1px solid rgba(22, 50, 78, 0.08);
    }}
    .stat-label {{
      font-size: 12px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--teal);
      font-weight: 700;
    }}
    .stat-value {{
      margin-top: 6px;
      font-size: 30px;
      font-weight: 700;
    }}
    .stat-note {{
      margin-top: 6px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
    }}
    .hero-card {{
      margin-top: 22px;
      display: grid;
      grid-template-columns: minmax(0, 0.86fr) minmax(0, 1.14fr);
      gap: 24px;
      padding: 24px;
      border-radius: 34px;
      background:
        radial-gradient(circle at top left, rgba(201, 145, 56, 0.22), transparent 24%),
        linear-gradient(135deg, rgba(17, 40, 62, 0.99), rgba(24, 87, 99, 0.94));
      color: #fff;
      box-shadow: var(--shadow);
    }}
    .hero-copy {{
      padding: 8px 8px 8px 12px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .eyebrow {{
      color: #f0c66d;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
    }}
    .hero-copy h2 {{
      margin: 14px 0;
      font-size: clamp(28px, 3.6vw, 48px);
      line-height: 1.08;
    }}
    .hero-copy p {{
      margin: 0;
      color: rgba(255,255,255,0.78);
      font-size: 17px;
      line-height: 1.8;
    }}
    .hero-actions {{
      display: flex;
      gap: 12px;
      margin-top: 24px;
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
      background: linear-gradient(135deg, #e3b25c, #c57821);
      border-color: transparent;
      color: #172837;
    }}
    .recent-list {{
      margin: 24px 0 0;
      padding: 18px 0 0;
      list-style: none;
      display: grid;
      gap: 12px;
      border-top: 1px solid rgba(255,255,255,0.12);
    }}
    .recent-list li {{
      display: grid;
      gap: 3px;
    }}
    .recent-list span {{
      font-size: 12px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: rgba(240, 198, 109, 0.92);
    }}
    .recent-list strong {{
      font-size: 15px;
      line-height: 1.55;
      font-weight: 600;
      color: rgba(255,255,255,0.92);
    }}
    .hero-preview {{
      position: relative;
      display: block;
      min-height: 100%;
      border-radius: 26px;
      overflow: hidden;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.12);
    }}
    .hero-preview img {{
      display: block;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
    }}
    .preview-label {{
      position: absolute;
      right: 18px;
      bottom: 18px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(17, 40, 62, 0.72);
      border: 1px solid rgba(255,255,255,0.14);
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .06em;
    }}
    .archive-panel {{
      margin-top: 28px;
      padding: 24px;
    }}
    .archive-header {{
      margin-top: 34px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 18px;
      flex-wrap: wrap;
    }}
    .archive-header h3 {{
      margin: 0;
      font-size: 34px;
    }}
    .archive-header p {{
      margin: 10px 0 0;
      color: var(--muted);
      line-height: 1.7;
    }}
    .toolbar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .chip {{
      border: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(245, 236, 220, 0.95));
      color: var(--ink);
      border-radius: 999px;
      padding: 11px 16px;
      font-weight: 700;
      cursor: pointer;
    }}
    .chip.active {{
      background: linear-gradient(135deg, var(--navy), #1a5563);
      color: #fff;
      border-color: transparent;
    }}
    .grid {{
      margin-top: 24px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 22px;
    }}
    .card {{
      display: flex;
      flex-direction: column;
      background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(248, 241, 230, 0.95));
      border: 1px solid rgba(24, 50, 75, 0.08);
      border-radius: 26px;
      overflow: hidden;
      box-shadow: var(--shadow);
      min-height: 100%;
      transition: transform 180ms ease, box-shadow 180ms ease;
    }}
    .card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 28px 80px rgba(17, 40, 62, 0.16);
    }}
    .thumb {{
      display: block;
      aspect-ratio: 10 / 11;
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
      padding: 20px;
    }}
    .badge {{
      display: inline-flex;
      width: fit-content;
      padding: 7px 11px;
      border-radius: 999px;
      background: rgba(15, 123, 131, 0.1);
      color: var(--teal);
      font-weight: 700;
      font-size: 12px;
    }}
    .card-body h4 {{
      margin: 0;
      font-size: 22px;
      line-height: 1.35;
    }}
    .card-body p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.7;
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
    .link:hover {{
      color: var(--accent-strong);
    }}
    footer {{
      margin-top: 34px;
      padding: 22px 0 0;
      border-top: 1px solid rgba(24, 50, 75, 0.12);
      color: var(--muted);
      font-size: 14px;
      line-height: 1.8;
    }}
    @media (max-width: 920px) {{
      .hero-shell, .hero-card {{
        grid-template-columns: 1fr;
      }}
      .masthead {{
        padding: 24px;
      }}
      .masthead h1 {{
        margin-top: 56px;
      }}
      .title-divider {{
        display: none;
      }}
      .title-brand, .title-main {{
        display: block;
      }}
      .metric-grid {{
        grid-template-columns: 1fr 1fr;
      }}
      .hero-preview {{
        max-height: 520px;
      }}
      .archive-header h3 {{
        font-size: 28px;
      }}
    }}
    @media (max-width: 640px) {{
      .shell {{
        width: min(100vw - 20px, 1280px);
      }}
      .metric-grid {{
        grid-template-columns: 1fr;
      }}
      .hero-card {{
        padding: 16px;
      }}
      .hero-copy h2 {{
        font-size: 30px;
      }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero-shell">
      <div class="masthead">
        <div class="brand-kicker">LAdaxiansheng</div>
        <h1><span class="title-brand">LAdaxiansheng</span><span class="title-divider">|</span><span class="title-main">美股盘前简报</span></h1>
        <p>{SITE_SUBTITLE}。把日常版、专题版和深度研报统一放进一个更适合团队传播的在线展示页。</p>
        <div class="masthead-note">
          适合内部群转发、晨会投屏、客户同步和历史归档检索。所有图片保留原始清晰度，点击即可查看原图。
        </div>
      </div>
      <div class="sidepanel">
        <div class="metric-grid">
          <div class="metric">
            <div class="stat-label">内容总数</div>
            <div class="stat-value">{len(items)} 张</div>
            <div class="stat-note">包含日常版、专题版和深度研报。</div>
          </div>
          <div class="metric">
            <div class="stat-label">品牌形态</div>
            <div class="stat-value">公开网页</div>
            <div class="stat-note">适合外部链接分发与内部集中浏览。</div>
          </div>
          <div class="metric">
            <div class="stat-label">日常版</div>
            <div class="stat-value">{daily_count}</div>
            <div class="stat-note">每日盘前主简报。</div>
          </div>
          <div class="metric">
            <div class="stat-label">专题 / 研报</div>
            <div class="stat-value">{special_count + report_count}</div>
            <div class="stat-note">专题版 {special_count}，研报 {report_count}。</div>
          </div>
        </div>
      </div>
    </section>
    {latest_block}
    <section class="archive-panel" id="archive">
      <div class="archive-header">
        <div>
          <h3>内容归档展厅</h3>
          <p>支持按类型筛选。每张卡片都可以直接打开原图，更适合转发、投屏和历史回看。</p>
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
      页面由本地图片目录自动生成。后续新增 PNG 后重新运行构建脚本即可刷新站点，并同步公开页内容。
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
