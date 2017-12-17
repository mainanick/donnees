"""donnees

Donnees is a Pandas ORM:

Basic Example:
>>> import donnees as ds

>>> class Category(ds.Model):    
        table_name = 'donne_category'    
        fields = ('name',)


>>> category = Category.get(name='donnees')

>>> print(category)
<Category Set[1]>
"""
import requests

from donnees.models import Model