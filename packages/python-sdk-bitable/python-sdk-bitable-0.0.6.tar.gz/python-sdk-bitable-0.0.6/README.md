飞书多维表格 API Client Wrapper for Python
=======================
Installing
-----

```bash
pip install python-sdk-bitable
```

Documentation
-----
Full documentation here:待完善


Usage Example
-----
Below are some of the methods available in the wrapper.
```bash
bitable = Bitable('base_id', 'table_id', 'app_id', 'app_secret')

bitable.list_tables()

bitable.list_views()

bitable.list_records()

# CRUD  (insert update update delete)
bitable.insert({'Name': 'John'})

# batch insert
bitable.batch_insert([{'Name': 'Tom', 'Sex': 'male'}, {'Name': 'Bob','Sex': 'female'}])

# return first matched record
bitable.match('Name', 'Tom')

# return all matched records
bitable.search('Name', 'Tom')

bitable.update_by_field('Name', 'Tom', {"Sex": "male"})

```
For the full list and documentation visit the docs

License
-------
[MIT](https://choosealicense.com/licenses/mit/)


