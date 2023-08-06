class Setting:
    """--------------corresponding to the columns in Excel---------------------"""
    RUN = 0
    EXPLAIN = 1
    METHOD = 2
    URL = 3
    REQ_DATA = 4
    STATUS_CODE = 5
    RESPONSE = 6
    EXTRACT = 7  # =ROW(E3)
    VARIABLE = 8  # jsonpath
    EXPECT = 9
    PRE_FAIL = 10
    RESULT = 11

    """--------------corresponding to the columns in Excel---------------------"""

    """---------------do not change the configuration easily-------------------"""
    URL_CUT = 40
    MAX_LENGTH = 2000  # the max of xlwt to excel is 65536, but consuming too much memory while all in the max, It's better to be one order of magnitude less
    EXCEL_MAX_LENGTH = 65536  # max of xlwt to excel is 65536
    """---------------do not change the configuration easily-------------------"""

    # excel flag
    FLAG_NO = ['N', 'n', 'No', 'NO', 'no', '0']
    FLAG_YES = ['Y', 'y', 'Yes', 'YES', '1']
    # DEPENDED_FLAG = ['!', '！']

    """----------------for html------------------------------------------------"""
    html_ = u"""
    <?xml version="1.0" encoding="UTF-8"?>
    <html>
    <head>
        <title>{{html_title}}</title>
        <meta name="generator" content="HTMLTestRunner 0.8.2.2"/>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>


        <link href="https://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
        <script src="https://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
        <script src="https://cdn.bootcss.com/echarts/3.7.1/echarts.min.js"></script>


        <!-- 引入js
        <link href="js/bootstrap.min.css" rel="stylesheet">
        <script src="js/jquery.min.js"></script>
        <script src="js/bootstrap.min.js"></script>
        <script src="js/echarts.js"></script>
         -->

        <style type="text/css" media="screen">
            body {
                margin: 0;
                font-family: "Arial", "Microsoft YaHei", "黑体", "宋体", sans-serif;
                font-size: 18px;
                line-height: 1.5;
                line-height: 1.5;
                color: #333333;
            }

            .table {
                margin-bottom: 1px;
                width: 100%;
            }

            .hiddenRow {
                display: none;
            }

            .container-fluid {
                padding-right: 120px;
                padding-left: 120px;
            }

            .nav-tabs li {
                width: 186px;
                text-align: center;
            }
        </style>
    </head>

    <body >
        <script language="javascript" type="text/javascript">

        function showClassDetail(detail_id, hiddenRow_id, class_type) {
            console.log(document.getElementById(hiddenRow_id).className)

            if ('详细' ==  document.getElementById(detail_id).innerText) {
                if ('all' == class_type) {
                    document.getElementById(hiddenRow_id).className = 'all';
                }
                else if ('success' == class_type) {
                    document.getElementById(hiddenRow_id).className = 'success';
                }
                else if ('error' == class_type) {
                    document.getElementById(hiddenRow_id).className = 'error';
                }
                else{
                    document.getElementById(hiddenRow_id).className = 'untreaded';
                }
                document.getElementById(detail_id).innerText = "收起"
            }
            else {
                document.getElementById(detail_id).innerText = "详细"
                document.getElementById(hiddenRow_id).className = 'hiddenRow';
            }
        }

        </script>

        <div class="container-fluid">
            <div class="page-header">
                <h1 class="text-primary" style="font-size:45px;line-height:75px">&nbsp;&nbsp;{{html_title}}</h1>
            </div>

            <div class="col-md-12">
                <div class="col-md-4" style="Background-Color:#F5F5F5; height:300px">
                    <h3 style="line-height:25px">基本信息</h3>
                    <table class="table table-hover table-bordered" style="width:100%; height:11px">
                        <tbody>
                            <tr class="info">
                                <td class="text-center">开始时间</td>
                                <td class="text-center">{{start_time}}</td>
                            </tr>
                            <tr class="info">
                                <td class="text-center">测试耗时</td>
                                <td class="text-center">{{used_time}}</td>
                            </tr>
                            <tr class="info">
                                <td class="text-center">接口成功率</td>
                                <td class="text-center">{{rate}}</td>
                            </tr>
                            <tr class="info">
                                <td class="text-center">总用例个数</td>
                                <td class="text-center">{{sum_all_cases}}</td>
                            </tr>
                            <tr class="info">
                                <td class="text-center">执行用例数</td>
                                <td class="text-center">{{sum_executed_cases}}</td>
                            </tr>
                            <tr class="info">
                                <td class="text-center">跳过用例数</td>
                                <td class="text-center">{{sum_untreaded_cases}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="col-md-8">
                    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
                    <div id="main" style="height:300px;"></div>
                    <script type="text/javascript">
                        var myChart = echarts.init(document.getElementById('main'));
                        var option = {
                        backgroundColor: '#F5F5F5', //背景色

                        title: {
                            text: '数据统计',
                            x: 'center'
                        },

                        legend: {
                            orient: 'vertical',
                            x: 'left',
                            data: ['成功', '失败', '未检验']
                        },

                        color: ['#3c763d', '#a94442', '#0099CC'],

                        calculable: true,

                        series: [{
                            name: '测试结果',
                            type: 'pie',
                            radius: '55%',
                            center: ['50%', '60%'],
                            startAngle: 135,
                            data: [{
                                value: {{right_sum}},
                                name: '成功',
                                itemStyle: {
                                    normal: {
                                        label: {
                                            formatter: '{b} : {c} ({d}%)',
                                            textStyle: {
                                                align: 'left',
                                                fontSize: 15,
                                            }
                                        },
                                        labelLine: {
                                             length: 40,
                                        }
                                     }
                                }
                            }, {
                                value: {{error_sum}},
                                name: '失败',
                                itemStyle: {
                                    normal: {
                                        label: {
                                            formatter: '{b} : {c} ({d}%)',
                                            textStyle: {
                                                align: 'right',
                                                fontSize: 15,
                                            }
                                        },
                                        labelLine: {
                                            length: 40,
                                            }
                                        }
                                    }
                                }, {
                                value: {{untreated_sum}},
                                name: '未检验',
                                itemStyle: {
                                    normal: {
                                        label: {
                                            formatter: '{b} : {c} ({d}%)',
                                            textStyle: {
                                                align: 'right',
                                                fontSize: 15,
                                            }
                                       },
                                        labelLine: {
                                            length: 40,
                                            }
                                       }
                                   }
                               }],
                            }]
                        };
                        // 为echarts对象加载数据
                        myChart.setOption(option);
                    </script>
                </div>
            </div>
    """

    temp_label = '''
        <div><span>&nbsp;</span></div>

        <div class="col-md-12">
            <div class="tabbable" id="tabs-957640">
                <ul class="nav nav-tabs">
                    <li class="active">
                        <a href="#panel-0" data-toggle="tab" style="Background-Color: #428bca; color: #fff;">全  部 ({})</a>
                    </li>
                    <li>
                        <a href="#panel-1" data-toggle="tab" style="Background-Color: #5cb85c; color: #fff;">成  功 ({})</a>
                    </li>
                    <li>
                        <a href="#panel-2" data-toggle="tab" style="Background-Color: #d9534f; color: #fff;">失  败 ({})</a>
                    </li>
                    <li>
                        <a href="#panel-3" data-toggle="tab" style="Background-Color: #5bc0de; color: #fff;">未验证 ({})</a>
                    </li>
                </ul>
            </div>
            <div class="tab-content">
                <div class="tab-pane active" id="panel-0">
                    <table class="table table-hover table-bordered">
    {}
                    </table>
                </div>


                <div class="tab-pane" id="panel-1">
                    <table class="table table-hover table-bordered">
    {}
                    </table>
                </div>


                <div class="tab-pane" id="panel-2">
                    <table class="table table-hover table-bordered">
    {}
                    </table>
                </div>


                <div class="tab-pane" id="panel-3">
                    <table class="table table-hover table-bordered">
    {}
                    </table>
                </div>
            </div>
        </div>
    </div>
    </body>
    </html>
    '''

    title_temp = '''
                <table class="table table-hover table-bordered" style="Background-Color:#dff0d8">
                    <thead>
                        <colgroup>
    {}
                        </colgroup>
                        <tr>
    {}
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
     '''

    title_width = '''                         <col width='{}%'/>
    '''

    title = '''                         <td class="text-center"  style="Background-Color:#dff0d8">{}</td>
    '''

    table_data = '''                           <td class="text-center">{}</td>
    '''

    table_detail = '''                           <td class="text-center"><a href="javascript:showClassDetail('{}','{}', '{}')" class="detail" id = "{}">详细</a></td>
    '''

    detail_text = '''                   <tr class='hiddenRow' id="{}" >
                           <td colspan='{}'>
                               <div>
                                   <pre class="text-left" style="width:975;">{}</pre>
                               </div>
                           </td>
                       </tr> 
    '''

# 给pre的style加属性：width:975;
# 若pre换成p，加style="white-space:pre-wrap;"
# ontent="always" name="referrer"><meta name="theme-color" content="#ffffff"><meta name="description" content="全球领先的中文搜索引擎、致力于让网民更便捷地