"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix
    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                #change
                yield obj
        next_token = resp.get('NextContinuationToken', None)

        if not next_token:
            break

#---------------------------------------------------------

"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""

def fn(main_plan, obj: dict, extensions: list = []) -> list:
    """
    product processing

      Parameters:
    - main_plan: an object
    - obj (dict): A dictionary containing information about order items.
    - extensions (list, optional): An optional list of extensions (default is an empty list).

    Returns:
    - list: A list of dictionaries.

    """

    # Initialize variables
    items = []
    sp = False
    cd = False

    ext_p = {}
    # Initialization completion


    # Information parsing in a new dictionary, by id and quantity
    for ext in extensions:
        ext_p[ext['price'].id] = ext['qty']

    # Iterate through the elements of the obj object
    for item in obj['items'].data:
        #extracts the id of the item and places it in a new product dic
        product = {
            'id': item.id
        }

        #verifying if the id of the price is equal to that of the main_plan and if it is not found in ext_p
        if item.price.id != main_plan.id and item.price.id not in ext_p:
            # If the product's price doesn't match the main_plan and it's not in extensions
            product['deleted'] = True  # Mark the product as deleted
            cd = True  # mark the flag as true

        elif item.price.id in ext_p:
            #grab the quantity of product that has that id and store it in the qty variable
            qty = ext_p[item.price.id]
            if qty < 1:
                #if the quantity is less than 1 mark the product as eliminated
                product['deleted'] = True
            else:
                product['qty'] = qty  # if the quantity is greater than 1 assign the quantity to the product dictionary
            del ext_p[item.price.id]  #  the id is removed from the dictionary
        elif item.price.id == main_plan.id:
            sp = True  # the flag of sp is marked as true

        items.append(product)  # product is added to the item list

    # it checks if the sp flag was set if true nothing is done if false the product is created
    if not sp:
        items.append({
            'id': main_plan.id,
            'qty': 1  # with a quantity of 1
        })

    # the items that were not in obj are added.
    for price, qty in ext_p.items():
        if qty >= 1:
            items.append({
                'id': price,
                'qty': qty
            })

    return items  # return the list of processed products

#---------------------------------------------------------
"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b : a + b
    concat = lambda a, b : f'{a},{b}'
    divide = lambda a, b : a / b
    multiply = lambda a, b : a * b


def fn(fn_to_call, *args):

    return getattr(Caller, fn_to_call) (*args)

#---------------------------------------------------------
"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""
def fn(config, w, h):
    v = None
    ar = w / h

    if ar < 1:
        v = [r for r in config['p'] if r['width'] <= w]
    elif ar > 4 / 3:
        v = [r for r in config['l'] if r['width'] <= w]
    else:
        v = [r for r in config['s'] if r['width'] <= w]

    return v

"""
This code takes into account the width and height configuration of a video to calculate its aspect ratio (ar).
Based on this aspect ratio, it determines the appropriate configuration required for the video and returns a 
list of presets that meet the condition
where the video's width is greater than or equal to the configuration.
"""
#---------------------------------------------------------
"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests

class Helper:

    def __int__(self,domain,AUTHORIZATION_TOKEN):
        self.DOMAIN = domain
        self.token_type =  AUTHORIZATION_TOKEN.get("token_type", None)
        self.access_token = AUTHORIZATION_TOKEN.get('access_token',None)
        self.expires_in = AUTHORIZATION_TOKEN.get('expires_in',None)
        self.refresh_token = AUTHORIZATION_TOKEN.get("refresh_token",None)

    def set_search_images_endpoint(self, endpoint):
        self.SEARCH_IMAGES_ENDPOINT = endpoint

    def set_get_image_endpoint(self, endpoint):
        self.GET_IMAGE_ENDPOINT = endpoint

    def set_download_image_endpoint(self, endpoint):
        self.DOWNLOAD_IMAGE_ENDPOINT = endpoint


    def api_call(self, method, endpoint, **kwargs):

        if method not in ('GET', 'POST', 'PUT', 'DELETE'):
            raise ValueError("Método HTTP no válido")

        headers = {
            'Authorization': f'{self.token_type} {self.access_token}',
        }

        URL = f'{self.DOMAIN}/{endpoint}'

        send = {
            'headers': headers,
            'params': kwargs
        }

        try:
            response = requests.request(method, URL, **send)
            return response
        except requests.exceptions.RequestException as e:
            return {f"Error:{e}"}
        except requests.exceptions.HTTPError as e:
            return (f"Error:{e}")

    def search_images(self, **kwargs):
        return self.api_call('GET', self.SEARCH_IMAGES_ENDPOINT, **kwargs)

    def get_image(self, image_id, **kwargs):
        return self.api_call('GET', self.GET_IMAGE_ENDPOINT, **kwargs)

    def download_image(self, image_id, **kwargs):
        return self.api_call('POST', self.DOWNLOAD_IMAGE_ENDPOINT, **kwargs)
