# Grocery-App
Description:
In this project, I have designed a multi-user app (one required admin/store manager and other users) web application using the Flask framework, which allows Admins/Managers to create, edit and remove categories, add, edit, and remove products to those categories, view product details, update product information, and Users can buy many products for one or multiple sections, Ability to search for products, ability to add products to cart. Furthermore, the application also includes Form with validation for username and password for user and Separate form for admin login.


Technologies used:
1. Bootstrap: Used for designing the aesthetics and overall look of the application's user interface.
2. Flask: Utilized for developing web applications using Python, providing a lightweight and efficient framework.
3. Flask-SQL Alchemy: Employed to create database schemas and tables using SQL Alchemy with Flask. It offers default settings and helper functions.
4. render_template: This is used to render HTML templates in the application. It leverages the Jinja2 template engine and resides in the templates folder.
5. Datetime: A Python module used to handle date and time operations, including creating timestamps in the application.
6. session: A Flask extension supporting server-side sessions within the application.
7. request: Used to manage HTTP requests and responses within the application.
8. flash: Enables the generation of informative messages within the Flask application.
9. redirect: Used to redirect users to different endpoints via specified URLs and assigned status codes.
10. route: Used to bind specific URLs to associated functions that perform various tasks. These functions are triggered when the specified URL is accessed.


Database Schema:
1. User: id, username, password, role
2. Category: id, name
3. Order: id, product_name, category_name, amount, quantity, user_id
4. Coupon: id, code, value, type
5. Product: id, name, description, price, mgf_date, exp_date, stock, category_id , img_name
Architecture and Features of Grocery App Project:
•Technology Stack: HTML, CSS, Bootstrap, Flask, and Jinja2.
•Web application developed using Flask, a Python web framework.
•Front-end designed with HTML and CSS for user interface.
•Utilizes Bootstrap for responsive and visually appealing UI design.
•Jinja2 templating engine used for rendering dynamic data in HTML templates.
•Implements HTML Validation user authentication and authorization for secure access to certain functionalities.
•Utilizes SQLAlchemy, to interact with the database.
•Database schema includes tables for users, categories, products, coupon, order.
•Various routes defined to handle different functionalities such as adding products, updating product information, and processing product purchases.
•Provides a user-friendly and intuitive interface for managing product categories and purchases.


Routes and Views:
1. `@app.route('/manager', methods=['GET'])`: Manager page to manage categories and products.
2. `@app.route('/create/category', methods=['GET', 'POST'])`: Route to create new product categories.
3. @app.route('/manager/category/<int:category_id>', methods=['GET', 'POST'])
4. @app.route('/category/delete/<int:category_id>', methods=['GET', 'POST'])
5. `@app.route('/create/product', methods=['GET', 'POST'])`: Route to add new products to existing categories.
6. `@app.route('/update/product/<int:pro_id>', methods=['GET', 'POST'])`: Route to update product details.
7. `@app.route('/delete/product/<int:pro_id>', methods=['GET', 'POST'])`: Route to delete products.
8. @app.route('/manager/create/coupon', methods=['POST', 'GET'])
9. @app.route('/manager/delete/coupon/<int:id>', methods=['POST', 'GET'])
10. @app.route('/user', methods=['POST','GET'])
11. @app.route('/user/category/<int:category_id>', methods=['POST','GET'])
12. @app.route('/user/session/cart/activated', methods=['POST','GET'])
13. @app.route('/user/mycart')
14. `@app.route('/checkout', methods=['GET', 'POST'])`: Route to review and finalize purchases (User).
15. @app.route('/remove/item/<string:key>')
16. @app.route('/user/cancel/checkout')
17. @app.route('/user/history')
18. @app.route('/login/user',methods=['GET', 'POST'])
19. @app.route('/login/manager',methods=['GET', 'POST'])
20. @app.route('/register', methods=['GET', 'POST'])
21. @app.route('/logout')


Conclusion:

This documentation provides an overview of the models and overall system design of the web application. It describes the database schema and the different components of the application, including the models, routes, and user authentication. The grocery app project represents a successful implementation of a multi-user platform for buying groceries. With Flask as the foundation, it seamlessly integrates category and product management, user authentication, and an intuitive shopping experience. The use of Jinja2 templates and Bootstrap ensures a user-friendly interface.
