# free_song_list
# 喜马歌单生成工具说明文档

这个工具用于生成歌单图片，通过读取CSV文件中的歌曲数据，对其进行处理，并将生成的信息添加到一张图片中。

## 使用方式

1. **配置文件**
   在`songs.csv`里维护主播歌单
   在 `package.json` 文件中配置工具的参数，包括图片路径、字体样式、颜色等。

2. **运行说明**
   运行 `SongList` 类的 `run` 方法来执行工具。运行后，将生成一张包含歌单信息的图片，并保存在 `./result/song_list.jpg` 中。

3. **安装依赖**
   pip install -r requirements.txt   ps: 这里有很多包实际上用不到
4. **脚本执行方法**
   python song_list.py 或 使用 pyinstaller 打包
## 配置参数

- `name`: 工具的名称或标识。
- `version`: 工具的版本号。
- `png_filename`: 歌单模板图片的文件名。
- `font_style`: 歌单中汉字字体的样式。
- `font_en_style`: 歌单中英文字体的样式。
- `title`: 歌单的标题。
- `title_siz`e: 标题字体的大小。
- `font_size`: 汉字和英文字体的大小。
- `file_name`: 包含歌曲数据的 CSV 文件名。
- `font_color_1`, `font_color_2`, `font_color_3`: 字体颜色的 RGB 值。
- `1_num`, `2_num`, `3_num`, `4_num`, `5_num`, `10_num`, `999_num`: 不同长度歌曲的每行显示个数。

## 主要方法

- `cut_image`: 裁剪图片的方法
- `image_writer`: 添加文字信息到图片的方法
- `read_data`: 读取歌曲数据的方法
- `reset_row`: 重置歌曲行数信息的方法
- `make_data`: 生成歌曲坐标信息的方法

