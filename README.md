# XYu1230的技术博客

这是一个基于 Hexo 框架搭建的个人技术博客，使用 Butterfly 主题。

## 博客信息

- **作者**: XYu1230
- **主题**: Butterfly
- **框架**: Hexo 8.1.1
- **GitHub**: [https://github.com/XYu1230](https://github.com/XYu1230)
- **邮箱**: xyu1230@foxmail.com

## 技术栈

- **静态站点生成器**: Hexo 8.0+
- **模板引擎**: Pug
- **样式语言**: Stylus
- **Markdown 解析**: hexo-renderer-marked
- **主题**: hexo-theme-butterfly

## 项目结构

```
my-blog/
├── source/              # 源文件目录
│   ├── _posts/         # 博客文章
│   ├── about/          # 关于页面
│   ├── tags/           # 标签页面
│   └── categories/     # 分类页面
├── themes/             # 主题目录
│   └── hexo-theme-butterfly/
├── scaffolds/          # 文章模板
├── _config.yml         # 站点配置
└── package.json        # 依赖配置
```

## 本地开发

### 安装依赖

```bash
npm install
```

### 启动本地服务器

```bash
hexo server
```

访问 http://localhost:4000 查看博客。

### 新建文章

```bash
hexo new "文章标题"
```

### 清理缓存

```bash
hexo clean
```

### 生成静态文件

```bash
hexo generate
```

## 主题配置

本博客使用了自定义的配色方案：

- **主背景色**: #fcfcf8 (米白色)
- **主题色**: #4a5b6c (深灰蓝)
- **强调色**: #6c7b8b (中灰蓝)

主要特性：
- 简约大方的设计风格
- 响应式布局
- 支持暗黑模式
- 实时运行时间显示
- 社交媒体链接集成

## 博客理念

> 热爱技术，持续学习  
> 行则将至  
> 代码改变世界  
> nobody is nobody

## 许可证

Copyright © 2026 XYu1230. All Rights Reserved.
