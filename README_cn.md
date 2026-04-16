# QuarkCV - 数据驱动的 XeLaTeX 简历模板

[EN](README.md) / 简体中文

一个精致、数据驱动的 XeLaTeX 简历模板，将结构化的 YAML 转换成干净、现代、链接丰富的 PDF。

![](Demo/resume_demo.png)

专为那些既想要 LaTeX 的视觉品质，又想要结构化数据的可维护性，还想要在项目变更时无需反复重写模板代码就能灵活更新简历的人而设计。

## 为什么这个模板与众不同

- **数据优先。** 你的简历内容存放在 `Data/*.yml` 中，而不是散落在各个 TeX 代码块里。
- **兼顾简历的字段设计。** 丰富的个人主页风格数据，可以与简洁的简历专用字段（如 `resume_title`、`resume_summary`、`resume_highlights`）共存。
- **处处可点击。** 邮箱、电话、个人主页、学校链接、项目链接、论文链接以及本地文件，都会生成为可点击的 PDF 链接。
- **优雅的排版。** 与典型的学术简历模板相比，本模板采用了自定义字体、更紧凑的层级、更柔和的配色、支持头像的个人信息头部，以及更整洁的章节对齐。
- **易于扩展。** 增加更多项目、奖项或论文，而不会让主 TeX 文件变成维护的噩梦。
- **安全的降级方案。** 头像图片会缓存在本地，如果无法获取则自动显示占位符。

## 工作原理

1. 编辑 `Data/` 中的数据文件。
2. 运行 `python scripts/build_resume_data.py`。
3. 脚本直接生成 `main.tex`。
4. 使用 XeLaTeX 编译 `main.tex`。

由此形成的工作流中，`main.tex` 是生成的产物，而 `Data/*.yml` 才是真正的数据源。

## 项目结构

```
QuarkCV/
├─ Data/
│  ├─ _config.yml
│  ├─ profile.yml
│  ├─ education.yml
│  ├─ project.yml
│  ├─ awards.yml
│  ├─ publications.yml
│  └─ resume-avatar.jpg        # 自动缓存（如果可能）
├─ Fonts/
├─ scripts/
│  └─ build_resume_data.py
├─ myresume.sty
├─ main.tex                    # 由脚本生成
└─ Readme.md
```

## 快速开始

### 1. 编辑你的数据

更新 `Data/` 中的 YAML 文件：

- `Data/_config.yml`：身份信息、主题、联系方式、可见性开关、预览数量、头像
- `Data/profile.yml`：个人简介、专注领域、技能
- `Data/education.yml`：教育经历及简洁的简历要点
- `Data/project.yml`：项目条目、简历标题、简历摘要
- `Data/awards.yml`：奖项及获奖原因
- `Data/publications.yml`：论文及链接

### 2. 生成 `main.tex`

```bash
python scripts/build_resume_data.py
```

### 3. 编译 PDF

```bash
xelatex main.tex
```

如果你希望最终编译结果更干净，可以运行两次 XeLaTeX。

## 数据设计理念

本模板刻意将丰富的存档数据与简历展示数据分离开来。

例如，一个项目可以包含：

- `title`：完整的原始项目名称
- `description`：适合个人主页的长篇描述
- `resume_title`：你希望在简历上展示的短标题
- `resume_summary`：你希望招聘人员首先看到的简洁陈述

这意味着你可以为自己的个人网站保留详细的记录，同时仍然生成一份聚焦、高信息密度的一页或短篇幅简历。

同样的理念也应用于：

- `profile.yml` 中的 `resume_summary` 和 `resume_focus`
- `education.yml` 中的 `resume_summary` 和 `resume_highlights`
- `project.yml` 中的 `resume_title` 和 `resume_summary`

## 配置亮点

在 `Data/_config.yml` 中，你可以控制：

- `theme.accent_color`
- `theme.accent_soft_color`
- `section_visibility`
- `list_preview_count`
- `contact_links`
- `avatar`

这为你提供了一种干净的方式来重新定制模板主题或调整内容密度，而无需触碰排版逻辑。

## 可点击的链接

生成的 PDF 支持以下类型的可点击链接：

- 邮箱
- 电话
- 个人主页
- GitHub
- Google Scholar
- CV 链接
- 学校 / 机构链接
- 项目链接
- 论文链接
- 本地文件（如 PDF）

## 头像支持

在 `Data/_config.yml` 中设置 `avatar` 为：

- 远程图片 URL
- 本地相对路径
- 或留空

如果提供了远程 URL，生成器会尝试将其缓存到本地 `Data/resume-avatar.*`。如果失败，模板会优雅地回退到基于姓名首字母的占位符，而不会中断编译。

## 适用人群

- 正在制作第一份正式技术简历的学生
- 希望获得更干净学术 CV 模板的研究人员
- 拥有众多项目和不断积累经验的工程师
- 任何想要一份漂亮的 LaTeX 简历，但不想每次修改内容时都去编辑原始 TeX 代码的人

## 定制建议

- 在 `_config.yml` 中更换主题色
- 增加或减少项目 / 奖项的预览数量
- 通过切换 `section_visibility.publications` 来添加论文发表部分
- 调整 YAML 结构以适用于实习、服务、演讲或开源贡献
- 如果你想要更紧凑或更具杂志感的版面，可以在 `myresume.sty` 中调整间距和字体

## 推荐的工作流程

- 将 `Data/*.yml` 视为你的内容源
- 将 `scripts/build_resume_data.py` 视为内容到排版的桥梁
- 将 `main.tex` 视为生成的输出
- 将 `myresume.sty` 视为视觉系统

这种分离保证了即使简历不断增长，项目也能保持良好的可维护性。

## 注意事项

- 请使用 XeLaTeX 进行编译。
- `main.tex` 是自动生成的，手动编辑的内容会被覆盖。
- 如果你的头像或本地链接文件移动了位置，请在重新编译前再次运行生成脚本。

## 开源许可

你可以自由使用、修改和混合此模板，用于个人简历、作品集简历以及学术 CV 变体。

如果你基于此模板制作了自己的公开模板，欢迎保留出处说明。