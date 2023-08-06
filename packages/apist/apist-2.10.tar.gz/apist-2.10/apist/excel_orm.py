import json
import re
from json import JSONDecodeError
from apist.logs import log
import jsonpath
import xlwt
import xlrd
from xlutils.copy import copy
from xlwt.Style import default_style
from apist.setting import Setting

global_di = dict()  # 提取的变量，供全局使用


class Excel:
    def __init__(self, excel_file, sheet_name=''):
        self.excel_file = excel_file
        self.book = xlrd.open_workbook(excel_file, formatting_info=True)

        # open the table with the specified name
        try:
            if sheet_name:
                self.sheet_ = self.book.sheet_by_name(sheet_name=sheet_name)
                self.sheet_name_index = self.book.sheet_names().index(sheet_name)
            else:
                self.sheet_ = self.book.sheet_by_index(0)
                self.sheet_name_index = 0
        except xlrd.biffh.XLRDError:
            log.error("no such table %s' in excel" % sheet_name)
        self.book_copy = copy(self.book)
        self.sheet = self.book_copy.get_sheet(self.sheet_name_index)

    def cell_value(self, row: int, col):
        value = self.sheet_.cell_value(int(row), col)
        return str(value)

    def get_run(self, row: int):
        run = self.cell_value(row, Setting.RUN)  # 读的是1.0
        try:
            run = int(float(run))
        except ValueError:
            log.warning("优先级列无法转化为int，已置为默认1")
            run = 1
        return run

    def get_explain(self, row: int):
        return self.cell_value(row, Setting.EXPLAIN)

    def get_method(self, row: int):
        method = self.cell_value(row, Setting.METHOD)
        if method.lower() not in ["get", "post", "put", "delete"]:
            raise ValueError("method invalid")
        return method

    def get_url(self, row: int):
        url = self.cell_value(row, Setting.URL)
        if not url.startswith("http"):
            raise ValueError("url invalid")
        return url

    def get_req_data(self, row: int) -> tuple:
        data = self.cell_value(row, Setting.REQ_DATA)

        # 校验：有{}的情况表明是有依赖的
        if '{}' in data and not self.setup_variable(row):
            log.error("请检查第%s行’请求参数‘或‘前置变量’" % row)
            return ()

        # 表单参数前面加 f
        if data.startswith('f'):
            return data[1:], 'param'
        return data, 'json'

    def get_status_code(self, row: int):
        return self.cell_value(row, Setting.STATUS_CODE)

    def get_response(self, row):
        return self.cell_value(row, Setting.RESPONSE)

    def teardown_extract(self, row: int, response) -> bool:
        """
        响应提取（正则或jsonpath），无论是正则还是jsonpath提取出来的都是list，把响应提取出来，存到全局字典。
        re: uid = 'uid:\d+'
        jsonpath: uid = '$..uid'
        """
        row = int(row)
        extract: str = self.cell_value(row, Setting.EXTRACT)

        # 校验为空、无法分割的情况
        if not extract:
            return False
        res = """提取表达式必须符合正则或者jsonpath要求，如name="$..data.name", msg='msg":"\w+"'"""
        try:
            k, v = extract.split('=')
        except ValueError:
            log.warning("""提取失败，%s""" % res)
            return False

        # jsonpath提取
        if v.startswith("$"):
            try:
                response = json.loads(response)
                v = jsonpath.jsonpath(response, v)
            except JSONDecodeError:
                log.error("""jsonpath提取为空，%s""" % res)
                return False
        # 正则提取
        else:
            v = re.findall(v, response)
            if not v:
                log.error("""re提取为空，%s""" % res)
                return False

        global_di[k] = v[0]  # 存第一个即可
        return True

    def setup_variable(self, row):
        """
        变量，此变量必须是‘后置提取’列的键名。
        """
        variable_value = self.cell_value(row, Setting.VARIABLE)

        # 校验为空、不在全局字典里
        if not variable_value:
            return
        if variable_value not in global_di:
            log.error("你输入的变量名不在全局变量内，请检查'变量名'和'后置提取'")

        return global_di.get(variable_value)

    def get_expect(self, row):
        return self.cell_value(row, Setting.EXPECT)

    def get_pre_fail(self, row):
        pre_fail = self.cell_value(row, Setting.PRE_FAIL)
        if pre_fail:
            if pre_fail not in Setting.FLAG_YES:
                raise ValueError("pre fail invalid, it must in %s" % Setting.FLAG_YES)
        return pre_fail

    def get_result(self, row):
        return self.cell_value(row, Setting.RESULT)

    def get_columns(self, sheet='', row=0):
        return self.all_columns(sheet=sheet, row=row)

    def get_rows(self, sheet=0):
        return self.all_rows(sheet=sheet)

    def get_email(self):
        return self.email_sheet()

    def get_header(self):
        return self.header_sheet()


class ApiExcel(Excel):
    def email_sheet(self) -> dict:
        if "email" not in self.book.sheet_names():
            log.warning("no such sheet 'email'")
            return {}
        es = self.book["email"]
        cols = self.all_columns(es)
        values = self.all_columns(es, row=1)
        email_dict = {}
        for i, j in zip(cols, values):
            email_dict[i] = j
        return email_dict

    def header_sheet(self):
        if "header" not in self.book.sheet_names():
            log.error("no such sheet 'header'")
            return None
        hs = self.book["header"]
        cols = self.get_columns(hs)
        values = self.get_columns(hs, row=1)
        headers = {}
        for i, j in zip(cols, values):
            headers[i] = j
        return headers

    def all_columns(self, sheet='', row=0):
        columns = []
        sheet = sheet if sheet else self.sheet_
        try:
            for i in range(20):
                col = sheet.cell_value(row, i)
                if col:
                    columns.append(col)
        except IndexError:
            pass
        return columns

    def all_rows(self, sheet=0):
        sheet = sheet if sheet else self.sheet_
        return sheet.nrows

    @staticmethod
    def gen_style(cell_style=1):
        """
        Beautification of Excel form style
        """
        style, al, font = xlwt.XFStyle(), xlwt.Alignment(), xlwt.Font()
        if cell_style == 1:
            style.alignment.wrap = 1  # wrap automatically
        elif cell_style == 2:
            style.alignment.wrap = 1  # wrap automatically
            font.colour_index = 4
        elif cell_style == 3:
            font.bold = True
            font.colour_index = 3  # set green color
        elif cell_style == 4:
            font.bold = True
            font.colour_index = 2  # set red color
        else:
            style.alignment.wrap = 1
        style.alignment = al
        style.font = font
        style.alignment.vert = 0x01  # set vertical center
        style.alignment.horz = 0x02  # set horizontal center
        # to see the details by "print(style.alignment.vert, style.font.bold)"
        return style

    def write_cell(self, row, col, value: str, style=default_style):
        self.sheet.write(int(row), col, str(value), style)
        self.book_copy.save(self.excel_file)

    def write_response(self, row, value):
        """
        write response to excel
        """
        return self.write_cell(row, Setting.RESPONSE, value)

    def write_status_code(self, row, status_code):
        row = int(row)
        if status_code == 200:
            color = 3
        else:
            color = 4
        return self.write_cell(row, Setting.STATUS_CODE, status_code, self.gen_style(color))

    def write_result(self, row, result, color_index: int):
        return self.write_cell(row, Setting.RESULT, result, self.gen_style(color_index))
