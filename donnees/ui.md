
```python
>>> import donnees as ds

class Category(ds.Model):
    # If table_name is not specified the class name(lowercased) is assumed to be the table name
    table_name = 'donne_category'
    fields = ('name', 'id',)

class Product(ds.Model):
    fields = ('name', 'category',)
    exclude = ('price',)
    related = (Category,)


>>> category = Category.get(name='donnees')

>>> product = Product.get(name='cola')
#calls the db again to fetch category
>>> c = product.category

# Uses one sql statement to fetch related field
>>> product = Product.fetch('category').get(name='cola')
#does not call db already fetched
>>> print(product.category)


>>> import pandas
>>> isinstance(users, pandas.DataFrame)
```