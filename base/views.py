from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Topic, Comment, Currency, User, Listed, Role
from .models import Product
from django.http import HttpResponse
from .forms import EditUserForm, MyUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Product.objects.filter(Q(catogory__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    room_count = rooms.count()
    products = Product.objects.all()
    topic = Topic.objects.all()[:5]
    content = {'products': products, 'rooms': rooms,'topic':topic,'room_count':room_count}
    return render(request, 'base/products.html', content)


def registerPage(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()

            # Assign a role to the user (e.g., 'user' role)
            try:
                user_role = Role.objects.get(name='User')
                user.role = user_role  # Assign role to the user
            except Role.DoesNotExist:
                messages.error(request, 'Role "User" does not exist.')
                return redirect('register')

            user.save()  # Save the user with the assigned role
            login(request, user)  # Log the user in
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        form = MyUserCreationForm()  # Initialize an empty form for GET requests

    context = {'form': form}
    return render(request, 'base/login.html', context)
def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password is incorrect')

    context = {'page': page}
    return render(request, 'base/login.html', context)

@login_required(login_url='/login')
def sellers(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'base/sellers.html', context)

@login_required(login_url='/login')
def all_users(request):
    user = get_object_or_404(User, id=request.user.id)
    if user.role.name == "Admin":
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'base/allusers.html', context)
    else:
        return redirect('home')


@login_required(login_url='/login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not Listed.objects.filter(user=request.user, product=product).exists():
        Listed.objects.create(user=request.user, product=product)
    return redirect('wishlist')


@login_required(login_url='/login')
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.username = form.cleaned_data.get('username').lower()
            user.bio = form.cleaned_data.get('bio')
            user.avatar = form.cleaned_data.get('avatar')
            user.email = form.cleaned_data.get('email')

            try:
                if user.role == 'Admin':
                    user_role = Role.objects.get(name='Admin')
                else:
                    user_role = Role.objects.get(name='User')
                user.role = user_role
            except Role.DoesNotExist:
                messages.error(request, "Role does not exist.")

                return redirect('edit_user', user_id=user.id)

            user.save()
            login(request, user)

            # Redirect after successful form submission
            return redirect('home')
        else:
            messages.error(request, 'Error in form submission.')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'base/userPage.html', {'form': form, 'user': user})

@login_required(login_url='/login')
def wishlist_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Check if the listing exists and then delete it
    listing = Listed.objects.filter(user=request.user, product=product).first()
    if listing:
        listing.delete()
    return redirect('wishlist')


@login_required(login_url='/login')
def wishlist(request):
    wished_products = Listed.objects.filter(user=request.user)

    return render(request, 'base/wishlist.html', {'wished_products': wished_products})


@login_required(login_url='/login')
def sellerPage(request, pk):
    try:
        user = User.objects.get(username=pk)
    except:
        user = User.objects.get(id=pk)
    products = Product.objects.filter(creator=user)  # Use 'creator' instead of 'user'
    context = {'products': products, 'user': user}
    return render(request, 'base/sellerPage.html', context)


@login_required(login_url='/login')
def deleteProduct(request, pk):
    room = Product.objects.get(id=pk)
    if request.user != room.creator:
        return redirect('home')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_product.html', {'obj': room})


@login_required(login_url='/login')
def create_product(request):
    categories = Topic.objects.all()
    currencies = Currency.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        currency_name = request.POST.get('currency')
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        currency, created = Currency.objects.get_or_create(name=currency_name)
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Ensure this is captured
        Product.objects.create(
            name=name,
            description=description,
            currency=currency,
            price=price,
            image=image,  # Ensure this is saved
            catogory=topic,
            creator=request.user
        )
        return redirect('home')  # Or any other appropriate URL

    context = {'categories': categories, 'currencies': currencies}
    return render(request, 'base/create_product.html', context)


def productRoom(request, pk):
    product = get_object_or_404(Product, id=pk)
    comment = product.comment_set.all()  # Fetch related comments
    currency = product.currency  # This is fine as it fetches the related Currency object

    if request.method == 'POST':

        if request.method == 'POST':
            comment_text = request.POST.get('comment')  # Get comment from form
            Comment.objects.create(user=request.user, product=product, body=comment_text)
        return redirect('product', pk=product.id)

    context = {'comment': comment, 'product': product, 'currency': currency}
    return render(request, 'base/productRoom.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')
