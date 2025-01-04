# Bili Downloader Pro

[English](README.md) | [中文说明](README_zh.md)

Bili Downloader Pro 是一个基于 [BBDown](https://github.com/nilaoda/BBDown) 的强大的B站视频批量下载工具，支持通过Excel文件管理UP主列表，自动下载视频内容、音频、字幕和弹幕。

### 功能特点

- 批量下载多个UP主的视频
- 支持下载：
  - 视频文件（支持aria2加速下载）
  - 仅音频文件
  - 字幕（包括AI生成的字幕）
  - 弹幕
  - 视频封面
- 基于Excel的用户管理
- 详细的日志系统
- Docker容器支持
- 可选的任务完成邮件通知

**注**：自动发送邮件功能依赖于 **Resend** 模块。请按照以下步骤配置并启用邮件发送功能：

1. **访问 Resend**  
   前往 [Resend](https://resend.com) 官网，注册并完成相关配置。

2. **获取 API Key**  
   在 Resend 控制台中获取您的 `API Key`。

3. **配置代码**  
   将获取到的 `API Key` 填入代码中对应的位置，并取消相关代码的注释以启用邮件发送功能。

完成上述步骤后，自动发送邮件功能即可正常使用。

### 环境要求

- Python
- BBDown
- aria2（可选，用于加速下载）

### 快速开始

#### 1. 克隆仓库：
```bash
git clone https://github.com/fangd123/bili-downloader-pro.git
cd Bili Downloader Pro
```

#### 2. 使用Docker：

`Dockerfiles` 目录包含针对不同系统架构的镜像构建脚本，您可以根据需求自行构建所需的镜像。

**使用方法：**

1. 进入 `Dockerfiles` 目录。
2. 选择与目标系统架构对应的构建脚本。
3. 运行构建命令以生成镜像。

**示例：**

```bash
cd Dockerfiles
docker build -t <镜像名称> -f <Dockerfile路径> .
```

请根据实际情况替换 `<镜像名称>` 和 `<Dockerfile路径>`。


#### 3. 或直接使用Python运行：
```bash
pip install -r requirements.txt
python main.py
```

### 配置说明

1. 准备Excel文件（`list.xlsx`），格式如下：

| UID | 用户名 |
|-----|--------|
| 12345 | UP主1 |
| 67890 | UP主2 |

2. （可选）在`main.py`中配置邮件通知：
```python
resend.api_key = 'YOUR_RESEND_API_KEY'
"to": "your-email@example.com"
```

### 开源协议

MIT License