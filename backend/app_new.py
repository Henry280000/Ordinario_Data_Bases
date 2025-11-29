from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Importar módulos de conexión a bases de datos
from db_mysql import MySQLConnection
from db_mongodb import MongoDBConnection

# Configurar Flask
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')
app.secret_key = os.getenv('SECRET_KEY', 'tu_clave_secreta_muy_segura_cambiala_12345')

# Inicializar conexiones a bases de datos
mysql_conn = MySQLConnection()
mongo_conn = MongoDBConnection()

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para rutas que requieren rol de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        if session.get('rol') != 'ADMIN':
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def get_cart():
    """Obtener carrito de la sesión"""
    return session.get('cart', {})

def add_to_cart(product_id, quantity=1, size='M'):
    """Agregar producto al carrito"""
    cart = get_cart()
    cart_key = f"{product_id}_{size}"
    
    if cart_key in cart:
        cart[cart_key]['quantity'] += quantity
    else:
        cart[cart_key] = {
            'product_id': product_id,
            'size': size,
            'quantity': quantity
        }
    
    session['cart'] = cart
    session.modified = True

def get_cart_count():
    """Obtener cantidad total de items en el carrito"""
    cart = get_cart()
    return sum(item['quantity'] for item in cart.values())

@app.route('/')
def index():
    """Página principal"""
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    return render_template('index.html', user_name=user_name, cart_count=cart_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Iniciar sesión"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"DEBUG - Intento de login: email={email}, password={'*' * len(password) if password else 'None'}")
        
        # Buscar usuario en la base de datos
        query = "SELECT id_usuario, nombre, email, password_hash, rol, activo FROM Usuarios WHERE email = %s"
        result = mysql_conn.execute_query(query, (email,))
        
        print(f"DEBUG - Usuario encontrado: {bool(result)}")
        
        if not result:
            flash('Credenciales inválidas', 'danger')
            return redirect(url_for('login'))
        
        user = result[0]
        
        print(f"DEBUG - Usuario activo: {user['activo']}")
        print(f"DEBUG - Hash en DB (primeros 30 chars): {user['password_hash'][:30]}")
        print(f"DEBUG - Password ingresado: {password}")
        
        if not user['activo']:
            flash('Usuario inactivo', 'danger')
            return redirect(url_for('login'))
        
        # Verificar contraseña usando bcrypt
        import bcrypt
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = user['password_hash'].encode('utf-8')
            print(f"DEBUG - Password bytes: {password_bytes}")
            print(f"DEBUG - Hash bytes (primeros 30): {hash_bytes[:30]}")
            
            password_match = bcrypt.checkpw(password_bytes, hash_bytes)
            print(f"DEBUG - Password match: {password_match}")
        except Exception as e:
            print(f"DEBUG - Error en bcrypt: {str(e)}")
            password_match = False
        
        if not password_match:
            flash('Credenciales inválidas', 'danger')
            return redirect(url_for('login'))
        
        # Guardar en sesión
        session['user_id'] = user['id_usuario']
        session['user_name'] = user['nombre']
        session['user_email'] = user['email']
        session['rol'] = user['rol']
        
        flash(f'¡Bienvenido, {user["nombre"]}!', 'success')
        return redirect(url_for('catalogo'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registrar nuevo usuario"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Verificar si el email ya existe
        query = "SELECT id_usuario FROM Usuarios WHERE email = %s"
        result = mysql_conn.execute_query(query, (email,))
        
        if result:
            flash('El email ya está registrado', 'danger')
            return redirect(url_for('register'))
        
        # Hash de la contraseña
        import bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insertar usuario
        insert_query = "INSERT INTO Usuarios (nombre, email, password_hash, rol) VALUES (%s, %s, %s, 'CLIENTE')"
        mysql_conn.execute_query(insert_query, (nombre, email, password_hash))
        
        flash('Cuenta creada exitosamente. Por favor inicia sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('index'))

@app.route('/catalogo')
def catalogo():
    """Página de catálogo de productos"""
    # Obtener filtros
    marca = request.args.get('marca')
    equipo = request.args.get('equipo')
    busqueda = request.args.get('q')
    
    # Construir filtro para MongoDB
    filtro = {'activo': True}
    
    if marca:
        filtro['marca'] = {'$regex': marca, '$options': 'i'}
    if equipo:
        filtro['equipo'] = {'$regex': equipo, '$options': 'i'}
    if busqueda:
        filtro['$or'] = [
            {'nombre': {'$regex': busqueda, '$options': 'i'}},
            {'equipo': {'$regex': busqueda, '$options': 'i'}},
            {'tags': {'$regex': busqueda, '$options': 'i'}}
        ]
    
    # Obtener productos
    jerseys = list(mongo_conn.db.jerseys.find(filtro))
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('catalogo.html', jerseys=jerseys, user_name=user_name, 
                         cart_count=cart_count, busqueda=busqueda)

@app.route('/producto/<product_id>')
def producto_detalle(product_id):
    """Página de detalle de producto"""
    jersey = mongo_conn.db.jerseys.find_one({'_id': product_id})
    
    if not jersey:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('catalogo'))
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('producto_detalle.html', jersey=jersey, user_name=user_name, 
                         cart_count=cart_count)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart_route():
    """Agregar producto al carrito"""
    product_id = request.form.get('product_id')
    size = request.form.get('size', 'M')
    quantity = int(request.form.get('quantity', 1))
    
    add_to_cart(product_id, quantity, size)
    
    flash(f'Producto agregado al carrito', 'success')
    return redirect(request.referrer or url_for('catalogo'))

@app.route('/carrito')
def carrito():
    """Página del carrito"""
    cart = get_cart()
    cart_items = []
    total = 0
    
    for cart_key, item in cart.items():
        # Obtener información del producto desde MongoDB
        jersey = mongo_conn.db.jerseys.find_one({'_id': item['product_id']})
        if jersey:
            subtotal = jersey['precio_base'] * item['quantity']
            cart_items.append({
                'cart_key': cart_key,
                'product_id': item['product_id'],
                'nombre': jersey['nombre'],
                'equipo': jersey['equipo'],
                'precio': jersey['precio_base'],
                'size': item['size'],
                'quantity': item['quantity'],
                'subtotal': subtotal
            })
            total += subtotal
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('carrito.html', cart_items=cart_items, total=total, 
                         user_name=user_name, cart_count=cart_count)

@app.route('/update-cart', methods=['POST'])
def update_cart():
    """Actualizar cantidad en el carrito"""
    cart_key = request.form.get('cart_key')
    action = request.form.get('action')
    
    cart = get_cart()
    
    if cart_key in cart:
        if action == 'increase':
            cart[cart_key]['quantity'] += 1
        elif action == 'decrease':
            cart[cart_key]['quantity'] -= 1
            if cart[cart_key]['quantity'] <= 0:
                del cart[cart_key]
        elif action == 'remove':
            del cart[cart_key]
    
    session['cart'] = cart
    session.modified = True
    
    return redirect(url_for('carrito'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Página de checkout"""
    cart = get_cart()
    
    if not cart:
        flash('El carrito está vacío', 'warning')
        return redirect(url_for('carrito'))
    
    if request.method == 'POST':
        # Obtener campos individuales
        calle = request.form.get('calle', '').strip()
        numero = request.form.get('numero', '').strip()
        numero_int = request.form.get('numero_int', '').strip()
        colonia = request.form.get('colonia', '').strip()  # Puede venir de select o input
        municipio = request.form.get('municipio', '').strip()
        estado = request.form.get('estado', '').strip()
        codigo_postal = request.form.get('codigo_postal', '').strip()
        referencias = request.form.get('referencias', '').strip()
        
        print(f"DEBUG CHECKOUT - Colonia recibida: '{colonia}' (tipo: {type(colonia)})")
        
        # Combinar en dirección completa
        direccion_parts = []
        
        if calle and numero:
            if numero_int:
                direccion_parts.append(f"{calle} #{numero} Int. {numero_int}")
            else:
                direccion_parts.append(f"{calle} #{numero}")
        elif calle:
            direccion_parts.append(calle)
        
        if colonia:
            direccion_parts.append(f"Col. {colonia}")
        
        if codigo_postal:
            direccion_parts.append(f"CP {codigo_postal}")
        
        if municipio:
            direccion_parts.append(municipio)
        
        if estado:
            direccion_parts.append(estado)
        
        if referencias:
            direccion_parts.append(f"Ref: {referencias}")
        
        direccion_envio = ", ".join(direccion_parts)
        
        print(f"DEBUG CHECKOUT - Direccion completa: {direccion_envio}")
        
        # Preparar items para el pedido
        items = []
        cart_items = []
        total = 0
        
        for cart_key, item in cart.items():
            # Obtener información del producto
            jersey = mongo_conn.db.jerseys.find_one({'_id': item['product_id']})
            if jersey:
                # Generar SKU (formato: EQUIPO-HOME-2024-TALLA)
                # Ejemplo: jersey_rm_home_2024 -> RM-HOME-2024-M
                product_id_parts = item['product_id'].split('_')
                if len(product_id_parts) >= 4:
                    equipo_codigo = product_id_parts[1].upper()
                    tipo = product_id_parts[2].upper()
                    year = product_id_parts[3]
                    sku = f"{equipo_codigo}-{tipo}-{year}-{item['size']}"
                else:
                    sku = f"JERSEY-{item['size']}"
                
                subtotal = jersey['precio_base'] * item['quantity']
                items.append({
                    'sku': sku,
                    'cantidad': item['quantity']
                })
                cart_items.append({
                    'nombre': jersey['nombre'],
                    'size': item['size'],
                    'quantity': item['quantity'],
                    'precio': jersey['precio_base'],
                    'subtotal': subtotal
                })
                total += subtotal
        
        # Crear pedido directamente con transacciones
        connection = None
        cursor = None
        try:
            print(f"DEBUG CHECKOUT - Creando pedido...")
            print(f"DEBUG CHECKOUT - User ID: {session['user_id']}")
            print(f"DEBUG CHECKOUT - Direccion: {direccion_envio}")
            print(f"DEBUG CHECKOUT - Total items: {len(items)}")
            print(f"DEBUG CHECKOUT - Total: ${total}")
            
            # Obtener conexión directa para usar transacciones
            import mysql.connector
            connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', 'rootpassword'),
                database=os.getenv('MYSQL_DATABASE', 'ecommerce_db')
            )
            cursor = connection.cursor(dictionary=True)
            
            # Iniciar transacción
            connection.start_transaction()
            
            # 1. Insertar pedido
            cursor.execute(
                "INSERT INTO Pedidos (id_usuario, direccion_envio, total, estado) VALUES (%s, %s, %s, 'PROCESANDO')",
                (session['user_id'], direccion_envio, total)
            )
            id_pedido = cursor.lastrowid
            print(f"DEBUG CHECKOUT - Pedido creado con ID: {id_pedido}")
            
            # 2. Procesar cada item
            for item in items:
                sku = item['sku']
                cantidad = item['cantidad']
                
                print(f"DEBUG CHECKOUT - Procesando item: {sku} x{cantidad}")
                
                # Verificar que el SKU existe en inventario
                cursor.execute("SELECT sku, nombre_producto, talla, precio_unitario, cantidad_disponible FROM Inventario WHERE sku = %s FOR UPDATE", (sku,))
                inv_result = cursor.fetchone()
                
                if not inv_result:
                    raise Exception(f'Producto {sku} no encontrado en inventario')
                
                if inv_result['cantidad_disponible'] < cantidad:
                    raise Exception(f'Stock insuficiente para {sku}. Disponible: {inv_result["cantidad_disponible"]}, Solicitado: {cantidad}')
                
                # Insertar detalle del pedido
                subtotal = inv_result['precio_unitario'] * cantidad
                cursor.execute(
                    """INSERT INTO DetallePedido (id_pedido, sku, nombre_producto, talla, cantidad, precio_unitario, subtotal)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (id_pedido, sku, inv_result['nombre_producto'], inv_result['talla'], cantidad, inv_result['precio_unitario'], subtotal)
                )
                
                # Actualizar inventario
                cursor.execute("UPDATE Inventario SET cantidad_disponible = cantidad_disponible - %s WHERE sku = %s", (cantidad, sku))
                
                print(f"DEBUG CHECKOUT - Item procesado exitosamente: {sku}")
            
            # Confirmar transacción
            connection.commit()
            print(f"DEBUG CHECKOUT - Transacción completada exitosamente")
            
            # Limpiar carrito
            session['cart'] = {}
            session.modified = True
            
            flash(f'Pedido #{id_pedido} creado exitosamente. Total: ${total:.2f}', 'success')
            return redirect(url_for('mis_pedidos'))
            
        except Exception as e:
            # Revertir transacción en caso de error
            if connection:
                connection.rollback()
                print(f"DEBUG CHECKOUT - Transacción revertida")
            
            print(f"DEBUG CHECKOUT - Exception: {str(e)}")
            import traceback
            print(f"DEBUG CHECKOUT - Traceback: {traceback.format_exc()}")
            flash(f'Error al procesar el pedido: {str(e)}', 'danger')
            
        finally:
            # Cerrar cursor y conexión
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    # Calcular items y total para mostrar en el formulario
    cart_items = []
    total = 0
    
    for cart_key, item in cart.items():
        jersey = mongo_conn.db.jerseys.find_one({'_id': item['product_id']})
        if jersey:
            subtotal = jersey['precio_base'] * item['quantity']
            cart_items.append({
                'nombre': jersey['nombre'],
                'equipo': jersey['equipo'],
                'size': item['size'],
                'quantity': item['quantity'],
                'precio': jersey['precio_base'],
                'subtotal': subtotal
            })
            total += subtotal
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('checkout.html', cart_items=cart_items, total=total,
                         user_name=user_name, cart_count=cart_count)

@app.route('/mis-pedidos')
@login_required
def mis_pedidos():
    """Página de pedidos del usuario"""
    query = """
        SELECT p.id_pedido, p.fecha_pedido, p.total, p.estado, p.direccion_envio,
               (SELECT COUNT(*) FROM DetallePedido WHERE id_pedido = p.id_pedido) as total_items
        FROM Pedidos p
        WHERE p.id_usuario = %s
        ORDER BY p.fecha_pedido DESC
    """
    pedidos = mysql_conn.execute_query(query, (session['user_id'],))
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('mis_pedidos.html', pedidos=pedidos, user_name=user_name, 
                         cart_count=cart_count)

@app.route('/pedido/<int:pedido_id>')
@login_required
def pedido_detalle(pedido_id):
    """Página de detalle de un pedido"""
    # Verificar que el pedido pertenezca al usuario
    query_pedido = "SELECT * FROM Pedidos WHERE id_pedido = %s AND id_usuario = %s"
    pedido = mysql_conn.execute_query(query_pedido, (pedido_id, session['user_id']))
    
    if not pedido:
        flash('Pedido no encontrado', 'danger')
        return redirect(url_for('mis_pedidos'))
    
    # Obtener detalles del pedido
    query_detalles = """
        SELECT sku, nombre_producto, talla, cantidad, precio_unitario, subtotal
        FROM DetallePedido
        WHERE id_pedido = %s
    """
    detalles = mysql_conn.execute_query(query_detalles, (pedido_id,))
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('pedido_detalle.html', pedido=pedido[0], detalles=detalles,
                         user_name=user_name, cart_count=cart_count)

@app.route('/api/buscar-cp/<cp>')
def api_buscar_cp(cp):
    """API interna para buscar información de código postal"""
    # Base de datos simplificada de CPs más comunes de México
    codigos_postales = {
        '97115': {'estado': 'Yucatán', 'municipio': 'Mérida', 'colonias': ['Cholul', 'Hacienda Dzodzil', 'Sodzil Norte']},
        '97110': {'estado': 'Yucatán', 'municipio': 'Mérida', 'colonias': ['Cholul', 'San Antonio Xluch']},
        '97130': {'estado': 'Yucatán', 'municipio': 'Mérida', 'colonias': ['Francisco de Montejo', 'Montecarlo']},
        '97000': {'estado': 'Yucatán', 'municipio': 'Mérida', 'colonias': ['Centro', 'Mejorada']},
        '44100': {'estado': 'Jalisco', 'municipio': 'Guadalajara', 'colonias': ['Centro', 'Zona Centro']},
        '44600': {'estado': 'Jalisco', 'municipio': 'Guadalajara', 'colonias': ['Colinas de la Normal', 'Jardines Alcalde']},
        '64000': {'estado': 'Nuevo León', 'municipio': 'Monterrey', 'colonias': ['Centro', 'Monterrey Centro']},
        '66000': {'estado': 'Nuevo León', 'municipio': 'San Pedro Garza García', 'colonias': ['Del Valle']},
        '06000': {'estado': 'Ciudad de México', 'municipio': 'Cuauhtémoc', 'colonias': ['Centro', 'Centro Histórico']},
        '03100': {'estado': 'Ciudad de México', 'municipio': 'Benito Juárez', 'colonias': ['Del Valle Centro', 'Del Valle Norte']},
        '20000': {'estado': 'Aguascalientes', 'municipio': 'Aguascalientes', 'colonias': ['Zona Centro', 'Centro']},
        '76000': {'estado': 'Querétaro', 'municipio': 'Querétaro', 'colonias': ['Centro Histórico', 'Centro']},
        '37000': {'estado': 'Guanajuato', 'municipio': 'León', 'colonias': ['Centro', 'Zona Centro']},
        '80000': {'estado': 'Sinaloa', 'municipio': 'Culiacán', 'colonias': ['Centro', 'Centro Sinaloa']},
        '22000': {'estado': 'Baja California', 'municipio': 'Tijuana', 'colonias': ['Centro', 'Zona Centro']},
    }
    
    if cp in codigos_postales:
        data = codigos_postales[cp]
        return {
            'error': False,
            'response': {
                'cp': cp,
                'estado': data['estado'],
                'municipio': data['municipio'],
                'colonia': data['colonias']
            }
        }
    else:
        return {
            'error': True,
            'message': 'Código postal no encontrado'
        }

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Dashboard de administrador"""
    # Estadísticas
    stats_query = """
        SELECT 
            (SELECT COUNT(*) FROM Usuarios WHERE rol = 'CLIENTE') as total_clientes,
            (SELECT COUNT(*) FROM Pedidos) as total_pedidos,
            (SELECT SUM(total) FROM Pedidos WHERE estado = 'COMPLETADO') as ingresos_totales,
            (SELECT COUNT(*) FROM Pedidos WHERE estado = 'PENDIENTE') as pedidos_pendientes
    """
    stats = mysql_conn.execute_query(stats_query)[0]
    
    # Productos de MongoDB
    total_productos = mongo_conn.db.jerseys.count_documents({'activo': True})
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('admin_dashboard.html', stats=stats, total_productos=total_productos,
                         user_name=user_name, cart_count=cart_count)

@app.route('/admin/pedidos')
@admin_required
def admin_pedidos():
    """Lista de todos los pedidos (admin)"""
    estado_filtro = request.args.get('estado')
    
    if estado_filtro:
        query = """
            SELECT p.id_pedido, p.id_usuario, u.nombre as nombre_usuario, u.email,
                   p.direccion_envio, p.fecha_pedido, p.total, p.estado
            FROM Pedidos p
            JOIN Usuarios u ON p.id_usuario = u.id_usuario
            WHERE p.estado = %s
            ORDER BY p.fecha_pedido DESC
        """
        pedidos = mysql_conn.execute_query(query, (estado_filtro,))
    else:
        query = """
            SELECT p.id_pedido, p.id_usuario, u.nombre as nombre_usuario, u.email,
                   p.direccion_envio, p.fecha_pedido, p.total, p.estado
            FROM Pedidos p
            JOIN Usuarios u ON p.id_usuario = u.id_usuario
            ORDER BY p.fecha_pedido DESC
        """
        pedidos = mysql_conn.execute_query(query)
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('admin_pedidos.html', pedidos=pedidos, user_name=user_name, 
                         cart_count=cart_count)

@app.route('/admin/pedido/<int:pedido_id>/cambiar-estado', methods=['POST'])
@admin_required
def admin_cambiar_estado(pedido_id):
    """Cambiar el estado de un pedido (admin)"""
    nuevo_estado = request.form.get('nuevo_estado')
    
    if nuevo_estado in ['PENDIENTE', 'PROCESANDO', 'COMPLETADO', 'CANCELADO']:
        query = "UPDATE Pedidos SET estado = %s WHERE id_pedido = %s"
        mysql_conn.execute_query(query, (nuevo_estado, pedido_id))
        flash(f'Estado del pedido #{pedido_id} actualizado a {nuevo_estado}', 'success')
    else:
        flash('Estado no válido', 'danger')
    
    return redirect(url_for('admin_pedidos'))

@app.route('/admin/inventario')
@admin_required
def admin_inventario():
    """Ver y gestionar inventario"""
    # Obtener todo el inventario ordenado
    query = """
        SELECT id_inventario, sku, nombre_producto, talla, cantidad_disponible, 
               precio_unitario, fecha_actualizacion
        FROM Inventario
        ORDER BY nombre_producto, talla
    """
    inventario = mysql_conn.execute_query(query)
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('admin_inventario.html', inventario=inventario, 
                         user_name=user_name, cart_count=cart_count)

@app.route('/admin/inventario/<int:id_inventario>/actualizar', methods=['POST'])
@admin_required
def admin_actualizar_inventario(id_inventario):
    """Actualizar cantidad de un item de inventario"""
    nueva_cantidad = request.form.get('cantidad')
    
    try:
        nueva_cantidad = int(nueva_cantidad)
        if nueva_cantidad < 0:
            flash('La cantidad no puede ser negativa', 'danger')
            return redirect(url_for('admin_inventario'))
        
        query = """
            UPDATE Inventario 
            SET cantidad_disponible = %s, fecha_actualizacion = NOW()
            WHERE id_inventario = %s
        """
        mysql_conn.execute_query(query, (nueva_cantidad, id_inventario))
        flash('Inventario actualizado correctamente', 'success')
    except ValueError:
        flash('Cantidad inválida', 'danger')
    
    return redirect(url_for('admin_inventario'))

@app.route('/admin/inventario/agregar', methods=['GET', 'POST'])
@admin_required
def admin_agregar_inventario():
    """Agregar nuevo item al inventario"""
    if request.method == 'POST':
        sku = request.form.get('sku')
        nombre = request.form.get('nombre')
        talla = request.form.get('talla')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')
        
        try:
            cantidad = int(cantidad)
            precio = float(precio)
            
            if cantidad < 0 or precio < 0:
                flash('Cantidad y precio deben ser positivos', 'danger')
                return redirect(url_for('admin_agregar_inventario'))
            
            # Verificar si el SKU ya existe
            check_query = "SELECT id_inventario FROM Inventario WHERE sku = %s"
            existing = mysql_conn.execute_query(check_query, (sku,))
            
            if existing:
                flash(f'Ya existe un producto con el SKU {sku}', 'danger')
                return redirect(url_for('admin_agregar_inventario'))
            
            # Insertar nuevo item
            insert_query = """
                INSERT INTO Inventario (sku, nombre_producto, talla, cantidad_disponible, precio_unitario)
                VALUES (%s, %s, %s, %s, %s)
            """
            mysql_conn.execute_query(insert_query, (sku, nombre, talla, cantidad, precio))
            flash(f'Producto {nombre} agregado correctamente al inventario', 'success')
            return redirect(url_for('admin_inventario'))
            
        except ValueError:
            flash('Datos inválidos. Verifica cantidad y precio', 'danger')
    
    user_name = session.get('user_name')
    cart_count = get_cart_count()
    
    return render_template('admin_agregar_inventario.html', user_name=user_name, cart_count=cart_count)

if __name__ == '__main__':
    import webbrowser
    import threading
    
    port = 5001
    url = f"http://localhost:{port}"
    
    print("=" * 60)
    print("SERVIDOR FLASK INICIADO")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Catalogo: {url}/catalogo")
    print(f"Login: {url}/login")
    print(f"Admin: {url}/admin")
    print("=" * 60)
    print("Abriendo navegador automaticamente...")
    print("=" * 60)
    
    # Abrir navegador después de 1.5 segundos (para dar tiempo al servidor)
    def open_browser():
        import time
        time.sleep(1.5)
        webbrowser.open(url)
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(host='0.0.0.0', port=port, debug=True)
