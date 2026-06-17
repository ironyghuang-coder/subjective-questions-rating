import os

def read_files_to_list(directory):
    files_content = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                files_content.append(content)
    return files_content




if __name__ == "__main__":
    directory_path = 'D:\\work\\3D\\ai-agent-project\\doc'
    files_content = read_files_to_list(directory_path)

    for content in files_content:
        print(content, end='')