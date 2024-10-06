# pip install tqdm
import os

from tqdm import tqdm


INPUT_DIRECTORY = "./repository"  # ここに対象のディレクトリのパスを指定
OUTPUT_DIRECTORY = "./output"
OUTPUT_FILENAME = "repository.txt"
OUTPUT_FILEPATH = f"{OUTPUT_DIRECTORY}/{OUTPUT_FILENAME}"


def combine_files(input_dir, output_file):
    file_count = sum(len(files) for _, _, files in os.walk(input_dir))

    with open(output_file, 'w', encoding='utf-8') as out_file:
        with tqdm(total=file_count, desc="Combining files", unit="file") as pbar:
            for root, _, files in os.walk(input_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    for encoding in ['utf-8', 'latin-1', 'cp1252']:
                        try:
                            with open(file_path, 'r', encoding=encoding) as in_file:
                                # ファイル名を書き込む
                                out_file.write(f"```{os.path.relpath(file_path, input_dir)}\n")
                                # ファイルの内容を書き込む
                                out_file.write(in_file.read())
                                out_file.write("\n```\n")
                            break
                        except UnicodeDecodeError:
                            continue
                    else:
                        print(f"Skipping file due to encoding error: {file_path}")
                    pbar.update(1)

if __name__ == "__main__":
    combine_files(INPUT_DIRECTORY, OUTPUT_FILEPATH)
    print(f"All files have been combined into {OUTPUT_FILENAME}")
