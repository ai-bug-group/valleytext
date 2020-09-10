# -*- coding: utf-8 -*-
"""
valleytext
@date 2020/9/10
@author yzho0907、xiuzhizheng
"""
import queue


class Node:
    """
    字典树的节点
    """
    def __init__(self, depth: int):
        """
        初始化某个节点
        :param depth: 当前树的深度
        """
        # fail指针
        self.fail = None
        # 用来保存当前节点可能的关键 {'中国': 'LOC'}
        self.current_keywords_dict = dict()
        # 当前节点的叶子节点（Node）
        self.leaves = {}
        # 当前树的深度
        self.depth = depth

    def add_word(self, word: str):
        """
        在字典树里面添加一个字
        :param word: 字
               -type: str
               -len: 1
        :return: 节点
                 -type: Node
        """
        # 如果树里面有这个节点，则直接找到这个节点返回
        if word in self.leaves:
            return self.leaves.get(word)
        else:
            # 如果树里面没有这个节点，就新建一个
            node = Node(self.depth + 1)
            self.leaves[word] = node
        return node

    def add_one_keyword(self, keyword: str, value: str):
        """
        新增一个关键词
        :param keyword: 关键词
        :param value: 标签
        :return: 暂无
        """
        self.current_keywords_dict[keyword] = value

    def add_keywords_dict(self, keywords_dict: dict):
        """
        新增多个关键词
        :param keywords_dict: 多个关键词与对应标签的字典
               -type: dict
        :return: 暂无
        """
        if not isinstance(keywords_dict, dict):
            raise Exception("keywords need a dict")
        self.current_keywords_dict.update(keywords_dict)

    def set_fail(self, fail):
        """

        :param fail:
        :return:
        """
        self.fail = fail

    def get_leaves(self):
        """
        返回叶子对应的字
        :return: 字的列表
                 -type: KeyViews
        """
        return self.leaves.keys()

    def delete_leaf(self, key: str):
        """
        删除叶子
        :param key:
        :return:
        """
        self.leaves.pop(key)

    def next_node(self, word: str) -> object:
        """
        找到节点
        :param word: 字
               -type: str
        :return: 字对应的节点
                 -type: Node
        :rtype: Node
        """
        return self.leaves.get(word)


class Trie(object):
    """
    字典树和AC构建类
    """
    def __init__(self, words=None, case_sensitive=False):
        """
        初始化字典树
        :param words:
        """
        # 构建空的根节点
        self.root = Node(0)
        self.root.set_fail(self.root)
        self.is_tree_created = False
        # 是否大小写敏感
        self.case_sensitive = case_sensitive
        # 字典树中词语总数
        self._keywords_in_trie = 0
        # 如果初始时传入了数据那么就直接开始构建
        if words:
            self.create_trie(words)

    def __len__(self):
        """
        字典树的的词语总数
        :return: int
        """
        return self._keywords_in_trie

    def __contains__(self, keyword):
        """
        判断word是否在字典树种
        :param keyword:
        :return:
        """
        if not self.case_sensitive:
            keyword = keyword.lower()

        current_node = self.root
        for word in keyword:
            current_node = current_node.next_node(word)
            if not current_node:
                # 没有这个keyword
                return False
        return keyword in current_node.current_keywords_dict

    def __getitem__(self, keyword):
        """
        返回keyword的标签
        :param keyword: 关键字
        :return:
        """
        if not self.case_sensitive:
            keyword = keyword.lower()

        current_node = self.root
        for word in keyword:
            current_node = current_node.next_node(word)
            if not current_node:
                # 没有这个keyword
                return None
        if keyword in current_node.current_keywords_dict:
            return current_node.current_keywords_dict[keyword]
        return None

    def __setitem__(self, keyword, value=None):
        """
        新增加一个关键词
        :param keyword: 关键词
               -type: str
        :param value: 对应的标签
               -type: str
        :return:
        """
        self._add_keyword(keyword, value)
        self.create_automation()
        return True

    def __delitem__(self, keyword):
        """
        从字典树中删除某个关键词
        :param keyword: 关键词
        :return:
        """
        if not self.case_sensitive:
            keyword = keyword.lower()
        # 从当前节点开始查找
        current_node = self.root
        word_list = list(keyword)
        stack_nodes = [self.root]
        n = len(word_list)
        for i in range(n):
            current_node = current_node.next_node(word_list[i])
            if not current_node:
                # 没有这个keyword，退出
                return True
            stack_nodes.append(current_node)
        # 找到keyword，从小往上，如果为空就删除
        # 对于最后一个节点
        stack_node = stack_nodes.pop()
        father_node = stack_nodes[-1]
        # 如果该节点为空，直接删除
        if not stack_node.get_leaves():
            father_node.delete_leaf(word_list[-1])
        else:
            if keyword in stack_node.current_keywords_dict:
                del stack_node.current_keywords_dict[keyword]
                self._keywords_in_trie -= 1
            return True
        # 对于其他节点，如果该节点的叶子节点为空，并且该节点的current_keywords_dict也为空，删除该节点
        for i in range(n - 1, 0, -1):
            stack_node = stack_nodes.pop()
            father_node = stack_nodes[-1]
            if not stack_node.get_leaves() and not stack_node.current_keywords_dict:
                father_node.delete_leaf(word_list[i - 1])
            else:
                break
        self._keywords_in_trie -= 1
        self.create_automation()
        return True

    def create_trie(self, words_table):
        """
        构建字典树
        :param words_table: 字典
        :return: 返回字典树（本身）
                 -type: Trie
        """
        if isinstance(words_table, list):
            self.create_trie_from_list(words_table)
        elif isinstance(words_table, dict):
            self.create_trie_from_dict(words_table)
        return self

    def create_trie_from_list(self, keywords, value=''):
        """
        通过载入关键词的列表来创建字典树和AC自动机
        :param keywords: 关键词列表
               -type: list
        :param value: 这些关键的统一标签
               -type: str
        :return: 返回字典树（本身）
                 -type: Trie
        """
        for keyword in keywords:
            self._add_keyword(keyword, value)
        self.create_automation()
        return self

    def create_trie_from_dict(self, keywords_dict):
        """
        通过载入关键词的字典来创建字典树和AC自动机
        :param keywords_dict: 关键词字典
               -type: dict
               -example:
                    {
                        '设备': ['GPS', '设备'],
                        '动作': ['检测', '测试'],
                    }
        :return: 返回字典树（本身）
                 -type: Trie
        """
        for tag, values in keywords_dict.items():
            for value in values:
                self._add_keyword(value, tag)
        self.create_automation()
        return self

    def _add_keyword(self, keyword, value):
        """
        增加一个关键词
        :param keyword: 关键词
               -type: str
        :param value: 对应的标签
               -type: str
        :return: 暂无
        """
        if not self.case_sensitive:
            keyword = keyword.lower()
        current_node = self.root
        word_list = list(keyword)
        for word in word_list:
            current_node = current_node.add_word(word)
        # 如果value为空，则设置为自己
        if not value:
            value = keyword
        current_node.add_one_keyword(keyword, value)
        self._keywords_in_trie += 1

    def add_new_keyword(self, keyword, value):
        """
        新增加一个关键词
        :param keyword: 关键词
               -type: str
        :param value: 对应的标签
               -type: str
        :return: 暂无
        """
        return self.__setitem__(keyword, value)

    def create_automation(self):
        """
        构建失败路径--->如果某个节点没有孩子了，那么下面该从哪查起
        :return: 暂无
        """
        # 复制根节点
        root = self.root
        # 新建一个节点的队列
        node_queue = queue.Queue()

        # 先把根节点下的全部叶子节点拿出来
        for k, v in self.root.leaves.items():
            node_queue.put(v)
            v.set_fail(root)

        # BFS遍历字典树
        while not node_queue.empty():
            # 取出队首元素
            current_node = node_queue.get()
            leaves = current_node.get_leaves()

            # 遍历当前节点所有的叶子节点
            for word in leaves:
                target_node = current_node.next_node(word)

                node_queue.put(target_node)
                # 转到fail指针 (初始的fail指针都指向自己)
                trace_node = current_node.fail

                # 如果current_node没有word的叶子节点，则一直跳转fail节点，直到找到有word叶子的节点或者root节点
                while trace_node.next_node(word) is None and trace_node.depth != 0:
                    trace_node = trace_node.fail

                # 设置找到的word节点为target_node的fail
                if trace_node.next_node(word) is not None:
                    target_node.set_fail(trace_node.next_node(word))
                    target_node.add_keywords_dict(trace_node.next_node(word).current_keywords_dict)
                else:
                    target_node.set_fail(trace_node)
        self.is_tree_created = True

    @staticmethod
    def get_fail(current_node: Node, word: str) -> Node:
        """
        通过fail指针找到word节点，否则返回None
        :param current_node:当前的fail指针
        :param word: 字
               -type: str
               -len: 1
        :return: new_current_node: 下一个fail指针指到word节点
                 -type: Node
        """
        new_current_node = current_node.next_node(word)

        while not new_current_node and current_node.depth != 0:
            current_node = current_node.fail
            new_current_node = current_node.next_node(word)
        return new_current_node

    def remove_keyword(self, keyword: str):
        """
        从字典树中删除某个关键词
        :param keyword:待删除的关键词
               -type: str
        :return:暂无
        """
        return self.__delitem__(keyword)

    def extract_keywords_from_text(self, text, allow_over_laps=True):
        """
        前缀树最长字符串遍历到一条文本里面的关键词
        :param text:文本
        :param allow_over_laps:是否允许有被覆盖的词（目前还是有可能有交叉的词）
        :return: keywords:关键词表
                 -type: list
                 -example:
                 [(1, 3, '泵车', '设备'),
                 (8, 10, 'r口', '地点'),
                 (10, 13, '挖掘机', '设备'),
                 (13, 16, 'gps', '设备')]
        """
        keywords = []
        if not self.case_sensitive:
            text = text.lower()
        current_fail = self.root
        words_list = list(text)
        for word_position, word in enumerate(words_list):
            word_position += 1
            current_fail = self.get_fail(current_fail, word) or self.root
            if word_position > len(text) - 1 or allow_over_laps:
                # 最后一个字
                get_keywords_from_current_fail(keywords, current_fail, word_position)
            else:
                # 前缀遍历优先
                if words_list[word_position] in current_fail.leaves:
                    pass
                else:
                    get_keywords_from_current_fail(keywords, current_fail, word_position)
        return keywords


def create_trie(words, case_sensitive) -> Trie:
    """
    返回加载好数据的实例化Trie()
    :param words: 词表
           -type: list/dict
    :param case_sensitive: 是否大小写敏感
           -type: bool
    :return: AC优化后的字典树
             -type: Trie
    """
    if not isinstance(case_sensitive, bool):
        raise Exception("case_sensitive need a bool")
    return Trie(words, case_sensitive)


def get_keywords_from_current_fail(keywords_list, current_fail, position):
    """
    遍历到目前位置（词、句中字的位置）所有可能的关键词，取最长一个，更新到keywords_list里面去
    :param keywords_list:当前已经遍历到的合法词的列表
    :param current_fail:fail指针指到word节点
    :param position:指到节点在输入文本里面的位置
    :return:暂无
    """
    if current_fail.current_keywords_dict:
        current_keywords = ''
        length_of_keyword = 0
        # 前缀遍历的前提下最大字符串遍历
        for keyword in current_fail.current_keywords_dict:
            current_length_of_keyword = len(keyword)
            if current_length_of_keyword > length_of_keyword:
                current_keywords = keyword
                length_of_keyword = current_length_of_keyword
        keyword_combs = (position - length_of_keyword,
                         position,
                         current_keywords,
                         current_fail.current_keywords_dict[current_keywords])
        keywords_list.append(keyword_combs)


if __name__ == '__main__':
    words_dict = {'设备': ['GPS', '设备']}
    extractor = create_trie(words_dict, False)
    extracts = extractor.extract_keywords_from_text('我有一台gps设备')
    print(extracts)
