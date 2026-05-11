# -*- coding: utf-8 -*-
"""
Hexo博客管理工具
"""

import os
import subprocess
import re
import hashlib
import shutil
import urllib.request
import urllib.error
import time
from datetime import datetime

# 博客根目录
BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
# 文章目录
POSTS_DIR = os.path.join(BLOG_DIR, "source", "_posts")
# Typora路径
TYPORA_PATH = r"D:\Typora\Typora.exe"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def select_menu(title, options, show_back=True):
    """
    交互式选择菜单
    返回选中的索引，-1表示返回/退出
    """
    if os.name == "nt":
        import msvcrt
    else:
        import sys, tty, termios
    
    if show_back:
        options = list(options) + ["返回"]
    
    current = 0
    
    while True:
        clear_screen()
        print("=" * 50)
        print(f"  {title}")
        print("=" * 50)
        print()
        
        for i, opt in enumerate(options):
            if i == current:
                print(f"  > {opt}")
            else:
                print(f"    {opt}")
        
        print()
        print("-" * 50)
        print("  上/下键选择，回车确认，Esc返回")
        
        # 读取按键
        if os.name == "nt":
            key = msvcrt.getch()
            if key == b'\xe0':  # 方向键前缀
                key = msvcrt.getch()
                if key == b'H':  # 上
                    current = (current - 1) % len(options)
                elif key == b'P':  # 下
                    current = (current + 1) % len(options)
            elif key == b'\r':  # 回车
                if show_back and current == len(options) - 1:
                    return -1
                return current
            elif key == b'q' or key == b'\x1b':  # q或ESC
                return -1
        else:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
                if key == '\x1b':
                    sys.stdin.read(1)
                    arrow = sys.stdin.read(1)
                    if arrow == 'A':  # 上
                        current = (current - 1) % len(options)
                    elif arrow == 'B':  # 下
                        current = (current + 1) % len(options)
                elif key == '\r' or key == '\n':
                    if show_back and current == len(options) - 1:
                        return -1
                    return current
                elif key == 'q':
                    return -1
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)


def run_command(cmd):
    """执行命令并返回输出"""
    print(f"\n执行: {cmd}\n")
    print("-" * 50)
    
    process = subprocess.Popen(
        cmd,
        shell=True,
        cwd=BLOG_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    
    output = ""
    for line in process.stdout:
        print(line, end="")
        output += line
    
    process.wait()
    return process.returncode == 0, output


def open_with_typora(filepath):
    """用Typora打开文件"""
    if os.path.exists(TYPORA_PATH):
        try:
            # Windows下使用DETACHED_PROCESS标志使子进程独立
            creationflags = 0
            if os.name == "nt":
                creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            
            subprocess.Popen(
                [TYPORA_PATH, filepath],
                creationflags=creationflags,
                close_fds=True,
                shell=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"\n已用Typora打开")
        except Exception as e:
            print(f"\nTypora启动失败: {e}")
            try:
                os.startfile(filepath)
                print(f"已尝试用默认程序打开")
            except:
                pass
    else:
        try:
            os.startfile(filepath)
            print(f"\n已用默认程序打开")
        except:
            print(f"\n打开失败，请手动打开: {filepath}")


def _file_hash(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def normalize_images_in_post(md_path):
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return False, 0
    
    post_name = os.path.splitext(os.path.basename(md_path))[0]
    asset_dir = os.path.join(POSTS_DIR, post_name)
    copied_count = 0
    
    def repl(match):
        nonlocal copied_count
        alt_text = match.group(1)
        raw = match.group(2).strip()
        title = ""
        
        title_match = re.match(r'([^"\']+?)\s+(".*"|\\\'.*\\\')$', raw)
        if title_match:
            raw = title_match.group(1).strip()
            title = " " + title_match.group(2)
        
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1].strip()
        
        lower = raw.lower()
        if lower.startswith(("http://", "https://", "data:")):
            return match.group(0)
        if lower.startswith(("#", "/", "./", "../")):
            return match.group(0)
        
        path = raw
        if lower.startswith("file:///"):
            path = path[8:]
        elif lower.startswith("file://"):
            path = path[7:]
        
        if re.match(r"^[a-zA-Z]:[\\/]", path) is None:
            return match.group(0)
        
        path = path.replace("/", os.sep)
        if not os.path.exists(path):
            return match.group(0)
        
        os.makedirs(asset_dir, exist_ok=True)
        filename = os.path.basename(path)
        dest_path = os.path.join(asset_dir, filename)
        
        if os.path.exists(dest_path):
            if _file_hash(dest_path) != _file_hash(path):
                base, ext = os.path.splitext(filename)
                filename = f"{base}-{_file_hash(path)[:8]}{ext}"
                dest_path = os.path.join(asset_dir, filename)
        
        if not os.path.exists(dest_path):
            shutil.copy2(path, dest_path)
            copied_count += 1
        
        rel = f"{post_name}/{filename}".replace("\\", "/")
        return f"![{alt_text}]({rel}{title})"
    
    new_content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, content)
    if new_content != content:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True, copied_count
    
    return False, copied_count


def normalize_all_posts_images():
    if not os.path.exists(POSTS_DIR):
        return 0, 0
    
    updated_posts = 0
    total_copied = 0
    
    for f in os.listdir(POSTS_DIR):
        if f.endswith(".md"):
            changed, copied = normalize_images_in_post(os.path.join(POSTS_DIR, f))
            if changed:
                updated_posts += 1
            total_copied += copied
    
    if updated_posts or total_copied:
        print(f"\n已处理图片: 更新{updated_posts}篇，复制{total_copied}张")
    
    return updated_posts, total_copied


# 需要下载的外部图片域名列表
EXTERNAL_IMAGE_DOMAINS = [
    "i-blog.csdnimg.cn",
]


# 外部图片存储在 source/images/ 下，Hexo 会自动加 root 前缀
IMAGES_DIR = os.path.join(BLOG_DIR, "source", "images")


def download_external_images_in_post(md_path):
    """下载文章中的外部图片到 source/images/，并替换为根相对路径"""
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"  读取失败 {os.path.basename(md_path)}: {e}")
        return False, 0

    downloaded = 0
    replaced_external = 0

    # --- 第一步：下载外部图片（http 链接） ---
    http_pattern = re.compile(
        r'!\[([^\]]*)\]\(((https?://[^\)]+))\)'
        r'|<img[^>]+src="((https?://[^"]+))"[^>]*>'
    )

    def need_download(url):
        for domain in EXTERNAL_IMAGE_DOMAINS:
            if domain in url:
                return True
        return False

    # 收集所有需要下载的外部图片
    http_replacements = []
    for m in http_pattern.finditer(content):
        url = m.group(2) or m.group(4)
        if not url or not need_download(url):
            continue

        filename = url.rsplit("/", 1)[-1]
        filename = filename.split("?")[0]  # 去掉URL参数
        save_path = os.path.join(IMAGES_DIR, filename)

        if not os.path.exists(save_path):
            os.makedirs(IMAGES_DIR, exist_ok=True)
            print(f"    下载: {filename}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://blog.csdn.net/",
            }
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                with open(save_path, "wb") as f:
                    f.write(data)
                downloaded += 1
                time.sleep(0.3)
            except Exception as e:
                print(f"    [失败] {filename}: {e}")
                continue

        local_path = f"/images/{filename}"
        http_replacements.append((m.start(), m.end(), local_path))
        replaced_external += 1

    # 倒序替换外部链接
    for start, end, local_path in reversed(http_replacements):
        old_segment = content[start:end]
        new_segment = re.sub(
            r'\(https?://[^\)]+\)',
            f"({local_path})",
            old_segment,
            count=1,
        )
        new_segment = re.sub(
            r'src="https?://[^"]+"',
            f'src="{local_path}"',
            new_segment,
            count=1,
        )
        content = content[:start] + new_segment + content[end:]

    # --- 第二步：补修纯文件名（之前已下载但路径不对的情况） ---
    # 只匹配纯文件名（不含路径分隔符，不含冒号），避免误伤 C:\Windows 这类绝对路径
    bare_pattern = re.compile(r'!\[([^\]]*)\]\(([\w.+-]+\.(png|jpe?g|gif|svg|webp|bmp))\)')
    bare_replacements = []
    for m in bare_pattern.finditer(content):
        filename = m.group(2)
        if not os.path.exists(os.path.join(IMAGES_DIR, filename)):
            continue
        # 排除绝对路径或路径特征（首字符不是 `\w` 就不是纯文件名）
        if re.match(r'^[\w]', filename) is None or ":" in filename or "\\" in filename:
            continue
        local_path = f"/images/{filename}"
        bare_replacements.append((m.start(), m.end(), m.group(1), local_path))

    for start, end, alt, local_path in reversed(bare_replacements):
        content = content[:start] + f"![{alt}]({local_path})" + content[end:]

    replaced_fix = len(bare_replacements)
    changed = replaced_external > 0 or replaced_fix > 0

    if changed:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)

    parts = []
    if downloaded:
        parts.append(f"下载 {downloaded} 张")
    if replaced_external:
        parts.append(f"替换 {replaced_external} 张外链")
    if replaced_fix:
        parts.append(f"修正 {replaced_fix} 张路径")
    if parts:
        print(f"  {os.path.basename(md_path)}: {', '.join(parts)}")

    return changed, replaced_external + replaced_fix


def download_all_external_images():
    """扫描所有文章，下载外部图片并替换链接"""
    if not os.path.exists(POSTS_DIR):
        return 0

    total = 0
    print("\n检查外部图片...")
    for f in sorted(os.listdir(POSTS_DIR)):
        if f.endswith(".md"):
            _, count = download_external_images_in_post(os.path.join(POSTS_DIR, f))
            total += count

    if total:
        print(f"共处理 {total} 张外部图片\n")
    else:
        print("  无需处理\n")
    return total


def write_blog():
    """写博客"""
    clear_screen()
    print("=" * 50)
    print("  写博客")
    print("=" * 50)
    print()
    print("  直接回车返回上一级")
    print()
    
    title = input("  请输入博客标题: ").strip()
    
    if not title:
        return
    
    print(f"\n  正在创建: {title}")
    success, output = run_command(f'npx hexo new post "{title}"')
    
    if not success:
        print("\n创建失败！")
        input("\n按回车键继续...")
        return
    
    # 从输出中提取实际创建的文件路径
    match = re.search(r'Created:\s*(.+\.md)', output)
    if match:
        md_file = match.group(1).strip()
        if os.path.exists(md_file):
            print(f"\n文章已创建: {md_file}")
            open_with_typora(md_file)
            input("\n按回车键继续...")
            return
    
    # 备用：查找最近创建的文件（5秒内）
    import time
    now = time.time()
    for f in os.listdir(POSTS_DIR):
        if f.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, f)
            if now - os.path.getmtime(filepath) < 5:
                print(f"\n文章已创建: {filepath}")
                open_with_typora(filepath)
                input("\n按回车键继续...")
                return
    
    print(f"\n文章文件未找到")
    input("\n按回车键继续...")


def deploy_blog():
    """推送部署"""
    clear_screen()
    print("=" * 50)
    print("  推送部署")
    print("=" * 50)
    download_all_external_images()
    normalize_all_posts_images()
    
    confirm = select_menu("确认推送到GitHub触发部署？", ["确认部署", "取消"], show_back=False)

    if confirm != 0:
        return

    clear_screen()
    print("=" * 50)
    print("  正在部署...")
    print("=" * 50)

    from datetime import date
    today = date.today().isoformat()

    steps = [
        ("清理旧文件", "npx hexo clean"),
        ("生成静态文件", "npx hexo generate"),
        ("拉取远程最新代码", "git pull --rebase --autostash origin master"),
        ("暂存所有变更", "git add ."),
        ("提交代码", f'git commit -m "update: 博客更新 {today}"'),
        ("推送到GitHub", "git push origin master"),
    ]

    for i, (name, cmd) in enumerate(steps, 1):
        print(f"\n[{i}/{len(steps)}] {name}...")
        success, output = run_command(cmd)
        if not success:
            # git commit 没东西可提交不算失败
            if "nothing to commit" in output or "nothing added" in output:
                print("  无需提交，继续推送...")
                continue
            print(f"\n{name}失败！")
            input("\n按回车键继续...")
            return

    print("\n" + "=" * 50)
    print("  部署成功！")
    print("  https://blog.xyu1.asia")
    print("=" * 50)
    print("  Cloudflare Pages 将在几分钟内自动构建部署")
    print("=" * 50)
    input("\n按回车键继续...")


def preview_blog():
    """本地预览"""
    clear_screen()
    print("=" * 50)
    print("  本地预览")
    print("=" * 50)
    print("\n  启动后访问: http://localhost:4000")
    print("  按 Ctrl+C 停止\n")
    download_all_external_images()
    normalize_all_posts_images()
    
    try:
        run_command("npx hexo server")
    except KeyboardInterrupt:
        print("\n服务器已停止")
    
    input("\n按回车键继续...")


def list_posts():
    """查看文章列表"""
    if not os.path.exists(POSTS_DIR):
        clear_screen()
        print("\n文章目录不存在")
        input("\n按回车键继续...")
        return
    
    try:
        posts = sorted(
            [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")],
            key=lambda x: os.path.getmtime(os.path.join(POSTS_DIR, x)),
            reverse=True
        )
    except Exception as e:
        clear_screen()
        print(f"\n读取失败: {e}")
        input("\n按回车键继续...")
        return
    
    if not posts:
        clear_screen()
        print("\n暂无文章")
        input("\n按回车键继续...")
        return
    
    # 构建显示选项
    options = []
    for post in posts:
        filepath = os.path.join(POSTS_DIR, post)
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        name = post[:-3]  # 去掉.md
        options.append(f"{name}  [{mtime.strftime('%m-%d %H:%M')}]")
    
    while True:
        idx = select_menu(f"文章列表 ({len(posts)}篇)", options)
        
        if idx == -1:
            return
        
        filepath = os.path.join(POSTS_DIR, posts[idx])
        open_with_typora(filepath)
        input("\n按回车键继续...")


def main():
    """主程序"""
    os.chdir(BLOG_DIR)
    
    menu_options = [
        "写博客",
        "文章列表",
        "本地预览",
        "推送部署",
        "退出",
    ]
    
    while True:
        idx = select_menu("Hexo博客管理", menu_options, show_back=False)
        
        if idx == 0:
            write_blog()
        elif idx == 1:
            list_posts()
        elif idx == 2:
            preview_blog()
        elif idx == 3:
            deploy_blog()
        elif idx == 4 or idx == -1:
            clear_screen()
            print("\n  再见！\n")
            break


if __name__ == "__main__":
    main()
