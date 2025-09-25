function checkout() {
            if (cart.length === 0) return;
            
            const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);
            
            let orderSummary = 'Assalamu Alaikum! I want to place an order:\n\n';
            cart.forEach(item => {
                orderSummary += `${item.name} (${item.size}) x${item.quantity} = PKR ${(item.price * item.quantity).toLocaleString()}\n`;
            });
            orderSummary += `\nTotal Items: ${itemCount}\nTotal Amount: PKR ${total.toLocaleString()}\n\nPlease confirm my order. JazakAllahu Khairan!`;
            
            const phoneNumber = '923470105539';
            const whatsappURL = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(orderSummary)}`;
            
            window.open(whatsappURL, '_blank');
            
            alert(`🎉 Order Summary Sent to WhatsApp!\n\nItems: ${itemCount}\nTotal: PKR ${total.toLocaleString()}\n\nYour order details have been sent to our WhatsApp. We'll confirm your order shortly.\n\nJazakAllahu Khairan for choosing Al Barakah Scents!`);
            
            cart = [];
            saveCart();
            updateCartUI();
            renderProducts(getCurrentProducts());
            toggleCart();
        }

        function scrollToSection(sectionId) {
            document.getElementById(sectionId).scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }

        function performSearch() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
            if (!searchTerm) {
                renderProducts();
                return;
            }
            
            const filteredProducts = products.filter(product => 
                product.name.toLowerCase().includes(searchTerm) ||
                product.description.toLowerCase().includes(searchTerm) ||
                product.category.toLowerCase().includes(searchTerm)
            );
            
            renderProducts(filteredProducts);
            
            if (filteredProducts.length === 0) {
                document.getElementById('productGrid').innerHTML = `
                    <div class="col-12 text-center py-5">
                        <i class="bi bi-search display-1 text-muted"></i>
                        <h3 class="mt-3 text-muted">No products found</h3>
                        <p class="text-muted">Try searching for "oud", "rose", "musk" or other fragrance names</p>
                        <button class="btn btn-primary" onclick="renderProducts(); document.getElementById('searchInput').value=''">
                            Show All Products
                        </button>
                    </div>
                `;
            }
        }

        function submitContactForm(event) {
            event.preventDefault();
            const name = document.getElementById('contactName').value.trim();
            const email = document.getElementById('contactEmail').value.trim();
            const message = document.getElementById('contactMessage').value.trim();
            
            if (!name || !email || !message) {
                alert('Please fill in all required fields.');
                return;
            }
            
            const whatsappMessage = `Assalamu Alaikum! Contact Form Submission:\n\nName: ${name}\nEmail: ${email}\n\nMessage: ${message}\n\nJazakAllahu Khairan!`;
            const phoneNumber = '923470105539';
            const whatsappURL = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(whatsappMessage)}`;
            
            window.open(whatsappURL, '_blank');
            
            alert(`Thank you ${name}!\n\nYour message has been sent via WhatsApp. We'll respond to ${email} within 24 hours.\n\nJazakAllahu Khairan for contacting Al Barakah Scents!`);
            
            document.getElementById('contactForm').reset();
        }

        // Close cart when clicking outside
        document.addEventListener('click', function(e) {
            const cartSidebar = document.getElementById('cartSidebar');
            const cartBtn = e.target.closest('[onclick*="toggleCart"]');
        }
    );