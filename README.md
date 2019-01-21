# ShopifyChallenge

## Usage

Responses will be in JSON and have the form:
```json
{
    "data": "Importing Stuff",
    "status": "Description of important stuff failing or succeeding"
}
```

### Get all Products
URI: `GET /products`

Response:
```json 
{
                "data": [
                    {
                        "id": 1,
                        "price": 1200,
                        "quantity": 10,
                        "title": "Macbook"
                    },
                    {
                        "id": 2,
                        "price": 1800,
                        "quantity": 5,
                        "title": "Macbook Pro"
                    },
                    {
                        "id": 3,
                        "price": 800,
                        "quantity": 10,
                        "title": "iPad"
                    }
                ]
            }
```

### Get all Instock Products
URI: `GET /products/in-stock`

Response:
```json 
{
                "data": [
                    {
                        "id": 1,
                        "price": 1200,
                        "quantity": 10,
                        "title": "Macbook"
                    },
                    {
                        "id": 2,
                        "price": 1800,
                        "quantity": 5,
                        "title": "Macbook Pro"
                    },
                    {
                        "id": 3,
                        "price": 800,
                        "quantity": 10,
                        "title": "iPad"
                    }
                ]
            }
```


### Get all Orders
URI: `GET /orders`

Response:
```
{
                "data": [
                    {
                        "id": 1,
                        "total_price": 1200,
                        "user_id": 10

                    {
                        "id": 1,
                        "total_price": 1200,
                        "user_id": 10
                    },
                    {
                        "id": 1,
                        "total_price": 1200,
                        "user_id": 10
                    }
                ]
            }
```

### Create new Product
URI: `POST /product/add`

JSON Body:
```
           {
                "title": "Macbook",
                "price": 1000.10,
                "quantity": 5
            }
```   
Response:
- {'status': 'New product successfully added'}, 201
- {'status': 'Existing product. Stock has been added'}), 201
- {'status': 'An error occurred, product could not be added'}), 404



### Create new Cart
URI: `GET /cart/create`

### Create new User
URI: `POST /user/create`

JSON Body:
```
 {
                "username": "shelbaz",
                "password": "abs241",
                "email": "shaw1n@gmail.com"
}
```
Response:
- {'status': 'User id: xxxx' created successfully , cart-id: xxxxx ')}), 201
- {'status': 'An error occurred, user could not be added'}), 404

  
### Add to cart
URI: `POST /cart/add/<userid>`
Argument: userid 

JSON Body:
```
{
            "products": [
                {
                    "id": 1,
                    "quantity": 1
                },
                {
                    "id": 2,
                    "quantity": 2
                },
                {
                    "id": 3,
                    "quantity": 1
                }
                      ]
        }
```
Response:
- {'status': 'Products added to cart of user: xxxx' }
- {'status': 'An error occurred, products could not be added'}), 404


### Remove from cart
URI: `POST /cart/remove/<userid>`
Argument: userid 

JSON Body:
```
{
            "products": [
                {
                    "id": 1
                },
                {
                    "id": 2
                },
                {
                    "id": 3
                }
                      ]
        }
```
Response:
- {'status': 'Products removed from cart of user: xxxx '}
- {'status': 'An error occurred, products could not be removed'}), 404
   
### Checkout from cart
URI: `GET /cart/checkout/<userid>`
Argument: userid 


Response:
- {'status': 'User has checked out and created an order# xxxxx + ' with total ' + $xxxx }


### Get user
URI: `GET /user/<userid>`

### Get product
URI: `GET /product/<productid>`

### Get cart
URI: `GET /cart/<cartid>`

### Get cart items
URI: `GET /cart/items/<cartid>`

### Get order 
URI: `GET /order/<orderid>`
