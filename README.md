🚀 Instrucciones de Ejecución en Local
Para replicar el entorno de desarrollo y levantar el servidor de pruebas:

Clonar el repositorio y posicionarse en la carpeta raíz.

Activar el entorno virtual de Python:

Bash
    source .venv/bin/activate
    ```
3.  **Instalar las dependencias** requeridas:
```bash
    pip install -r requirements.txt
    ```
4.  **Iniciar el servidor** de desarrollo:
```bash
    python3 manage.py runserver
    ```
5.  Acceder a la plataforma desde el navegador web en `http://127.0.0.1:8000/`.

---

## 📸 Capturas del Sistema en Funcionamiento

### 1. Catálogo de Prendas
https://github.com/user-attachments/assets/c3086233-6f7c-4d6b-8df2-e8be13adbd0b

### 2. Panel de Gestión de Productos (Control de Catálogo)
https://github.com/user-attachments/assets/61648a41-4d9e-4227-b218-4a46953d1034

### 3. Formulario de Carga
(https://github.com/user-attachments/assets/a1359f3b-2b0f-4a1d-ae48-24ce9d982506

### 4. Panel de Administración
https://github.com/user-attachments/assets/5123a41c-f588-429e-b48e-b862f93118da

# Vittas Indumentaria - Sistema de Gestión E-Commerce

Sistema integral de gestión de catálogo, control de stock y administración de comercio electrónico desarrollado en **Django** y estilizado de forma nativa con **Tailwind CSS**. Este proyecto fue desarrollado desde cero para la materia Ingeniería de Software (Trabajo Práctico Evaluativo 2026).


*   **Ecosistema de Base de Datos:** Contiene **7 modelos relacionados** en la base de datos (`Usuario`, `Producto`, `Categoria`, `Talle`, `VarianteProducto`, `Pedido` y `DetallePedido`), superando el mínimo de 6 requerido.
*   **Gestión de Multimedia Functional:** El modelo `Producto` posee un campo `ImageField` completamente operativo para la carga de imágenes de las prendas en el servidor local.
*   **Usuarios Personalizados:** Extensión del sistema de autenticación de Django mediante `AbstractUser` para incluir campos de legajo, contacto y dirección.
*   **Control de Acceso y Permisos (RBAC):** Flujo completo de Login/Logout y Registro por templates. Los usuarios de la firma se agrupan en roles corporativos (`Vendedores`, `Teroseros`) con permisos granulares para el uso de las vistas de creación, edición y baja.
*   **Navegación Interactiva y Panel de Control:** CRUD completo para la gestión interna de prendas y categorías. Además, el Panel de Administración de Django fue enriquecido con filtros de búsqueda avanzada, inlines de variantes de stock y marcas visuales de estado.
*   **Optimización del Servidor:** Inclusión de un `Context Processor` global encargado de inyectar de manera dinámica las categorías de ropa en la barra de navegación.

---

## 🛠️ Arquitectura del Proyecto (Estructura de Archivos)

```text
.
├── tienda/                     # Aplicación principal del negocio
│   ├── admin.py                # Personalización avanzada del Django Admin
│   ├── context_processors.py   # Inyector dinámico del menú de categorías
│   ├── forms.py                # Formularios con inyección de clases Tailwind
│   ├── models.py               # Declaración de los 7 modelos relacionales
│   ├── templates/tienda/       # Sistema completo de Plantillas (HTML + Tailwind)
│   │   ├── base.html           # Estructura madre, mensajes y barra de navegación global
│   │   ├── catalogo.html       # Galería e interfaz pública del e-commerce
│   │   ├── detalle_producto.html # Vista técnica y ampliación de cada prenda
│   │   ├── confirmar_borrado.html # Pantalla de seguridad para confirmación de bajas lógicas
│   │   ├── login.html          # Interfaz de inicio de sesión de usuarios
│   │   ├── registro.html       # Formulario de alta para nuevos clientes
│   │   ├── crud_productos.html # Panel maestro de control de stock y catálogo
│   │   ├── form_producto.html  # Formulario estilizado de alta/edición de prendas
│   │   ├── crud_empleados.html # Panel de control de personal y roles de la firma
│   │   ├── form_empleado.html  # Formulario interactivo de altas/ediciones de legajos
│   │   ├── form_categorias.html # Formulario de gestión para agrupaciones de catálogo
│   │   └── form_talle.html     # Formulario de alta para la matriz de talles de ropa
│   └── views.py                # Controladores (Vistas Basadas en Clases con Mixins de seguridad)
