from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from profiles.models import UserProfile
from .forms import *
from .models import *
from .forms import ProductForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


# Create your views here.
def products_category(request,category):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.filter(sku=category)
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'


    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)



# @login_required(login_url='login')
def update(request,pk):
    task=Comments.objects.get(id=pk)
    id=task.product.id
    form=taskform(instance=task)  
    context={'form':form}

    if request.method=='POST':
        form=taskform(request.POST,instance=task)
        if form.is_valid():
            form.save()
        return redirect('/products/{}'.format(id))

    return render(request,'products/update.html',context)

def delete(request,pk):
    item=Comments.objects.get(id=pk)
    id=item.product.id
    if request.method=='POST':
        item.delete()
        return redirect('/products/{}'.format(id))
    print(item.product.id)
    context={
        'item':item
    }
    return render(request,'products/delete.html',context)




def product_detail(request, product_id):
    """ A view to show individual product details """

    form=taskform()     # blank form
    if request.method=='POST':
        form=taskform(request.POST)      
        Comments.objects.create(comment=request.POST['title'],product=Product.objects.get(pk=product_id),user=UserProfile.objects.get(user=request.user.id))
        if form.is_valid():
            form.save()                    
        return redirect('/products/{}'.format(product_id))

    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product_id).values()
    comments = Comments.objects.filter(product=product_id) 
    usernames_for_comments=[]
    usernames_for_reviews=[]
    
    comments_data=[]
    reviews_data=[]
    for i in comments:
        get_id=UserProfile.objects.get(id=i.user_id)
        user=User.objects.get(id=get_id.user_id)
        usernames_for_comments.append(user)

    for i in reviews:
    
        get_id=UserProfile.objects.get(id=i['user_id'])
        user=User.objects.get(id=get_id.user_id)
        usernames_for_reviews.append(user)

    for i in range(0,len(reviews)):
        x=[]
        review=list(reviews)[i]
        username=usernames_for_reviews[i]
        stars=review['stars']
        x={
            'review':review,
            'username':username.username,
            "stars":stars,
            "stars_range":range(0,stars),
        }
        reviews_data.append(x)

    for i in range(0,len(comments)):
        x=[]
        comment=list(comments)[i]
        username=usernames_for_comments[i]
        x={
            'comment':comment,
            'username':username.username
        }
        comments_data.append(x)


    usernames_for_comments=list(usernames_for_comments)
    context = {
        'product': product,
        'reviews': reviews_data,
        'comments': comments_data,
        'form':form,
        "user_id":UserProfile.objects.get(user=request.user.id).id
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)