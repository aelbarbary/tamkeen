from django.contrib import admin
from .models import  *
from .forms import *

admin.site.site_header = 'TAMKEEN admin'

class AnswersInline(admin.TabularInline):
        model = Answer
        form = AnswerForm

class QuestionsInline(admin.TabularInline):
        model = Question
        form = QuestionForm
        inlines = [AnswersInline]
        show_change_link = True

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline]
    form = QuizForm

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswersInline]
    form = QuestionForm

class AnswerAdmin(admin.ModelAdmin):
    form = AnswerForm

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm

class BookReserveInline(admin.TabularInline):
        model = BookReserve
        form = BookReserveForm
        show_change_link = True

class BookAdmin(admin.ModelAdmin):
    inlines = [BookReserveInline]
    form = BookForm

class NewMemberRequestAdmin(admin.ModelAdmin):
    model = NewMemberRequest

class InquiryAdmin(admin.ModelAdmin):
    model = Inquiry

class UserAwardsInline(admin.TabularInline):
        model = UserAward

class AwardAdmin(admin.ModelAdmin):
    inlines = [UserAwardsInline]
    model = Award

class SuggestedVideoAdmin(admin.ModelAdmin):
    model = SuggestedVideo

class CheckoutAdmin(admin.ModelAdmin):
    model = Checkout

class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(NewMemberRequest, NewMemberRequestAdmin)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(SuggestedVideo, SuggestedVideoAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Attendance, AttendanceAdmin)
