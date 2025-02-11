from rest_framework import serializers
from .models import Forms, Choice, RadioButton, CheckBox, DropDown, ShortChoice, LongChoice, RangeField, FileUpload, SpecialField, Response, TextAnswer, ChoiceAnswer, RangeAnswer, FileAnswer
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class FormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = ['user','title','sub_title','description']


# Serializer for Choice model
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text']

# Base serializer for questions
class BaseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = ['id', 'question_text', 'required', 'order']

# Specific serializers for each type of question
class RadioButtonSerializer(BaseQuestionSerializer):
    options = ChoiceSerializer(many=True)

    class Meta(BaseQuestionSerializer.Meta):
        model = RadioButton
        fields = BaseQuestionSerializer.Meta.fields + ['options']

class CheckBoxSerializer(BaseQuestionSerializer):
    options = ChoiceSerializer(many=True)

    class Meta(BaseQuestionSerializer.Meta):
        model = CheckBox
        fields = BaseQuestionSerializer.Meta.fields + ['options']

class DropDownSerializer(BaseQuestionSerializer):
    options = ChoiceSerializer(many=True)

    class Meta(BaseQuestionSerializer.Meta):
        model = DropDown
        fields = BaseQuestionSerializer.Meta.fields + ['options']

class ShortChoiceSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = ShortChoice
        fields = BaseQuestionSerializer.Meta.fields

class LongChoiceSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = LongChoice
        fields = BaseQuestionSerializer.Meta.fields

class RangeFieldSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = RangeField
        fields = BaseQuestionSerializer.Meta.fields + ['start', 'end']

class FileUploadSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = FileUpload
        fields = BaseQuestionSerializer.Meta.fields

class SpecialFieldSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = SpecialField
        fields = BaseQuestionSerializer.Meta.fields

# Serializer for Forms
class FormsSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Forms
        fields = ['id', 'user', 'title', 'sub_title', 'description', 'questions']

    def get_questions(self, obj):
        questions = obj.basequestion_set.all().order_by('order')
        question_data = []

        for question in questions:
            if isinstance(question, RadioButton):
                question_data.append(RadioButtonSerializer(question).data)
            elif isinstance(question, CheckBox):
                question_data.append(CheckBoxSerializer(question).data)
            elif isinstance(question, DropDown):
                question_data.append(DropDownSerializer(question).data)
            elif isinstance(question, ShortChoice):
                question_data.append(ShortChoiceSerializer(question).data)
            elif isinstance(question, LongChoice):
                question_data.append(LongChoiceSerializer(question).data)
            elif isinstance(question, RangeField):
                question_data.append(RangeFieldSerializer(question).data)
            elif isinstance(question, FileUpload):
                question_data.append(FileUploadSerializer(question).data)
            elif isinstance(question, SpecialField):
                question_data.append(SpecialFieldSerializer(question).data)

        return question_data

# Serializer for Response model
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'user', 'form', 'submitted_at']

# Base serializer for answers
class AnswerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAnswer  # Placeholder model for AnswerBase
        fields = ['response', 'question']

# Serializer for TextAnswer model
class TextAnswerSerializer(AnswerBaseSerializer):
    answer_text = serializers.CharField()

    class Meta(AnswerBaseSerializer.Meta):
        model = TextAnswer
        fields = AnswerBaseSerializer.Meta.fields + ['answer_text']

# Serializer for ChoiceAnswer model
class ChoiceAnswerSerializer(AnswerBaseSerializer):
    selected_choices = ChoiceSerializer(many=True)

    class Meta(AnswerBaseSerializer.Meta):
        model = ChoiceAnswer
        fields = AnswerBaseSerializer.Meta.fields + ['selected_choices']

# Serializer for RangeAnswer model
class RangeAnswerSerializer(AnswerBaseSerializer):
    selected_value = serializers.FloatField()

    class Meta(AnswerBaseSerializer.Meta):
        model = RangeAnswer
        fields = AnswerBaseSerializer.Meta.fields + ['selected_value']

# Serializer for FileAnswer model
class FileAnswerSerializer(AnswerBaseSerializer):
    uploaded_file = serializers.FileField()

    class Meta(AnswerBaseSerializer.Meta):
        model = FileAnswer
        fields = AnswerBaseSerializer.Meta.fields + ['uploaded_file']
