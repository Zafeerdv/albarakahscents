document.addEventListener("DOMContentLoaded", function() {

    // Render single product card
    function createProductCard(product) {
        return `
        <div class="col-6 col-sm-6 col-md-4 col-lg-3 d-flex" data-category="${product.category}">
            <div class="card shadow-sm product-card w-100">
                <a href="/product/${product.id}/">
                    <img src="${product.image}" alt="${product.name}" class="product-thumb">
                </a>
                <div class="card-body text-center">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="price">PKR ${product.price}</p>
                    <p class="text-muted small">${product.description.length > 60 ? product.description.slice(0,60)+'...' : product.description}</p>
                    <button class="btn btn-success add-to-cart-btn mt-2 w-100" data-product-id="${product.id}">
                        Add to Cart
                    </button>
                </div>
            </div>
        </div>`;
    }

    // Render all products
    function renderProducts(productsToShow = products) {
        const grid = document.getElementById('productGrid');
        grid.innerHTML = productsToShow.map(createProductCard).join('');
        attachAddToCart(); // attach event listener after rendering
    }

    // Attach add-to-cart event
    function attachAddToCart() {
        document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const productId = this.dataset.productId;

                fetch(`/add-to-cart/${productId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "X-Requested-With": "XMLHttpRequest"
                    }
                })
                .then(res => res.json())
                .then(data => {
                    if(data.success){
                        alert("Product added to cart!");
                        // Optional: update cart badge
                    }
                });
            });
        });
    }

    // Filter products by category
    window.filterProducts = function(category) {
        const filtered = category === 'all' ? products : products.filter(p => p.category === category.toLowerCase());
        renderProducts(filtered);

        document.querySelectorAll('.category-pill').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`.category-pill[onclick="filterProducts('${category}')"]`)?.classList.add('active');
    }

    // CSRF helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    renderProducts(); // Initial render
});
