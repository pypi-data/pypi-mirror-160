import requests
import posixpath
import time
from collections import OrderedDict
from .params import BitableParams
from .auth import FeiShuAuth


class BITable:
    VERSION = "v1"
    API_BASE_URL = "https://open.feishu.cn/open-apis/bitable/"
    API_LIMIT = 1.0 / 5  # 5 per second
    API_URL = posixpath.join(API_BASE_URL, VERSION, "apps")
    MAX_RECORDS_PER_REQUEST = 100

    def __init__(self, base_id: str, table_id: str, app_id: str, app_secret: str, timeout: int = None):
        """
        Instantiate a new BITable instance

        >>> bitable = BITable('base_id', 'table_id','app_id', 'app_secret')

        Args:
            base_id (``str``): BiTable base identifier
            table_id (``str``): BiTable table identifier
            app_id (``str``): API key
            app_secret (``str``): API secret key

        Keyword Args:
            timeout (``int``, ``Tuple[int, int]``, optional): Optional timeout
                parameters to be used in request. `See requests timeout docs.
                <https://requests.readthedocs.io/en/master/user/advanced/#timeouts>`_
        """
        session = requests.Session()
        session.auth = FeiShuAuth(app_id=app_id, app_secret=app_secret)
        self.session = session
        self.table_id = table_id
        self.url_app = posixpath.join(self.API_URL, base_id, "tables")
        self.url_table = posixpath.join(self.API_URL, base_id, "tables", table_id)
        self.timeout = timeout

    def _process_params(self, params):
        """
        Process params names or values as needed using filters
        """
        new_params = OrderedDict()
        for param_name, param_value in sorted(params.items()):
            param_value = params[param_name]
            ParamClass = BitableParams._get(param_name)
            new_params.update(ParamClass(param_value).to_param_dict())
        return new_params

    def _chunk(self, iterable, chunk_size):
        """Break iterable into chunks."""
        for i in range(0, len(iterable), chunk_size):
            yield iterable[i: i + chunk_size]

    def _build_batch_record_objects(self, records):
        return [{"fields": record} for record in records]

    def _process_response(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            err_msg = str(exc)

            # Attempt to get Error message from response, Issue #16
            try:
                error_dict = response.json()
            except ValueError:
                pass
            else:
                if "error" in error_dict:
                    err_msg += " [Error: {}]".format(error_dict["error"])
            exc.args = (*exc.args, err_msg)
            raise exc
        else:
            return response.json()

    def record_url(self, record_id):
        """ Builds URL with record id """
        return posixpath.join(self.url_table, "records", record_id)

    def _request(self, method, url, params=None, json_data=None):
        response = self.session.request(
            method, url, params=params, json=json_data, timeout=self.timeout
        )
        return self._process_response(response)

    def _get(self, url, **params):
        processed_params = self._process_params(params)
        return self._request("get", url, params=processed_params)

    def _post(self, url, json_data):
        return self._request("post", url, json_data=json_data)

    def _put(self, url, json_data):
        return self._request("put", url, json_data=json_data)

    def _patch(self, url, json_data):
        return self._request("patch", url, json_data=json_data)

    def _delete(self, url):
        return self._request("delete", url)

    def _delete_batch(self, record_ids):
        if len(record_ids) == 1:
            return self.delete(record_ids[0])
        return self._request("post", self.url_table + "/records/batch_delete", json_data={"records": record_ids})

    def get(self, record_id):
        """
        Retrieves a record by its id
        >>> record = bitable.get('recwPQIfs4wKPyc9D')

        Args:
            record_id(``str``): Bitable record id

        Returns:
            record (``dict``): Record
        """
        record_url = self.record_url(record_id)
        return self._get(record_url)

    def get_iter(self, url, **options):
        """
        Record Retriever Iterator

        Returns iterator with lists in batches according to pageSize.
        To get all records at once use :any:`get_all`

        >>> for page in bitable.get_iter():
        ...     for record in page:
        ...         print(record)
        [{'fields': ... }, ...]


    Keyword Args:
            view_id (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            page_size (``int``, optional ): The number of records returned
                in each request. Must be less than or equal to 100.
                Default is 100. See :any:`PageSizeParam`.
            field_names (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.
            formula (``str``, optional): Bitable formula.
                See :any:`FormulaParam`.

        Returns:
            iterator (``list``): List of Records, grouped by pageSize

        """
        offset = None
        while True:
            data = self._get(url, page_token=offset, **options)
            if not data.get('data').get('items'):
                break
            records = data.get("data", {"items": []}).get("items", [])
            time.sleep(self.API_LIMIT)
            yield records
            if data.get("data").get("has_more"):
                pass
            else:
                break
            offset = data.get("data").get("page_token")
            if not offset:
                break

    def get_all(self, **options):
        """
        Retrieves all records repetitively and returns a single list.

        >>> bitable.get_all()
        >>> bitable.get_all(view_id='MyView', fields_name=['ColA', '-ColB'])
        [{'fields': ... }, ...]


    Keyword Args:


        Returns:
            records (``list``): List of Records

        >>> records = bitable.get_all(view_id='All')

        """
        all_records = []
        url = self.url_table + '/records'
        for records in self.get_iter(url=url, **options):
            all_records.extend(records)
        return all_records

    def match(self, field_name, field_value, **options):
        """
        Returns first match found in :any:`get_all`

        >>> bitable.match('Name', 'John')
        {'fields': {'Name': 'John'} }

        Args:
            field_name (``str``): Name of field to match (column name).
            field_value (``str``): Value of field to match.

        Keyword Args:
            view_id (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.

        Returns:
            record (``dict``): First record to match the field_value provided
        """
        from_name_and_value = BitableParams.FormulaParam.from_name_and_value
        formula = from_name_and_value(field_name, field_value)
        options["formula"] = formula
        options["page_size"] = 100
        for record in self.get_all(**options):
            return record
        else:
            return {}

    def search(self, field_name, field_value, record=None, **options):
        """
        Returns all matching records found in :any:`get_all`

        >>> bitable.search('Gender', 'Male')
        [{'fields': {'Name': 'John', 'Gender': 'Male'}, ... ]

        >>> bitable.search('Checkbox Field', 1)
        [{'fields': {'Name': 'John', 'Gender': 'Male'}, ... ]

        Args:
            field_name (``str``): Name of field to match (column name).
            field_value (``str``): Value of field to match.

        Keyword Args:
            view_id (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.

        Returns:
            records (``list``): All records that matched ``field_value``

        """
        records = []
        from_name_and_value = BitableParams.FormulaParam.from_name_and_value
        formula = from_name_and_value(field_name, field_value)
        options["formula"] = formula
        records = self.get_all(**options)
        return records

    def insert(self, fields):
        """
        Inserts a record

        >>> record = {'Name': 'John'}
        >>> bitable.insert(record)

        Args:
            fields(``dict``): Fields to insert.
                Must be dictionary with Column names as Key.

        Returns:
            record (``dict``): Inserted record

        """
        return self._post(
            self.url_table + "/records", json_data={"fields": fields}
        )

    def batch_insert(self, records):
        """
        Breaks records into chunks of 10 and inserts them in batches.
        Follows the set API rate.
        To change the rate limit use ``bitable.API_LIMIT = 0.2``
        (5 per second)

        >>> records = [{'Name': 'John'}, {'Name': 'Marc'}]
        >>> bitable.batch_insert(records)

        Args:
            records(``list``): Records to insert
            typecast(``boolean``): Automatic data conversion from string values.

        Returns:
            records (``list``): list of added records
        """
        inserted_records = []
        for chunk in self._chunk(records, self.MAX_RECORDS_PER_REQUEST):
            new_records = self._build_batch_record_objects(chunk)
            response = self._post(
                self.url_table + "/records/batch_create", json_data={"records": new_records}
            )
            inserted_records += response["data"]["records"]
            time.sleep(self.API_LIMIT)
        return inserted_records

    def update(self, record_id, fields):
        """
        Updates a record by its record id.
        Only Fields passed are updated, the rest are left as is.

        >>> record = bitable.match('Employee Id', 'DD13332454')
        >>> fields = {'Status': 'Fired'}
        >>> bitable.update(record['id'], fields)

        Args:
            record_id(``str``): Id of Record to update
            fields(``dict``): Fields to update.
                Must be dictionary with Column names as Key

        Returns:
            record (``dict``): Updated record
        """
        record_url = self.record_url(record_id)
        return self._put(
            record_url, json_data={"fields": fields}
        )

    def batch_update(self, records):
        """
        Updates a records by their record id's in batch.

        Args:
            records(``list``): List of dict: [{"id": record_id, "fields": fields_to_update_dict}]


        Returns:
            records(``list``): list of updated records
        """
        updated_records = []
        for chunk in self._chunk(records, self.MAX_RECORDS_PER_REQUEST):
            chunk_records = [{"id": x["id"], "fields": x["fields"]} for x in chunk]
            response = self._post(
                self.url_table + "/records/batch_update", json_data={"records": chunk_records}
            )
            updated_records += response["data"]["records"]
        #
        return updated_records

    def update_by_field(self, field_name, field_value, fields, **options):
        """
        Updates the first record to match field name and value.
        Only Fields passed are updated, the rest are left as is.

        >>> record = {'Name': 'John', 'Tel': '540-255-5522'}
        >>> bitable.update_by_field('Name', 'John', record)

        Args:
            field_name (``str``): Name of field to match (column name).
            field_value (``str``): Value of field to match.
            fields(``dict``): Fields to update.
                Must be dictionary with Column names as Key

        Keyword Args:
            view_id (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.

        Returns:
            record (``dict``): Updated record
        """
        record = self.match(field_name, field_value, **options)
        return {} if not record else self.update(record["id"], fields)

    def delete(self, record_id):
        """
        Deletes a record by its id

        >>> record = bitable.match('Employee Id', 'DD13332454')
        >>> bitable.delete(record['id'])

        Args:
            record_id(``str``): Bitable record id

        Returns:
            record (``dict``): Deleted Record
        """
        record_url = self.record_url(record_id)
        return self._delete(record_url)

    def batch_delete(self, record_ids):
        """
        Breaks records into batches of 10 and deletes in batches, following set
        API Rate Limit (5/sec).
        To change the rate limit set value of ``Bitable.API_LIMIT`` to
        the time in seconds it should sleep before calling the function again.

        >>> record_ids = ['recXwOiq8H', 'recg2vK7Bh']
        >>> bitable.batch_delete(records_ids)

        Args:
            records(``list``): Record Ids to delete

        Returns:
            records(``list``): list of records deleted

        """
        chunks = self._chunk(record_ids, self.MAX_RECORDS_PER_REQUEST)
        deleted_records = []
        for chunk in chunks:
            print(chunk)
            response = self._delete_batch(chunk)
            deleted_records += response["data"]["records"] if len(chunk) > 1 else [response]
            time.sleep(self.API_LIMIT)
        return deleted_records

    def list_tables(self, **options):
        all_records = []
        for records in self.get_iter(url=self.url_app, **options):
            all_records.extend(records)
        return all_records

    def list_views(self, **options):
        all_records = []
        for records in self.get_iter(url=self.url_table + "/views", **options):
            all_records.extend(records)
        return all_records

    def __repr__(self):
        return "<BiTable table:{}>".format(self.table_id)


def main():
    pass


if __name__ == '__main__':
    main()
