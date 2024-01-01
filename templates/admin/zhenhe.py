# 导入os模块，用于操作文件和目录
import os

# 定义一个函数，用于遍历当前目录及其所有子目录下的所有文件，并返回一个文件列表
def get_all_files():
    all_files = []
    for root, dirs, filenames in os.walk("."):
        for filename in filenames:
            # 只获取.html, .css, .js, .py文件
            if filename.endswith((".html", ".css", ".js", ".py")):
                # 拼接文件的完整路径
                filepath = os.path.join(root, filename)
                # 将文件路径添加到列表中
                all_files.append(filepath)
    return all_files

# 定义一个函数，用于读取一个文件的内容，并返回一个字符串
def read_file(filepath):
    if not os.path.exists(filepath):
        return f"File '{filepath}' not found.\n\n"
    # 以只读模式打开文件
    with open(filepath, "r", encoding="utf-8") as file:
        # 读取文件的全部内容
        content = file.read()
    return content

# 定义一个函数，用于将一个字符串写入到一个文件中
def write_file(filepath, content):
    # 以追加模式打开文件
    with open(filepath, "a", encoding="utf-8") as file:
        # 写入字符串到文件中
        file.write(content)

# 获取当前目录及其所有子目录下的所有指定类型文件列表
all_files = get_all_files()

# 定义要创建的文件的名称
output = "project_content.txt"

# 输出目录结构
directory_structure = "Directory Structure:\n"
for root, dirs, files in os.walk("."):
    level = root.count(os.sep)
    indent = " " * 4 * level
    directory_structure += f"{indent}{os.path.basename(root)}/\n"
    subindent = " " * 4 * (level + 1)
    for file in files:
        directory_structure += f"{subindent}{file}\n"

# 将目录结构写入到输出文件中
write_file(output, directory_structure + "\n\n")

# 遍历所有文件并读取内容写入到输出文件中
for file in all_files:
    # 读取文件的内容
    content = read_file(file)
    # 在文件内容前加上文件的路径
    content = f"File: {file}\n{content}\n"
    # 将文件内容写入到输出文件中
    write_file(output, content)

# 打印提示信息
print(f"已将当前目录及其所有子目录下的所有 HTML、CSS、JavaScript 和 Python 文件的内容写入到 {output} 文件中，并输出目录结构。")
