from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
def update_comment(request,pk):
    task = Comments.objects.get(id=pk)  # search comment with that id
    id = task.product.id   # id of the product
    form = taskform(instance=task)
    context = {'form':form}

    if request.method=='POST':
        form=taskform(request.POST,instance=task)
        if form.is_valid():
            form.save()
        return redirect('/products/{}'.format(id))

    return render(request,'products/update.html',context)


def delete_comment(request,pk):
    item=Comments.objects.get(id=pk)  # fetched comment 
    id=item.product.id  # product id is fetched here 
    if request.method=='POST':
        item.delete()
        return redirect('/products/{}'.format(id))  # refreshing the page
    # print(item.product.id)
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
    usernames_for_comments =[]
    usernames_for_reviews =[]
    
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
            'username': username.username,
            "stars": stars,
            "stars_range": range(0,stars), 
        }
        reviews_data.append(x)

    for i in range(0,len(comments)):
        x=[]
        comment =list(comments)[i]
        username=usernames_for_comments[i]
        x={
            'comment':comment,
            'username':username.username
        }
        comments_data.append(x)

    user = UserProfile.objects.filter(user=request.user.id).first()
    user_id = None 
    if user is not None:
        user_id = user.id
    usernames_for_comments=list(usernames_for_comments)
    context = {
        'product': product,
        'reviews': reviews_data,
        'comments': comments_data,
        'form': form,
        'user_id': user_id
    }

    return render(request, 'products/product_detail.html', context)



@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
    

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

def delete_products(request,pk):
    item=Product.objects.get(id=pk)  # fetched comment 
    id=item.product.id  # product id is fetched here 
    if request.method=='POST':
        item.delete()
        return redirect('/products/{}'.format(id))  # refreshing the page
    # print(item.product.id)
    context={
        'item':item
    }
    return render(request,'products/delete.html',context)