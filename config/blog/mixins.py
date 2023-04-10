from blog.models import Article, Category
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import Http404



class ArticleManagingMixin():
    """
    Control access for editing and deleting articles.
    """
    def get_article_owner(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        return self.request.user == article.owner


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("دسترسی لازم را ندارید.")
        else:
            if self.get_article_owner() == False and request.user.is_superuser == False or request.user.is_staff == False:
                raise Http404("دسترسی لازم را ندارید.")
            else:
                return super().dispatch(request, *args, **kwargs)




class ArticleViewingMixin():

    def article_detail(self):
        slug = self.kwargs.get('slug')
        # status = self.kwargs.get('status')
        article_detail_dict = None
        article = get_object_or_404(Article, slug=slug)
        article_detail_dict['article'] = article
        article_detail_dict['status'] = article.status
        return article_detail_dict

    
    def get_article_owner(self):
        article_detail_dict = self.article_detail()
        article_owner = article_detail_dict['article'].owner
        return article_owner == self.request.user

    def get_article_status(self):
        return self.article_detail['status']



    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff or self.get_article_status == 'p':
                return super().dispatch(request, *args, **kwargs)
            else:
                if self.get_article_owner() == True:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    raise Http404("دسترسی لازم را ندارید.")
        else:
            if self.get_article_status == 'p':
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("دسترسی لازم را ندارید.")






class AdminStaffManagingMixin():

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated == False:
            raise Http404("دسترسی لازم را ندارید.")
        else:
            if request.user.is_superuser == False or request.user.is_staff == False:
                raise Http404("دسترسی لازم را ندارید.")
            else:
                return super().dispatch(request, *args, **kwargs)





class CategoryManagingMixin(AdminStaffManagingMixin):
    pass





class ArticleAdminManagingMixin(AdminStaffManagingMixin):
    pass



class CategoryViewingMixin():
    def category_status(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return category.status


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            if self.category_status() == 'p':
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("دسترسی لازم را ندارید.")