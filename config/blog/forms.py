from django import forms
from .models import Article, Category, ArticleReturn, ArticleReport
from django.utils.html import format_html


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        STATUS_CHOICES = (
            ('d',  "پیش نویس"),
            ('p', "منتشر شده"),
        )
        self.fields['status'] = forms.ChoiceField(choices=STATUS_CHOICES, label="وضعیت", initial='d', error_messages={'invalid_choice' : "داده نامعتبری برای وضعیت وارد شده است."})
        self.fields['category'].required = False
        self.fields['title'].required = True
        self.fields['title'].error_messages = {'required' : "این فیلد را پر کنید."}
        self.fields['description'].required = True
        self.fields['description'].error_messages = {'required' : "این فیلد را پر کنید."}
        # self.fields['category'] = forms.ModelMultipleChoiceField(queryset=Category.objects.completed_category(), widget=forms.MultipleChoiceField(), required=False, label="دسته بندی")
        
    class Meta:
        model = Article
        fields = ['title', 'category', 'description', 'thumbnail', 'status']







class CategoryForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

        if self.form_request.user.is_superuser == False and self.form_request.user.is_staff == False:
            self.fields['parent'].disabled = True
            self.fields['parent'].initial = None
            self.fields['parent'].help_text = format_html("<ul>  <li>{}</li>  </ul>".format("این بخش تنها توسط ادمین اصلاح می شود."))

        self.fields['parent'] = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Category.objects.completed_category(), label="والد", required=False)
        
    class Meta:
        model = Category
        fields = ['parent', 'title']







class ArticleReturnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleReturnForm, self).__init__(*args, **kwargs)
        # self.fields['reason'].widget = forms.CheckboxSelectMultiple()
        self.fields['reason'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=ArticleReturn.REASON_CHOICES, required=False)

    class Meta:
        model = ArticleReturn
        fields = ['reason', 'description']







class ArticleReportForm(forms.ModelForm):
    class Meta:
        model = ArticleReport
        fields = ['reason', 'description']
