---
title: hexo快速入门-搭建属于自己的博客
date: 2026-01-17 22:01:49
tags:
  - Hexo
  - 博客
categories:
  - 教程
---

## Hexo 快速入门：搭建属于自己的博客（从 0 到上线）

Hexo 是一个基于 Node.js 的静态博客框架：你写 Markdown，它帮你生成静态网页，然后把这些网页部署到 GitHub Pages、Vercel、Netlify 或服务器上即可访问。优点是：**快、轻、可定制、维护成本低**。

### 你将完成什么

- 本地初始化 Hexo 博客
- 选择并配置主题
- 写第一篇文章
- 部署上线（以 GitHub Pages 为例）
- 常见问题与优化建议

------

## 准备环境

### 安装 Node.js

Hexo 依赖 Node.js。建议安装 **LTS 版本**。

安装后验证：

```bash
node -v
npm -v
```

### 安装 Git（用于部署）

验证：

```bash
git -v
```

> Windows 用户推荐安装 Git for Windows，并用 Git Bash 执行命令更省心。

------

## 安装 Hexo 并创建博客项目

### 安装 Hexo CLI

```bash
npm install -g hexo-cli
hexo -v
```

### 初始化博客

选择一个目录，比如你的工作区：

```bash
mkdir my-blog
cd my-blog
hexo init
npm install
```

初始化完成后目录结构大概是：

- `source/`：文章、页面、资源
- `themes/`：主题
- `_config.yml`：站点配置
- `scaffolds/`：文章模板
- `package.json`：依赖管理

### 本地启动预览

```bash
hexo clean
hexo g
hexo s
```

浏览器打开：`http://localhost:4000`

------

## 配置博客基础信息

打开项目根目录的 `_config.yml`，重点改这些：

```yml
title: 你的博客标题
subtitle: 你的副标题（可选）
description: 你的网站描述（SEO用）
author: 你的名字
language: zh-CN
timezone: Asia/Shanghai
url: https://你的域名（部署后再填）
```

#### 常见建议

- `language` 用 `zh-CN` 对中文主题更友好
- `timezone` 尽量设置正确，否则文章时间可能乱

------

## 写你的第一篇文章

### 新建文章

```bash
hexo new "Hello Hexo"
```

会生成文件：`source/_posts/Hello-Hexo.md`

### 文章格式说明

打开文章你会看到类似：

```markdown
---
title: Hello Hexo
date: 2026-01-17 12:00:00
tags:
---

这里写正文，支持 Markdown。
```

你可以加 tags / categories：

```yml
tags:
  - Hexo
  - 博客
categories:
  - 技术
```

### 生成并预览

```bash
hexo clean
hexo g
hexo s
```

------

## 安装与更换主题（推荐做法）

Hexo 默认主题是 landscape，很多人会换成更好看的主题，例如：

- **Butterfly**（功能强、中文资料多）
- **Next**（经典、简洁）
- **Fluid**（中文友好、易配置）

### 通用换主题流程

以 `butterfly` 为例（假设你选择这个主题）：

```bash
cd my-blog
git clone https://github.com/jerryc127/hexo-theme-butterfly.git themes/butterfly
```

然后修改站点 `_config.yml`：

```yml
theme: butterfly
```

重启预览：

```bash
hexo clean
hexo g
hexo s
```

> 不同主题会有自己的配置文件，一般在 `themes/主题名/_config.yml`。更推荐使用主题支持的“配置覆盖”（例如把主题配置复制到根目录并命名为 `_config.butterfly.yml`，避免升级主题后配置被覆盖）。

------

## 部署上线（GitHub Pages 方式）

这是最常见的免费方案：仓库 + 自动托管。

### 创建 GitHub 仓库

在 GitHub 新建仓库：

- 如果你想使用默认域名：仓库名建议为 `username.github.io`
- 或者任意名字也可以（路径会不一样）

假设你的 GitHub 用户名是 `xyu12301`，仓库名是：

- `xyu12301.github.io`

### 安装部署插件

在博客根目录：

```bash
npm install hexo-deployer-git --save
```

### 配置部署信息

编辑根目录 `_config.yml`，添加：

```yml
deploy:
  type: git
  repo: https://github.com/你的用户名/你的仓库名.git
  branch: main
```

如果你的默认分支是 `master` 就写 `master`。

### 配置站点 url

同一个 `_config.yml`：

```yml
url: https://你的用户名.github.io
```

### 一键部署

```bash
hexo clean
hexo g
hexo d
```

部署成功后访问：

- `https://你的用户名.github.io`

------

## 绑定自定义域名（可选但推荐）

### 购买域名后做解析

在域名控制台添加解析：

- `CNAME`：`www` -> `你的用户名.github.io`
- 或 `A`：根域名 `@` 指向 GitHub Pages 的 IP（GitHub 文档里会给）

### GitHub Pages 设置

仓库 Settings -> Pages：

- Custom domain 填你的域名
- 勾选 HTTPS

### Hexo 侧配置

在 `source/` 目录创建 `CNAME` 文件（无后缀）：
内容为你的域名，例如：

```
www.example.com
```

然后重新部署：

```bash
hexo clean
hexo g
hexo d
```

------

## 常用命令速查

```bash
hexo new "文章标题"   # 新建文章
hexo g               # 生成静态文件
hexo s               # 本地预览
hexo d               # 部署
hexo clean           # 清理缓存/生成文件
```

快捷组合：

```bash
hexo clean && hexo g && hexo s
hexo clean && hexo g && hexo d
```

------

## 常见问题（排坑）

### 端口被占用

换端口

```bash
hexo s -p 5000
```

### 部署失败：权限/鉴权问题

优先使用 SSH：

1. 配 SSH key 到 GitHub
2. repo 改为：

```yml
repo: git@github.com:用户名/仓库名.git
```

### 修改配置不生效

每次改配置/主题后建议：

```bash
hexo clean
hexo g
hexo s
```

### 图片怎么放？

常见方式：

- 放 `source/images/xxx.png`，文章中用 `/images/xxx.png`
- 或使用主题自带的资源管理方式
- 或用图床（GitHub、OSS、Cloudflare R2）
