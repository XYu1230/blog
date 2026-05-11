
'use strict';

/**
 * 修复 Hexo post_asset_folder 开启后图片路径问题
 * 
 * 问题描述：
 * 1. 开启 post_asset_folder: true 后，Typora 需要引用格式为 ![alt](文章名/图片.png) 才能预览
 * 2. Hexo 生成页面时，文章位于 /YYYY/MM/DD/文章名/，图片位于 /YYYY/MM/DD/文章名/图片.png
 * 3. 此时页面中的 ![alt](文章名/图片.png) 解析为 /YYYY/MM/DD/文章名/文章名/图片.png -> 404
 * 
 * 解决方案：
 * 在 Hexo 渲染前，将 ![alt](文章名/图片.png) 替换为 HTML 标签 <img src="{% asset_path 图片.png %}" alt="alt">
 * 使用 asset_path 标签可以正确解析 post_asset_folder 中的图片路径，且避免 Markdown 解析器的问题
 */

hexo.extend.filter.register('before_post_render', function(data) {
  if (!data.slug) return data; // 如果没有 slug 跳过

  // 获取文章的文件名（作为文件夹名）
  // data.slug 通常是 "文章标题"，但也可能是 "目录/文章标题"
  const slugParts = data.slug.split('/');
  const folderName = slugParts[slugParts.length - 1];

  // 构造正则：匹配 ![alt](Folder/filename) 或 ![alt](Folder/filename "title")
  // Typora 格式：![image-xxx](文章标题/image-xxx.png)
  const regex = new RegExp(`!\\[(.*?)\\]\\(${escapeRegExp(folderName)}[\\\\/](.*?)\\)`, 'g');
  
  data.content = data.content.replace(regex, function(match, alt, filename) {
    // filename 可能包含 title，如 "image.png \"title\""
    // 我们主要提取真实文件名
    let realFilename = filename;
    let title = alt; // 默认使用 alt 作为 title

    // 简单的处理：如果 filename 包含空格或引号，尝试提取
    // 这里假设用户主要是简单的图片引用
    const parts = filename.split(/\s+/);
    if (parts.length > 0) {
      realFilename = parts[0];
    }
    
    // 返回 HTML <img> 标签 + asset_path
    // 这样可以确保路径被正确解析为绝对路径
    return `<img src="{% asset_path ${realFilename} %}" alt="${alt}" title="${title}">`;
  });

  return data;
});

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
