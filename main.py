import openpyxl
import subprocess
import os
from datetime import datetime
from loguru import logger
#import resend
from pathlib import Path
import time

# 配置日志
log_path = "logs"
if not os.path.exists(log_path):
    os.makedirs(log_path)

logger.add(
    os.path.join(log_path, "download_{time}.log"),
    rotation="1 day",
    retention="7 days",
    level="INFO"
)


class BilibiliDownloader:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.start_time = datetime.now()
        self.failed_videos = []
        self.total_videos = 0
        self.success_count = 0

        # 创建失败记录文件
        self.failed_file = f"failed_downloads_{self.start_time.strftime('%Y%m%d_%H%M%S')}.txt"

    def get_user_videos(self, uid, username):
        """获取用户的所有视频链接"""
        try:
            cmd = f'BBDown --config-file BBDown.config https://space.bilibili.com/{uid}'
            subprocess.run(cmd, shell=True, check=False)

            # 检查是否生成了视频列表文件
            video_list_file = f"{username}的投稿视频.txt"
            if not os.path.exists(video_list_file):
                logger.error(f"Failed to generate video list for user {username} (UID: {uid})")
                return []

            with open(video_list_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]

        except subprocess.CalledProcessError as e:
            logger.error(f"Error getting videos for user {username} (UID: {uid}): {str(e)}")
            return []

    def download_video_resources(self, url):
        """下载视频、字幕和弹幕"""
        try:
            # 下载音频
            cmd_video = f'BBDown --audio-only --config-file BBDown.config {url}'
            subprocess.run(cmd_video, shell=True, check=True)
            # 下载视频
            cmd_video = f'BBDown -aria2 --config-file BBDown.config {url}'
            subprocess.run(cmd_video, shell=True, check=True)

            # 下载字幕
            cmd_subtitle = f'BBDown --sub-only --skip-ai false --config-file BBDown.config {url}'
            subprocess.run(cmd_subtitle, shell=True, check=True)

            # 下载弹幕
            cmd_danmaku = f'BBDown --danmaku-only -dd --cover-only --config-file BBDown.config {url}'
            subprocess.run(cmd_danmaku, shell=True, check=True)

            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading resources for URL {url}: {str(e)}")
            self.failed_videos.append(url)
            with open(self.failed_file, 'a', encoding='utf-8') as f:
                f.write(f"{url}\n")
            return False

    def send_completion_email(self):
        """发送完成通知邮件"""
        end_time = datetime.now()
        duration = end_time - self.start_time

        email_body = f"""
        下载任务完成！

        开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
        结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
        总耗时: {duration}

        总计视频数: {self.total_videos}
        成功下载: {self.success_count}
        失败数量: {len(self.failed_videos)}
        """

        resend.api_key = 'YOUR_RESEND_API_KEY'

        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": "your-email@example.com",  # 替换为你的邮箱
                "subject": "Bilibili视频下载任务完成通知",
                "text": email_body
            })
            logger.info("Completion email sent successfully")
        except Exception as e:
            logger.error(f"Failed to send completion email: {str(e)}")

    def run(self):
        """运行下载任务"""
        try:
            # 读取Excel文件
            workbook = openpyxl.load_workbook(self.excel_path)
            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):  # 假设第一行是标题行
                uid = row[0]  # 假设UID在第一列
                username = row[1]  # 假设用户名在第二列

                logger.info(f"Processing user: {username} (UID: {uid})")

                # 获取用户视频列表
                videos = self.get_user_videos(uid, username)
                self.total_videos += len(videos)

                # 下载每个视频的资源
                for video_url in videos:
                    logger.info(f"Downloading resources for video: {video_url}")
                    if self.download_video_resources(video_url):
                        self.success_count += 1
                    time.sleep(1)  # 添加延迟以避免请求过于频繁

            # 发送完成通知邮件
            # self.send_completion_email()

        except Exception as e:
            logger.error(f"An error occurred during execution: {str(e)}")
            raise


if __name__ == "__main__":
    downloader = BilibiliDownloader("list.xlsx")  # 替换为你的Excel文件路径
    downloader.run()