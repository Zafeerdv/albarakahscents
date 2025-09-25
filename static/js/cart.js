document.addEventListener("DOMContentLoaded", function() {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function() {
            const productId = this.dataset.productId;
            const btn = this;

            fetch(`/add-to-cart/${productId}/`, {  // URL me product_id send ho raha
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.product_quantity !== undefined) {
                    btn.textContent = `Add to Cart (${data.product_quantity})`;
                    btn.classList.add("btn-success");
                    btn.classList.remove("btn-warning");

                    // Update cart badge
                    const cartBadge = document.getElementById("cartCount");
                    if(cartBadge) cartBadge.textContent = data.cart_count;
                } else if (data.error) {
                    alert(data.error);
                }
            })
        });
    });

});

//     // Update quantity in cart details page
//     const updateForms = document.querySelectorAll(".cart-card form, .table-responsive form");
//     updateForms.forEach(form => {
//         form.addEventListener("submit", function(e) {
//             e.preventDefault();
//             const formData = new FormData(this);
//             const actionUrl = this.getAttribute("action");

//             fetch(actionUrl, {
//                 method: "POST",
//                 headers: {
//                     "X-CSRFToken": getCookie("csrftoken"),
//                     "X-Requested-With": "XMLHttpRequest"
//                 },
//                 body: formData
//             })
//             .then(res => res.json())
//             .then(data => {
//                 if (data.cart_count !== undefined) {
//                     // Update cart badge
//                     const cartBadge = document.getElementById("cartCount");
//                     if (cartBadge) cartBadge.textContent = data.cart_count;

//                     // Reload cart details
//                     if (document.getElementById("cartDetailsContainer")) {
//                         fetch("/cart/")
//                         .then(res => res.text())
//                         .then(html => {
//                             document.getElementById("cartDetailsContainer").innerHTML = html;
//                         });
//                     }
//                 } else if (data.error) {
//                     alert(data.error);
//                 }
//             })
//             .catch(err => console.error("Update cart error:", err));
//         });
//     });

// });
