#! -*- coding:utf-8 -*-
import sys
import jieba.analyse
import numpy as np
from sklearn import preprocessing

sys.path.append("..")
import logger

reload(sys)
sys.setdefaultencoding('utf-8')

log = logger.initLogger("TextTagger")


class TextTagger:
    # 控制变量，外部可修改
    partOfSpeech = ('n', 'nr', 'ns', 'nt', 'nz', 'nrt', 'j', 'b', 'vn', 'ng')
    topN = 5
    title_weight_rate = 1.0
    content_weight_rate = 0.8
    ifidf_filter_weight = 0.4
    textrank_filter_weight = 0.4
    lable_weight_threshold = 0.8

    # 输入输出文件的缓存
    __INPUT_CORPUS_PATH = ""
    __OUTPUT_DETAIL_PATH = ""
    __OUTPUT_LABEL_PATH = ""

    # 需要加载的词典
    __COMMON_SEGGER_PATH = "dict/dict.txt.big"
    __SOUGOU_SEGGER_PATH = "dict/sougo.dict.txt"
    __EXT_SEGGER_PATH = "dict/ext_dict.txt"
    __ANALYSE_STOP_WORDS = "dict/stopwords.txt"
    __ANALYSE_STOP_WORDS_EXT = "dict/ext_stopwords.txt"
    __ANALYSE_TFIDF = "dict/idf.txt.big"

    # 内部计算使用变量
    __total_lables_dict = {}  # 最终导出的标签词典，输出格式：word count flag
    __sample_tags_dict = {}  # 合并标签用的词典，保存各源头的权重
    __count = 0
    __dump_mode = "all"

    def __init__(self, isLoadExtDict=False):
        if isLoadExtDict:
            self.load_dict()

    def load_dict(self):
        """
        加载词典方法，加载的词典具体如下：
        1. 切词词典（通用）
        2. 切词词典（用户新增专名）
        3. 标签分析的停用词典（通用）
        4. 标签分析的停用词典（用户自定义）
        5. 标签分析的词频（通用）
        """
        log.info("begin to load segger dict ...")
        jieba.load_userdict(self.__COMMON_SEGGER_PATH)
        jieba.load_userdict(self.__EXT_SEGGER_PATH)
        jieba.load_userdict(self.__SOUGOU_SEGGER_PATH)
        log.info("all segger dict load success")

        log.info("begin to load analyse dict ...")
        jieba.analyse.set_stop_words(self.__ANALYSE_STOP_WORDS)
        jieba.analyse.set_stop_words(self.__ANALYSE_STOP_WORDS_EXT)
        jieba.analyse.set_idf_path(self.__ANALYSE_TFIDF)
        log.info("all analyse dict load success")

    def extract_tag_batch(self, corpus_in, detail_out, labels_out):
        try:

            self.__INPUT_CORPUS_PATH = corpus_in
            self.__OUTPUT_DETAIL_PATH = detail_out
            self.__OUTPUT_LABEL_PATH = labels_out

            fi = open(self.__INPUT_CORPUS_PATH, 'r')
            fo = open(self.__OUTPUT_DETAIL_PATH, 'w')

            int
            line = 0
            # 逐条处理语料
            for line in fi:
                self.proces(line, fo)

            # 输出标签词典
            self.__dump_lables()
        finally:
            fi.close()
            fo.close()

    def proces(self, line, outfile):
        """
        单条语料的处理函数，取标题、内容，分别计算tfidf、textrank的关键词，并合并
        Parameters:
            line - 输入的一行语料
        Returns: 无
        Raises: 无
        """

        # 重置每条记录合并tag的dict
        self.__sample_tags_dict.clear()
        self.__count = self.__count + 1
        # dump
        dump_list = []

        # 切分文本
        segs = line.strip().split('\t')
        # id = int(segs[0])
        title = segs[2]
        content = segs[3]
        # cateName = segs[5]
        out_str = "%(line)d\t【%(title)s】\t%(content)s\n" % (
            {"line": self.__count, "title": title, "content": content})
        dump_list.append(out_str)

        # 提取标题的关键词
        self.__adjust_param(title, type="title")
        tags = self.tag_by_ifidf(title)
        self.__merge_tag(tags, "tf")  # 合并关键词，打标签，记录来源
        dump_list.append("title（tfidf）：%s\n" % self.tag2str(tags, self.__dump_mode))

        # tags = self.tag_by_textrank(title)
        # self.__merge_tag(tags, "tr")  # 合并关键词，打标签，记录来源
        # dump_list.append("title（TextRank）：%s\n" % self.tag2str(tags, self.__dump_mode))

        # 提取内容的关键词
        self.__adjust_param(content, type="content")
        tags = self.tag_by_ifidf(content)
        self.__merge_tag(tags, "cf")  # 合并关键词，打标签，记录来源
        dump_list.append("content（tfidf）：%s\n" % self.tag2str(tags, self.__dump_mode))

        tags = self.tag_by_textrank(content)
        self.__merge_tag(tags, "cr")  # 合并关键词，打标签，记录来源
        dump_list.append("content（TextRank）：%s\n" % self.tag2str(tags, self.__dump_mode))

        # 合并后的标签数据
        dump_list.append("标签：%s\n" % self.__dump_merged_tags())
        dump_list.append("\n")

        for line in dump_list:
            log.debug(line.strip('\n'))

        outfile.writelines(dump_list)

        if self.__count % 100 == 0:
            log.info("processed %d lines" % self.__count)

    def __merge_tag(self, tags, src):
        # merge result
        for turple in tags:

            key = "%s[%s]" % (turple[0].word, turple[0].flag)

            # 累加权重、源头
            if self.__sample_tags_dict.has_key(key):
                dict = self.__sample_tags_dict.get(key)
                dict[src] = turple[1]
                self.__sample_tags_dict[key] = dict
            else:
                dict = {}
                dict[src] = turple[1]
                self.__sample_tags_dict[key] = dict

            # 记录总的标签库
            if self.__total_lables_dict.has_key(key):
                count = self.__total_lables_dict.get(key) + 1
                self.__total_lables_dict[key] = count
            else:
                self.__total_lables_dict[key] = 1

    def __dump_merged_tags(self):
        tags_list = []
        for k, v in self.__sample_tags_dict.iteritems():
            tuple = self.__get_weight_src(v)
            # 组合元组
            tags_list.append((k.encode("utf-8"), tuple[0], tuple[1]))
        tags_list.sort(key=lambda x: x[1], reverse=True)
        # 按格式输出满足指定阈值的标签词
        tags_list = ["%s:%.2f(%s)" % (tag[0], tag[1], tag[2]) for tag in tags_list if tag[1] >= self.lable_weight_threshold]
        result = ' '.join(tags_list)
        return result

    # 效果不好，废弃
    def __get_weight_src_v1(self, dict={}):
        # 组合权重，构造src标识
        src_list = []
        weight = 0.0
        key_num = len(dict.keys())
        keys = dict.keys()
        for k, v in dict.iteritems():
            src_list.append(k)
            if k == "tf" or k == "tr":
                 weight = v * self.title_weight_rate
            elif k == "cf" or k == "cr":
                 weight = v * self.content_weight_rate
            else:
                log.warn("get unkown process type, set weight_rate=1.0, type=%s" % (k))
                weight = v

        # 归一化权重，以便做截断
        if key_num == 1:
            if "tf" in keys or "tr" in keys:
                weight = weight / self.title_weight_rate
            elif "cf" in keys or "cr" in keys:
                weight = weight / self.content_weight_rate
            else:
                log.warn("normalize final weight by unkown swtich, key_num=1 keys=" % (" ".join(keys)))
        elif key_num == 2:
            if "tf" in keys and "tr" in keys:
                weight = weight / self.title_weight_rate / 2
            elif "cf" in keys and "cr" in keys:
                weight = weight / self.content_weight_rate / 2
            else:
                weight = weight / (self.title_weight_rate + self.content_weight_rate)
        elif key_num == 3:
            weight = weight / (self.title_weight_rate + self.content_weight_rate * 2)
        else:
            log.warn("normalize final weight by unkown swtich, key_num<>(1,2,3) keys=" % (" ".join(keys)))

        # 拼接源头词
        src_str = " ".join(src_list)
        return (weight, src_str)

    def __get_weight_src(self, dict={}):
        # 组合权重，构造src标识
        src_list = []
        weight = 0.0
        for k, v in dict.iteritems():
            src_list.append(k)
            if k == "tf" or k == "tr":
                 weight = weight + v * self.title_weight_rate
            elif k == "cf" or k == "cr":
                 weight = weight + v * self.content_weight_rate
            else:
                log.warn("get unkown process type, set weight_rate=1.0, type=%s" % (k))
                weight = weight + v

        # 拼接源头词
        src_str = " ".join(src_list)
        return (weight, src_str)


    def __dump_lables(self):

        if self.__OUTPUT_LABEL_PATH == "":
            log.fatal("label output path is null !")
            return

        log.info("begin to dump lables to=%s" % (self.__OUTPUT_LABEL_PATH))
        out_list = []
        for k, v in self.__total_lables_dict.iteritems():
            segs = k.replace(']', '').split('[')
            out_list.append((segs[0], v, segs[1]))

        # 按词频排序
        out_list.sort(key=lambda x: x[1], reverse=True)

        try:
            outfile = open(self.__OUTPUT_LABEL_PATH, 'w')
            for tuple in out_list:
                result = "%(word)s\t%(count)d\t%(flag)s\n" % ({"word": tuple[0], "count": tuple[1], "flag": tuple[2]})
                outfile.write(result)
        finally:
            outfile.close()

        log.info("dump labes success")

    def __adjust_param(self, input_str, type="default"):
        """
        调节内部参数的方法
        标题：关键词为 1.0 倍权重，根据长度分别提取1-3个关键词
        内容：关键词为 0.8 被权重，根据长度分别提取3-8个关键词
        Parameters:
            input_str - 待处理的字符串，默认为utf-8
            type - 待处理字符串的类型，可选值为：title, content, default
        Returns: 无
        Raises: 无
        """
        # utf-8字符串占3个字节
        str_len = len(input_str) / 3

        if type == "title":
            if str_len <= 4:
                self.topN = 1
            elif str_len <= 8:
                self.topN = 2
            else:
                self.topN = 3
        elif type == "content":
            if str_len <= 10:
                self.topN = 2
            if str_len <= 20:
                self.topN = 3
            elif str_len <= 40:
                self.topN = 5
            else:
                self.topN = 8
        elif type == "default":
            self.topN = 5
        else:
            log.warn("input type is invalid, params set to default, InputType=" + type)
            self.topN = 5

    def tag_by_ifidf(self, input_str):
        """
        采用 IFIDF 方法提取关键词
        Parameters:
            input_str - 待处理的字符串，默认为utf-8
        Returns: 标签对象，格式为 (pair(word, flag), weight)
        """
        tags = jieba.analyse.extract_tags(input_str, topK=self.topN, withWeight=True, allowPOS=self.partOfSpeech,
                                          withFlag=True)
        # 对tfidf的权重进行归一化
        arr_list = []
        weights = [turple[1] for turple in tags]
        weights.append(0.0)  # 占位符，防止最小值被归一化为0
        arr_list.append(weights)
        arr = np.array(arr_list)
        norm_arr = preprocessing.normalize(arr_list, norm='max')
        tags = [(turple[0], norm_arr[0, i]) for i, turple in enumerate(tags) if
                norm_arr[0, i] > self.ifidf_filter_weight]
        return tags

    def tag_by_textrank(self, input_str):
        """
        采用 TextRank 方法提取关键词
        Parameters:
            input_str - 待处理的字符串，默认为utf-8
        Returns: 标签对象，格式为 (pair(word, flag), weight)
        """
        tags = jieba.analyse.textrank(input_str, topK=self.topN, withWeight=True, allowPOS=self.partOfSpeech,
                                      withFlag=True)
        tags = [tuple for tuple in tags if tuple[1] > self.textrank_filter_weight]  # 阈值过滤
        return tags

    def tag2str(self, tags, mode="all", src_tag=""):
        """
        tag 对象转换为字符串
        Parameters:
            tags - 标签对象，格式为 (pair(word, flag), weight)
            mode - 输出格式，可选值为： all，word_only，word_weight, word_flag
            src_tag - 源标签，用来跟踪关键词来源，为“”则不输出
        Returns: string，"你好[n]:"
        """
        if mode == "all":
            tag_str_list = ["%s[%s]:%.2f" % (turple[0].word, turple[0].flag, turple[1]) for turple in tags]
        elif mode == "word_only":
            tag_str_list = ["%s" % (turple[0].word) for turple in tags]
        elif mode == "word_weight":
            tag_str_list = ["%s:%.2f" % (turple[0].word, turple[1]) for turple in tags]
        elif mode == "word_flag":
            tag_str_list = ["%s[%s]" % (turple[0].word, turple[0].flag, turple[1]) for turple in tags]
        else:
            log.warn("tag2str input mode is invalid, using all mode as default, Tag2StrMode=" + mode)
            tag_str_list = ["%s[%s]:%.2f" % (turple[0].word, turple[0].flag, turple[1]) for turple in tags]

        result = ' '.join(tag_str_list)
        if src_tag != "":
            result = result + "-" + src_tag
        return result


tagger = TextTagger(isLoadExtDict=True)
# tagger = TextTagger()
tagger.extract_tag_batch('data/corpus.txt', 'data/corpus_tag.txt', 'data/corpus_labels.txt')
