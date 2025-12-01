db = db.getSiblingDB('ecommerce_catalog');

db.createCollection('jerseys');
db.jerseys.createIndex({ "marca": 1 });
db.jerseys.createIndex({ "equipo": 1 });
db.jerseys.createIndex({ "temporada": 1 });
db.jerseys.createIndex({ "precio": 1 });
db.jerseys.createIndex({ "categoria": 1 });
db.jerseys.createIndex({ "tags": 1 });

db.jerseys.insertMany([
    {
        _id: "jersey_rm_home_2024",
        nombre: "Real Madrid Jersey Home 2024",
        equipo: "Real Madrid",
        marca: "Adidas",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del Real Madrid temporada 2024/2025. Incluye tecnología Climacool para máxima ventilación.",
        categoria: "Clubes Europeos",
        imagenes: [
            "/static/images/jerseys/jersey_rm_home_2024.png"
        ],
        tallas_disponibles: ["S", "M", "L", "XL", "XXL"],
        caracteristicas: {
            material: "100% Poliéster reciclado",
            tecnologia: "Climacool",
            corte: "Ajustado",
            peso: "170g"
        },
        precio_base: 89.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["real madrid", "adidas", "la liga", "champions league"],
        fecha_lanzamiento: new Date("2024-07-01"),
        activo: true,
        rating_promedio: 4.8,
        total_reviews: 156
    },
    {
        _id: "jersey_bar_home_2024",
        nombre: "Barcelona Jersey Home 2024",
        equipo: "Barcelona",
        marca: "Nike",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del FC Barcelona temporada 2024/2025. Diseño icónico con rayas blaugrana y tecnología Dri-FIT.",
        categoria: "Clubes Europeos",
        imagenes: [
            "/static/images/jerseys/jersey_bar_home_2024.png"
        ],
        tallas_disponibles: ["S", "M", "L", "XL", "XXL"],
        caracteristicas: {
            material: "100% Poliéster reciclado",
            tecnologia: "Dri-FIT ADV",
            corte: "Stadium Fit",
            peso: "165g"
        },
        precio_base: 89.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["barcelona", "nike", "la liga", "blaugrana"],
        fecha_lanzamiento: new Date("2024-07-01"),
        activo: true,
        rating_promedio: 4.7,
        total_reviews: 203
    },
    {
        _id: "jersey_man_home_2024",
        nombre: "Manchester United Jersey Home 2024",
        equipo: "Manchester United",
        marca: "Adidas",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del Manchester United temporada 2024/2025. Rojo clásico con detalles en negro.",
        categoria: "Premier League",
        imagenes: [
            "/static/images/jerseys/jersey_man_home_2024.png"
        ],
        tallas_disponibles: ["S", "M", "L", "XL", "XXL"],
        caracteristicas: {
            material: "100% Poliéster",
            tecnologia: "Aeroready",
            corte: "Regular Fit",
            peso: "175g"
        },
        precio_base: 79.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["manchester united", "adidas", "premier league", "red devils"],
        fecha_lanzamiento: new Date("2024-06-15"),
        activo: true,
        rating_promedio: 4.6,
        total_reviews: 189
    },
    {
        _id: "jersey_liv_home_2024",
        nombre: "Liverpool Jersey Home 2024",
        equipo: "Liverpool",
        marca: "Nike",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del Liverpool FC temporada 2024/2025. Rojo intenso con tecnología de ventilación.",
        categoria: "Premier League",
        imagenes: [
            "/static/images/jerseys/jersey_liv_home_2024.png"
        ],
        tallas_disponibles: ["S", "M", "L", "XL"],
        caracteristicas: {
            material: "100% Poliéster reciclado",
            tecnologia: "Dri-FIT",
            corte: "Stadium Fit",
            peso: "168g"
        },
        precio_base: 79.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["liverpool", "nike", "premier league", "reds"],
        fecha_lanzamiento: new Date("2024-06-20"),
        activo: true,
        rating_promedio: 4.9,
        total_reviews: 245
    },
    {
        _id: "jersey_psg_home_2024",
        nombre: "PSG Jersey Home 2024",
        equipo: "Paris Saint-Germain",
        marca: "Nike",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del PSG temporada 2024/2025. Azul marino con franja central roja.",
        categoria: "Clubes Europeos",
        imagenes: [
            "/static/images/jerseys/jersey_psg_home_2024.png"
        ],
        tallas_disponibles: ["M", "L", "XL"],
        caracteristicas: {
            material: "100% Poliéster",
            tecnologia: "Dri-FIT",
            corte: "Stadium Fit",
            peso: "170g"
        },
        precio_base: 84.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["psg", "paris", "nike", "ligue 1"],
        fecha_lanzamiento: new Date("2024-07-10"),
        activo: true,
        rating_promedio: 4.5,
        total_reviews: 134
    },
    {
        _id: "jersey_bay_home_2024",
        nombre: "Bayern Munich Jersey Home 2024",
        equipo: "Bayern Munich",
        marca: "Adidas",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del Bayern Munich temporada 2024/2025. Rojo bávaro tradicional.",
        categoria: "Bundesliga",
        imagenes: [
            "/static/images/jerseys/jersey_bay_home_2024.png"
        ],
        tallas_disponibles: ["S", "M", "L", "XL"],
        caracteristicas: {
            material: "100% Poliéster reciclado",
            tecnologia: "Aeroready",
            corte: "Slim Fit",
            peso: "172g"
        },
        precio_base: 89.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["bayern", "munich", "adidas", "bundesliga"],
        fecha_lanzamiento: new Date("2024-06-25"),
        activo: true,
        rating_promedio: 4.7,
        total_reviews: 167
    },
    {
        _id: "jersey_ame_home_2024",
        nombre: "Club América Jersey Home 2024",
        equipo: "Club América",
        marca: "Nike",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del Club América temporada 2024/2025. Amarillo icónico de Las Águilas.",
        categoria: "Liga MX",
        imagenes: [
            "/static/images/jerseys/jersey_ame_home_2024.png"
        ],
        tallas_disponibles: ["S", "M", "L", "XL", "XXL"],
        caracteristicas: {
            material: "100% Poliéster",
            tecnologia: "Dri-FIT",
            corte: "Stadium Fit",
            peso: "165g"
        },
        precio_base: 74.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["america", "nike", "liga mx", "aguilas"],
        fecha_lanzamiento: new Date("2024-06-10"),
        activo: true,
        rating_promedio: 4.8,
        total_reviews: 198
    },
    {
        _id: "jersey_dor_home_2024",
        nombre: "Borussia Dortmund Jersey Home 2024",
        equipo: "Borussia Dortmund",
        marca: "Puma",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del Borussia Dortmund temporada 2024/2025. Amarillo y negro característico del BVB.",
        categoria: "Bundesliga",
        imagenes: [
            "/static/images/jerseys/jersey_dor_home_2024.png"
        ],
        tallas_disponibles: ["S", "M", "L", "XL"],
        caracteristicas: {
            material: "100% Poliéster reciclado",
            tecnologia: "DryCELL",
            corte: "Regular Fit",
            peso: "170g"
        },
        precio_base: 79.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["dortmund", "puma", "bundesliga", "bvb"],
        fecha_lanzamiento: new Date("2024-06-28"),
        activo: true,
        rating_promedio: 4.6,
        total_reviews: 142
    },
    {
        _id: "jersey_mia_home_2024",
        nombre: "Inter Miami CF Jersey Home 2024",
        equipo: "Inter Miami CF",
        marca: "Adidas",
        temporada: "2024/2025",
        tipo: "Home",
        descripcion: "Jersey oficial del Inter Miami CF temporada 2024/2025. Rosa característico con detalles en negro.",
        categoria: "MLS",
        imagenes: [
            "/static/images/jerseys/jersey_mia_home_2024.png"
        ],
        tallas_disponibles: ["S", "M", "L", "XL", "XXL"],
        caracteristicas: {
            material: "100% Poliéster reciclado",
            tecnologia: "Aeroready",
            corte: "Regular Fit",
            peso: "168g"
        },
        precio_base: 84.99,
        edicion_especial: false,
        personalizable: true,
        tags: ["inter miami", "mls", "adidas", "miami"],
        fecha_lanzamiento: new Date("2024-07-05"),
        activo: true,
        rating_promedio: 4.9,
        total_reviews: 312
    }
]);

db.createCollection('comentarios');

db.comentarios.createIndex({ "producto_id": 1 });
db.comentarios.createIndex({ "usuario_id": 1 });
db.comentarios.createIndex({ "rating": 1 });
db.comentarios.createIndex({ "fecha": -1 });

db.comentarios.insertMany([
    {
        producto_id: "jersey_rm_home_2024",
        usuario_id: 2,
        usuario_nombre: "Juan Pérez",
        rating: 5,
        titulo: "Excelente calidad",
        comentario: "El jersey es de excelente calidad. Los colores son vibrantes y el material es muy cómodo. Totalmente recomendado.",
        fecha: new Date("2024-08-15"),
        verificado: true,
        util_count: 23
    },
    {
        producto_id: "jersey_rm_home_2024",
        usuario_id: 3,
        usuario_nombre: "María García",
        rating: 4,
        titulo: "Muy bueno pero caro",
        comentario: "La calidad es excelente, pero el precio es un poco elevado. Aun así, vale la pena por ser producto oficial.",
        fecha: new Date("2024-08-20"),
        verificado: true,
        util_count: 15
    },
    {
        producto_id: "jersey_bar_home_2024",
        usuario_id: 2,
        usuario_nombre: "Juan Pérez",
        rating: 5,
        titulo: "Perfecto para fanáticos del Barça",
        comentario: "Como seguidor del Barcelona, este jersey es imprescindible. El diseño es hermoso y la calidad Nike es notable.",
        fecha: new Date("2024-07-30"),
        verificado: true,
        util_count: 31
    },
    {
        producto_id: "jersey_liv_home_2024",
        usuario_id: 3,
        usuario_nombre: "María García",
        rating: 5,
        titulo: "¡You'll Never Walk Alone!",
        comentario: "El mejor jersey de la temporada. La tecnología Dri-FIT funciona perfectamente. ¡YNWA!",
        fecha: new Date("2024-09-01"),
        verificado: true,
        util_count: 42
    }
]);

db.createCollection('logs');

db.logs.createIndex({ "tipo": 1 });
db.logs.createIndex({ "usuario_id": 1 });
db.logs.createIndex({ "timestamp": -1 });
db.logs.createIndex({ "ip": 1 });

db.logs.insertMany([
    {
        tipo: "LOGIN",
        usuario_id: 1,
        usuario_email: "admin@jerseys.com",
        ip: "192.168.1.100",
        user_agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        timestamp: new Date("2024-11-20T10:30:00Z"),
        exitoso: true
    },
    {
        tipo: "BUSQUEDA",
        usuario_id: 2,
        termino: "real madrid",
        resultados: 3,
        ip: "192.168.1.101",
        timestamp: new Date("2024-11-20T11:15:00Z")
    },
    {
        tipo: "VISTA_PRODUCTO",
        usuario_id: 2,
        producto_id: "jersey_rm_home_2024",
        ip: "192.168.1.101",
        timestamp: new Date("2024-11-20T11:16:30Z")
    },
    {
        tipo: "AGREGAR_CARRITO",
        usuario_id: 2,
        producto_id: "jersey_rm_home_2024",
        sku: "RM-HOME-2024-M",
        cantidad: 1,
        ip: "192.168.1.101",
        timestamp: new Date("2024-11-20T11:20:00Z")
    }
]);

print("===========================================");
print("Base de datos MongoDB inicializada correctamente");
print("===========================================");
print("Total de jerseys: " + db.jerseys.countDocuments());
print("Total de comentarios: " + db.comentarios.countDocuments());
print("Total de logs: " + db.logs.countDocuments());
print("===========================================");
print("Índices creados en jerseys:");
db.jerseys.getIndexes().forEach(function(index) {
    print("  - " + JSON.stringify(index.key));
});
print("===========================================");
