/**
 * JavaScript para UX - Validación de formularios y animaciones
 * NO maneja lógica de negocio - todo se hace en el servidor
 */

// Auto-ocultar mensajes flash después de 4 segundos
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const flashes = document.querySelectorAll('.flash-message');
        flashes.forEach(function(flash) {
            flash.style.animation = 'slideOut 0.3s ease-out forwards';
            setTimeout(function() {
                flash.remove();
            }, 300);
        });
    }, 4000);
});

// Validación de formularios antes de enviar
document.addEventListener('DOMContentLoaded', function() {
    // Validar formulario de login
    const loginForm = document.querySelector('form[action*="login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const email = this.querySelector('input[type="email"]').value;
            const password = this.querySelector('input[type="password"]').value;
            
            if (!email || !password) {
                e.preventDefault();
                alert('Por favor completa todos los campos');
                return false;
            }
            
            if (!email.includes('@')) {
                e.preventDefault();
                alert('Por favor ingresa un email válido');
                return false;
            }
        });
    }
    
    // Validar formulario de registro
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const nombre = this.querySelector('input[name="nombre"]').value;
            const email = this.querySelector('input[type="email"]').value;
            const password = this.querySelector('input[type="password"]').value;
            
            if (!nombre || !email || !password) {
                e.preventDefault();
                alert('Por favor completa todos los campos');
                return false;
            }
            
            if (password.length < 6) {
                e.preventDefault();
                alert('La contraseña debe tener al menos 6 caracteres');
                return false;
            }
        });
    }
    
    // Validar formulario de checkout
    const checkoutForm = document.querySelector('form[action*="checkout"]');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            const direccion = this.querySelector('textarea[name="direccion_envio"]').value;
            
            if (!direccion || direccion.length < 10) {
                e.preventDefault();
                alert('Por favor ingresa una dirección completa (mínimo 10 caracteres)');
                return false;
            }
            
            // Confirmar pedido
            if (!confirm('¿Confirmar pedido? Se procesará el pago y se enviará a la dirección indicada.')) {
                e.preventDefault();
                return false;
            }
        });
    }
});

// Confirmación para eliminar items del carrito
document.addEventListener('DOMContentLoaded', function() {
    const removeButtons = document.querySelectorAll('button[name="action"][value="remove"]');
    removeButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('¿Eliminar este producto del carrito?')) {
                e.preventDefault();
                return false;
            }
        });
    });
});

// Animación suave al agregar al carrito
document.addEventListener('DOMContentLoaded', function() {
    const addToCartForms = document.querySelectorAll('form[action*="add-to-cart"]');
    addToCartForms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            if (btn) {
                btn.textContent = 'AGREGANDO...';
                btn.disabled = true;
            }
        });
    });
});

// Animaciones CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .form-input:focus {
        outline: none;
        border-color: #ff6b00;
        box-shadow: 0 0 0 3px rgba(255, 107, 0, 0.1);
        transition: all 0.2s;
    }
    
    .btn {
        transition: all 0.2s;
    }
    
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .btn:active {
        transform: translateY(0);
    }
    
    .product-card {
        transition: all 0.3s;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
`;
document.head.appendChild(style);
