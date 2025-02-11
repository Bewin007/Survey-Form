# from django.db import models
# from user.models import User
# # Create your models here.

# class Forms(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     sub_title= models.CharField(max_length=255)
#     description = models.TextField()

# class Choice(models.Mode):
#     choice_text = models.CharField(max_length=255)

# class RadioButton(models.Model):
#     choice_type = models.CharField(max_length=255,null=True,blank=True)
#     question_text = models.CharField(max_length=255)
#     required = models.BooleanField()
#     options = models.ManyToManyField(Choice)

# class CheckBox(models.Model):
#     choice_type = models.CharField(max_length=255,null=True,blank=True)
#     question_text = models.CharField(max_length=255)
#     required = models.BooleanField()
#     options = models.ManyToManyField(Choice)

# class DropDown(models.Model):
#     choice_type = models.CharField(max_length=255,null=True,blank=True)
#     question_text = models.CharField(max_length=255)
#     required = models.BooleanField()
#     options = models.ManyToManyField(Choice)

# class Shotchoice(models.Model):
#     question_text = models.CharField(max_length=255)
#     required = models.BooleanField()

# class Longchoice(models.Model):
#     question_text = models.TextField()
#     required = models.BooleanField()

# class RangeField(models.Model):
#     choice_type = models.CharField(max_length=255,null=True,blank=True)
#     question_text = models.TextField()
#     start = models.FloatField(default=1,blank=True)
#     end = models.FloatField()

# class FileUpload(models.Model):
#     question_text = models.TextField()
#     required = models.BooleanField()

# class SpecialField(models.Model):
#     choice_type = models.CharField(max_length=255,null=True,blank=True)
#     question_text = models.TextField()
#     required = models.BooleanField()


    


from django.db import models
from user.models import User

class Forms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Form creator
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    description = models.TextField()

class Choice(models.Model):
    choice_text = models.CharField(max_length=255)

class BaseQuestion(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    question_text = models.TextField()
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField()  # Tracks question order

    class Meta:
        abstract = True  # This makes it an abstract base class

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who submitted
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)  # The form being submitted
    submitted_at = models.DateTimeField(auto_now_add=True)

class AnswerBase(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)  # Link to response
    question = models.ForeignKey(BaseQuestion, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True  # Makes this an abstract model

class TextAnswer(AnswerBase):
    answer_text = models.TextField()

class ChoiceAnswer(AnswerBase):
    selected_choices = models.ManyToManyField(Choice)

class RangeAnswer(AnswerBase):
    selected_value = models.FloatField()

class FileAnswer(AnswerBase):
    uploaded_file = models.FileField(upload_to="uploads/")
