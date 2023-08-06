# Copyright © 2022 BAAI. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License")
import importlib
import os

from  flagai.model.file_utils import _get_model_id, _get_vocab_path
import copy


class LazyImport(object):

    def __init__(self, name):
        self.cache = {}
        self.mod_name = name

    def __getattr__(self, name):
        mod = self.cache.get(self.mod_name)
        if not mod:
            mod = importlib.import_module(self.mod_name)
            self.cache[self.mod_name] = mod
        return getattr(mod, name)


ALL_TASK = {
    "bert_lm": ["flagai.model.bert_model", "BertModel"],
    "bert_seq2seq": ["flagai.model.bert_model", "BertForSeq2seq"],
    "bert_title-generation": ["flagai.model.bert_model", "BertForSeq2seq"],
    "bert_masklm": ["flagai.model.bert_model", "BertForMaskLM"],
    "bert_sequence-labeling":
    ["flagai.model.bert_model", "BertForSequenceLabeling"],
    "bert_sequence-labeling-crf":
    ["flagai.model.bert_model", "BertForSequenceLabeling"],
    "bert_sequence-labeling-gp":
    ["flagai.model.bert_model", "BertForSequenceLabeling"],
    "bert_ner": ["flagai.model.bert_model", "BertForSequenceLabeling"],
    "bert_ner-crf": ["flagai.model.bert_model", "BertForSequenceLabelingCRF"],
    "bert_ner-gp": ["flagai.model.bert_model", "BertForSequenceLabelingGP"],
    "bert_embedding": ["flagai.model.bert_model", "BertForEmbedding"],
    "bert_classification": ["flagai.model.bert_model", "BertForClsClassifier"],
    "bert_semantic-matching":
    ["flagai.model.bert_model", "BertForClsClassifier"],
    "gpt2_seq2seq": ("flagai.model.gpt2_model", "GPT2Model"),
    "gpt2_lm": ("flagai.model.gpt2_model", "GPT2Model"),
    "cpm_seq2seq": ("flagai.model.gpt2_model", "GPT2Model"),
    "cpm_lm": ("flagai.model.gpt2_model", "GPT2Model"),
    "t5_seq2seq": ["flagai.model.t5_model", "T5Model"],
    "t5_lm": ["flagai.model.t5_model", "T5Model"],
    "glm_lm": ["flagai.model.glm_model", "GLMModel"],
    "glm_seq2seq": ["flagai.model.glm_model", "GLMForSeq2Seq"],
    "glm_poetry": ["flagai.model.glm_model", "GLMForSeq2Seq"],
    "glm_classification":
    ["flagai.model.glm_model", "GLMForSequenceClassification"],
    "glm_title-generation": ["flagai.model.glm_model", "GLMForSeq2Seq"],
    "opt_seq2seq": ("flagai.model.opt_model","OPTModel"),
    "opt_lm": ("flagai.model.opt_model","OPTModel"),
    "vit_classification": ("flagai.model.vision.vit", "VisionTransformer")

}

MODEL_DICT = {
    "bert-base-en": ["flagai.model.bert_model", "BertModel", "bert", "nlp"],
    "roberta-base-ch": ["flagai.model.bert_model", "BertModel", "bert", "nlp"],
    "t5-base-en": ["flagai.model.t5_model", "T5Model", "t5", "nlp"],
    "t5-base-ch": ["flagai.model.t5_model", "T5Model", "t5", "nlp"],
    "glm-large-ch": ["flagai.model.glm_model", "GLMModel", "glm", "nlp"],
    "glm-large-en": ["flagai.model.glm_model", "GLMModel", "glm", "nlp"],
    "gpt2-base-ch": ["flagai.model.gpt2_model", "GPT2Model", "gpt2", "nlp"],
    "cpm-large-ch": ["flagai.model.gpt2_model", "GPT2Model", "cpm", "nlp"],
    "opt-125m-en": ["flagai.model.opt_model","OPTModel", "opt", "nlp"],
    "opt-350m-en": ["flagai.model.opt_model","OPTModel", "opt", "nlp"],
    "opt-1.3b-en": ["flagai.model.opt_model","OPTModel", "opt", "nlp"],
    "opt-2.7b-en": ["flagai.model.opt_model","OPTModel", "opt", "nlp"],
    "opt-6.7b-en": ["flagai.model.opt_model","OPTModel", "opt", "nlp"],
    "opt-13b-en": ["flagai.model.opt_model","OPTModel", "opt", "nlp"],
    "opt-30b-en": ["flagai.model.opt_model","OPTModel", "opt", "nlp"],
    "opt-66b-en": ["flagai.model.opt_model","OPTModel", "opt", "nlp"],
    "glm-10b-ch": ["flagai.model.glm_model", "GLMModel", "glm", "nlp"],

    "vit-base-p16-224":["flagai.model.vision.vit", "VisionTransformer", "vit", "vision"],
    "vit-base-p16-384":["flagai.model.vision.vit", "VisionTransformer", "vit", "vision"],
    "vit-base-p32-224":["flagai.model.vision.vit", "VisionTransformer", "vit", "vision"],
    "vit-base-p32-384":["flagai.model.vision.vit", "VisionTransformer", "vit", "vision"],
    "vit-large-p16-224":["flagai.model.vision.vit", "VisionTransformer", "vit", "vision"],
    "vit-large-p16-384":["flagai.model.vision.vit", "VisionTransformer", "vit", "vision"],
    "vit-large-p32-224":["flagai.model.vision.vit", "VisionTransformer", "vit", "vision"],
    "vit-large-p32-384":["flagai.model.vision.vit", "VisionTransformer", "vit", "vision"],
}

TOKENIZER_DICT = {
    "bert-base-en": ["flagai.data.tokenizer.bert.bert_tokenizer", "BertTokenizer"],
    "roberta-base-ch": ["flagai.data.tokenizer.bert.bert_tokenizer", "BertTokenizer"],
    "t5-base-en": ["flagai.data.tokenizer.t5.t5_pegasus_tokenizer", "T5PegasusTokenizer"],
    "t5-base-ch": ["flagai.data.tokenizer.t5.t5_pegasus_tokenizer", "T5PegasusTokenizer"],
    "glm-large-ch": [
        "flagai.data.tokenizer.glm_large_ch.glm_large_ch_tokenizer",
        "GLMLargeChTokenizer"
    ],
    "glm-large-en": [
        "flagai.data.tokenizer.glm_large_en.glm_large_en_tokenizer",
        "GLMLargeEnWordPieceTokenizer"
    ],
    "glm-10b-ch": [
        "flagai.data.tokenizer.glm_large_ch.glm_large_ch_tokenizer",
        "GLMLargeChTokenizer"
    ],
    "gpt2-base-ch": ["flagai.data.tokenizer.bert.bert_tokenizer", "BertTokenizer"],
    "cpm-large-ch": ["flagai.data.tokenizer.cpm_1.cpm1_tokenizer", "CPMTokenizer"],
    "opt-125m-en": ["flagai.data.tokenizer.opt.opt_en_tokenizer","OPTTokenizer"],
    "opt-350m-en": ["flagai.data.tokenizer.opt.opt_en_tokenizer","OPTTokenizer"],
    "opt-1.3b-en": ["flagai.data.tokenizer.opt.opt_en_tokenizer","OPTTokenizer"],
    "opt-2.7b-en": ["flagai.data.tokenizer.opt.opt_en_tokenizer","OPTTokenizer"],
    "opt-6.7b-en": ["flagai.data.tokenizer.opt.opt_en_tokenizer","OPTTokenizer"],
    "opt-13b-en": ["flagai.data.tokenizer.opt.opt_en_tokenizer","OPTTokenizer"],
    "opt-30b-en": ["flagai.data.tokenizer.opt.opt_en_tokenizer","OPTTokenizer"],
    "opt-66b-en": ["flagai.data.tokenizer.opt.opt_en_tokenizer","OPTTokenizer"],
}

class AutoLoader:

    def __init__(self,
                 task_name: str = "lm",
                 model_name: str = "RoBERTa-base-ch",
                 model_dir: str = "./checkpoints/",
                 only_download_config: bool = False,
                 device="cpu",
                 **kwargs):
        """
        Args:
            task_name: The task name, for example, "cls" for classification,
                      "sequence_labeling" for ner, part-of-speech tagging
                       and so on, "seq2seq" for sequence to sequence task.
            model_name: The model name, for example, "BERT-base-ch",
                        "RoBERTa-base-ch", "GPT2-base-ch",
                        "T5-base-ch" and so on.
            model_dir: The first level of the model download directory.
            load_pretrain_params: Whether to load the downloaded parameters.
            target_size: For the classification task, all labels size.
            inner_dim: For global pointer ner task, inner_dim is the
                       representation dim of start and end tokens.
        Examples::

            # load BERT-base-ch model and tokenizer to do the two
            # classification task of text.
            # Then the download path of config, model, vocab files is the
            # "./checkpoints/BERT-base-ch"
            >>> auto_loader = AutoLoader(task_name,
                                         model_name="BERT-base-ch",
                                         model_dir="checkpoints",
                                         load_pretrain_params=True,
                                         class_num=2)

        """
        
        raw_model_name = copy.deepcopy(model_name)

        model_name = model_name.lower()

        if model_name not in MODEL_DICT:
            print(f"The model_name: {model_name} is not be supported")
            print(f"All supported models are {list(MODEL_DICT.keys())}")
            return

        brief_model_name = MODEL_DICT[model_name][2]
        model_type = MODEL_DICT[model_name][3]

        # The dir to save config, vocab and model.

        self.model_name = ALL_TASK.get(f"{brief_model_name}_{task_name}", None)
        if self.model_name is None:
            print(f"For the model_name: {model_name}, task_name: {task_name} \
                is not be supported.")
            tasks = self.get_task_name(brief_model_name)
            print(
                f"For the model_name: {model_name}, these tasks are be supported: {tasks}"
            )
            return


        model_id = _get_model_id(f"{raw_model_name}-{task_name}")
        if model_id != 'null':
            model_name_ = f"{raw_model_name}-{task_name}"
        else:
            model_name_ = raw_model_name
        download_path = os.path.join(model_dir, model_name_)
        os.makedirs(download_path, exist_ok=True)
        self.model = getattr(LazyImport(self.model_name[0]),
                             self.model_name[1]).from_pretrain(
                                 download_path=model_dir,
                                 model_name=model_name_,
                                 only_download_config=only_download_config,
                                 device=device,
                                 **kwargs)

        model_id = _get_model_id(model_name)

        print("*"*20, task_name, model_id, model_name)
        if model_type == "nlp":
            if "glm" in model_name and "ch" in model_name:
                vocab_file = os.path.join(download_path,'cog-pretrained.model')
                if not os.path.exists(vocab_file):
                    vocab_file = _get_vocab_path(download_path, "cog-pretrain.model", model_id)
            elif "glm" in model_name and "en" in model_name:
                vocab_file = "GLM-large-en"
            elif model_name == "cpm-large-ch":
                # two files to load
                vocab_file_1 = os.path.join(download_path, "vocab.json")
                vocab_file_2 = os.path.join(download_path, "chinese_vocab.model")
                if not os.path.exists(vocab_file_1):
                    vocab_file_1 = _get_vocab_path(download_path, "vocab.json",
                                                   model_id)
                if not os.path.exists(vocab_file_2):
                    vocab_file_2 = _get_vocab_path(download_path,
                                                   "chinese_vocab.model", model_id)
            else:
                vocab_file = os.path.join(download_path, 'vocab.txt')
                if not os.path.exists(vocab_file):
                    vocab_file = _get_vocab_path(download_path, "vocab.txt",
                                                 model_id)
            tokenizer_class = TOKENIZER_DICT[model_name]
            tokenizer_class = getattr(LazyImport(tokenizer_class[0]),
                                        tokenizer_class[1])
            if model_name == "cpm-large-ch":
                self.tokenizer = tokenizer_class(vocab_file_1, vocab_file_2)
            elif brief_model_name == "opt":
                self.tokenizer = tokenizer_class("facebook/opt-350m")
            elif model_name in ["glm-large-en", "glm-large-ch"]:
                self.tokenizer = tokenizer_class()
            else :
                self.tokenizer = tokenizer_class(vocab_file)
        elif model_type == "vision":
            self.tokenizer = None

    def get_task_name(self, brief_model_name):
        all_model_task = list(ALL_TASK.keys())
        model_tasks = [t for t in all_model_task if brief_model_name in t]
        tasks = [t.split("_")[-1] for t in model_tasks]
        tasks = list(set(tasks))
        return tasks

    def get_tokenizer(self):
        return self.tokenizer

    def get_model(self):
        return self.model

    def load_pretrain_params(self, model_path):
        self.model.load_huggingface_weights(model_path)

        print(f"Loading done: {model_path}")
