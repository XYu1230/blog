# Hexo 博客迁移到 Cloudflare Pages 实施计划

## 上下文

当前博客部署在 GitHub Pages (`https://xyu1230.github.io/blog`)，访问有时不稳定。用户希望迁移到 Cloudflare Pages 以提高访问稳定性，并使用自定义域名 `xyu1.asia`（已绑定到 Cloudflare）。

## 实施方案

### 策略
使用 Cloudflare Pages 的 GitHub 集成功能，保持现有 git 工作流，实现自动构建部署。

### 核心决策
1. **路径结构**：从 `/blog/` 迁移到根路径 `/`（使用自定义域名更简洁）
2. **部署方式**：GitHub 集成自动部署
3. **并行运行**：初期保留 GitHub Pages 作为备份

---

## 实施步骤

### 步骤 1：修改配置文件

**文件**：`_config.yml`

修改内容：
```yaml
# 原配置
url: https://xyu1230.github.io/blog
root: /blog/

# 改为
url: https://blog.xyu1.asia
root: /
```

---

### 步骤 2：创建 Node.js 版本配置（推荐）

**新建文件**：`.nvmrc`
```
22.16.0
```

或者稍后在 Cloudflare Pages 设置中添加环境变量 `NODE_VERSION = 22.16.0`

---

### 步骤 3：Cloudflare Pages 创建项目

1. 登录 https://dash.cloudflare.com
2. 导航到 **Workers & Pages** → **Pages** → **Create a project**
3. 选择 **Connect to Git** → **GitHub** 授权
4. 选择仓库：`XYu1230/blog`
5. 配置构建设置：
   - **Project name**: my-blog（或自定义）
   - **Production branch**: master
   - **Build command**: `npm run build`
   - **Build output directory**: `public`
6. 点击 **Save and Deploy**

---

### 步骤 4：绑定自定义域名

1. 在 Cloudflare Pages 项目页面，点击 **Custom domains**
2. 点击 **Set up a custom domain**
3. 输入子域名：`blog.xyu1.asia`
4. 系统会自动配置 DNS（CNAME 指向 pages.dev）
5. 等待域名状态变为 "Active"

---

### 步骤 5：验证部署

1. 访问 `https://blog.xyu1.asia` 检查主页是否正常
2. 测试导航链接：首页、归档、标签、分类
3. 检查文章内容是否完整
4. 验证图片、CSS、JS 是否正常加载
5. 确认 HTTPS 正常工作（锁图标）

---

## 关键文件

| 文件路径 | 操作 |
|----------|------|
| `_config.yml` | 修改 url 和 root 配置 |
| `.nvmrc` | 新建，指定 Node.js 版本 |
| `package.json` | 无需修改（已有构建脚本） |
| `.github/dependabot.yml` | 无需修改（继续正常工作） |

---

## URL 变更说明

| 旧 URL | 新 URL |
|--------|--------|
| `https://xyu1230.github.io/blog/` | `https://blog.xyu1.asia/` |
| `https://xyu1230.github.io/blog/2026/01/17/post-title/` | `https://blog.xyu1.asia/2026/01/17/post-title/` |

**注意**：URL 从子路径 `/blog/` 变为根路径，但使用子域名 `blog.xyu1.asia`。

---

## 回滚方案

如果迁移后出现问题，可以：

1. **快速回滚**：暂时访问 `https://xyu1230.github.io/blog`（GitHub Pages 继续运行）
2. **DNS 切换**：在 Cloudflare DNS 中将 `xyu1.asia` 的 CNAME 指向 `xyu1230.github.io`
3. **完全回滚**：恢复 `_config.yml` 中的原始配置

---

## 预期收益

- ✅ 访问稳定性提升（Cloudflare 全球 CDN）
- ✅ 加载速度更快
- ✅ 内置 Web Analytics
- ✅ 自动 SSL/TLS 证书
- ✅ 保持现有 git 工作流不变
