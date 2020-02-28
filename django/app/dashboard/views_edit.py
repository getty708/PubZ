from django.http import Http404
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views import generic
# from django.contrib.auth.models import User
from users.models import User
from django.contrib.auth.decorators import login_required


from core.models import Author, AuthorOrder, Bibtex, Book, Tag, TagChain
from dashboard import forms



"""
User
"""
def get_login_user(user_id):
    return get_object_or_404(User, pk=user_id)


"""
Bibtex
"""
@login_required
def bibtex_edit(request, bibtex_id=None):
    msg = False
    if bibtex_id:
        bibtex = get_object_or_404(Bibtex, pk=bibtex_id)
        submit_url = reverse("dashboard:bibtex_edit",
                             kwargs={'bibtex_id':bibtex.id})
    else:
        bibtex = Bibtex()
        submit_url = reverse("dashboard:bibtex_add")

    if request.method == 'POST':
        form = forms.BibtexForm(request.POST, instance=bibtex)
        if form.is_valid():
            bibtex_new = form.save(commit=False)
            bibtex_new.owner = get_login_user(request.user.id)
            bibtex_new.save()
            return redirect('dashboard:bib_detail', pk=bibtex.id,)
        else:
            print("validation fail")
    else:
        form = forms.BibtexForm(instance=bibtex)

    return render(request,
                  'dashboard/bibtex/edit.html',
                  {'msg': msg,
                   'form':form,
                   'bibtex': bibtex,
                   'submit_url': submit_url})


@login_required
def bibtex_edit_step1(request):
    msg = False
    bibtex = Bibtex()
    submit_url = reverse("dashboard:bibtex_add_step1")

    if request.method == 'POST':
        form = forms.BibtexFormStep1(request.POST)
        if form.is_valid():
            bibtex.language = form.cleaned_data['lang']
            if form.cleaned_data['lang'] == 'EN':
                bibtex.title_en = form.cleaned_data['title']
            elif form.cleaned_data['lang'] == 'JA':
                bibtex.title_ja = form.cleaned_data['title']
            bibtex.book = form.cleaned_data['book']
            bibtex.owner = get_login_user(request.user.id)
            bibtex.save()
            print("Saved", bibtex)
            return redirect('dashboard:bibtex_edit', bibtex_id=bibtex.id,)
        else:
            print("validation fail")
    else:
        form = forms.BibtexFormStep1()

    return render(request,
                  'dashboard/bibtex/edit_step1.html',
                  {'msg': msg,
                   'form':form,
                   'submit_url': submit_url})

"""
Book
"""
@login_required
def book_edit(request, book_id=None):
    msg = False
    if book_id:
        book = get_object_or_404(Book, pk=book_id)
        submit_text = "Update"
        submit_url = reverse("dashboard:book_edit",kwargs={'book_id':book.id})
    else:
        book = Book()
        submit_text = "Add New"
        submit_url = reverse("dashboard:book_add")

    if request.method == 'POST':
        form = forms.BookForm(request.POST, instance=book)
        if form.is_valid():
            book_new = form.save(commit=False)
            book_new.owner = get_login_user(request.user.id)
            book_new.save()
            return redirect('dashboard:book_detail', book.id)
        else:
            print("validation fail")
    else:
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
@login_required
def author_edit(request, author_id=None):
    msg = False
    if author_id:
        author = get_object_or_404(Author, pk=author_id)
        submit_url = reverse("dashboard:author_edit",
                             kwargs={'author_id':author.id})
    else:
        author = Author()
        submit_url = reverse("dashboard:author_add")

    if request.method == 'POST':
        form = forms.AuthorForm(request.POST, instance=author)
        if form.is_valid():
            print(form.cleaned_data)
            author_new = form.save(commit=False)
            author_new.owner = get_login_user(request.user.id)
            author_new.save()
            return redirect('dashboard:author_detail', author.id)
        else:
            print("validation fail")
    else:
        form = forms.AuthorForm(instance=author)
    return render(request,
                  'dashboard/author/edit.html',
                  {'msg': msg,
                   'form':form,
                   'author': author,
                   'submit_url': submit_url})


"""
AuthorOrder
"""
@login_required
def author_order_edit(request, author_order_id=None):
    msg = False
    if author_order_id:
        author_order = get_object_or_404(AuthorOrder, pk=author_order_id)
        bibtex = author_order.bibtex
        submit_url = reverse("dashboard:author_order_edit",
                             kwargs={'author_order_id':author_order.id})
    else:
        author_order = AuthorOrder()
        submit_url = reverse("dashboard:author_order_add")
        if "bibtex" in request.GET:
            bibtex_id = request.GET.get("bibtex")
            bibtex = get_object_or_404(Bibtex, pk=bibtex_id)
            author_order.bibtex = bibtex
        elif request.method == 'POST':
            pass
        else:
            raise Http404("Invalid BibtexID")

    print(request.method)
    if request.method == 'POST':
        form = forms.AuthorOrderForm(request.POST, instance=author_order)
        if form.is_valid():
            author_order_new = form.save(commit=False)
            author_order_new.owner = get_login_user(request.user.id)
            author_order_new.save()
            return redirect('dashboard:detail', author_order.bibtex.id)
        else:
            raise Http404("Valiation Failed")        

    form = forms.AuthorOrderForm(instance=author_order)
    return render(request,
                  'dashboard/author_order/edit.html',
                  {'msg': msg,
                   'form':form,
                   'bibtex': bibtex,
                   'author_order': author_order,
                   'submit_url': submit_url})



"""
Tag
"""
@login_required
def tag_edit(request, tag_id=None):
    msg = False
    if tag_id:
        tag = get_object_or_404(Tag, pk=tag_id)
        submit_url = reverse("dashboard:tag_edit",
                             kwargs={'tag_id':tag.id})
    else:
        tag = Tag()
        submit_url = reverse("dashboard:tag_add")

    if request.method == 'POST':
        form = forms.TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag_new = form.save(commit=False)
            tag_new.owner = get_login_user(request.user.id)
            tag_new.save()
            return redirect('dashboard:tag_index')

    form = forms.TagForm(instance=tag)
    return render(request,
                  'dashboard/tag/edit.html',
                  {'msg': msg,
                   'form': form,
                   'tag': tag,
                   'submit_url': submit_url})


"""
TagChain
"""
def tagchain_edit(request, tagchain_id=None):
    msg = False
    if tagchain_id:
        tagChain = get_object_or_404(TagChain, pk=tagchain_id)
        bibtex = tagChain.bibtex
        submit_url = reverse("dashboard:tagchain_edit",
                             kwargs={'tagchain_id':tagChain.id})
    else:
        tagChain = TagChain()
        submit_url = reverse("dashboard:tagchain_add")
        if "bibtex" in request.GET:
            bibtex_id = request.GET.get("bibtex")
            bibtex = get_object_or_404(Bibtex, pk=bibtex_id)
            tagChain.bibtex = bibtex
        elif request.method == 'POST':
            pass
        else:
            raise Http404("Invalid BibtexID")

    if request.method == 'POST':
        form = forms.TagChainForm(request.POST, instance=tagChain)
        if form.is_valid():
            tagChain_new = form.save(commit=False)
            tagChain_new.owner = get_login_user(request.user.id)
            tagChain_new.save()
            return redirect('dashboard:tag_index')

    form = forms.TagChainForm(instance=tagChain)
    return render(request,
                  'dashboard/tagChain/edit.html',
                  {'msg': msg,
                   'form': form,
                   'bibtex': bibtex,
                   'tagChain': tagChain,
                   'submit_url': submit_url})
