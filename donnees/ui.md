
A pandas.DataFrame ORM
```python
>>> import donnees as ds

class Category(ds.Model):
    # Optional: If table_name is not specified the class name(lowercased) is assumed to be the table name
    table_name = 'donne_category'
    # Optional: if not given all fields are fetched
    fields = ('name',)

class Product(ds.Model):
    fields = ('name', 'category',)
    exclude = ('price',)
    related = (Category,)


>>> category = Category.get(name='donnees')

>>> product = Product.get(name='cola')
>>> print(product)
<Product [id=1]>

>>> product = Product.all()
>>> print(product)
<Product Set[2]>

#calls the db again to fetch category
>>> c = product.category

# Uses one sql statement to fetch related field
>>> product = Product.fetch('category').get(name='cola')
#does not call db, already fetched category
>>> print(product.category)
<Category [id=1]>


>>> import pandas
>>> isinstance(users, pandas.DataFrame)
True
```