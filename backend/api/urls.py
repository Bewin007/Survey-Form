from django.urls import path
from .views import *

urlpatterns = [
    path("questions/create/", QuestionCreateView.as_view(), name="question-create"),
    
    path('forms/', FormView.as_view(), name='form-create'),
    path("forms/<int:pk>/questions", FormQuestionsView.as_view(), name="form-questions"),
    
    
    path("forms/<int:pk>/answers/", SubmitFormView.as_view(), name="submit-answers"),
    
    path('form-submissions/<int:id>/', FormSubmissionResponseView.as_view(), name='form-submission-response-get'),
    
    path('forms/<int:form_id>/submissions/', FormSubmissionListView.as_view(), name='form-submissions'),
    path('forms/<int:form_id>/submissions-with-answers/', FormSubmissionsWithAnswersView.as_view(), name='form-submissions-with-answers'),
]
