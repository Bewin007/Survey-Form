from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Forms, Choice, RadioButton, CheckBox, DropDown, ShortChoice, LongChoice, 
    RangeField, FileUpload, SpecialField, Response, TextAnswer, ChoiceAnswer, 
    RangeAnswer, FileAnswer
)

@admin.register(Forms)
class FormsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'sub_title')
    search_fields = ('title', 'user__username')
    list_filter = ('user',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_text')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'form', 'required', 'order')
    search_fields = ('question_text',)
    list_filter = ('form',)

admin.site.register(RadioButton, QuestionAdmin)
admin.site.register(CheckBox, QuestionAdmin)
admin.site.register(DropDown, QuestionAdmin)
admin.site.register(ShortChoice, QuestionAdmin)
admin.site.register(LongChoice, QuestionAdmin)
admin.site.register(RangeField, QuestionAdmin)
admin.site.register(FileUpload, QuestionAdmin)
admin.site.register(SpecialField, QuestionAdmin)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'form', 'submitted_at')
    search_fields = ('user__username', 'form__title')
    list_filter = ('form',)

# Generic Inline for Answers
class AnswerInline(GenericTabularInline):
    extra = 1
    readonly_fields = ('content_type', 'object_id')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'response', 'content_type', 'object_id')
    search_fields = ('response__form__title',)

admin.site.register(TextAnswer, AnswerAdmin)
admin.site.register(ChoiceAnswer, AnswerAdmin)
admin.site.register(RangeAnswer, AnswerAdmin)
admin.site.register(FileAnswer, AnswerAdmin)
