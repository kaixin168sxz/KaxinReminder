# 导入模块

import pickle

English_conversion = str.maketrans("abcdefghijklmnopqrstuvwxyz", "qwertyuiopasdfghjklmnbvczx")    # 加密密码
Digital_transformation = str.maketrans("0123456789", "2587413690")
English_Reverse_conversion = str.maketrans("qwertyuiopasdfghjklmnbvczx", "abcdefghijklmnopqrstuvwxyz")    # 解密密码
Digital_Reverse_conversion = str.maketrans("2587413690", "0123456789")


# 定义文件操作类
class Files:
    """
    Files 文件操作类\n
    函数:\n
    save_file(file_content)\n
    read_file()\n
    NameCopyFile(new_path, file_name)\n
    CopyFile(new_path)\n
    save_wave_file(data)\n
    """
    def __init__(self, file_name):    # 定义self 类全局变量
        self.file_name = file_name

    # 保存文件
    def save_file(self, file_content):
        """
        保存.kx文件\n
        file_content为要保存的内容
        :param file_content:
        :return:
        """
        global English_conversion, Digital_transformation
        data = str(pickle.dumps(file_content))
        # 对序列化后的二进制数据进行字符串替换操作
        new_data_1 = data.translate(English_conversion)
        new_data_2 = new_data_1.translate(Digital_transformation)

        # 将替换后的二进制数据写入文件
        with open(self.file_name, 'w') as file_save:
            file_save.write(new_data_2)
            file_save.flush()

    # 读取文件
    def read_file(self):
        """
        读取.kx文件\n
        :return:
        """
        global Digital_Reverse_conversion, English_Reverse_conversion
        # 从文件中读取替换后的二进制数据
        with open(self.file_name, 'r') as file_read:
            r = (file_read.read())
        # 对读取的二进制数据进行字符串替换操作，恢复原始数据
        old_data_1 = r.translate(English_Reverse_conversion)
        old_data_2 = pickle.loads(eval(old_data_1.translate(Digital_Reverse_conversion)))
        return old_data_2