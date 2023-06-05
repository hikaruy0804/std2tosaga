import csv
import re
from transformers import T5ForConditionalGeneration, T5Tokenizer

class Std2saga:
    def __init__(self, model_name_or_path="sonoisa/t5-base-japanese", model_dir="model", max_input_length=64, max_target_length=64, csv_path='方言辞書.csv'):  #model、csv_pathのパス修正が必要
        self.model_name_or_path = model_name_or_path
        self.model_dir = model_dir
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length
        
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_dir, is_fast=True)
        self.trained_model = T5ForConditionalGeneration.from_pretrained(self.model_dir)
        self.trained_model.eval()  # Set the model in evaluation mode
        self.dictionary = self.create_dictionary_from_csv(csv_path)  # Load dictionary at the initialization
        self.brackets_pattern = re.compile(r"(^【[^】]*】)|(【[^】]*】$)")

    def remove_brackets(self, text):
        return self.brackets_pattern.sub("", text)

    def normalize_text(self, text):
        assert "\n" not in text and "\r" not in text
        text = text.replace("\t", " ")
        text = text.strip()
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
        # 辞書でtextと一致する場合は、対応するsagaを出力
        saga = self.dictionary.get(text)
        if saga is not None:
            return saga

        inputs = [self.preprocess_body(text)]
        batch = self.tokenizer.batch_encode_plus(
            inputs, max_length=self.max_input_length, truncation=True, 
            padding="longest", return_tensors="pt")

        input_ids = batch['input_ids']
        input_mask = batch['attention_mask']

        outputs = self.trained_model.generate(
            input_ids=input_ids, attention_mask=input_mask, 
            max_length=self.max_target_length,
            temperature=2.0,
            num_beams=6,
            diversity_penalty=2.0,
            num_beam_groups=6,
            num_return_sequences=1,
            repetition_penalty=1.6,
        )

        generated_titles = [self.tokenizer.decode(ids, skip_special_tokens=True, 
                                            clean_up_tokenization_spaces=False) 
                            for ids in outputs]

        return generated_titles[0]
    
    
    
    
#コード添削
# import csv
# import re
# from transformers import T5ForConditionalGeneration, T5Tokenizer

# class Std2saga:
#     def __init__(self, model_name_or_path="sonoisa/t5-base-japanese", model_dir="model", max_input_length=64, max_target_length=64, csv_path='方言辞書.csv'):
#         self.model_name_or_path = model_name_or_path
#         self.model_dir = model_dir
#         self.max_input_length = max_input_length
#         self.max_target_length = max_target_length
#         self.csv_path = csv_path
#         self.brackets_pattern = re.compile(r"(^【[^】]*】)|(【[^】]*】$)")
#         self.dictionary = None
#         self.tokenizer = None
#         self.trained_model = None

#     def load_model(self):
#         if not self.tokenizer or not self.trained_model:
#             self.tokenizer = T5Tokenizer.from_pretrained(self.model_dir, is_fast=True)
#             self.trained_model = T5ForConditionalGeneration.from_pretrained(self.model_dir)
#             self.trained_model.eval()  # Set the model in evaluation mode

#     def load_dictionary(self):
#         if not self.dictionary:
#             self.dictionary = self.create_dictionary_from_csv(self.csv_path)  # Load dictionary at the initialization

#     # other methods are same as before

#     def sagaben(self, text):
#         self.load_model()
#         self.load_dictionary()
        
#         # the remaining part of the code is the same

