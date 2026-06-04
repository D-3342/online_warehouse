from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.view_count += 1
    product.save(update_fields=['view_count'])

    popular_products = (
        Product.objects
        .exclude(pk=product.pk)
        .select_related('category')
        .order_by('-view_count')[:8]
    )

    return render(request, 'pages/products/detail.html', {
        'product': product,
        'popular_products': popular_products,
    })
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    if selected_category and selected_category != '':
        try:
            category_id = int(selected_category)
            products = products.filter(category_id=category_id)
        except (ValueError, TypeError):
            pass

    if search_query and search_query != '':
        products = products.filter(name__icontains=search_query)

    popular_products = Product.objects.annotate(
        views_count=Count('views')
    ).order_by('-views_count', '-id')[:8]

    context = {
        'products': products,
        'popular_products': popular_products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }

    return render(request, 'pages/index.html', context)