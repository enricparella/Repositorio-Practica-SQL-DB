# Normalización del modelo de datos

El modelo de datos de KTE E-Commerce se ha diseñado siguiendo los principios de normalización para reducir la redundancia, mantener la coherencia de la información y facilitar las relaciones entre las diferentes entidades.

## Primera Forma Normal (1NF)

El modelo cumple la Primera Forma Normal porque cada tabla dispone de una clave primaria que identifica de forma única cada registro y todos los campos contienen valores atómicos.

No existen grupos de datos repetidos dentro de una misma fila. Por ejemplo, los productos de un pedido no se almacenan mediante campos como `product_1`, `product_2` o `product_3`. Cada producto asociado a un pedido se representa mediante un registro independiente en la tabla `order_items`.

## Segunda Forma Normal (2NF)

El modelo también cumple la Segunda Forma Normal porque cumple previamente la 1NF y los atributos de cada tabla dependen de la entidad identificada por su clave primaria.

La relación de muchos a muchos entre pedidos y productos se resuelve mediante la tabla intermedia `order_items`. Cada línea de pedido identifica el pedido y el producto correspondiente mediante `order_id` y `product_id`, almacenando únicamente información propia de esa línea, como la cantidad, el precio en el momento de la compra y el descuento aplicado.

De esta forma, la información propia de los pedidos permanece en `orders` y la información propia de los productos permanece en `products`.

## Tercera Forma Normal (3NF)

Por último, el modelo cumple la Tercera Forma Normal porque cumple previamente la 2NF y evita almacenar información que dependa de atributos no clave pertenecientes a otras entidades.

Por ejemplo, los datos personales y geográficos de los clientes se almacenan únicamente en `customers`, mientras que `orders` utiliza `customer_id` para relacionar cada pedido con su cliente.

De igual manera, la información de las categorías se almacena en `categories` y los productos únicamente mantienen la referencia `category_id`. Los pagos se encuentran separados en `payments` y las valoraciones en `reviews`, relacionadas con las entidades correspondientes mediante sus claves.

Esta separación evita duplicar información y permite actualizar los datos de cada entidad sin tener que modificar múltiples registros en otras tablas.

## Conclusión:

La estructura final separa las distintas responsabilidades del modelo en las tablas `customers`, `categories`, `products`, `orders`, `order_items`, `payments` y `reviews`, conectadas mediante claves primarias y foráneas.

El diseño cumple las tres primeras formas normales y proporciona una estructura adecuada para almacenar y analizar los datos del e-commerce.