import icu as icu
import operator
import os
import re
from enum import Enum
from functools import lru_cache
from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.annotator import AnnotatorParameters, AnnotatorBase
from pymultirole_plugins.v1.schema import Document, Category, Sentence
from transformers import pipeline, ZeroShotClassificationPipeline
from typing import Type, List, cast, Optional

_home = os.path.expanduser("~")
xdg_cache_home = os.environ.get("XDG_CACHE_HOME") or os.path.join(_home, ".cache")


class TrfModel(str, Enum):
    distilbert_base_uncased_mnli = "typeform/distilbert-base-uncased-mnli"
    camembert_base_xnli = "BaptisteDoyen/camembert-base-xnli"
    mDeBERTa_v3_base_mnli_xnli = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"


class ProcessingUnit(str, Enum):
    document = "document"
    segment = "segment"


class ZeroShotClassifierParameters(AnnotatorParameters):
    model: TrfModel = Field(
        TrfModel.distilbert_base_uncased_mnli,
        description="""Which [Transformers model)(
                            https://huggingface.co/models?pipeline_tag=zero-shot-classification) fine-tuned
                            for Zero-shot classification to use, can be one of:<br/>
                            <li>`typeform/distilbert-base-uncased-mnli`: This is the uncased DistilBERT model
                            fine-tuned on Multi-Genre Natural Language Inference (MNLI) dataset for the
                            zero-shot classification task. The model is not case-sensitive, i.e., it does not
                            make a difference between "english" and "English".
                            <li>`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`: This multilingual model can perform natural
                            language inference (NLI) on 100 languages and is therefore also suitable for multilingual
                            zero-shot classification.
                            <li>`BaptisteDoyen/camembert-base-xnli`: Camembert-base model fine-tuned on french
                            part of XNLI dataset.""",
    )
    model_str: str = Field(
        None,
        description="""Which [Transformers model)(
                            https://huggingface.co/models?pipeline_tag=zero-shot-classification) fine-tuned
                            for Zero-shot classification to use.""",
    )
    processing_unit: ProcessingUnit = Field(
        ProcessingUnit.document,
        description="""The processing unit to apply the classification in the input
                                            documents, can be one of:<br/>
                                            <li>`document`
                                            <li>`segment`""",
    )
    candidate_labels: str = Field(
        "sport,politics,science",
        description="""The comma-separated list of possible class labels to classify
                                        each sequence into. For example `\"sport,politics,science\"`""",
    )
    multi_label: bool = Field(
        False, description="Whether or not multiple candidate labels can be true."
    )
    multi_label_threshold: float = Field(
        0.5, description="If multi-label you can set the threshold to make predictions."
    )
    hypothesis_template: Optional[str] = Field(
        None,
        description="""The template used to turn each label into an NLI-style
                                               hypothesis. This template must include a {} for the
                                               candidate label to be inserted into the template. For
                                               example, the default template in english is
                                               `\"This example is {}.\"`""",
    )


class ZeroShotClassifierAnnotator(AnnotatorBase):
    """[🤗 Transformers](https://huggingface.co/transformers/index.html) Zero-shot classifier."""

    # cache_dir = os.path.join(xdg_cache_home, 'trankit')

    def annotate(
        self, documents: List[Document], parameters: AnnotatorParameters
    ) -> List[Document]:
        params: ZeroShotClassifierParameters = cast(
            ZeroShotClassifierParameters, parameters
        )
        if params.hypothesis_template is None or not params.hypothesis_template.strip():
            if params.model == TrfModel.distilbert_base_uncased_mnli:
                params.hypothesis_template = "This example is {}."
            elif params.model == TrfModel.camembert_base_xnli:
                params.hypothesis_template = "Ce texte parle de {}."
        model = params.model_str if params.model_str is not None else params.model.value
        # Create cached pipeline context with model
        p: ZeroShotClassificationPipeline = get_pipeline(model)
        candidate_labels = comma_separated_to_list(params.candidate_labels)
        if params.processing_unit == ProcessingUnit.document:
            dtexts = [document.text for document in documents]
            results = p(
                dtexts, candidate_labels, hypothesis_template=params.hypothesis_template
            )
            for doc, result in zip(documents, results):
                doc.categories = compute_categories(
                    result, params.multi_label_threshold, params.multi_label
                )
        else:
            for document in documents:
                if not document.sentences:
                    document.sentences = [Sentence(start=0, end=len(document.text))]
                stexts = [document.text[s.start : s.end] for s in document.sentences]
                results = p(
                    stexts,
                    candidate_labels,
                    hypothesis_template=params.hypothesis_template,
                )
                for sent, result in zip(document.sentences, results):
                    sent.categories = compute_categories(
                        result, params.multi_label_threshold, params.multi_label
                    )
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ZeroShotClassifierParameters


def compute_categories(
    result: dict, multi_label_threshold, multi_label=False
) -> List[Category]:
    cats: List[Category] = []
    if multi_label:
        for label, score in zip(result["labels"], result["scores"]):
            if score > multi_label_threshold:
                cats.append(Category(label=label, score=score))
    else:
        index, score = max(enumerate(result["scores"]), key=operator.itemgetter(1))
        label = result["labels"][index]
        cats.append(Category(label=label, score=score))
    return cats


@lru_cache(maxsize=None)
def get_pipeline(model):
    p = pipeline("zero-shot-classification", model=model)
    return p


nonAlphanum = re.compile(r"[\W]+", flags=re.ASCII)
underscores = re.compile("_{2,}", flags=re.ASCII)
trailingAndLeadingUnderscores = re.compile(r"^_+|_+\$", flags=re.ASCII)
# see http://userguide.icu-project.org/transforms/general
transliterator = icu.Transliterator.createInstance(
    "Any-Latin; NFD; [:Nonspacing Mark:] Remove; NFC; Latin-ASCII; Lower;",
    icu.UTransDirection.FORWARD,
)


def sanitize_label(string):
    result = transliterator.transliterate(string)
    result = re.sub(nonAlphanum, "_", result)
    result = re.sub(underscores, "_", result)
    result = re.sub(trailingAndLeadingUnderscores, "", result)
    return result
