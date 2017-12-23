<table>
  <tr>
    <td><strong> données</strong></td>
    <td>/ˈdɒneɪ/</td>
    <td>data</td>
  </tr>     
</table>

*Initial development. Still in design spec.* 

Used to build datasets from database results

#### *Does not support complex queries*


A pandas.DataFrame ORM
```python
>>> import donnees as ds

class Category(ds.Model):    
    table_name = 'donne_category'
    # Optional: if not given all fields are fetched
    fields = ('name',)

class Product(ds.Model):
    table_name = 'donne_products'
    fields = ('name', 'category',)    
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
