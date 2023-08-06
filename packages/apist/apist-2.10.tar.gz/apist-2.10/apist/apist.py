import glob
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import ConnectTimeout
from apist.setting import Setting
import platform
import random
from bottle import template
import webbrowser
import sys
import datetime
from apist.logs import log
import os
from apist.emails import Email
from apist.excel_orm import ApiExcel


class Api:
    def __init__(self, excel_file: str, sheet=0, mark=1, is_email=False):
        self.TIME1 = datetime.datetime.now()
        excel_file = os.path.abspath(excel_file)
        folder = os.path.dirname(excel_file)
        self.folder = folder if folder else print('没有这个文件：%s' % excel_file) or sys.exit()
        log.info('start...')
        self.excel_file, self.req = excel_file, Request()
        self.excel = ApiExcel(excel_file)
        self.headers = self.excel.get_header()
        mark, sheet = mark if isinstance(mark, int) else 1, sheet if isinstance(sheet, int or str) else 0
        self.rows, self.mark, self.is_email = self.excel.get_rows(sheet=sheet), mark, is_email
        self.run()

    def run(self):
        all_cases, pass_cases, fail_cases, fake_fail_cases = self.do_req()
        self.do_res(all_cases)  # 回填excel
        Report.generate(all_cases, pass_cases, fail_cases, fake_fail_cases, report_file_folder=self.folder,
                        waste_time=datetime.datetime.now() - self.TIME1)  # 生成html报告
        self.do_email(self.is_email)

    def do_req(self):
        """
        处理请求
        """
        # 初始化信息
        e = self.excel
        status_code_li, all_cases, pass_cases, fail_cases, fake_fail_cases, res_flag = [], [], [], [], [], '接口'

        # 遍历所有行
        for i in range(1, self.rows):
            # 标签决定是否运行，可用于优先级
            if e.get_run(i) != self.mark:
                continue

            method, url = e.get_method(i).lower(), e.get_url(i)
            data, data_type = e.get_req_data(i)

            # 提取前置变量的值，整合到请求参数
            rely = self.excel.setup_variable(i)
            if rely:
                if not data:
                    res = '第%s行的请求参数不合法，无法合并前置变量' % (i + 1)
                    log.error(res)
                    status_code, res_text, res_flag = 402, 'excel错误：' + res, '内部'
                else:
                    data = data.replace("{}", '%s')
                    data = data % rely

            status_code, res_text = self.send_req(
                method, url, data, self.headers, data_type=data_type
            )

            # 后置提取存到全量字典
            is_extract = e.teardown_extract(i, res_text)

            # 响应截取，有后置提取的保留全响应，其余的截取一部分
            if is_extract:
                res_text = res_text[:Setting.EXCEL_MAX_LENGTH]
            else:
                res_text = res_text[:Setting.MAX_LENGTH]
                res_text = res_text if len(res_text) < Setting.MAX_LENGTH else res_text + " ..."

            # analysis result
            pre_fail, expect = e.get_pre_fail(i), e.get_expect(i)
            if not expect:
                if status_code == 200:
                    result, flag = 'PASS', 1
                elif pre_fail:
                    result, flag = 'PASS', 2
                else:
                    result, flag = 'FAIL', 0
            else:
                if expect in res_text:
                    result, flag = 'PASS', 1
                elif pre_fail:
                    result, flag = 'PASS', 2
                else:
                    result, flag = 'FAIL', 0

            status_code_li.append(status_code)

            req_data, detail_request_url = data if data else '', '请求地址：' + url + '\n'
            detail_request_data, detail_response = '请求参数：' + req_data + '\n', res_flag + '响应：' + res_text + '\n'

            # Avoid interpreting labels, for html
            detail, explain = detail_request_url + detail_request_data + detail_response.replace('<', '&lt;').replace(
                '>', '&gt;'), e.get_explain(i)
            the_case = [str(i), explain, url[:Setting.URL_CUT] + '...' if len(url) > Setting.URL_CUT else url,
                        status_code, expect, result, '详细', detail]
            all_cases.append(the_case)
            fail_cases.append(the_case) if flag == 0 else fake_fail_cases.append(
                the_case) if flag == 2 else pass_cases.append(the_case)
        return all_cases, pass_cases, fail_cases, fake_fail_cases

    def send_req(self, method: str, url: str, data: str, headers: dict, data_type='json'):
        """
        发送请求
        :param method: 请求方式
        :param url: 地址
        :param data: 请求参数
        :param headers: 请求头
        :param data_type: 请求参数类型 json or form
        """
        req = self.req
        try:
            if method == "get":
                status_code, res_text = req.get(url, params=data, headers=headers)
            elif method in ["post", "put"]:
                data = eval(data)
                if not type(data) == dict:
                    status_code, res_text = 402, "invalid request data that can't convert to dict"
                else:
                    if data_type == 'json':
                        status_code, res_text = req.request(method, url, data=data, headers=headers)
                    else:
                        status_code, res_text = req.request(method, url, params=data, headers=headers)
            elif method == 'delete':
                status_code, res_text = req.delete(url, data=data, headers=headers)
            else:
                raise ValueError("must be get/post/put/delete")
        except (ConnectTimeout, ConnectionError):
            status_code, res_text = 500, "ConnectTimeout"
        return status_code, res_text

    def do_res(self, case_li: list):
        """
        处理响应
        """
        success_num = fail_num = 0
        fail_urls, fail_status = [], []
        for _ in case_li:
            id_, explain, url, s_code, expect, result, no_use, detail = _
            star = detail.index('响应：') + 3
            res = detail[star:]
            self.excel.write_status_code(id_, s_code)
            self.excel.write_response(id_, res)
            if result == 'PASS':
                log.info('%d \t%s' % (s_code, url))
                success_num += 1
                color_index = 3
            else:
                log.error('%d \t%s' % (s_code, url))
                color_index = 4
                fail_num += 1

            self.excel.write_result(id_, result, color_index)

        all_num = success_num + fail_num
        all_num = all_num if all_num else 1

        # success rate and failure rate
        success_rate, failure_rate = round(success_num / all_num, 4) * 100, round(fail_num / all_num, 4) * 100

        log.info("执行完毕...\n\n本次共执行 %d条用例，通过%d条，失败%d条；成功率为%d%%, 失败率为%d%%" % (
            all_num, success_num, fail_num, success_rate, failure_rate))
        return success_num, fail_num, fail_urls, fail_status

    def do_email(self, is_email):
        if not is_email:
            return

        email_dict = self.excel.email_sheet()

        # weather run
        is_email2 = email_dict.get('run')
        if not is_email2 or is_email2 in Setting.FLAG_NO:
            log.info("the email run is an empty string, do not send email")
            return
        elif is_email2 not in Setting.FLAG_YES:
            log.error("ValueError: the email run must in %s" % (Setting.FLAG_YES + Setting.FLAG_NO))
            return

        # msg for email
        name, pd, to, tittle, content, attachment = email_dict.get('name'), email_dict.get('password'), email_dict.get(
            'to'), email_dict.get('tittle'), email_dict.get('content'), email_dict.get('attachment')

        if not (name and pd and to):
            log.error("email name or password missing")
            return False

        if attachment and '.' not in attachment:
            log.error("wrong file type %s" % attachment)
            return

        return Email(name, pd, to, tittle, content, attachment)


class Request:
    def request(self, method: str, url: str, data=None, json=None, **kwargs):
        res = requests.request(method=method, url=url, data=data, json=json, **kwargs)
        return self.call_back(res)

    def get(self, url: str, params=None, **kwargs):
        res = requests.get(url=url, params=params, **kwargs)
        return self.call_back(res)

    def delete(self, url: str, data=None, **kwargs):
        res = requests.delete(url=url, data=data, **kwargs)
        return self.call_back(res)

    @staticmethod
    def call_back(res):
        status_code = res.status_code
        res_text = res.text
        return status_code, res_text


cases = {}


class Report:
    @staticmethod
    def generate(all_case: list = '', right_case: list = '', error_case: list = '',
                 untreaded_cases: list = '', report_file_folder='', waste_time=None):
        """
        generate report by all these cases
        """
        global cases
        if not all_case or (not right_case and not error_case and not untreaded_cases):
            raise ValueError("No cases report")

        cases = {'all_cases': all_case,
                 'right_cases': right_case,
                 'error_cases': error_case,
                 'untreaded_cases': untreaded_cases}

        # generate report
        html_report_object = HtmlReport(report_cases=cases, delta=waste_time)
        html = html_report_object.gen_html_report(Setting.html_)

        # saved file
        report_file_folder_save = os.path.join(report_file_folder, "reports")
        if not os.path.exists(report_file_folder_save):
            os.mkdir(report_file_folder_save)
        with open(os.path.join(report_file_folder_save,
                               datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".html"), 'wb') as f:
            f.write(html.encode('utf-8'))

        # fixed file
        fixed_path = os.path.join(report_file_folder, "report.html")
        with open(fixed_path, 'wb') as f:
            f.write(html.encode('utf-8'))

        # Keep only the report of the latest (month)
        for i in glob.glob(report_file_folder_save + os.sep + '*.html')[:-30]:
            os.remove(i)
        if platform.system().lower() in ["windows", "macos"]:
            webbrowser.open(fixed_path)


class HtmlReport:
    def __init__(self, html_title: str = '测试报告', pie_theme: str = '数据统计', test_info: list = None,
                 report_table_title: list = None, report_cases: dict = None, delta=None):
        self.html_title = html_title
        self.pie_theme = pie_theme
        if not pie_theme or not isinstance(html_title, str):
            log.error('invalid html title or pie name')
            sys.exit(0)

        if not report_table_title:
            self.report_table_title = ['用例id', '接口说明', 'URL', '状态码', '期望值', '测试结果', '详情']
        elif not isinstance(report_table_title, list):
            log.error('invalid type of report_table_title, it must be list')
            sys.exit(0)

        now1 = datetime.datetime.now()
        time1 = now1.strftime("%Y-%m-%d %H:%M:%S")
        if not delta:
            m, s = random.randint(0, 3), random.randint(1, 59)
            delta = datetime.timedelta(seconds=s, minutes=m)
        time2 = (now1 - delta).strftime("%Y-%m-%d %H:%M:%S")
        d_s = delta.seconds + 1
        m, s = d_s // 60, d_s % 60
        waste = str(m) + "分" + str(s) + "秒"

        len_all, len_r, len_e, len_u = len(report_cases), len(report_cases['right_cases']), len(
            report_cases['error_cases']), len(report_cases['untreaded_cases'])

        if not test_info:
            test_info = [
                time2, time1, waste, len(report_cases['all_cases']),
                len_r + len_e, len_u]
            self.test_info = test_info
        elif not isinstance(test_info, list):
            log.error('invalid type of test_info, it must be list')
            sys.exit(0)

        if isinstance(report_cases, dict) and len_all > 0:
            self.report_cases = report_cases
            self.pie_sum_number = {
                'right_sum': len_r,
                'error_sum': len_e,
                'untreated_sum': len_u}
        else:
            log.error('invalid type of report_cases, it must be list')
            sys.exit(0)

    def packaged_cases(self, export_label_title, data_key, class_name, pannel_num):
        cases_num, cases_packaged = 1, ''
        cases_packaged = ''.join(
            [cases_packaged, '                   <tr class="{}">\n'.format(class_name), export_label_title,
             '                   </tr>\n'])
        for data_case in self.report_cases[data_key]:
            detail_id, hidden_id = ''.join([pannel_num, '-detail-', str(cases_num)]), ''.join(
                [pannel_num, '-hidden-', str(cases_num)])
            cases_num += 1
            cases_packaged = ''.join([cases_packaged, '                   <tr class="{}">\n'.format(class_name)])
            for data in data_case[:-1]:
                if '详细' == data:
                    cases_packaged = ''.join([cases_packaged,
                                              Setting.table_detail.format(detail_id, hidden_id, 'success',
                                                                          detail_id)])
                else:
                    cases_packaged = ''.join([cases_packaged, Setting.table_data.format(data)])
            cases_packaged = ''.join([cases_packaged, '                   </tr>\n'])
            cases_packaged = ''.join(
                [cases_packaged, Setting.detail_text.format(hidden_id, len(data_case) - 1, data_case[-1])])
        return cases_packaged

    def gen_html_report(self, html_template):
        export_label_title = ''
        for label_title in self.report_table_title:
            export_label_title = ''.join([export_label_title, Setting.title.format(label_title)])

        str_right_datas, str_untreated_cases, str_error_cases, str_all_cases = '', '', '', ''
        all_num = len(cases['all_cases'])
        right_num = len(cases['right_cases'])
        rate = '{:.2%}'.format(round(right_num / all_num, 5))

        for data_key in self.report_cases.keys():
            if 'right_cases' == data_key:
                str_right_datas = self.packaged_cases(export_label_title, data_key, 'success', 'panel1')
            elif 'untreaded_cases' == data_key:
                str_untreated_cases = self.packaged_cases(export_label_title, data_key, 'untreaded', 'panel3')
            elif 'error_cases' == data_key:
                str_error_cases = self.packaged_cases(export_label_title, data_key, 'error', 'panel2')
            else:
                str_all_cases = self.packaged_cases(export_label_title, data_key, 'all', 'panel0')
        export_label_datas = Setting.temp_label.format(
            all_num, right_num,
            len(cases['error_cases']),
            len(cases['untreaded_cases']),
            str(str_all_cases[0:-1]),
            str(str_right_datas[0:-1]),
            str(str_error_cases[0:-1]),
            str(str_untreated_cases[0:-1])
        )
        # right_name_and_rate = '成功 ' + rate
        html_template = ''.join([html_template, export_label_datas])
        view = template(
            html_template,
            html_title=self.html_title,
            theme=self.pie_theme,
            start_time=self.test_info[0],
            # end_time=self.test_info[1],
            used_time=self.test_info[2],
            rate=rate,
            sum_all_cases=self.test_info[3],
            sum_executed_cases=self.test_info[4],
            sum_untreaded_cases=self.test_info[5],
            right_sum=self.pie_sum_number['right_sum'],
            error_sum=self.pie_sum_number['error_sum'],
            untreated_sum=self.pie_sum_number['untreated_sum']
        )
        return view
