from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic



from core.models import Author, Bibtex, Book, AuthorOrder, Tag
from notification import alert

"""
Bibtex
"""
class IndexView(generic.ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date', 'title_en', 'title_ja')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_style_list"] = ["INTPROC","JOURNAL","CONF_DOMESTIC","CONF_DOMESTIC_NO_REVIEW","CONF_NATIONAL","BOOK","KEYNOTE","NEWS","OTHERS","AWARD"]
        return context

class AddTestDatas(generic.ListView):###for test
    template_name = 'dashboard/index.html'
    context_object_name = 'latest_bibtex_list'

    ##add Tag
    tag1 = Tag(name="Clustering",description="for clustering")
    tag2 = Tag(name="Wikipedia",description="for wikipedia")
    tag1.save()
    tag2.save()

    ##add author
    author_1 = Author(name_en='Tatsuya Nakamura', dep_en='Osaka University',mail="mail@mail.co.jp")
    author_1.save()
    author_2 = Author(name_en='Takahiro Hara', dep_en='Osaka University',mail="mail@mail.co.jp")
    author_2.save()

    ##add book
    book1 = Book(title="ACM Transactions on Asian and Low-Resource Language Information Processing",style="INTPROC")
    book2 = Book(title="IEEE",style="JOURNAL")
    book1.save()
    book2.save()

    ##add bibtex
    bibtex1 = Bibtex(language='EN', title_en='Wikipedia-Based Relatedness Measurements for Multilingual Short Text Clustering',book=book1,volume=3,number=5,chapter=1,page="10-20")
    bibtex2 = Bibtex(language='EN', title_en='wikipedia-based for clustering 2',book=book2,volume=2,number=2,chapter=2,page="15-24")
    bibtex1.save()
    bibtex2.save()

    ##add AuthorOrder
    AuthorOrder(bibtex=bibtex1,author=author_1,order=1).save()
    AuthorOrder(bibtex=bibtex1,author=author_2,order=2).save()
    #AuthorOrder(bibtex=bibtex2,author=author_1,order=1).save()
    #AuthorOrder(bibtex=bibtex2,author=author_2,order=2).save()

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date', 'title_en', 'title_ja')

class IndexViewTable(generic.ListView):
    template_name = 'dashboard/bibtex/index_tab.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date')


class IndexViewBib(generic.ListView):
    template_name = 'dashboard/bibtex/index_bib.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date')

class IndexViewLatex(generic.ListView):
    template_name = 'dashboard/bibtex/index_latex.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date')



class DetailView(generic.DetailView):
    model = Bibtex
    template_name = 'dashboard/detail.html'


"""
Book
"""
class BookIndexView(generic.ListView):
    template_name = 'dashboard/book/index.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        return Book.objects.order_by('title')


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'dashboard/book/detail.html'




"""
Author
"""
class AuthorIndexView(generic.ListView):
    template_name = 'dashboard/author/index.html'
    context_object_name = 'latest_author_list'

    def get_queryset(self):
        return Author.objects.order_by('name_en')


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'dashboard/author/detail.html'


"""
Notification
"""
def notification_alert(request):
    msg = False
    # Send Email
    status = alert.send_email_test()
    return render(request,
                  'notification/alert.html',
                  {
                      'msg': msg,
                      'status': status,
                  })
