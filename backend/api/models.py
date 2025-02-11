from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user.models import User

class Forms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    description = models.TextField()

class Choice(models.Model):
    choice_text = models.CharField(max_length=255)

class BaseQuestion(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    question_text = models.TextField()
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField()

    class Meta:
        abstract = True

class RadioButton(BaseQuestion):
    options = models.ManyToManyField(Choice)

class CheckBox(BaseQuestion):
    options = models.ManyToManyField(Choice)

class DropDown(BaseQuestion):
    options = models.ManyToManyField(Choice)

class ShortChoice(BaseQuestion):
    pass

class LongChoice(BaseQuestion):
    pass

class RangeField(BaseQuestion):
    start = models.FloatField(default=1)
    end = models.FloatField()

class FileUpload(BaseQuestion):
    pass

class SpecialField(BaseQuestion):
    pass

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

class AnswerBase(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True

class TextAnswer(AnswerBase):
    answer_text = models.TextField()

class ChoiceAnswer(AnswerBase):
    selected_choices = models.ManyToManyField(Choice)

class RangeAnswer(AnswerBase):
    selected_value = models.FloatField()

class FileAnswer(AnswerBase):
    uploaded_file = models.FileField(upload_to="uploads/")
