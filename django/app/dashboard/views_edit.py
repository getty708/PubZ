from django.http import Http404
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views import generic



from core.models import Author, Bibtex, Book
from dashboard import forms



"""
Bibtex
"""
def bibtex_edit(request, bibtex_id=None):
    msg = False
    if bibtex_id:
        book = get_object_or_404(Bibtex, pk=bibtex_id)
        submit_url = reverse("dashboard:bibtex_edit",
                             kwargs={'bibtex_id':bibtex.id})
    else:
        bibtex = Bibtex()
        submit_url = reverse("dashboard:bibtex_add")
        
    if request.method == 'POST':
        form = forms.BookForm(request.POST, instance=bibtex)
        if form.is_valid():
            bibtex_new = form.save(commit=False)
            bibtex_new.save()
            print("Saved", bibtex)
            return redirect('dashboard:bibtex_index')
        else:
            print("validation fail")

    form = forms.BibtexForm(instance=bibtex)
    return render(request,
                  'dashboard/bibtex/edit.html',
                  {'msg': msg,
                   'form':form,
                   'bibtex': bibtex,
                   'submit_url': submit_url})





"""
Book
"""
def book_edit(request, book_id=None):
    msg = False
    if book_id:
        book = get_object_or_404(Book, pk=book_id)
        submit_text = "更新"
        submit_url = reverse("dashboard:book_edit",kwargs={'book_id':book.id})
    else:
        book = Book()
        submit_text = "登録"
        submit_url = reverse("dashboard:book_add")
        
    if request.method == 'POST':
        form = forms.BookForm(request.POST, instance=book)
        if form.is_valid():
            book_new = form.save(commit=False)
            book_new.save()
            return redirect('dashboard:book_index')        

    form = forms.BookForm(instance=book)    
    return render(request,
                  'dashboard/book/edit.html',
                  {'msg': msg,
                   'form':form,
                   'book': book,
                   'submit_text': submit_text,
                   'submit_url': submit_url})
    


"""
Author
"""
def author_edit(request, author_id=None):
    msg = False
    if author_id:
        author = get_object_or_404(Author, pk=book_id)
        submit_url = reverse("dashboard:author_edit",
                             kwargs={'author_id':author.id})
    else:
        author = Author()
        submit_url = reverse("dashboard:author_add")
        
    if request.method == 'POST':
        form = forms.AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author_new = form.save(commit=False)
            author_new.save()
            return redirect('dashboard:author_index')

    form = forms.AuthorForm(instance=author)    
    return render(request,
                  'dashboard/author/edit.html',
                  {'msg': msg,
                   'form':form,
                   'author': author,
                   'submit_url': submit_url})



