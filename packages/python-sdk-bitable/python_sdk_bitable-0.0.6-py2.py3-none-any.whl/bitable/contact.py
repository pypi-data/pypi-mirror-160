import requests
import posixpath
import time
from collections import OrderedDict
from .params import BitableParams
from .auth import FeiShuAuth



class Contact(object):
    VERSION = "v3"
    API_BASE_URL = "https://open.feishu.cn/open-apis/contact/"
    API_LIMIT = 1.0 / 5  # 5 per second
    API_URL = posixpath.join(API_BASE_URL, VERSION)
    API_URL_DEPARTMENT = posixpath.join(API_URL, "departments")
    API_URL_USER = posixpath.join(API_URL, "users")
    MAX_RECORDS_PER_REQUEST = 50

    def __init__(self, department_id: str, app_id: str, app_secret: str, timeout: int = None):
        """
        Instantiate a new Contact instance

        >>> contact = Contact('department_id','app_id', 'app_secret')

        Args:
            department_id (``str``): Contact department_id open_id
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
        self.department_id = department_id
        self.url_department = posixpath.join(self.API_URL_DEPARTMENT, department_id)
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
            print(response.json())
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

    def user_url(self, user_id):
        """ Builds URL with user id """
        return posixpath.join(self.API_URL_USER, user_id)

    def department_url(self, department_id):
        """ Builds URL with department id """
        return posixpath.join(self.API_URL_DEPARTMENT, department_id)

    def _request(self, method, url, params=None, json_data=None):
        print("2::",url)
        response = self.session.request(
            method, url, params=params, json=json_data, timeout=self.timeout
        )
        return self._process_response(response)

    def _get(self, url, **params):
        processed_params = self._process_params(params)
        return self._request("get", url, params=processed_params)

    def _post(self, url, json_data):
        return self._request("post", url, json_data=json_data)

    def get_user_by_id(self, user_id):
        """
        Retrieves a record by its id

        >>> record = contact.get_user_by_id('ou_9e6b08727792e298dc53d8caad3a7ebe')

        Args:
            user_id(``str``): user open_id

        Returns:
            record (``dict``): Record
        """
        user_url = self.user_url(user_id)
        return self._get(user_url)

    def get_department_by_id(self, department_id):
        """
        Retrieves a record by its id

        >>> record = contact.get_department_by_id('od-fc1c5ca97995ffd66957f7023840f564')

        Args:
            user_id(``str``): user open_id

        Returns:
            record (``dict``): Record
        """
        department_url = self.department_url(department_id)
        return self._get(department_url)

    def search_user_id_by_mobiles(self, phone_numbers: list):
        search_url = posixpath.join(self.API_URL_USER, "batch_get_id?user_id_type=open_id")
        return self._post(search_url, json_data={"mobiles": phone_numbers})

    def get_iter(self, url, **options):
        """
        Record Retriever Iterator

        Returns iterator with lists in batches according to pageSize.
        To get all records at once use :any:`get_all`

        >>> for page in contact.get_iter():
        ...     for record in page:
        ...         print(record)
        [{'fields': ... }, ...]


    Keyword Args:
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

    def get_all_children_dept(self, **options):
        """
        Retrieves all records repetitively and returns a single list.

        >>> contact.get_all_children_dept()
        [{'fields': ... }, ...]


    Keyword Args:


        Returns:
            records (``list``): List of Records

        >>> records = get_all_children_dept(page_size=50)

        """
        all_records = []
        url = posixpath.join(self.API_URL_DEPARTMENT, self.department_id, 'children?fetch_child=true')
        for records in self.get_iter(url=url, **options):
            all_records.extend(records)
        return all_records

    def get_employees(self, department_id: str, **options):
        """
        Retrieves all records repetitively and returns a single list.

        >>> contact.get_all_employees()
        [{'fields': ... }, ...]


    Keyword Args:


        Returns:
            records (``list``): List of Records

        >>> records = get_employees(page_size=50)

        """
        all_records = []
        url = posixpath.join(self.API_URL_USER, f"find_by_department?department_id={department_id}&page_size=40&department_id_type=open_department_id")
        print(url)
        for records in self.get_iter(url=url, **options):
            all_records.extend(records)
        return all_records

    def get_full_employees_by_dept_id(self) -> str:
        departments = [i.get('open_department_id') for i in self.get_all_children_dept() if
                       not i.get('status').get('is_deleted')]
        print(len(departments))
        total_employees = []
        for department in departments:
            la = self.get_employees(department)
            total_employees += la
            print(department,len(la))
        return total_employees



def main():
    pass


if __name__ == '__main__':
    main()
