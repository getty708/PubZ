from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic



from core.models import Author, Bibtex, Book, AuthorOrder
from notification import alert

"""
Bibtex
"""
class IndexView(generic.ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date', 'title_en', 'title_ja')

class AddTestDatas(generic.ListView):###for test
    template_name = 'dashboard/index.html'
    context_object_name = 'latest_bibtex_list'

    ##add author
    author_1 = Author(name_en='Tatsuya Nakamura', dep_en='Osaka University',mail="mail@mail.co.jp")
    author_1.save()
    author_2 = Author(name_en='Takahiro Hara', dep_en='Osaka University',mail="mail@mail.co.jp")
    author_2.save()

    ##add book
    book = Book(title="ACM Transactions on Asian and Low-Resource Language Information Processing",style="INTPROC")
    book.save()

    ##add bibtex
    bibtex = Bibtex(language='EN', title_en='Wikipedia-Based Relatedness Measurements for Multilingual Short Text Clustering',book=book,volume=3,number=5,chapter=1,page="10-20",pub_date=datetime.date(2018, 2, 1))
    bibtex.save()

    ##add AuthorOrder
    AuthorOrder(bibtex=bibtex,author=author_1,order=1)
    AuthorOrder(bibtex=bibtex,author=author_2,order=2)

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
