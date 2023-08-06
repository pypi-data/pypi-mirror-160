import os
import json
import time
import pandas as pd
import six
from googletrans import Translator

def cevir(file, save_path, source_language=None):
    allowed_extensions = [".txt", ".xlsx", ".json"]
    translator = Translator()
    extension = os.path.splitext(file)[1]

    def translate_text(text, source_language, detect_source_language):
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        if detect_source_language:
            source_language = translator.detect(text).lang
            result = translator.translate(text, src=source_language, dest="tr")

        else:
            result = translator.translate(text, source_language=source_language, dest="tr")

        return result.text

    def translate_json(json_file, source_language, detect_source_language):
        search_dict = json.load(open(json_file, "r", encoding="utf-8"))
        def translate_recursively(search_dict, field, detect_source_language):
            for key, value in search_dict.items():
                if isinstance(value, field):
                    if "https://" not in value:
                        translation = translate_text(value, source_language, detect_source_language)
                        search_dict[key] = translation

                elif isinstance(value, dict):
                    results = translate_recursively(value, field, detect_source_language)

                elif isinstance(value, (list, tuple)):
                    for item in value:
                        if isinstance(item, dict):
                            more_results = translate_recursively(item, field, detect_source_language)
                        
                        elif isinstance(item, (list, tuple)):
                            for new_item in item:
                                if isinstance(new_item, dict):
                                    more_results = translate_recursively(item, field, detect_source_language)

                                elif isinstance(new_item, field):
                                    if "https://" not in new_item:
                                        translation = translate_text(new_item, source_language, detect_source_language)
                                        item[item.index(new_item)] = translation

                        elif isinstance(item, field):
                            if "https://" not in item:
                                translation = translate_text(item, source_language, detect_source_language)
                                value[value.index(item)] = translation

                    search_dict[key] = value
                        
            return search_dict
        
        translated_dict = translate_recursively(search_dict, str, detect_source_language)
        return translated_dict

    def translate_excel(excel_file, source_language, detect_source_language):
        df = pd.read_excel(excel_file)

        for index, row in list(df.iterrows()):
            for column in list(df.columns):
                if isinstance(row[column], str):
                    translation = translate_text(row[column], source_language, detect_source_language)
                    df.replace(row[column], translation, inplace=True)

        return df

    def translate_txt(txt_file, source_language, detect_source_language):
        data = open(txt_file, "r", encoding="utf-8").readlines()
        translations = ["\n"] * len(data)

        for datum in data:
            if datum != "\n":
                translation = translate_text(datum.replace("\n", ""), source_language, detect_source_language)
                translations[data.index(datum)] = translation
            else:
                translations[data.index(datum)] = datum

        return translations

    if extension.lower() not in allowed_extensions:
        raise TypeError("Uzantı dosyası desteklenilmiyor. Lütfen desteklenilen uzantıları görmek için https://ceveri-package.readthedocs.io adresinden ÇeVeri dokümantasyonlarını ziyaret ediniz.")

    if source_language == None:
        detect_source_language = True
    else:
        detect_source_language = False

    if extension.lower() == ".json":
        translated_dict = translate_json(file, source_language, detect_source_language)
        with open(save_path, 'w', encoding="utf-8") as f:
            json.dump(translated_dict, f, indent=4, ensure_ascii=False)

    if extension.lower() == ".xlsx":
        translated_df = translate_excel(file, source_language, detect_source_language)
        translated_df.to_excel(save_path)

    if extension.lower() == ".txt":
        translation_list = translate_txt(file, source_language, detect_source_language)
        with open(save_path, "w", encoding="utf-8") as f:
            for line in translation_list:
                if line != "\n":
                    f.writelines(line+"\n")
                else:
                    f.writelines(line)

    print("Dosya başarıyla çevrildi.")
    print("Çevrilen dosyaya " + save_path + " adresinden erişebilirsiniz.")

