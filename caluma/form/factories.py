from factory import Faker, LazyAttribute, Maybe, SubFactory

from ..core.factories import DjangoModelFactory
from . import models


class FormFactory(DjangoModelFactory):
    slug = Faker("slug")
    name = Faker("multilang", faker_provider="name")
    description = Faker("multilang", faker_provider="text")
    meta = {}
    is_published = False
    is_archived = False

    class Meta:
        model = models.Form


class QuestionFactory(DjangoModelFactory):
    slug = Faker("slug")
    label = Faker("multilang", faker_provider="name")
    type = Faker("word", ext_word_list=models.Question.TYPE_CHOICES)
    is_required = "true"
    is_hidden = "false"
    configuration = {}
    meta = {}
    is_archived = False

    row_form = Maybe(
        "is_table", yes_declaration=SubFactory(FormFactory), no_declaration=None
    )
    sub_form = Maybe(
        "is_form", yes_declaration=SubFactory(FormFactory), no_declaration=None
    )

    class Meta:
        model = models.Question

    class Params:
        is_table = LazyAttribute(lambda q: q.type == models.Question.TYPE_TABLE)
        is_form = LazyAttribute(lambda q: q.type == models.Question.TYPE_FORM)


class OptionFactory(DjangoModelFactory):
    slug = Faker("slug")
    label = Faker("multilang", faker_provider="name")
    meta = {}

    class Meta:
        model = models.Option


class QuestionOptionFactory(DjangoModelFactory):
    option = SubFactory(OptionFactory)
    question = SubFactory(QuestionFactory)
    sort = 0

    class Meta:
        model = models.QuestionOption


class FormQuestionFactory(DjangoModelFactory):
    form = SubFactory(FormFactory)
    question = SubFactory(QuestionFactory)
    sort = 0

    class Meta:
        model = models.FormQuestion


class DocumentFactory(DjangoModelFactory):
    form = SubFactory(FormFactory)
    family = None
    meta = {}

    class Meta:
        model = models.Document


class AnswerFactory(DjangoModelFactory):
    question = SubFactory(QuestionFactory)
    document = SubFactory(DocumentFactory)
    date = None
    meta = {}

    value = Maybe("is_plain", yes_declaration=Faker("name"), no_declaration=None)
    value_document = Maybe(
        "is_form", yes_declaration=SubFactory(DocumentFactory), no_declaration=None
    )

    class Meta:
        model = models.Answer

    class Params:
        is_plain = LazyAttribute(
            lambda a: a.question.type
            not in [models.Question.TYPE_FORM, models.Question.TYPE_TABLE]
        )
        is_form = LazyAttribute(lambda a: a.question.type == models.Question.TYPE_FORM)


class AnswerDocumentFactory(DjangoModelFactory):
    answer = SubFactory(AnswerFactory)
    document = SubFactory(DocumentFactory)
    sort = 0

    class Meta:
        model = models.AnswerDocument


class FileFactory(DjangoModelFactory):
    name = Faker("file_name")

    class Meta:
        model = models.File
