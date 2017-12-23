
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

# Result Set
>>> print(category.results)
<Category [1]>

# Pandas DataFrame
>>> import pandas
>>> isinstance(category.df, pandas.DataFrame)
True

# SQL statement used
>>> print(category.sql)
"SELECT * FROM category WHERE name='donnees';"


>>> products = Product.all(limit=1000)
>>> print(products)
<Product [1000]>

```