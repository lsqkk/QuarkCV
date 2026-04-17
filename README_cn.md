# QuarkCV - 数据驱动的 XeLaTeX 简历模板

[EN](README.md) / 简体中文

[![XeLaTeX](https://img.shields.io/badge/Compiler-XeLaTeX-245C73?style=flat-square)](#快速开始)
[![Data Driven](https://img.shields.io/badge/Content-YAML%20Driven-4C8DA3?style=flat-square)](#为什么-quarkcv-好用)
[![Academic Demo](https://img.shields.io/badge/Demo-Academic%20Profile-6C8E7B?style=flat-square)](#这个仓库是什么)
[![Local First Avatar](https://img.shields.io/badge/Avatar-Local%20First-C59B6D?style=flat-square)](#头像逻辑)

一个精致、数据驱动的 XeLaTeX 学术简历模板，适用于 Academic CV、研究型 Resume 和作品集风格的一页简历。

QuarkCV 将结构化 YAML 转换成干净、现代、链接丰富的 PDF，同时保持“内容数据”和“排版系统”彼此分离。内置精致的学术 demo、可点击 PDF 链接、本地优先头像机制，以及清晰分离的内容层与排版层。

![QuarkCV Demo](Demo/resume_demo.png)

## 一眼看懂

- 公开 demo 仓库，默认使用虚构学术示例数据
- `Data/*.yml` 是唯一内容源
- `main.tex` 由结构化数据自动生成
- 头像采用“本地优先，远程兜底”的策略
- 联系方式、学校、项目、论文等链接都支持点击跳转
- 适合 Academic CV、研究型 Resume 和模板二次开发

## 为什么 QuarkCV 好用

- 数据优先。简历内容统一放在 `Data/*.yml`，而不是散落在 TeX 代码块中。
- 面向简历的字段设计。长篇档案型内容可以和 `resume_title`、`resume_summary`、`resume_highlights` 这类简历专用字段并存。
- 分层清晰。`Data/*.yml` 负责内容，`scripts/build_resume_data.py` 负责生成，`myresume.sty` 负责视觉样式。
- PDF 全链路可点击。邮箱、电话、主页、学校、项目、论文和本地文件链接都会生成为可点击链接。
- 开箱即用的 demo。仓库已经内置了一套完整的学术示例数据，克隆后就能直接看懂模板的能力边界。
- 稳妥的降级方案。头像加载遵循“本地优先、远程可选、默认字母占位”的策略，适合离线和公开 demo 场景。

## 工作方式

1. 编辑 `Data/` 中的数据文件。
2. 运行 `python scripts/build_resume_data.py`。
3. 脚本会直接生成 `main.tex`。
4. 使用 XeLaTeX 编译 `main.tex`。

在这个工作流里：

- `Data/*.yml` 是唯一的数据源
- `main.tex` 是自动生成的产物
- `myresume.sty` 是排版与视觉系统

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
│  ├─ avatar.png
│  └─ resume-avatar.*         # 使用远程头像时可选的缓存文件
├─ Demo/
│  └─ resume_demo.png
├─ Fonts/
├─ scripts/
│  └─ build_resume_data.py
├─ myresume.sty
├─ main.tex                   # 由脚本自动生成
├─ README.md
└─ README_cn.md
```

## 快速开始

### 1. 编辑数据

更新 `Data/` 下的 YAML 文件：

- `Data/_config.yml`：身份信息、主题色、联系方式、章节开关、展示数量、头像
- `Data/profile.yml`：个人简介、研究方向、技能
- `Data/education.yml`：教育经历和精简亮点
- `Data/project.yml`：项目条目、简历标题、简历摘要
- `Data/awards.yml`：奖项与简短说明
- `Data/publications.yml`：论文与对应链接

### 2. 生成 `main.tex`

```bash
python scripts/build_resume_data.py
```

### 3. 编译 PDF

```bash
xelatex main.tex
```

为了得到更稳定的最终输出，建议运行两次 XeLaTeX。

## Demo 数据设计理念

这个模板刻意把“档案型详细内容”和“简历型展示内容”区分开来。

以项目为例，你可以同时保留：

- `title`：完整项目名
- `description`：适合主页展示的长描述
- `resume_title`：适合放在简历上的短标题
- `resume_summary`：适合招聘者快速阅读的精简摘要

这个模式在模板里是统一的：

- `profile.yml` 使用 `resume_summary` 和 `resume_focus`
- `education.yml` 使用 `resume_summary` 和 `resume_highlights`
- `project.yml` 使用 `resume_title` 和 `resume_summary`

这样同一份数据既能支撑更完整的个人主页内容，也能生成更聚焦的简历输出。

## 头像逻辑

在 `Data/_config.yml` 中，你可以把 `avatar` 设置为：

- 本地相对路径，例如 `./Data/avatar.png`
- 远程 `http` / `https` 图片链接
- 留空

头像解析顺序如下：

1. 如果本地路径存在，优先直接使用本地文件。
2. 如果填写的是远程链接，则尝试下载并缓存到本地。
3. 如果以上都失败，则自动显示基于姓名首字母生成的默认字母头像。

这个逻辑可以保证模板在离线环境、公开 demo 仓库和真实个人使用场景下都比较稳。

## 可点击链接

生成后的 PDF 支持以下可点击链接：

- 邮箱
- 电话
- 个人主页
- GitHub
- Google Scholar
- CV 链接
- 学校和机构链接
- 项目链接
- 论文链接
- 本地文件，例如 PDF

## 适合谁使用

- 准备研究型简历的学生
- Ph.D. 申请者和研究生
- 想要更干净学术 CV 模板的研究人员
- 更喜欢结构化数据而不是手改 TeX 的工程师和创作者
- 希望维护一个可公开展示模板仓库的模板作者

## 亮点特性

- 结构化内容编写，支持简历专用精简字段
- 比传统 TeX 简历模板更干净的学术风格视觉
- 默认内置虚构学术人物数据，适合公开展示
- 生成流程稳定清晰，方便 fork 和二次扩展
- 对链接、章节、展示数量和头像行为都有合理默认值

## 可定制方向

- 修改 `theme.accent_color` 和 `theme.accent_soft_color`
- 调整 `list_preview_count` 以适配一页或两页布局
- 通过 `section_visibility` 控制章节显示
- 新增基于 YAML 的章节，例如实习、教学、学术服务、演讲、基金等
- 在 `myresume.sty` 中继续微调字体、间距和整体风格

## 推荐工作流

- 把 `Data/*.yml` 当作内容层
- 把 `scripts/build_resume_data.py` 当作生成器
- 把 `main.tex` 当作自动生成的输出
- 把 `myresume.sty` 当作设计层

这种分层方式能让项目持续扩展，同时不会把 `main.tex` 变成难以维护的大杂烩。

## 注意事项

- 请使用 XeLaTeX 编译。
- `main.tex` 是自动生成的，手动修改会被覆盖。
- 如果你更新了头像路径或本地文件链接，请先重新生成再编译。
- 当前仓库默认展示的人物信息是虚构示例，仅用于模板 demo。

## 常见问题

### 可以直接拿来做我自己的真实简历吗？

可以。把 `Data/*.yml` 中的 demo 数据替换成你自己的内容，重新生成 `main.tex` 并编译即可。

### 我需要直接修改 TeX 吗？

大多数情况下不需要。通常只需要编辑 `Data/*.yml`。如果想进一步改视觉风格，再去调整 `myresume.sty`。

### 可以只使用本地头像吗？

可以，而且这是最适合公开 demo 仓库和稳定构建的方式。

### 可以扩展新的章节吗？

可以。当前结构本来就比较适合继续扩展，例如增加实习、教学、演讲、基金、学术服务等 YAML 驱动章节。

## 路线图

- 增加更多 demo 变体，例如学术版、工业版、混合版
- 提供更紧凑和更舒展的布局预设
- 增加教学、基金、演讲等更丰富的章节 schema
- 完善截图和展示资源，方便模板主页展示

## 开源许可

你可以自由使用、修改和二次创作这个模板，用于个人简历、学术 CV、作品集简历以及衍生模板。

如果你公开发布了基于此模板的 fork 或衍生模板，欢迎保留出处说明。
