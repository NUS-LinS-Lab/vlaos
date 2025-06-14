import imageio
import cv2
import numpy as np
import os

# 输入输出路径
input_path = "basketball.mp4"
output_path = "new_basketball.mp4"

def process_video(input_path, output_path):
    # 打开视频读取器
    reader = imageio.get_reader(input_path)
    fps = reader.get_meta_data()["fps"]
    size = reader.get_meta_data()["size"]
    width, height = size
    print(f"视频分辨率: {width}x{height}, 帧率: {fps}")

    # 标题带参数
    h_title = 32
    w1, w2, w3, w4 = 224, 448, 224, 224
    x_positions = [0, w1, w1 + w2, w1 + w2 + w3]
    titles = ["observation", "language reasoning", "visual reasoning", "goal image"]

    # 打开视频读取器
    reader = imageio.get_reader(input_path)
    fps = reader.get_meta_data()["fps"]
    width, height = reader.get_meta_data()["size"]

    # 标题带参数
    h_title = 32
    w1, w2, w3, w4 = 224, 448, 224, 224
    x_positions = [0, w1, w1 + w2, w1 + w2 + w3]
    titles = ["observation", "language reasoning", "visual reasoning", "goal image"]

    # 打开视频写入器
    writer = imageio.get_writer(output_path, fps=fps)

    # 字体设置
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_color = (0, 0, 0)  # 黑色文字
    thickness = 2

    for frame in reader:
        # 转为 BGR（OpenCV 格式）
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 覆盖标题带为纯白色
        frame_bgr[0:h_title, :] = 255  # numpy broadcasting

        # 写入标题文字
        for i, (x, title) in enumerate(zip(x_positions, titles)):
            region_width = [w1, w2, w3, w4][i]
            text_size = cv2.getTextSize(title, font, font_scale, thickness)[0]
            text_x = x + (region_width - text_size[0]) // 2
            text_y = (h_title + text_size[1]) // 2
            cv2.putText(frame_bgr, title, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)

        # 转回 RGB 并写入新帧
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        writer.append_data(frame_rgb)

    reader.close()
    writer.close()

def process_all_videos(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(".mp4") and not filename.endswith("_labeled.mp4"):
                input_path = os.path.join(dirpath, filename)
                output_name = os.path.splitext(filename)[0] + "_labeled.mp4"
                output_path = os.path.join(dirpath, output_name)
                print(f"Processing: {input_path}")
                process_video(input_path, output_path)
                print(f"Saved to: {output_path}")


# 指定根目录
if __name__ == "__main__":
    folder_path = "media/videos"  # 🔁 替换为你的视频根目录路径
    process_all_videos(folder_path)