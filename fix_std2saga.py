import re
import csv
import time
import unicodedata
from transformers import T5ForConditionalGeneration, T5Tokenizer

class Std2saga:
    def __init__(self, model_name_or_path="sonoisa/t5-base-japanese", model_dir="model", max_input_length=64, max_target_length=64,): #train_batch_size=64, eval_batch_size=64, num_train_epochs=20):
        self.model_name_or_path = model_name_or_path
        self.model_dir = model_dir
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length
        # self.train_batch_size = train_batch_size
        # self.eval_batch_size = eval_batch_size
        # self.num_train_epochs = num_train_epochs
        
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_dir, is_fast=True)
        self.trained_model = T5ForConditionalGeneration.from_pretrained(self.model_dir)

    def unicode_normalize(self, cls, s):
        pt = re.compile('([{}]+)'.format(cls))
        def norm(c):
            return unicodedata.normalize('NFKC', c) if pt.match(c) else c
        s = ''.join(norm(x) for x in re.split(pt, s))
        s = re.sub('－', '-', s)
        return s

    def remove_extra_spaces(self, s):
        s = re.sub('[ 　]+', ' ', s)
        blocks = ''.join(('\u4E00-\u9FFF',  # CJK UNIFIED IDEOGRAPHS
                        '\u3040-\u309F',  # HIRAGANA
                        '\u30A0-\u30FF',  # KATAKANA
                        '\u3000-\u303F',  # CJK SYMBOLS AND PUNCTUATION
                        '\uFF00-\uFFEF'   # HALFWIDTH AND FULLWIDTH FORMS
                        ))
        basic_latin = '\u0000-\u007F'

        def remove_space_between(cls1, cls2, s):
            p = re.compile('([{}]) ([{}])'.format(cls1, cls2))
            while p.search(s):
                s = p.sub(r'\1\2', s)
            return s

        s = remove_space_between(blocks, blocks, s)
        s = remove_space_between(blocks, basic_latin, s)
        s = remove_space_between(basic_latin, blocks, s)
        return s

    def normalize_neologd(self, s):
        s = s.strip()
        s = self.unicode_normalize('０-９Ａ-Ｚａ-ｚ｡-ﾟ', s)

        def maketrans(f, t):
            return {ord(x): ord(y) for x, y in zip(f, t)}

        s = re.sub('[﹣－ｰ—―─━ー]+', 'ー', s)  # normalize choonpus
        s = re.sub('[~∼∾〜〰～]+', '〜', s)  # normalize tildes (modified by Isao Sonobe)
        s = s.translate(
            maketrans('!"#$%&\'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣',
                '！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」'))

        s = self.remove_extra_spaces(s)
        s = self.unicode_normalize('！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝〜', s)  # keep ＝,・,「,」
        s = re.sub('[’]', '\'', s)
        s = re.sub('[”]', '"', s)
        return s

    def remove_brackets(self, text):
        text = re.sub(r"(^【[^】]*】)|(【[^】]*】$)", "", text)
        return text

    def normalize_text(self, text):
        assert "\n" not in text and "\r" not in text
        text = text.replace("\t", " ")
        text = text.strip()
        text = self.normalize_neologd(text)
        text = text.lower()
        return text

    def preprocess_body(self, text):
        return self.normalize_text(text.replace("\n", " "))

    def create_dictionary_from_csv(self, csv_file_path):
        dictionary = {}
        with open(csv_file_path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                dictionary[row[0]] = row[1]
        return dictionary

    def sagaben(self, text):
        # CSVファイルのパスを指定して辞書を読み込む
        csv_path = '方言辞書.csv'
        dictionary = self.create_dictionary_from_csv(csv_path)

        # 辞書でtextと一致する場合は、対応するsagaを出力
        if text in dictionary:
            time.sleep(0.3)
            return dictionary[text]

        else:
            self.trained_model.eval()

            inputs = [self.preprocess_body(text)]
            batch = self.tokenizer.batch_encode_plus(
                inputs, max_length=self.max_input_length, truncation=True, 
                padding="longest", return_tensors="pt")

            input_ids = batch['input_ids']
            input_mask = batch['attention_mask']

            outputs = self.trained_model.generate(
                input_ids=input_ids, attention_mask=input_mask, 
                max_length=self.max_target_length,  # <--- max_lengthをここに追加
                temperature=2.0,          # 生成にランダム性を入れる温度パラメータ
                num_beams=6,             # ビームサーチの探索幅
                diversity_penalty=2.0,    # 生成結果の多様性を生み出すためのペナルティ
                num_beam_groups=6,       # ビームサーチのグループ数
                num_return_sequences=1,  # 生成する文の数
                repetition_penalty=1.6,   # 同じ文の繰り返し（モード崩壊）へのペナルティ
            )

            generated_titles = [self.tokenizer.decode(ids, skip_special_tokens=True, 
                                                clean_up_tokenization_spaces=False) 
                                for ids in outputs]

            return generated_titles[0]