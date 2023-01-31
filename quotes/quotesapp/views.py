from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quotes, Authors, Tags
from .forms import AuthorForm, TagForm, QuoteForm


# Create your views here.

def main(request, page = 1):
    cnt_quotes = 3
    quotes_list = []
    quotes = Quotes.objects.all()
    cnt_pages = 0
    if len(quotes) % cnt_quotes == 0:
        cnt_pages = len(quotes) // cnt_quotes
    else:
        cnt_pages = len(quotes) // cnt_quotes + 1
    previos = page - 1
    next = page + 1 if page < cnt_pages else 0
    start_q = (page - 1) * cnt_quotes
    end_q = (page - 1) * cnt_quotes + cnt_quotes

    print(previos, next)
    for el in quotes[start_q:end_q]:
        tags = el.tags.all()
        quotes_list.append({
            'id': el.id,
            'quote': el.quote[:200] + '....' if len(el.quote) > 200 else el.quote,
            'tags': [{'id': el.id, 'name': el.name} for el in tags],
            'author': el.author.fullname,
            'author_id': el.author.id
        })

    return render(request, 'quotesapp/quotes.html', {'quotes_list': quotes_list, 'previous': previos, 'next': next})


def author(request, author_id):
    author = get_object_or_404(Authors, pk=author_id)
    return render(request, 'quotesapp/author.html', {'author': author})


def tag(request, tag_id):
    quotes_list = []
    quotes = Quotes.objects.filter(tags=tag_id)
    for el in quotes:
        tags = el.tags.all()
        quotes_list.append({
            'id': el.id,
            'quote': el.quote[:200] + '....' if len(el.quote) > 200 else el.quote,
            'tags': [{'id': el.id, 'name': el.name} for el in tags],
            'author': el.author.fullname,
            'author_id': el.author.id
        })
    return render(request, 'quotesapp/quotes_by_tag.html', {'quotes_list': quotes_list})


def detail(request, quote_id):
    quote = get_object_or_404(Quotes, pk=quote_id)
    return render(request, 'quotesapp/detail.html', {'quote': quote})

@login_required
def addauthor(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:authors')
        else:
            return render(request, 'quotesapp/form_author.html', {'form': form})
    return render(request, 'quotesapp/form_author.html', {'form': AuthorForm()})

@login_required
def addtag(request):
    print('Add tag')
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:tags')
        else:
            return render(request, 'quotesapp/form_tags.html', {'form': form})
    return render(request, 'quotesapp/form_tags.html', {'form': TagForm()})

@login_required
def addquote(request):
    print('Add quote')
    tags = Tags.objects.all().order_by('name')
    authors = Authors.objects.all().order_by('fullname')
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            choice_tags = Tags.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/form_quote.html', {'tags': tags, 'authors': authors, 'form': form})
    return render(request, 'quotesapp/form_quote.html', {'tags': tags, 'authors': authors, 'form': QuoteForm})


def get_authors(request):
    authors = Authors.objects.all().order_by('fullname')
    return render(request, 'quotesapp/get_authors.html', {'authors': authors})


def get_tags(request):
    tags = Tags.objects.all().order_by('name')
    return render(request, 'quotesapp/get_tags.html', {'tags': tags})

@login_required
def remove_quote(request, quote_id):
    print(quote_id)
    Quotes.objects.filter(id=quote_id).delete()
    return redirect(to='quotesapp:main')

@login_required
def remove_tag(request, tag_id):
    Tags.objects.filter(id=tag_id).delete()
    return redirect(to='quotesapp:tags')

@login_required
def remove_author(request, author_id):
    Authors.objects.filter(id=author_id).delete()
    return redirect(to='quotesapp:authors')

@login_required
def edit_author(request, author_id):
    author = get_object_or_404(Authors, pk=author_id)
    form = AuthorForm({
        'id': author.id,
        'fullname': author.fullname,
        'born_date': author.born_date,
        'born_location': author.born_location,
        'description': author.description
    })
    return render(request, 'quotesapp/form_author.html', {'form': form})