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
    end = models.FloatField(default=10)

class FileUpload(BaseQuestion):
    file_upload = models.FileField(upload_to="uploads/")

class SpecialField(BaseQuestion):
    special_field = models.TextField()






# --- Form Submission Model ---
class FormSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)

# --- Response Models ---
class RadioButtonResponse(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name="radio_responses")
    question = models.ForeignKey(RadioButton, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # Single choice selected

class CheckBoxResponse(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name="checkbox_responses")
    question = models.ForeignKey(CheckBox, on_delete=models.CASCADE)
    selected_choices = models.ManyToManyField(Choice)  # Multiple choices selected

class DropDownResponse(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name="dropdown_responses")
    question = models.ForeignKey(DropDown, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # Single choice selected

class ShortChoiceResponse(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name="short_text_responses")
    question = models.ForeignKey(ShortChoice, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)

class LongChoiceResponse(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name="long_text_responses")
    question = models.ForeignKey(LongChoice, on_delete=models.CASCADE)
    answer_text = models.TextField()

class RangeFieldResponse(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name="range_responses")
    question = models.ForeignKey(RangeField, on_delete=models.CASCADE)
    value = models.FloatField()

class FileUploadResponse(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name="file_upload_responses")
    question = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")

class SpecialFieldResponse(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name="special_responses")
    question = models.ForeignKey(SpecialField, on_delete=models.CASCADE)
    special_text = models.TextField()
