# coding=utf-8
import re
import os
from time import time
"""
    Update link list in README.md. So I don't need to update README's link list manually.
    1. Traversal all files those contents are LeetCode.
    2. Rewrite those links into README.md.
"""


def trans2link(file):
    """
    :param file: like "50.powx-n.md".
    :return: "/000-099/50.powx-n.md".
    """
    number = file[: file.find('.')]
    case = str(int(number) // 100)
    base_dir = "/{}00-{}99/".format(case, case)
    # print(file, number, link)
    return base_dir + file


if __name__ == "__main__":
    print("Start...")
    start_time = time()
    '''
    FIX file path error.
    file needs to be accurately located, Like '..../Leetcode'.
    '''
    upper_path = os.path.abspath(os.path.dirname(__file__))
    target_file_path = os.path.join(upper_path, "README.md")
    dirs = os.listdir(upper_path)
    dirs.sort()
    all_files = []

    chinese_titles = []
    for dir_ in dirs:
        # DIRs like "000-099".
        if dir_.find('-') > 0:
            # use complete path.
            files = os.listdir(os.path.join(upper_path, dir_))
            if len(files):
                '''
                1.Here, notice this two strings: 10.file1 < 3.file2.
                If put format like 010.file1 and 003.file2, this error will be missed.
                But not change format, I should find the num.
                2.Because dirs are sorted, this only happens in 000-099 dir.
                '''
                if '000-099' in dir_:
                    files.sort(key=lambda x: int(x[: x.find('.')]))
                else:
                    files.sort()
                '''
                Add Chinese title. 2019.12.04
                '''
                for file in files:
                    with open(os.path.join(upper_path, dir_, file), 'r', encoding='utf-8') as fm:
                        number = file[:file.find('.')]
                        # [LeetCode - 378. 有序矩阵中第K小的元素]
                        pattern_c = re.compile(r'\[LeetCode.*' + number + r'\.(.*)\]')
                        all_lines = fm.readlines()
                        for line_ in all_lines:
                            title = pattern_c.search(line_)
                            if title:
                                # print(number, title.groups(1)[0])
                                chinese_titles.append(title.groups(1)[0])
            all_files.extend(files)
    # [number.English_title Chinese_title]
    pattern = re.compile(r'\[(\d+)\.((\w+-*)+)(.*)\]')
    with open(target_file_path, 'r+', encoding='utf-8') as f:
        # lines are all data in README, and use new_lines to store new content.
        lines = f.readlines()
        new_lines = []
        index = 0
        flag = True
        old_links = []
        new_links = []
        for line in lines:
            is_link = pattern.search(line)
            # Find link list's start, then update.
            if is_link:
                # Record all old link's name.
                old_links.append(line[line.find('[') + 1: line.find(']')])
                if flag:
                    flag = False
                    for file_name, title in zip(all_files, chinese_titles):
                        line = "[{} {}]({}){}\n".format(file_name[: -3], title, trans2link(file_name), "    ")
                        # print this line without '\n'.
                        print(line[: -1])
                        # Contain new link's name.
                        new_links.append(line[line.find('[') + 1: line.find(']')])
                        new_lines.append(line)
            else:
                new_lines.append(line)
        # Clear file, and rewrite.
        f.seek(0)
        f.truncate(0)
        f.writelines(new_lines)
        print("...Done.\tTotal {} files.".format(len(all_files)))
        # Select new links.
        diff_links = list(set(new_links) - set(old_links))
        for i in diff_links:
            print(i)
        print("...Spend time: {:.4f}s.".format(time() - start_time))
