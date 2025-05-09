from flask import Flask, request, jsonify
from utils import Load_json, Save_json
import json

app = Flask(__name__)

#detting the path for the json file
path = 'data.json'

# Load the update_products from the file
products = Load_json(path)


#route for home age
@app.route('/')
def home():
    return "Welcome to the Product API!"


#route for getting/reading products using query parameters
@app.route('/products/get', methods=['GET'])
def get_products_query():

    # get all query args
    args = request.args.to_dict(flat=True)

    # Extract fields param if exists
    fields = args.pop("fields", None)

    filtered_data = []
    for product in products:
        match = True
        for key, value in args.items():
            if str(product.get(key)) != value:
                match = False
                break
        if match:
            filtered_data.append(product)

    # If no filters matched, fallback to return all
    if not args:
        filtered_data = products

    # If fields are specified, return only those fields
    if fields:
        selected_fields = fields.split(",")
        filtered_data = [
            {key: item[key] for key in selected_fields if key in item}
            for item in filtered_data
        ]

    if filtered_data:
        # Return the response
        return jsonify({"status": "success", "Product List": filtered_data})
    else:
        # Return an error message if no products matched the filters
        return jsonify({"status": "error", "message": "No products found matching the criteria."}), 404
    


#route for getting/reading products by ID using path parameters
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products_by_id(product_id):

    # Get the product using IDs
    product_item = next((product for product in products if product['id'] == product_id), None)

    if product_item:
        return jsonify(product_item), 200
    else:
        return jsonify({'error': 'No products found'}), 404



#route for adding/createing to product details using query parameters
@app.route('/products/create', methods=['POST'])
def create_products_query():
    
    # get all query args
    args = request.args.to_dict(flat=True)

    # Extract fields param if exists
    fields = args.pop("fields", None)
    
    # Validate required fields (e.g. id, name)
    if 'id' not in args or 'name' not in args:
        return jsonify({'error': 'Missing required fields: id and name'}), 400
    
    # if the product ID already exists, return an error
    if any(p['id'] == args['id'] for p in products):
        return jsonify({'error': 'Product ID already exists'}), 400
    
    # Convert 'id' to an integer
    args['id'] = int(args['id'])

    # create a new product
    new_product = {key: value for key, value in args. items()}
    products.append(new_product)

    # save the updated products list to the file
    Save_json(products, path)

    # If fields are specified, return only those fields
    if fields:
        selected_fields = fields.split(",")
        new_product = {key: new_product[key] for key in selected_fields if key in new_product}
            

    if new_product:
        # Return the response
        return jsonify({"status": "success", "Updated Product List": products}), 201
    else:
        # Return an error message if no products matched the filters
        return jsonify({"status": "error", "message": "No products found matching the criteria."}), 404 


#route for adding/creating to product details by usig path parameters
@app.route('/products/', methods=['POST'])
def create_products_by_id():
    # Get the prduct update_products from the json body
    update_products = request.get_json()

    if not update_products :
        return jsonify({'error': 'No update_products provided'}), 400
    
    elif any(p['id'] == update_products['id'] for p in products):
        return jsonify({'error': 'Product ID already exists'}), 400
    
    else:
        # Add the product to the list of products
        products.append(update_products)
        Save_json(products, path) # Save the updated products list to the file


    return jsonify({'message': 'Product created successfully', 'product': products}), 200 #status code for susccessfully updated  





#route for updating product details using query parameters
@app.route('/products/update', methods=['PUT', 'PATCH'])
def update_products_query():
    # get all query args
    args = request.args.to_dict(flat=True)

    # Extract fields param if exists
    fields = args.pop("fields", None)

    # Validate required field 'id'
    if 'id' not in args:
        return jsonify({'error': 'Missing required fields: id'}), 400
    
    # flag for update product status
    update_product = []

    if(request.method == 'PUT'):

        # flag for product found
        found = False

        for idx, product in enumerate(products):
            if product['id'] == int(args['id']):
                
                # update the product details
                products[idx].update(args)

                # Ensure the 'id' field remains an integer
                products[idx]['id'] = int(products[idx]['id'])

                update_product = products[idx]

                found = True
                break
        
        if not found:
            return jsonify({'error': 'Product not found'}), 404
        
        # If fields are specified, return only those fields
        if fields:
            selected_fields = fields.split(",")
            update_product = {key: update_product[key] for key in selected_fields if key in update_product}

        Save_json(products, path) # Save the updated products list to the file

        return jsonify({'message': 'Product Updated Successfully', 'product': update_product}), 200
    
    elif(request.method == 'PATCH'):

        # flag for product found
        found = False

        # update the product details
        for idx, product in enumerate(products):
            if product['id'] == int(args['id']):
                
                # update the product details
                products[idx].update(args)

                # Ensure the 'id' field remains an integer
                products[idx]['id'] = int(products[idx]['id'])

                update_product = products[idx]

                found = True
                break
        
        if not found:
            return jsonify({'error': 'Product not found'}), 404
        
        # If fields are specified, return only those fields
        if fields:
            selected_fields = fields.split(",")
            update_product = {key: update_product[key] for key in selected_fields if key in update_product}

        
        # Save the updated products list to the file
        Save_json(products, path)

        return jsonify({'message': 'Product Updated Successfully', 'product': update_product}), 200



#route for updating product details
@app.route('/products/<int:product_id>', methods=['PUT', 'PATCH'])
def update_products_by_id(product_id):
    # Get the product update_products from the json body
    update_products = request.get_json()

    if(request.method == 'PUT'):

        # Flag for product found
        found = False
        # Update the product details
        for idx, product in enumerate(products):
            if product['id'] == product_id:
                # Update the product details
                products[idx].update(update_products)
                found = True
                break

        if not found:
            return jsonify({'error': 'Product not found'}), 404
        
        Save_json(products, path) # Save the updated products list to the file

        return jsonify({'message': 'Product Updated Successfully', 'product': product}), 200
            

    elif(request.method == 'PATCH'):

        # Flag for product found
        found = False

        # Update the product details
        for idx, product in enumerate(products):
            if product['id'] == product_id:
                # Update the product details
                products[idx].update(update_products)
                found = True
                break

        if not found:
            return jsonify({'error': 'Product not found'}), 404
        
        Save_json(products, path) # Save the updated products list to the file

        return jsonify({'message': 'Product Updated Successfully', 'product': product}), 200



#route for deleting product details uding query parameters
@app.route('/products/delete', methods=['DELETE'])
def delete_products_query():

    # get all query args
    args = request.args.to_dict(flat=True)

    # Extract fields param if exists
    field_to_delete = args.pop("fields", None)

    # Validate required field 'id'
    if 'id' not in args:
        return jsonify({'error': 'Missing required fields: id'}), 400

    # Flag for product found
    found = False

    # product delete status
    deleted_product = []

    # Delete the product details
    for idx, product in enumerate(products):
        if product['id'] == int(args['id']):
            if field_to_delete:
                # Delete single/multiple fields
                fields = field_to_delete.split(",")
                for field in fields:
                    if field in product:
                        del product[field]
                    else:
                        return jsonify({'error': f"Field '{field_to_delete}' not found in product"}), 404
            
                deleted_product = product  # Keep the updated product
                found = True

            else:
                # Store the product details before deletion
                deleted_product = product
                products.pop(idx)
                found = True
                break

    if not found:
        return jsonify({'error': 'Product not found'}), 404
        
    Save_json(products, path) # Save the updated products list to the file

     # Return the response
    if field_to_delete:
        return jsonify({'message': f"Field '{field_to_delete}' deleted successfully", 'product': deleted_product}), 200
    else:
        return jsonify({'message': 'Product Deleted Successfully', 'product': deleted_product}), 200


#route for deleting product details using path parameters
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_products_by_id(product_id):

    update_products = request.get_json()

    if not update_products:
        return jsonify({'error': 'No update_products provided'}), 400
    
    for product in products:
        if product['id'] == product_id:
            # Delete the product from the list of products
            products.remove(product)
            Save_json(products, path) # Save the updated products list to the file

            return jsonify({'message': 'Product Deleted Successfully'}), 200
        


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)