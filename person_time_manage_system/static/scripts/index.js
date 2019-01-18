// var symptomName = last_month_day();

$(function(){
    var date_now = "2019-1-14"
    $.get("/api/v1/statistics/weekly/all/"+date_now).done(function (data){
        init0(data)
        init1("Chart1", data.working_and_study_tomato_nums_of_each_day)
        init2("Chart2", data.sleep_hours)
        init3("Chart3", data.every_day_category_details)
        init4("Chart4", data.each_category_time_sum)
        init5("Chart5", data.missing_info)
    })
})

function init0(data){
    //设置开始时间、结束时间
    var tlabel =document.getElementById("id_start_date");
    tlabel.innerHTML=data.start_date
    var tlabel =document.getElementById("id_end_date");
    tlabel.innerHTML=data.end_date

    // 工作、学习番茄时钟数
    var tlabel =document.getElementById("id_work_tomato_nums");
    tlabel.innerHTML=data.working_tomato_nums
    var tlabel =document.getElementById("id_study_tomato_nums");
    tlabel.innerHTML=data.study_tomato_nums

    // 运动、娱乐次数
    var tlabel =document.getElementById("exercise_nums");
    tlabel.innerHTML=data.execise_nums
    var tlabel =document.getElementById("fun_nums");
    tlabel.innerHTML=data.fun_nums
}

function init1(id_str, data1){
    // 番茄始终达标率
    var nums = data1
    //设置番茄始终达标数
    var pieChart1 = echarts.init(document.getElementById(id_str));
    pieChart1.setOption({
        grid:{
               left: '5%',
               right: '5%',
               bottom: '20%',
               containLabel: true
       },
    series: [
        {
        title: {
            "show": false
        },
        name: "",
        type: "gauge",
        min: 0,
        max: 100,
        splitNumber: 10,
        startAngle: 180,
        endAngle: 0,
        center: ["50%", "80%"],
        radius: 145,
        axisLabel: {
            distance: 0,
            fontFamily: "Microsoft YaHei UI",
            fontSize: 16,
            fontWeight: "normal",
            fontStyle: "normal",
            color: "#FFFFFF"
        },
        axisLine: {
            lineStyle: {
                width: 2,
                color: [
                    [1, {
                        "x": "0.00",
                        "y": "0.00",
                        "x2": "1.00",
                        "y2": "1.00",
                        "type": "linear",
                        "global": false,
                        "colorStops": [{
                            "offset": 0,
                            "color": "rgba(0,0,0,1)"
                        }, {
                            "offset": 1,
                            "color": "rgba(202,95,95,1)"
                        }, {
                            "offset": 0.3579,
                            "color": "rgba(34,72,61,1)"
                        }, {
                            "offset": 0.6895,
                            "color": "rgba(39,175,88,1)"
                        }, {
                            "offset": 0.1211,
                            "color": "rgba(52,225,41,1)"
                        }, {
                            "offset": 0.8105,
                            "color": "rgba(218,190,35,1)"
                        }]
                    }]
                ]
            }
        },
        pointer: {
            show: true
        },
        itemStyle: {
            normal: {
                color: {
                    "x": "0.00",
                    "y": "0.00",
                    "x2": "1.00",
                    "y2": "1.00",
                    "type": "linear",
                    "global": false,
                    "colorStops": [{
                        "offset": 0,
                        "color": "rgba(0,0,0,1)"
                    }, {
                        "offset": 1,
                        "color": "rgba(202,95,95,1)"
                    }, {
                        "offset": 0.3579,
                        "color": "rgba(34,72,61,1)"
                    }, {
                        "offset": 0.6895,
                        "color": "rgba(224,229,37,1)"
                    }]
                },
                "borderColor": {
                    "x": "0.00",
                    "y": "0.00",
                    "x2": "1.00",
                    "y2": "1.00",
                    "type": "linear",
                    "global": false,
                    "colorStops": [{
                        "offset": 0,
                        "color": "rgba(0,0,0,1)"
                    }, {
                        "offset": 1,
                        "color": "rgba(202,95,95,1)"
                    }, {
                        "offset": 0.3579,
                        "color": "rgba(34,72,61,1)"
                    }, {
                        "offset": 0.6895,
                        "color": "rgba(224,229,37,1)"
                    }]
                },
                "borderWidth": 1
            }
        },
        axisTick: {
            "length": 16,
            "lineStyle": {
                "width": 4,
                "color": {
                    "x": "0.00",
                    "y": "0.00",
                    "x2": "1.00",
                    "y2": "1.00",
                    "type": "linear",
                    "global": false,
                    "colorStops": [{
                        "offset": 0,
                        "color": "rgba(0,0,0,1)"
                    }, {
                        "offset": 1,
                        "color": "rgba(202,95,95,1)"
                    }, {
                        "offset": 0.3579,
                        "color": "rgba(34,72,61,1)"
                    }, {
                        "offset": 0.6895,
                        "color": "rgba(224,229,37,1)"
                    }]
                }
            }
        },
        splitLine: {
            "length": 32,
            "lineStyle": {
                "width": 4,
                "color": {
                    "x": "0.00",
                    "y": "0.00",
                    "x2": "1.00",
                    "y2": "1.00",
                    "type": "linear",
                    "global": false,
                    "colorStops": [{
                        "offset": 0,
                        "color": "rgba(0,0,0,1)"
                    }, {
                        "offset": 1,
                        "color": "rgba(202,95,95,1)"
                    }, {
                        "offset": 0.3579,
                        "color": "rgba(34,72,61,1)"
                    }, {
                        "offset": 0.6895,
                        "color": "rgba(224,229,37,1)"
                    }]
                }
            }
        },
        detail: {
            show: false
        },
        data: [{
            value: nums,
            name: "半圆仪表_0"
        }]
    },
        {
        title: {
            "show": false
        },
        name: "",
        type: "gauge",
        min: 0,
        max: 100,
        splitNumber: 1,
        startAngle: 180,
        endAngle: 0,
        center: ["50%", "80%"],
        radius: 170,
        axisLine: {
            lineStyle: {
                width: 25.6,
                color: [
                    [nums/100, {
                        x: "0.00",
                        y: "0.00",
                        x2: "1.00",
                        y2: "1.00",
                        type: "linear",
                        global: false,
                        colorStops: [{
                            offset: 0,
                            color: "rgba(0,0,0,1)"
                        }, {
                            offset: 1,
                            color: "rgba(202,95,95,1)"
                        }, {
                            offset: 0.3579,
                            color: "rgba(34,72,61,1)"
                        }, {
                            offset: 0.6895,
                            color: "rgba(224,229,37,1)"
                        }]
                    }],
                    [1, "rgba(0,0,0,0)"]
                ],
                shadowColor: '#DFE127', //默认透明
                shadowBlur: 20
            }
        },
        pointer: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLabel: {
            show: false
        },
        splitLine: {
            show: false
        },
        detail: {
            show: false
        }
    },
        {
        title: {
            show: false
        },
        name: "",
        type: "gauge",
        min: 0,
        max: 100,
        splitNumber: 1,
        startAngle: 180,
        endAngle: 0,
        center: ["50%", "80%"],
        radius: 170,
        axisLine: {
            lineStyle: {
                width: 2,
                color: [
                    [1, {
                        x: "0.00",
                        y: "0.00",
                        x2: "1.00",
                        y2: "1.00",
                        type: "linear",
                        global: false,
                        colorStops: [{
                            offset: 0,
                            color: "rgba(0,0,0,1)"
                        }, {
                            offset: 1,
                            color: "rgba(202,95,95,1)"
                        }, {
                            offset: 0.3579,
                            color: "rgba(34,72,61,1)"
                        }, {
                            offset: 0.6895,
                            color: "rgba(39,175,88,1)"
                        }, {
                            offset: 0.1211,
                            color: "rgba(52,225,41,1)"
                        }, {
                            offset: 0.8105,
                            color: "rgba(218,190,35,1)"
                        }]
                    }]
                ]
            }
        },
        pointer: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLabel: {
            show: false
        },
        splitLine: {
            length: 25.6,
            lineStyle: {
                width: 2,
                color: {
                    x: "0.00",
                    y: "0.00",
                    x2: "1.00",
                    y2: "1.00",
                    type: "linear",
                    global: false,
                    colorStops: [{
                        offset: 0,
                        color: "rgba(0,0,0,1)"
                    }, {
                        offset: 1,
                        color: "rgba(202,95,95,1)"
                    }, {
                        offset: 0.3579,
                        color: "rgba(34,72,61,1)"
                    }, {
                        offset: 0.6895,
                        color: "rgba(39,175,88,1)"
                    }, {
                        offset: 0.1211,
                        color: "rgba(52,225,41,1)"
                    }, {
                        offset: 0.8105,
                        color: "rgba(218,190,35,1)"
                    }]
                }
            }
        },
        detail: {
            show: false
        }
    }]
    });
}

function init2(id_str, data){
        var category = [];
        var dottedBase = +new Date();
        var lineData = [];
        var barData = [];
        var missData = [];
        for (var i = 0; i < data.actual_hours.length; i++) {

            category.push(data.actual_hours[i].category);
            barData.push(data.actual_hours[i].hours)
            lineData.push(data.standard_hours);
            missData.push(data.standard_hours-data.actual_hours[i].hours)
        }

        // option
        option2 = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow',
                    label: {
                        show: true,
                        backgroundColor: '#333'
                    }
                }
            },
            legend: {
                data: ["标准时长", '实际时长'],
                textStyle: {
                    color: '#ccc'
                }
            },
            xAxis: {
                data: category,
                axisLine: {
                    lineStyle: {
                        color: '#ccc'
                    }
                }
            },
            yAxis: {
                splitLine: {show: false},
                axisLine: {
                    lineStyle: {
                        color: '#ccc'
                    }
                }
            },
            series: [{
                name: '标准时长',
                type: 'line',
                smooth: true,
                showAllSymbol: true,
                symbol: 'emptyCircle',
                symbolSize: 15,
                data: lineData
            }, {
                name: '实际时长',
                type: 'bar',
                barWidth: 10,
                itemStyle: {
                    normal: {
                        barBorderRadius: 5,
                        color: new echarts.graphic.LinearGradient(
                            0, 0, 0, 1,
                            [
                                {offset: 0, color: '#14c8d4'},
                                {offset: 1, color: '#43eec6'}
                            ]
                        )
                    }
                },
                data: barData
            }, {
                name: '标准时长',
                type: 'bar',
                barGap: '-100%',
                barWidth: 10,
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(
                            0, 0, 0, 1,
                            [
                                {offset: 0, color: 'rgba(20,200,212,0.5)'},
                                {offset: 0.2, color: 'rgba(20,200,212,0.2)'},
                                {offset: 1, color: 'rgba(20,200,212,0)'}
                            ]
                        )
                    }
                },
                z: -12,
                data: lineData
            }, {
                name: '标准时长',
                type: 'pictorialBar',
                symbol: 'rect',
                itemStyle: {
                    normal: {
                        color: '#0f375f'
                    }
                },
                symbolRepeat: true,
                symbolSize: [12, 4],
                symbolMargin: 1,
                z: -10,
                data: lineData
            }]
        };

        var histogramChart = echarts.init(document.getElementById(id_str));
        histogramChart.setOption(option2)
}

function init3(id_str, data){
          var corlor_list = ["rgba(255,144,128,1)",
              "rgba(0,191,183,1)",
              "rgba(55,126,184,1)",
             "rgba(77,175,74,1)",
              "rgba(152,78,163,1)",
              "rgba(255,127,0,1)",
              "rgba(255,255,51,1)",
              "rgba(166,86,40,1)",
              "rgba(247,129,191,1)",
              "rgba(102,194,165,1)",
              "rgba(252,141,98,1)",
              "rgba(141,160,203,1)",
              "rgba(231,138,195,1)",
          ]
            var xData = data.xData
            var legendData =  data.legends
            var all_data_list = data.data
            var total_data = data.sum

            var total_series =         {
                        name: "总数",
                        type: "line",
                        stack: "总量",
                        symbolSize:10,
                        symbol:'circle',
                        itemStyle: {
                            normal: {
                                color: "rgba(252,230,48,1)",
                                barBorderRadius: 0,
                                label: {
                                    show: true,
                                    position: "top",
                                    formatter: function(p) {
                                        return p.value > 0 ? (p.value) : '';
                                    }
                                }
                            }
                        },
                        data: total_data
                    }

            var gen_label = function (label, data, color){
                        return {
                        name: label,
                        type: "bar",
                        barMaxWidth: 50,
                        barGap: "10%",
                        stack: "总量",
                        itemStyle: {
                            normal: {
                                color: color,
                                "barBorderRadius": 0,
                                "label": {
                                    "show": true,
                                    "textStyle": {
                                        "color": "#fff"
                                    },
                                    "position": "insideTop",
                                    formatter: function(p) {
                                        return p.value > 0 ? (p.value) : '';
                                    }
                                }
                            }
                        },
                        data:data
                    }
            }

            var seriesObj = []
            for(var i=0;i<xData.length;i++){
                var t_series = gen_label(legendData[i],all_data_list[i],corlor_list[i])
                seriesObj.push(t_series)
            }
            seriesObj.push(total_series)

            option = {
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        type: "shadow",
                        textStyle: {
                            color: "#fff"
                        }

                    },
                },
                grid: {
                    borderWidth: 0,
                    top: 110,
                    bottom: 95,
                    textStyle: {
                        color: "#fff"
                    }
                },
                legend: {
                    x: '4%',
                    top: '11%',
                    textStyle: {
                        color: '#90979c',
                    },
                    data: legendData
                },
                calculable: true,
                xAxis: [{
                    type: "category",
                    axisLine: {
                        lineStyle: {
                            color: '#90979c'
                        }
                    },
                    splitLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                    splitArea: {
                        show: false
                    },
                    axisLabel: {
                        interval: 0,

                    },
                    data: xData,
                }],
                yAxis: [{
                    type: "value",
                    splitLine: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#90979c'
                        }
                    },
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        interval: 0,

                    },
                    splitArea: {
                        show: false
                    },

                }],
                dataZoom: [
                    {
                    show: true,
                    height: 30,
                    xAxisIndex: [
                        0
                    ],
                    bottom: 30,
                    start: 0,
                    end: 100,
                    handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
                    handleSize: '110%',
                    handleStyle:{
                        color:"#d3dee5",

                    },
                       textStyle:{
                        color:"#fff"},
                       borderColor:"#90979c"
                    }, {
                    type: "inside",
                    show: true,
                    height: 15,
                    start: 1,
                    end: 35
                }],
                series: seriesObj
            }

            var mapChart = echarts.init(document.getElementById(id_str));
            mapChart.setOption(option)
}

function init4(id_str, data1){
         var scaleData = data1;
         var rich = {
             white: {
                 color: '#ddd',
                 align: 'center',
                 padding: [5, 0]
             }
         };
         var placeHolderStyle = {
             normal: {
                 label: {
                     show: false
                 },
                 labelLine: {
                     show: false
                 },
                 color: 'rgba(0, 0, 0, 0)',
                 borderColor: 'rgba(0, 0, 0, 0)',
                 borderWidth: 0
             }
         };
         var data = [];
         for (var i = 0; i < scaleData.length; i++) {
             data.push({
                 value: scaleData[i].value,
                 name: scaleData[i].name,
                 itemStyle: {
                     normal: {
                         borderWidth: 5,
                         shadowBlur: 30,
                         borderColor: new echarts.graphic.LinearGradient(0, 0, 1, 1, [{
                             offset: 0,
                             color: '#7777eb'
                         }, {
                             offset: 1,
                             color: '#70ffac'
                         }]),
                         shadowColor: 'rgba(142, 152, 241, 0.6)'
                     }
                 }
             }, {
                 value: 4,
                 name: '',
                 itemStyle: placeHolderStyle
             });
         }
         var seriesObj = [{
             name: '',
             type: 'pie',
             clockWise: false,
             radius: ["70%", "70%"],
             hoverAnimation: false,
             itemStyle: {
                 normal: {
                     label: {
                         show: true,
                         position: 'outside',
                         color: '#ddd',
                         formatter: function (params) {
                             var percent = 0;
                             var total = 0;
                             for (var i = 0; i < scaleData.length; i++) {
                                 total += scaleData[i].value;
                             }
                             percent = ((params.value / total) * 100).toFixed(0);
                             if (params.name !== '') {
                                 return params.name + '\n{white|' + '占比' + percent + '%}';
                             } else {
                                 return '';
                             }
                         },
                         rich: rich
                     },
                     labelLine: {
                         show: false
                     }
                 }
             },
             data: data
         }];
         option = {
             tooltip: {
                 show: false
             },
             legend: {
                 show: false
             },
             toolbox: {
                 show: false
             },
             series: seriesObj
         }

         var lineChart = echarts.init(document.getElementById(id_str));
         lineChart.setOption(option)
}

function init5(id_str, data){
        var tbody =document.getElementById(id_str);
        var info = data;
        for(var i = 0;i < info.length; i++) { //遍历一下json数据
            var trow = getDataRow(info[i]); //定义一个方法,返回tr数据
            tbody.appendChild(trow);

        }
        function getDataRow(h){
         var row = document.createElement('tr'); //创建行

         var idCell = document.createElement('td'); //创建第一列id
         idCell.innerHTML = h.start_time; //填充数据
         row.appendChild(idCell); //加入行  ，下面类似

         var nameCell = document.createElement('td');//创建第二列name
         nameCell.innerHTML = h.end_time;
         row.appendChild(nameCell);

         var jobCell = document.createElement('td');//创建第三列job
         jobCell.innerHTML = h.during;
         row.appendChild(jobCell);

         var jobCell = document.createElement('td');//创建第三列job
         jobCell.innerHTML = h.type;
         row.appendChild(jobCell);

         return row; //返回tr数据
         }


}

