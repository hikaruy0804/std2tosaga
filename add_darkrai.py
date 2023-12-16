# import fasttext
import random

class Darkrai:
    def __init__(self):
        self.darkrai_path ='/cc.ja.300.bin',
        # self.model_ft = fasttext.load_model(self.darkrai_path)
        self.len_similar_word = 10
        
    def darkrai_sentence(self, text):
        random_len = random.randint(0, self.len_similar_word -1)
        query_word = text
        # similar_words = self.model_ft.get_nearest_neighbors(query_word, k=self.len_similar_word)
        # score, word = similar_words[random_len]
        # darkrai_sentence = str(query_word +' vs ' + word + ' vs ' + ' ダークライ')
        # return darkrai_sentence
        return text