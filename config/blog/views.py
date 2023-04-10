from urllib import request
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import ArticleForm, CategoryForm, ArticleReturnForm, ArticleReportForm
from .models import Article, Category, ArticleReturn
from .models import ArticleReport as ArticleReportModel
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import ArticleManagingMixin, CategoryManagingMixin, ArticleViewingMixin, CategoryViewingMixin
from django.views import View
from django.http import Http404
# Create your views here.



class AddArticle(LoginRequiredMixin, CreateView):
    template_name = 'blog/article-add-edit.html'
    form_class = ArticleForm
    model = Article
    success_url = reverse_lazy('ArticleList')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)





class ArticleList(ListView):
    model = Article
    template_name = 'blog/article-list.html'
    paginate_by = 8

    def get_queryset(self):
        if self.request.user.is_authenticated == False:
            return get_list_or_404(Article.objects.published_article())
        else:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                return get_list_or_404(Article.objects.published_article())
            else:
                isReported = self.request.GET.get('isReported')
                if isReported == 'F' or None:
                    return get_list_or_404(Article.objects.published_article())
                elif isReported == 'T':
                    return get_list_or_404(Article.objects.reported_article())
                else:
                    return get_list_or_404(Article.objects.published_article())




class SpecificArticleReportsList(ListView):
    model = ArticleReportModel
    template_name = 'blog/article-list.html'
    paginate_by = 8

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        global reportedArticle
        reportedArticle = get_object_or_404(Article, status='p', slug=slug)
        return get_list_or_404(ArticleReportModel, article=reportedArticle, is_checked=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportedArticle'] = reportedArticle
        return context





class ArticleDetail(ArticleViewingMixin, DetailView):
    model = Article
    template_name = 'blog/article-detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        global article
        article = get_object_or_404(Article, slug=slug)
        return article
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['commnet_list'] = article.article_comment.all()
    #     return context





class EditArticle(ArticleManagingMixin, UpdateView):
    model = Article
    template_name = 'blog/article-add-edit.html'
    form_class = ArticleForm
    success_url = reverse_lazy('ArticleList')

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, slug=slug)





class DeleteArticle(ArticleManagingMixin, DeleteView):
    model = Article
    template_name = 'blog/article-delete.html'
    success_url = reverse_lazy('ArticleList')





class CategoryList(ListView):
    model = Category
    template_name = 'blog/category-list.html'
    paginate_by = 6

    def get_queryset(self):
        global requestedStatus
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or self.request.user.is_staff:
                categoryStatus = self.request.GET.get('categoryStatus')
                if categoryStatus == 'p' or categoryStatus == None:
                    requestedStatus = 'p'
                    return Category.objects.completed_category()
                elif categoryStatus == 'd':
                    requestedStatus = 'd'
                    return Category.objects.drafted_category()
                else:
                    requestedStatus = 'p'
                    return Category.objects.completed_category()
            else:
                requestedStatus = 'p'
                return Category.objects.completed_category()
        else:
            requestedStatus = 'p'
            return Category.objects.completed_category()




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requestedStatus'] = requestedStatus
        return context






class CategoryDetail(CategoryViewingMixin, ListView):
    model = Article
    template_name = 'blog/category-detail.html'
    paginate_by = 8

    # def dispatch(self, request, *args, **kwargs):
    #     slug = self.kwargs.get('slug')
    #     global category
    #     category = get_object_or_404(Category, slug=slug)
    #     if category.status == 'p':
    #         return super().dispatch(request, *args, **kwargs)
    #     else:
    #         raise Http404('دسترسی لازم را ندارید.')

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        global category
        category = get_object_or_404(Category, slug=slug)
        return Article.objects.published_article().filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context





class AddCategory(CreateView):
    model = Category
    template_name = 'blog/category-add.html'
    form_class = CategoryForm
    success_url = reverse_lazy('ArticleList')

    def get_form_kwargs(self):
        kwargs = super(AddCategory, self).get_form_kwargs()
        kwargs.update({ 'request' : self.request })
        return kwargs
    
    def form_valid(self, form):
        title = form.instance.title
        try:
            Category.objects.get(title__iexact = title)
        except Category.DoesNotExist:
            if self.request.user.is_superuser or self.request.user.is_staff:
                # parentPK = form.instance.parent.pk
                # if parentPK == form.instance.pk:
                #     form.add_error('parent', "یک دسته بندی نمی تواند زیرمجموعه ای از خودش باشد.")
                #     return super().form_invalid()
                form.instance.status = 'p'
            else:
                form.instance.status = 'd'
        else:
            form.add_error('parent', "این دسته بندی وجود دارد.")
            return super().form_invalid(form)
        return super().form_valid(form)





class EditCategory(CategoryManagingMixin, UpdateView):
    model = Category
    template_name = 'blog/category-edit.html'
    form_class = CategoryForm
    success_url = reverse_lazy('ArticleList')

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug)

    def get_form_kwargs(self):
        kwargs = super(EditCategory, self).get_form_kwargs()
        kwargs.update({ 'request' : self.request })
        return kwargs
    
    def form_valid(self, form):
        title = form.instance.title
        pk = form.instance.pk
        categoryObjectList = Category.objects.filter(title__iexact = title)

        categoryObjectCountResult = 0
        for obj in categoryObjectList:
            if obj.pk != pk:
                categoryObjectCountResult += 1

        if categoryObjectCountResult == 1:
            form.instance.status = 'p'
        else:
            form.add_error('parent', "این دسته بندی وجود دارد.")
            return super().form_invalid(form)
        return super().form_valid(form)


    def form_invalid(self, form):
        print(form.errors.as_json())
        return super().form_invalid(form)




# class ArticleReturn(CreateView):
#     model = ArticleReturn
#     template_name = 'blog/article-return.html'
#     form_class = ArticleReturnForm
#     success_url = reverse_lazy('ArticleList')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = self.kwargs.get('pk')
#         global articleReport
#         global returnedArticle
#         articleReport = get_object_or_404(ArticleReport, pk=pk)
#         returnedArticle = get_object_or_404(articleReport.article)
#         context['articleReport'] = articleReport
#         context['returnedArticle'] = returnedArticle
#         return context

#     def form_valid(self, form):
#         returnedArticle.status = 'r'
#         returnedArticle.save()
#         form.instance.article = returnedArticle
#         return super().form_valid(form)






class ArticleReport(CreateView):
    model = ArticleReportModel
    template_name = 'blog/article-report.html'
    form_class = ArticleReportForm
    success_url = reverse_lazy('ArticleList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        global willBeReportedArticle
        willBeReportedArticle = get_object_or_404(Article, status='p', slug=slug)
        context['object'] = willBeReportedArticle
        return context

    def form_valid(self, form):
        willBeReportedArticle.is_reported = True
        willBeReportedArticle.save()
        form.instance.article = willBeReportedArticle
        return super().form_valid(form)






class CheckAndManageReports(View):

    def get(self, request, slug):
        global article
        article = get_object_or_404(Article, status='p', slug=slug)
        global articleReports
        articleReports = article.articleReport.filter(is_checked=False)
        # articleReports = ArticleReportModel.objects.filter(article=article, is_checked=False)
        form = ArticleReturnForm()
        context = {
            'article' : article,
            'articleReports' : articleReports,
            'form' : form
        }
        return render(request, 'blog/article-report-detail-and-return.html', context)


    def post(self, request, slug):
        if request.POST.get('ignore'):
            article.is_reported = False
            article.save()
            articleReports.update(is_checked=True, checked_by=request.user)
            return redirect('ArticleList')

        elif request.POST.get('return'):
            form = ArticleReturnForm(request.POST)
            if form.is_valid():
                # form = form.save(commit=False) replaced with the line below it.
                form.instance.article = article
                form.save()
                article.status = 'r'
                article.is_reported = False
                article.save()
                articleReports.update(is_checked=True, checked_by=request.user)
                return redirect('ArticleList')

        else:
            form = ArticleReturnForm(request.POST)
            form.add_error(None, "این عمل در بین اعمال مجاز برای مقالات نیست.")

        context = {
            'article' : article,
            'articleReports' : articleReports,
            'form' : form
        }
        return render(request, 'blog/article-report-detail-and-return.html', context)
            







# This class returns each users articles.
class UserArticleList(ListView):
    model = Article
    template_name = 'blog/article-list.html'
    paginate_by = 8

    def get_queryset(self):
        articleStatus = self.request.POST.get('articleStatus')
        if articleStatus == '-' or None:
            return get_list_or_404(Article, owner=self.request.user)
        elif articleStatus == 'p':
            return get_list_or_404(Article, owner=self.request.user, status='p')
        elif articleStatus == 'd':
            return get_list_or_404(Article, owner=self.request.user, status='d')
        elif articleStatus == 'r':
            return get_list_or_404(Article, owner=self.request.user, status='r')    
        else:
            return get_list_or_404(Article, owner=self.request.user)


