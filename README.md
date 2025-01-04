# Bili Downloader Pro

[English](README.md) | [中文说明](README_zh.md)

Bili Downloader Pro is a powerful, automated tool for batch downloading video content from Bilibili based on [BBDown](https://github.com/nilaoda/BBDown). It supports downloading videos, audio, subtitles, and danmaku (comments) from multiple creators simultaneously using an Excel file for input management.

### Features

- Batch download videos from multiple Bilibili creators
- Support for downloading:
  - Video files (with aria2 support for faster downloads)
  - Audio-only files
  - Subtitles (including AI-generated subtitles)
  - Danmaku (comment overlays)
  - Video cover images
- Excel-based user management
- Detailed logging system
- Docker support for easy deployment
- Optional email notifications upon task completion

**Attention**: Automated Email Sending Feature relies on the **Resend** module. Please follow the steps below to configure and enable the email sending functionality:

1. **Visit Resend**  
   Go to the [Resend](https://resend.com) website, register, and complete the necessary setup.

2. **Obtain API Key**  
   Retrieve your `API Key` from the Resend console.

3. **Configure the Code**  
   Insert the obtained `API Key` into the appropriate location in the code, and uncomment the relevant code sections to enable the email sending feature.

Once the above steps are completed, the automated email sending feature will be ready for use.

### Prerequisites

- Python
- BBDown
- aria2 (optional, for faster downloads)

### Quick Start

#### 1. Clone the repository:
```bash
git clone https://github.com/fangd123/bili-downloader-pro.git
cd Bili Downloader Pro
```

#### 2 Using Docker:

The `Dockerfiles` directory contains image build scripts for different system architectures. You can build the required images based on your needs.

**Usage:**

1. Navigate to the `Dockerfiles` directory.
2. Select the build script corresponding to your target system architecture.
3. Run the build command to generate the image.

**Example:**

```bash
cd Dockerfiles
docker build -t <image-name> -f <Dockerfile-path> .
```

Replace `<image-name>` and `<Dockerfile-path>` with the appropriate values as needed.



#### 3. Or run directly with Python:
```bash
pip install -r requirements.txt
python main.py
```

### Configuration

1. Prepare your Excel file (`list.xlsx`) with the following format:

| UID | Username |
|-----|----------|
| 12345 | creator1 |
| 67890 | creator2 |

2. (Optional) Configure email notifications in `main.py`:
```python
resend.api_key = 'YOUR_RESEND_API_KEY'
"to": "your-email@example.com"
```

### License

MIT License