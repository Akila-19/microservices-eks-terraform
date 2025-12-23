const API_GATEWAY = 'http://ad8d2cdddcd4d463595a8bbfe1f6981a-1534883163.us-east-1.elb.amazonaws.com:8080';

window.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    loadUsers();
    loadProducts();
});

async function checkHealth() {
    try {
        const response = await fetch(`${API_GATEWAY}/status`);
        const data = await response.json();
        
        document.getElementById('user-status').textContent = 
            data.services['user-service'] === 'healthy' ? 'Healthy ✓' : 'Offline ✗';
        document.getElementById('user-status').className = 
            data.services['user-service'] === 'healthy' ? 'status healthy' : 'status unhealthy';
            
        document.getElementById('product-status').textContent = 
            data.services['product-service'] === 'healthy' ? 'Healthy ✓' : 'Offline ✗';
        document.getElementById('product-status').className = 
            data.services['product-service'] === 'healthy' ? 'status healthy' : 'status unhealthy';
    } catch (error) {
        document.getElementById('user-status').textContent = 'Offline ✗';
        document.getElementById('user-status').className = 'status unhealthy';
        document.getElementById('product-status').textContent = 'Offline ✗';
        document.getElementById('product-status').className = 'status unhealthy';
    }
}

async function loadUsers() {
    const container = document.getElementById('users-list');
    container.innerHTML = '<div class="loading">Loading users...</div>';

    try {
        const response = await fetch(`${API_GATEWAY}/api/users`);
        const data = await response.json();

        if (data.users && data.users.length > 0) {
            container.innerHTML = data.users.map(user => `
                <div class="item">
                    <h3>${user.name}</h3>
                    <p>📧 ${user.email}</p>
                    <p style="font-size: 0.8rem; color: #999;">ID: ${user.id}</p>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div class="error">No users found</div>';
        }
    } catch (error) {
        container.innerHTML = '<div class="error">Failed to load users</div>';
    }
}

async function loadProducts() {
    const container = document.getElementById('products-list');
    container.innerHTML = '<div class="loading">Loading products...</div>';

    try {
        const response = await fetch(`${API_GATEWAY}/api/products`);
        const data = await response.json();

        if (data.products && data.products.length > 0) {
            container.innerHTML = data.products.map(product => `
                <div class="item">
                    <h3>${product.name}</h3>
                    <p>💰 $${product.price} | 📦 Stock: ${product.stock}</p>
                    <p style="font-size: 0.8rem; color: #999;">ID: ${product.id}</p>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div class="error">No products found</div>';
        }
    } catch (error) {
        container.innerHTML = '<div class="error">Failed to load products</div>';
    }
}