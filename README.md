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
    fields = ('id', 'name',)

class Product(ds.Model):
    table_name = 'donne_products'
    fields = ('name', 'category',)    
    related = (Category,)

#Fetch all
>>> category = Category.all()

#Fetch but limit only first 1000
>>> category = Category.all(limit=1000)

#Get Specific
>>> category = Category.get(name='donnees')

# Result Set
>>> print(category.results)
<Category [1]>

# Fields
first_category = category.results[0]
>>> print(first_category.id)
1
>>> print(first_category.name)
"Drinks"

# Pandas DataFrame
>>> import pandas
>>> isinstance(category.df, pandas.DataFrame)
True

# SQL statement used
>>> print(category.sql)
"SELECT id, name FROM category WHERE name='donnees';"

```
