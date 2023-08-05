import itertools as it
import logging
import re
import string
import sys
from pathlib import Path

from enchant import request_pwl_dict
from enchant.utils import levenshtein

from ..region import DataError, TextConfig
from ..span import Span
from ..util import load_config
from ..vision import Vision

#from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
from transformers import pipeline

# b ../docint/pipeline/sents_fixer.py:87


class OfficerMisalignedError(DataError):
    pass


class OfficerMultipleError(DataError):
    num_officers: int


@Vision.factory(
    "words_fixer",
    default_config={
        "item_name": "list_items",
        "conf_dir": "conf",
        "conf_stub": "wordfix",
        "pre_edit": True,
        "dict_file": "output/pwl_words.txt",
        "lv_dist_cutoff": 1,
        "ignore_paren_len": 7,
        "unicode_file": "conf/unicode.txt",
        "officer_at_start": True,
    },
)
class WordsFixer:
    def __init__(
        self,
        item_name,
        conf_dir,
        conf_stub,
        pre_edit,
        dict_file,
        lv_dist_cutoff,
        ignore_paren_len,
        unicode_file,
        officer_at_start,
    ):


        ignore_puncts = string.punctuation
        self.punct_tbl = str.maketrans(ignore_puncts, " " * len(ignore_puncts))
        self.item_name = item_name
        self.conf_dir = conf_dir
        self.conf_stub = conf_stub
        self.pre_edit = pre_edit
        self.dict_file = Path(dict_file)
        self.lv_dist_cutoff = lv_dist_cutoff
        self.ignore_paren_len = ignore_paren_len
        self.unicode_file = unicode_file
        self.officer_at_start = officer_at_start

        self.ignore_parent_strs = [
            "harg",
            "depart",
            "defence",
            "banking",
            "indep",
            "state",
            "indapendent",
            "smt .",
            "deptt",
            "shrimati",
            "indap",
            "indop",
        ]

        u_lines = [line.split() for line in Path(self.unicode_file).read_text().split("\n") if line.strip()]
        self.unicode_dict = dict((u, a if a != "<ignore>" else "") for u, a in u_lines)

        self.dictionary = request_pwl_dict(str(self.dict_file))

        # TODO PLEASE MOVE THIS TO OPTIONS
        print('Reading model')
        
        #tokenizer = AutoTokenizer.from_pretrained("/Users/mukund/Github/huggingface/bert-base-NER")
        #model = AutoModelForTokenClassification.from_pretrained("/Users/mukund/Github/huggingface/bert-base-NER")


        #self.nlp = pipeline("ner", model=model, tokenizer=tokenizer)
        self.nlp = pipeline("ner")
        print('DONE Reading model')                

        self.test_doc = True

        self.lgr = logging.getLogger(f"docint.pipeline.{self.conf_stub}")
        self.lgr.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        self.lgr.addHandler(stream_handler)
        self.file_handler = None

    def add_log_handler(self, doc):
        handler_name = f"{doc.pdf_name}.{self.conf_stub}.log"
        log_path = Path("logs") / handler_name
        self.file_handler = logging.FileHandler(log_path, mode="w")
        self.lgr.info(f"adding handler {log_path}")

        self.file_handler.setLevel(logging.DEBUG)
        self.lgr.addHandler(self.file_handler)

    def remove_log_handler(self, doc):
        self.file_handler.flush()
        self.lgr.removeHandler(self.file_handler)
        self.file_handler = None

    def _fix_text(self, text):
        if not text.isascii():
            sys.stderr.write(f"{text}\n")
        text = text.strip()
        text = text.translate(self.punct_tbl).strip()
        return text

    def is_correctable(self, text):
        suggestions = self.dictionary.suggest(text)
        if not suggestions:
            return False

        top_suggestion = suggestions[0].lower()
        lv_dist = levenshtein(top_suggestion, text.lower())
        # print(f'\t{text}->{suggestions[0]} {lv_dist}')

        if lv_dist <= self.lv_dist_cutoff or top_suggestion.startswith(text.lower()):
            return True
        else:
            return False

    def fix_unicode(self, list_item):
        ignore_config = TextConfig(rm_labels=["ignore"], rm_nl=True)
        for text, word in list_item.iter_word_text(ignore_config):
            if not word.text.isascii():
                u_text = word.text
                if u_text in self.unicode_dict:
                    a_text = self.unicode_dict[u_text]
                    self.lgr.debug(f"UnicodeFixed: {u_text}->{a_text}")
                    list_item.replace_word_text(word, "<all>", a_text)
                else:
                    sys.stderr.write(f"NOTFOUND: {u_text}\n")

    def is_mergeable(self, text, next_word):
        if next_word is None:
            return False

        next_text = self._fix_text(next_word.text)
        if not next_text:
            return False

        merged_text = text + next_text
        if self.dictionary.check(merged_text):
            # self.lgr.debug(f"MergeFound >{text}+{next_text}<")
            return True
        elif self.is_correctable(merged_text):
            # self.lgr.debug(f"MergeCorrected {merged_text}")
            return True
        else:
            # print(f"Merge NotFound {merged_text}")
            return False

    def merge_words(self, list_item):
        merge_count = 0
        ignore_config = TextConfig(rm_labels=["ignore", "person"], rm_nl=True)

        last_merged_word, merge_words = None, []  # don't alter spans while iterating
        for word, next_word in list_item.iter_word_pairs(ignore_config):
            text = self._fix_text(word.text)

            if (
                (not word)
                or (not next_word)  # noqa: W503
                or (not text)  # noqa: W503
                or (id(word) == id(last_merged_word))  # noqa: W503
            ):
                continue

            if self.is_mergeable(text, next_word):
                self.lgr.debug(f"Merged: {word.text} {next_word.text}")
                merge_words.append((word, next_word))
                merge_count += 1
                last_merged_word = next_word

        [list_item.merge_word(word, next_word) for (word, next_word) in merge_words]
        return merge_count

    def correct_words(self, list_item):
        correct_count = 0
        ignore_config = TextConfig(rm_labels=["ignore", "person"], rm_nl=True)

        replace_words = []  # don't alter spans while iterating
        for text, word in list_item.iter_word_text(ignore_config):
            text = self._fix_text(text)
            if not word or not text:
                continue

            if self.dictionary.check(text):
                continue

            if len(text) <= 2:
                if text in ("uf", "cf", "qf", "nf", "af", "bf"):
                    replace_words.append((word, "of"))
                    self.lgr.debug(f"SpellCorrected {text} -> of")
                    correct_count += 1
                else:
                    pass
            elif self.is_correctable(text):
                suggestions = self.dictionary.suggest(text)
                self.lgr.debug(f"SpellCorrected {text} -> {suggestions[0]}")
                replace_words.append((word, suggestions[0]))
                correct_count += 1
            else:
                self.lgr.debug(f"SpellNOTFOUND {text}")
        [list_item.replace_word_text(w, "<all>", t) for (w, t) in replace_words]
        return correct_count

    def mark_names2(self, list_item):
        ignore_config = TextConfig(rm_labels=["ignore"], rm_nl=True)
        line_text = list_item.line_text(ignore_config)

        ner_results = self.nlp(line_text)
        ner_results = [r for r in ner_results if r["entity"].endswith("-PER")]
        officer_spans = [Span(r["start"], r["end"]) for r in ner_results]

        # FIX THIS
        officer_spans = Span.reduce(officer_spans, line_text, " .,")

        list_item.add_spans(officer_spans, "officer", ignore_config)

    def mark_names(self, list_item):
        def get_person_spans(ner_results, line_text):
            def is_mergeable(last_end, new_start):
                if last_end == new_start:
                    return True
                elif line_text[last_end:new_start].strip(" .") == "":
                    return True
                else:
                    return False

            def merge_spans(spans, ner_result):
                # first time, change spans
                if isinstance(spans, dict):
                    first_start, first_end = spans["start"], spans["end"]
                    spans = [(first_start, first_end)]

                last_start, last_end = spans[-1]
                if is_mergeable(last_end, ner_result["start"]):
                    spans[-1] = (last_start, ner_result["end"])
                else:
                    spans.append((ner_result["start"], ner_result["end"]))
                return spans

            person_spans = [r for r in ner_results if r["entity"].endswith("-PER")]
            person_spans.sort(key=lambda r: r["start"])
            if not person_spans:
                return []
            elif len(person_spans) == 1:
                return [(person_spans[0]["start"], person_spans[0]["end"])]

            *_, final_spans = it.accumulate(person_spans, func=merge_spans)
            return final_spans

        # correct_count = 0
        ignore_config = TextConfig(rm_labels=["ignore"], rm_nl=True)
        line_text = list_item.line_text(ignore_config)

        ner_results = self.nlp(line_text)
        # self.lgr.debug(ner_results)

        # per_names = [r["word"] for r in ner_results if r["entity"].endswith("-PER")]
        # self.lgr.debug(', '.join(per_names))

        person_spans = get_person_spans(ner_results, line_text)
        for start, end in person_spans:
            start = min(start, 0) if start < 25 else start
            list_item.add_span(start, end, "person", ignore_config)
            # self.lgr.debug(f'PERSON {line_text[start:end]}')

        person_spans = list_item.get_spans("person")
        if not person_spans:
            return

        # TODO THIS IS ONLY FOR SENTENCES THAT START WITH NAME
        # 1_Upload_2791 has the name in the middle !!!
        # Mohd. Taslimuddin has two spans >Mohd.< and >d. Taslimuddin<

        merged_spans = Span.accumulate(person_spans)
        # move to word boundary
        first_span = merged_spans[0]
        boundary_char = line_text[first_span.end].translate(self.punct_tbl).strip()
        if boundary_char and boundary_char != " ":
            name = line_text[first_span.start : first_span.end]  # noqa: E203
            try:
                new_end = line_text.index(" ", first_span.end)
                first_span.end = new_end
                new_name = line_text[first_span.start : first_span.end]  # noqa: E203
                self.lgr.debug(f"NameExpansion: {name}->{new_name}")
            except Exception as e:  # noqa: F841
                pass

        list_item.label_spans["person"] = merged_spans

    def mark_manual_words(self, list_item):
        if list_item.get_spans("person"):
            return 0

        ignore_config = TextConfig(rm_labels=["ignore"], rm_nl=True)
        line_text = list_item.line_text(ignore_config)
        pm_words = ("the prime minister", "prime minister", "p.m.")
        pm_word = [w for w in pm_words if line_text.lower().startswith(w)]
        if pm_word:
            pm_word = pm_word[0]
            start = line_text.lower().index(pm_word)
            end = start + len(pm_word)
            list_item.add_span(start, end, "person", ignore_config)
            self.lgr.debug(f"PERSON {line_text[start:end]}")
            return 1
        else:
            return 0

    def blank_paren_words(self, list_item):
        text_config = TextConfig(rm_nl=True)
        line_text = list_item.line_text(text_config)

        # char_list = list(line_text)
        paren_count = 0
        for m in re.finditer(r"\((.*?)\)", line_text):
            mat_str = m.group(1).lower()
            if len(mat_str) < self.ignore_paren_len:
                continue
            elif any([sl in mat_str for sl in self.ignore_parent_strs]):
                continue
            else:
                s, e = m.span()
                self.lgr.debug(f"BLANKPAREN: {m.group(0)} ->[{s}: {e}]")
                # list_item.blank_line_text_no_nl(s, e)
                list_item.add_span(s, e, "ignore", text_config)
                paren_count += 1
        # end for
        return paren_count

    def blank_punct(self, list_item):
        ignore_config = TextConfig(rm_labels=["ignore", "person"], rm_nl=True)
        line_text = list_item.line_text(ignore_config)
        punct_count = 0

        ignore_spans = []

        for m in re.finditer(r"[.,;\']", line_text):
            s, e = m.span()
            ignore_spans.append((s, e))
            punct_count += 1

        for m in re.finditer("in the", line_text):
            s, e = m.span()
            ignore_spans.append((s, e))
            punct_count += 1

        ignore_spans.sort()
        self.lgr.debug(list_item.str_spans())
        for (s, e) in reversed(ignore_spans):
            list_item.add_span(s, e, "ignore", ignore_config)

        return punct_count

    def fix_list(self, list_item):
        paren_count = self.blank_paren_words(list_item)  # noqa: F841

        unicode_count = self.fix_unicode(list_item)  # noqa: F841

        name_count = self.mark_names(list_item)  # noqa: F841

        merge_count = self.merge_words(list_item)  # noqa: F841

        # self.lgr.debug(f'B>{list_item.line_text_no_nl()}')

        correct_count = self.correct_words(list_item)  # noqa: F841

        manual_count = self.mark_manual_words(list_item)  # noqa: F841

        punct_count = self.blank_punct(list_item)  # noqa: F841

        return merge_count, correct_count

    def test(self, list_item, path):
        person_spans = list_item.get_spans("person")
        non_zero_spans = [s for s in person_spans if s.start != 0]

        errors = []

        if self.officer_at_start and non_zero_spans:
            msg = f'incorrect span: {",".join(str(s) for s in non_zero_spans)}'
            errors.append(OfficerMisalignedError(path=path, msg=msg))

        if len(person_spans) > 2:
            msg = f'incorrect span: {",".join(str(s) for s in person_spans)}'
            errors.append(OfficerMultipleError(path=path, msg=msg, num_officers=len(person_spans)))
        return errors

    def set_config(self, doc_config):
        old_config = {}
        for (k, v) in doc_config:
            if k != "edits" and (getattr(self, k, None) is not None):
                old_config[k] = getattr(self, k)
                setattr(self, k, doc_config[k])
        return old_config

    def revert_config(self, old_config):
        for k, v in old_config:
            setattr(self, k, v)

    def __call__(self, doc):
        self.add_log_handler(doc)
        self.lgr.info(f"word_fixer: {doc.pdf_name}")

        doc_config = load_config(self.conf_dir, doc.pdf_name, self.conf_stub)
        old_officer_at_start = self.officer_at_start
        self.officer_at_start = doc_config.get("officer_at_start", self.officer_at_start)

        if self.pre_edit:
            edits = doc_config.get("edits", [])
            if edits:
                print(f"Edited document: {doc.pdf_name}")
                doc.edit(edits)

        NL = "\n"
        for page_idx, page in enumerate(doc.pages):
            # access what to fix through path
            items = getattr(page, self.item_name, [])
            for (list_idx, list_item) in enumerate(items):
                item_path = f"pa{page.page_idx}.{self.item_name[:2]}{list_idx}"
                indent_str = f"{doc.pdf_name}:{page_idx}>{list_idx}"  # noqa: F841

                self.lgr.debug(f'\n{list_item.line_text().replace(NL, " ")}<')
                self.fix_list(list_item)
                list_item_errors = self.test(list_item, item_path)

                list_item.errors += list_item_errors
                if type(list_item).__name__ == "ListItem":
                    list_item.list_errors += list_item_errors

                err_str = list_item.error_counts_str
                self.lgr.debug(list_item.str_spans())
                if err_str:
                    self.lgr.debug(f"error: {err_str}")

                self.lgr.debug(f'A>{list_item.line_text().replace(NL, " ")}<\n')

        # self.revert_config(old_config)
        self.officer_at_start = old_officer_at_start
        self.remove_log_handler(doc)
        return doc
