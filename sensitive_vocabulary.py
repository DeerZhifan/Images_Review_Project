# -*- coding: utf-8 -*-


class SensitiveVocabulary():
    """敏感信息库"""
    def __init__(self, root):
        """初始化参数"""
        self.root = root

    def build(self):
        """建立敏感信息库"""
        words = []
        with open(self.root, 'r') as f:
            while True:
                line = f.readline().split('\n')[0]
                if not line:
                    break
                else:
                    words.append(line)
        return words


if __name__ == '__main__':
    words_root = '/users/vita/desktop/sensitive_words'
    sensitive_engine = SensitiveVocabulary(words_root)
    sensitive_words = sensitive_engine.build()
    print(len(sensitive_words))
