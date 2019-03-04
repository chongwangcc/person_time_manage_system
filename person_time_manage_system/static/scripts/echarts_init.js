
//仪表盘初始化
function dashboard_init(id_str, data1){
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

//柱状图
function bar_init(id_str, data){
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

//可选择柱状图
function select_bar_init(id_str, data){
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

        for(var i=0;i<legendData.length;i++){
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

//饼状图
function pie_init(id_str, data1){
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

//词云图
function word_cloud_init(id_str, data1){

    var data=data1

    var option = {
           series: [
                {
                width: '90%',
                height: '90%',
               type: 'wordCloud',
                    gridSize: 2,
                    sizeRange: [12, 50],
                    rotationRange: [-90, 90],
                    shape: 'pentagon',
                    textStyle: {
                        normal: {
                            color: function () {
                                return 'rgb(' + [
                                        Math.round(Math.random() * 255),
                                        Math.round(Math.random() * 255),
                                        Math.round(Math.random() * 255)
                                    ].join(',') + ')';
                            }
                        },
                        emphasis: {
                            shadowBlur: 10,
                            shadowColor: '#333'
                        }
                    },
                    data:data
                }
                ]
      };
    var mychart = echarts.init(document.getElementById(id_str));
    mychart.setOption(option);
}

//雷达图
function radar_init(id_str, data1){

    var data = data1

    var option = {
        tooltip: {},
      legend: {
          x:"left",
          top: 20,
          itemWidth: 12,
          itemHeight: 12,
          data: data.name,
          textStyle: {
              color: '#fff'
          }
      },
      radar: {
          radius: '60%',
          splitNumber: 8,
          splitLine: {
              lineStyle: {
                  color: '#fff',
                  opacity: .2
              }
          },
          splitArea: {
              areaStyle: {
                  color: 'rgba(127,95,132,.3)',
                  opacity: 1,
                  shadowBlur: 45,
                  shadowColor: 'rgba(0,0,0,.5)',
                  shadowOffsetX: 0,
                  shadowOffsetY: 15,
              }
          },
          indicator: [{
              name: '睡眠力',
              max: 10
          }, {
              name: '工作力',
              max: 10
          }, {
              name: '娱乐力',
              max: 10
          }, {
              name: '运动力',
              max: 10
          }, {
              name: '学习力',
              max: 10
          }]
      },
      series: [{
          type: 'radar',
          symbolSize: 0,
          areaStyle: {
              normal: {
                  shadowBlur: 13,
                  shadowColor: 'rgba(0,0,0,.2)',
                  shadowOffsetX: 0,
                  shadowOffsetY: 10,
                  opacity: 1
              }
          },
          data: data
      }],
      color: ['#ef4b4c', '#b1eadb']

  };
    var histogramChart1 = echarts.init(document.getElementById(id_str));
    histogramChart1.setOption(option);
}

//折线图
 function line_init(id_str, data1){

    var this_month_data = data1.efficient_period_using_rate.data

    option = {
        tooltip:{},
        legend: {
            data:[data1.efficient_period_using_rate.name],
             textStyle: {
              color: '#fff'
          }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : ['1','2','3','4','5','6','7',
                        '8','9','10','11','12','13','14',
                        '15','16','17','18','19','20','21',
                        '22','23','24','25','26','27','28',
                        '29','30','31'],
                axisLine: {
                lineStyle: {
                    color: '#ccc'
                }
            },
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLine: {
                lineStyle: {
                    color: '#ccc'
                }
            },
            }
        ],
        series : [
            {
                name:data1.efficient_period_using_rate.name,
                type:'line',
                stack: '总量',
                areaStyle: {},
                data:this_month_data
            }
        ]
    };
    var histogramChart1 = echarts.init(document.getElementById(id_str));
          histogramChart1.setOption(option);
}

//矩形图
function rect_init(id_str, data1){
        // https://echarts.baidu.com/examples/editor.html?c=treemap-drill-down
    // var uploadedDataURL = "data/asset/data/ec-option-doc-statistics-201604.json";
    //     $.getJSON(uploadedDataURL, function (rawData) {}
    var data_json = data1
    function convert(source, target, basePath) {
        for (var key in source) {
            var path = basePath ? (basePath + '.' + key) : key;
            if (key.match(/^\$/)) {
            }else {
                target.children = target.children || [];
                var child = {
                    name: path
                };
                target.children.push(child);
                convert(source[key], child, path);
            }
        }
        if (!target.children) {
            target.value = source.$count || 1;
        }else {
            target.children.push({
                name: basePath,
                value: source.$count
            });
        }
    }
    var data = [];
    convert(data_json, data, '');
    var myChart = echarts.init(document.getElementById(id_str));
    var formatUtil = echarts.format;
    myChart.setOption(option = {
        tooltip: {
            formatter: function (info) {
                var value = info.value;
                var treePathInfo = info.treePathInfo;
                var treePath = [];

                for (var i = 1; i < treePathInfo.length; i++) {
                    treePath.push(treePathInfo[i].name);
                }

                return [
                    '<div class="tooltip-title">' + formatUtil.encodeHTML(treePath.join('/')) + '</div>',
                    '用时: ' + formatUtil.addCommas(value) + ' 小时',
                ].join('');
            }
        },
        series: [{
            type: 'treemap',
            visibleMin: 300,
            data: data.children,
            leafDepth: 1,
            levels: [
                {
                    itemStyle: {
                        normal: {
                            borderColor: '#555',
                            borderWidth: 4,
                            gapWidth: 4
                        }
                    }
                },
                {
                    colorSaturation: [0.3, 0.6],
                    itemStyle: {
                        normal: {
                            borderColorSaturation: 0.7,
                            gapWidth: 2,
                            borderWidth: 2
                        }
                    }
                },
                {
                    colorSaturation: [0.3, 0.5],
                    itemStyle: {
                        normal: {
                            borderColorSaturation: 0.6,
                            gapWidth: 1
                        }
                    }
                },
                {
                    colorSaturation: [0.3, 0.5]
                }
            ]
        }]
    })
}
