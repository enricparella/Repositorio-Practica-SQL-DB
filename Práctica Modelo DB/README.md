# KTE E-commerce — Modelo de datos en BigQuery

Este proyecto implementa un modelo de datos para KTE E-commerce utilizando Google Cloud BigQuery.

El modelo representa el flujo principal de una plataforma de comercio electrónico mediante siete entidades/tablas relacionadas en una sola DB, siendo estas: clientes, categorías, productos, pedidos, líneas de pedido, pagos y valoraciones.

La práctica incluye el diseño del modelo entidad-relación, la creación de las tablas en BigQuery, la generación y carga de datos sintéticos, la validación de la integridad y coherencia de los datos y la ejecución de consultas SQL orientadas al análisis del negocio.

El desarrollo se presenta mediante tres notebooks y, adicionalmente, mediante un script `seed.py` que permite automatizar la creación y población de la base de datos desde la línea de comandos.


## Modelo de datos

El modelo está formado por siete tablas que representan las principales entidades y operaciones del e-commerce:

- **`customers`**: almacena la información de los clientes, incluyendo datos de contacto, ubicación, canal de adquisición y fecha de registro.

- **`categories`**: contiene las categorías utilizadas para clasificar los productos, junto con su nombre y descripción.

- **`products`**: almacena el catálogo de productos, incluyendo su categoría, precios de venta y coste, stock disponible y estado activo.

- **`orders`**: representa los pedidos realizados por los clientes. Incluye el estado del pedido, la información de envío y las fechas asociadas a su ciclo de vida.

- **`order_items`**: contiene las líneas de cada pedido y resuelve la relación entre pedidos y productos. Registra el producto adquirido, la cantidad, el precio en el momento de la compra y el descuento aplicado.

- **`payments`**: registra la información de pago asociada a cada pedido, incluyendo el método de pago, estado, importe y fecha.

- **`reviews`**: almacena las valoraciones realizadas sobre productos comprados, vinculando cada valoración con su correspondiente línea de pedido.

Las relaciones principales del modelo son:

- Un cliente puede realizar múltiples pedidos.
- Una categoría puede contener múltiples productos.
- Un pedido puede contener múltiples líneas de pedido.
- Un producto puede aparecer en múltiples líneas de pedido.
- Cada pedido dispone de un pago asociado.
- Una línea de pedido puede disponer de una valoración.

La relación de muchos a muchos entre `orders` y `products` se resuelve mediante la tabla intermedia `order_items`.


## Parte I — Desarrollo mediante notebooks

### 01_setup_bigquery.ipynb

Configura la conexión con Google Cloud BigQuery mediante las variables de entorno del proyecto, crea el dataset `kte_ecom` y define los esquemas de las siete tablas del modelo.

Las tablas se crean en el orden necesario para respetar sus dependencias lógicas y dejar preparada la estructura sobre la que posteriormente se cargarán los datos.

### 02_generate_data.ipynb

Genera los datos sintéticos necesarios para poblar las siete tablas del modelo utilizando `Faker` y lógica aleatoria controlada según las reglas de negocio definidas.

En este notebook se crean los DataFrames de clientes, categorías, productos, pedidos, líneas de pedido, pagos y valoraciones, manteniendo la coherencia entre entidades y fechas.

También se define una función reutilizable para cargar cada DataFrame en BigQuery mediante `WRITE_TRUNCATE`, permitiendo reemplazar los datos existentes y validar que la carga se haya completado correctamente.

### 03_queries_verification.ipynb

Verifica que los datos cargados en BigQuery sean coherentes y cumplan las reglas definidas para el modelo.

Incluye comprobaciones sobre el número de registros, duplicados en identificadores, integridad referencial, reglas de negocio y consistencia entre estados y fechas.

Además, incorpora cinco consultas analíticas para comprobar el funcionamiento del modelo desde una perspectiva de negocio, incluyendo ingresos mensuales, productos más vendidos, clientes por país, tiempo medio de entrega e ingresos por categoría.

## Parte II — Seed automatizado

### seed.py

El archivo `seed.py` automatiza la creación y población completa del modelo de datos en BigQuery desde la línea de comandos.

Su objetivo es reproducir en una única ejecución las tareas realizadas de forma separada en los notebooks: preparar el dataset, crear las tablas, generar los datos sintéticos y cargarlos en BigQuery.

El script se ha estructurado mediante funciones independientes para separar cada responsabilidad y facilitar su lectura, mantenimiento y reutilización.

En primer lugar, `argparse` permite recibir desde terminal los principales parámetros de ejecución, como el identificador del proyecto de Google Cloud, el dataset de destino y el número de clientes y pedidos que se desean generar.

A continuación, el script establece la conexión con BigQuery y crea el dataset si todavía no existe. Después se definen los esquemas de las siete tablas y se crean en el orden correspondiente al modelo de datos.

La generación de información se realiza mediante funciones específicas para cada entidad:

- `generate_customers()` genera clientes sintéticos mediante `Faker`.
- `generate_categories()` crea el catálogo fijo de categorías.
- `generate_products()` genera el catálogo de productos, asignando categorías, precios, stock y estado.
- `generate_orders()` crea los pedidos y aplica lógica temporal en función de su estado.
- `generate_order_items()` genera las líneas de pedido y relaciona cada pedido con los productos adquiridos.
- `generate_payments()` calcula el importe de cada pedido a partir de sus líneas y asigna un estado de pago coherente con el estado del pedido.
- `generate_reviews()` genera valoraciones únicamente sobre líneas pertenecientes a pedidos entregados o devueltos, utilizando una probabilidad aproximada del 35 %.

Las relaciones entre tablas se mantienen durante la generación utilizando los identificadores previamente creados. De esta forma, los pedidos siempre hacen referencia a clientes existentes, las líneas de pedido a pedidos y productos válidos, los pagos a pedidos existentes y las valoraciones a líneas de pedido válidas.

La carga de los DataFrames se centraliza en la función `load_dataframe()`. Esta función utiliza `WRITE_TRUNCATE`, por lo que cada ejecución sustituye el contenido anterior de las tablas por el nuevo conjunto de datos generado. Esto permite ejecutar el seed repetidamente sin acumular registros de ejecuciones anteriores.

Después de cada carga se consulta de nuevo la tabla en BigQuery para comprobar el número de registros almacenados y confirmar que la operación se ha completado correctamente.

Finalmente, la función `main()´ coordina todo el proceso siguiendo el orden necesario:

1. Lectura de parámetros.
2. Conexión con BigQuery y creación del dataset.
3. Creación de las tablas.
4. Generación de los DataFrames.
5. Carga de los datos en BigQuery.
6. Confirmación de la finalización del proceso.

El bloque:

#```
python
if __name__ == "__main__":
    main()
#´´´
garantiza que el proceso completo se ejecute únicamente cuando seed.py se lanza directamente desde la terminal, evitando que se ejecute automáticamente si el archivo se importa desde otro módulo.

### Parámetros disponibles

El script permite configurar la ejecución mediante los siguientes argumentos:

- `--project`: ID del proyecto de Google Cloud. Obligatorio.
- `--dataset`: ID del dataset de BigQuery. Obligatorio.
- `--customers`: número de clientes a generar. Valor por defecto: `500`.
- `--orders`: número de pedidos a generar. Valor por defecto: `2000`.

### Ejecución

Desde la raíz del proyecto, el seed puede ejecutarse mediante:

python src/seed.py --project project-sql-big-query-epm --dataset kte_ecom --customers 500 --orders 2000

Los parámetros --customers y --orders pueden modificarse para generar conjuntos de datos de diferente tamaño.

## Diagrama entidad-relación

El diagrama entidad-relación representa gráficamente las siete tablas del modelo, sus campos, claves y relaciones.

Se encuentra disponible en:

`src/docs/er_diagram.png`


## Normalización

El modelo ha sido diseñado siguiendo los principios de normalización hasta la Tercera Forma Normal (3NF), con el objetivo de reducir redundancias y mantener la coherencia entre las diferentes entidades.

El análisis completo de la Primera, Segunda y Tercera Forma Normal se encuentra documentado en:

`src/docs/normalizacion.md`


## Instalación y configuración

Se recomienda utilizar un entorno virtual de Python para instalar las dependencias del proyecto.

### 1. Instalar las dependencias

Desde la raíz del proyecto:

```bash
pip install -r requirements.txt
```

### 2. Configurar las credenciales de Google Cloud

El proyecto requiere una cuenta de servicio con permisos para trabajar con BigQuery.

El archivo de credenciales debe guardarse en:

```text
src/credentials/service-account.json
```

La carpeta `credentials` está excluida del repositorio mediante `.gitignore` para evitar publicar información sensible.

### 3. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto tomando como referencia `.env.example`:

```env
GCP_PROJECT_ID=tu-proyecto
BQ_DATASET_ID=tu_dataset
GOOGLE_APPLICATION_CREDENTIALS=../credentials/service-account.json
```

El archivo `.env` también está excluido del repositorio y debe configurarse localmente antes de ejecutar los notebooks.

Una vez completada la configuración, los notebooks pueden ejecutarse en orden (`01`, `02` y `03`) o puede utilizarse `seed.py` para automatizar la creación y carga del modelo.

## Tecnologías utilizadas

## Tecnologías utilizadas

- **Python**: generación de datos, automatización y conexión con BigQuery.
- **Google Cloud BigQuery**: almacenamiento, gestión y consulta del modelo de datos.
- **SQL**: validación de datos y consultas analíticas.
- **Pandas**: creación y manipulación de DataFrames.
- **Faker**: generación de datos sintéticos.
- **google-cloud-bigquery**: integración entre Python y BigQuery.
- **python-dotenv**: gestión de variables de entorno.
- **Jupyter Notebook**: desarrollo y documentación del flujo principal de la práctica.
- **dbdiagram.io**: diseño y representación del diagrama entidad-relación.