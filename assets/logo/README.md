# Jaon Logo Assets

本目录包含 Jaon 编程语言的 Logo 资源。

## 文件说明

- `jaon-logo-16x16.png` ~ `jaon-logo-1024x1024.png` — 各种尺寸的方形 Logo
- `jaon-logo.ico` — 多尺寸 ICO 文件，可用于 Windows 图标
- `jaon-banner.png` — 横向 Banner（1200x400）
- `jaon-social.png` — 社交媒体预览图（1280x640）
- `design_logo.py` — Logo 生成脚本

## 重新生成

```bash
cd assets/logo
python design_logo.py
```

## 设计理念

Jaon 的 Logo 是 Python 与 Java 两大语言的视觉结合：

- **Java 的基因**：保留 Java 图标标志性的三条 S 形蒸汽线，象征企业级语言的稳健与成熟。
- **Python 的配色**：将三条线改为 Python 官方蓝（#3776AB）与黄（#FFD43B），两侧为蓝、中间为黄，体现 Python 的活力与简洁。
- **无背景图形**：去掉外圈圆盘，仅保留三条线，让标志在各种尺寸和主题下都清晰可辨。
- **透明背景**：方形 Logo 保留透明背景，可适配浅色与深色主题。
- **深色 Banner**：横向 Banner 与社交媒体图采用近黑色深空背景，突出蓝黄线条的对比。
