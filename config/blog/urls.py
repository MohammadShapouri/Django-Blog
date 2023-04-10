from django.urls import path
from . import views


                                                                                                                                    # View Function         Template Function     Template UI       Template Linking            Pagination
urlpatterns = [
    path('category/add', views.AddCategory.as_view(), name='AddCategory'),                                                          #      Y                        Y                   Y                 Y-N                        -
    path('article/<slug:slug>/report', views.ArticleReport.as_view(), name='ArticleReport'),
    path('article/<slug:slug>/reports-manage-return', views.CheckAndManageReports.as_view(), name='ArticleReports'),
    path('category/list', views.CategoryList.as_view(), name='CategoryList'),                                                       #      Y                        Y                   Y                  Y                         N
    path('category/<slug:slug>', views.CategoryDetail.as_view(), name='CategoryDetail'),                                            #      Y                        Y                   Y                  Y                         N
    path('category/<slug:slug>/edit', views.EditCategory.as_view(), name='EditCategory'),                                           #      Y                        Y                   Y                 Y-N                        -
    path('article/list', views.ArticleList.as_view(), name='ArticleList'),                                                          #      Y                        Y                   Y                  Y                         N
    path('article/add', views.AddArticle.as_view(), name='addArticle'),                                                             #     Y-N                      Y-N                  Y                 Y-N                        N
    path('article/<slug:slug>', views.ArticleDetail.as_view(), name='ArticleDetail'),                                               #     Y                        Y-N                 N/A                Y-N                        -
    path('article/<slug:slug>/edit', views.EditArticle.as_view(), name='EditArticle'),                                              #     Y-N                      Y-N                 N/A                Y-N                        -
    path('article/<slug:slug>/delete', views.DeleteArticle.as_view(), name='DeleteArticle'),

]