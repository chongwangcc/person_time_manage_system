
$(function(){
      init1();
      init2();
      init3();
      init4();
      init5();
      init6();
      init7();
      init8();
})
function init1(){
    var option = {
           series: [
                {
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
                    data: [
                        {
                            name: 'Sam S Club',
                            value: 10000,
                        }, {
                            name: 'Macys',
                            value: 6181
                        }, {
                            name: 'Amy Schumer',
                            value: 4386
                        }, {
                            name: 'Jurassic World',
                            value: 4055
                        }, {
                            name: 'Charter Communications',
                            value: 2467
                        }, {
                            name: 'Chick Fil A',
                            value: 2244
                        }, {
                            name: 'Planet Fitness',
                            value: 1898
                        }, {
                            name: 'Pitch Perfect',
                            value: 1484
                        }, {
                            name: 'Express',
                            value: 1112
                        }, {
                            name: 'Home',
                            value: 965
                        }, {
                            name: 'Johnny Depp',
                            value: 847
                        }, {
                            name: 'Lena Dunham',
                            value: 582
                        }, {
                            name: 'Lewis Hamilton',
                            value: 555
                        }, {
                            name: 'KXAN',
                            value: 550
                        }, {
                            name: 'Mary Ellen Mark',
                            value: 462
                        }, {
                            name: 'Farrah Abraham',
                            value: 366
                        }, {
                            name: 'Rita Ora',
                            value: 360
                        }, {
                            name: 'Serena Williams',
                            value: 282
                        }, {
                            name: 'NCAA baseball tournament',
                            value: 273
                        }, {
                            name: 'Point',
                            value: 273
                        }, {
                            name: 'Point Break',
                            value: 265
                        }]
                }
                ]
      };
    var histogramChart1 = echarts.init(document.getElementById('echart1'));
    histogramChart1.setOption(option);
}

function init2(){
    var option = {
      title: {
          text: '雷达图'
      },
      tooltip: {},
      legend: {
          top: 20,
          itemWidth: 12,
          itemHeight: 12,
          data: ['预算分配（Allocated Budget）', '实际开销（Actual Spending）'],
          textStyle: {
              color: '#fff'
          }
      },
      radar: {
          radius: '60%',
          splitNumber: 8,
          axisLine: {
              lineStyle: {
                  color: '#fff',
                  opacity: .2
              }
          },
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
              name: 'Sales',
              max: 6000
          }, {
              name: 'Administration',
              max: 16000
          }, {
              name: 'Information Techology',
              max: 30000
          }, {
              name: 'Customer Support',
              max: 35000
          }, {
              name: 'Development',
              max: 50000
          }, {
              name: 'Marketing',
              max: 25000
          }]
      },
      series: [{
          name: '预算 vs 开销（Budget vs spending）',
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
          data: [{
              value: [5000, 7000, 12000, 11000, 15000, 14000],
              name: '预算分配（Allocated Budget）',
          }, {
              value: [2500, 12000, 8000, 8500, 12000, 12000],
              name: '实际开销（Actual Spending）',
          }]
      }],
      color: ['#ef4b4c', '#b1eadb']

  };
    var histogramChart1 = echarts.init(document.getElementById('echart2'));
    histogramChart1.setOption(option);
}

function init3(){
    var cost = [0.2, 0.201, 1]//本期比上期（大于1按1处理）
    var dataCost = [1000.01,200000,200]//真是的金额
    var totalCost = [1, 1, 1]//比例综合
    var visits = [92, 102, 89]//本期占总的百分比*100
    var grade = ['运动时长', '学习时长', '工作时长']
    var data = {
        grade: grade,
        cost: cost,
        totalCost: totalCost,
        visits: visits,
        dataCost:dataCost
    };
    var option = {
        grid: {
            left: '240',
            right: '100'
        },
        xAxis: {
            show: false,
        },
        yAxis: {
            type: 'category',
            axisLabel: {
                margin: 100,
                show: true,
                color: '#4DCEF8',
                fontSize: 14
            },
            axisTick: {
                show: false,
            },
            axisLine: {
                show: false,
            },
            data: data.grade
        },
        series: [{
            type: 'bar',
            barGap: '-100%',
            label: {
                normal: {
                    show: true,
                    position: 'right',
                    color: '#fff',
                    fontSize: 14,
                    formatter:
                    function(param) {
                        return '环比：'+data.visits[param.dataIndex] +'%';
                    },
                }
            },
            barWidth: '35%',
            itemStyle: {
                normal: {
                    borderColor: '#4DCEF8',
                    borderWidth: 2,
                    barBorderRadius: 15,
                    color: 'rgba(102, 102, 102,0)'
                },
            },
            z: 1,
            data: data.totalCost,
            // data: da
        }, {
            type: 'bar',
            barGap: '-98%',
            barWidth: '33%',
            itemStyle: {
                normal: {
                    barBorderRadius: 16,
                    color: {
                        type: 'linear',
                        x: 0,
                        x1: 1,
                        colorStops: [{
                            offset: 0,
                            color: '#02ddff'
                        }, {
                            offset: 1,
                            color: '#00feff'
                        }]
                    }
                },
            },
            max: 1,
            label: {
                normal: {
                    show: true,
                    position: 'left',
                    color: '#fff',
                    fontSize: 14,
                    formatter: function(param) {
                        if(param.dataIndex=='0'){
                            return data.dataCost[param.dataIndex] + '元';
                        }
                        if(param.dataIndex=='1'){
                           return data.dataCost[param.dataIndex];
                        }
                        if(param.dataIndex=='2'){
                          return data.dataCost[param.dataIndex] + '万';
                        }

                    },
                }
            },
            labelLine: {
                show: true,
            },
            z: 2,
            data: data.cost,
        }]
    };
    var histogramChart1 = echarts.init(document.getElementById('echart3'));
    histogramChart1.setOption(option);
}

function init4(){
    option = {

        legend: {
            data:['邮件营销','联盟广告','视频广告','直接访问','搜索引擎']
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
                data : ['周一','周二','周三','周四','周五','周六','周日']
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'邮件营销',
                type:'line',
                stack: '总量',
                areaStyle: {},
                data:[120, 132, 101, 134, 90, 230, 210]
            },
            {
                name:'联盟广告',
                type:'line',
                stack: '总量',
                areaStyle: {},
                data:[220, 182, 191, 234, 290, 330, 310]
            },
            {
                name:'视频广告',
                type:'line',
                stack: '总量',
                areaStyle: {},
                data:[150, 232, 201, 154, 190, 330, 410]
            },
            {
                name:'直接访问',
                type:'line',
                stack: '总量',
                areaStyle: {normal: {}},
                data:[320, 332, 301, 334, 390, 330, 320]
            },
            {
                name:'搜索引擎',
                type:'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data:[820, 932, 901, 934, 1290, 1330, 1320]
            }
        ]
    };
    var histogramChart1 = echarts.init(document.getElementById('echart4'));
          histogramChart1.setOption(option);
}

function init5(){
    // https://echarts.baidu.com/examples/editor.html?c=treemap-drill-down
    var uploadedDataURL = "data/asset/data/ec-option-doc-statistics-201604.json";
    var myChart = echarts.init(document.getElementById('echart5'));
    myChart.showLoading();
    $.getJSON(uploadedDataURL, function (rawData) {

        myChart.hideLoading();

        function convert(source, target, basePath) {
            for (var key in source) {
                var path = basePath ? (basePath + '.' + key) : key;
                if (key.match(/^\$/)) {

                }
                else {
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
            }
            else {
                target.children.push({
                    name: basePath,
                    value: source.$count
                });
            }
        }

        var data = [];

        convert(rawData, data, '');

        myChart.setOption(option = {
            title: {
                text: 'ECharts 配置项查询分布',
                subtext: '2016/04',
                left: 'leafDepth'
            },
            tooltip: {},
            series: [{
                name: 'option',
                type: 'treemap',
                visibleMin: 300,
                data: data.children,
                leafDepth: 2,
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
    });
}

function init6() {

    var myChart = echarts.init(document.getElementById('echart6'));
    myChart.showLoading();
    $.get('data/asset/data/life-expectancy.json', function (data) {
        myChart.hideLoading();

        var itemStyle = {
            normal: {
                opacity: 0.8,
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowOffsetY: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
        };

        var sizeFunction = function (x) {
            var y = Math.sqrt(x / 5e8) + 0.1;
            return y * 80;
        };
        // Schema:
        var schema = [
            {name: 'Income', index: 0, text: '人均收入', unit: '美元'},
            {name: 'LifeExpectancy', index: 1, text: '人均寿命', unit: '岁'},
            {name: 'Population', index: 2, text: '总人口', unit: ''},
            {name: 'Country', index: 3, text: '国家', unit: ''}
        ];

        option = {
            baseOption: {
                timeline: {
                    axisType: 'category',
                    orient: 'vertical',
                    autoPlay: true,
                    inverse: true,
                    playInterval: 1000,
                    left: null,
                    right: 0,
                    top: 20,
                    bottom: 20,
                    width: 55,
                    height: null,
                    label: {
                        normal: {
                            textStyle: {
                                color: '#999'
                            }
                        },
                        emphasis: {
                            textStyle: {
                                color: '#fff'
                            }
                        }
                    },
                    symbol: 'none',
                    lineStyle: {
                        color: '#555'
                    },
                    checkpointStyle: {
                        color: '#bbb',
                        borderColor: '#777',
                        borderWidth: 2
                    },
                    controlStyle: {
                        showNextBtn: false,
                        showPrevBtn: false,
                        normal: {
                            color: '#666',
                            borderColor: '#666'
                        },
                        emphasis: {
                            color: '#aaa',
                            borderColor: '#aaa'
                        }
                    },
                    data: []
                },
                backgroundColor: '#404a59',
                title: [{
                    text: data.timeline[0],
                    textAlign: 'center',
                    left: '63%',
                    top: '55%',
                    textStyle: {
                        fontSize: 100,
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                }, {
                    text: '各国人均寿命与GDP关系演变',
                    left: 'center',
                    top: 10,
                    textStyle: {
                        color: '#aaa',
                        fontWeight: 'normal',
                        fontSize: 20
                    }
                }],
                tooltip: {
                    padding: 5,
                    backgroundColor: '#222',
                    borderColor: '#777',
                    borderWidth: 1,
                    formatter: function (obj) {
                        var value = obj.value;
                        return schema[3].text + '：' + value[3] + '<br>'
                                + schema[1].text + '：' + value[1] + schema[1].unit + '<br>'
                                + schema[0].text + '：' + value[0] + schema[0].unit + '<br>'
                                + schema[2].text + '：' + value[2] + '<br>';
                    }
                },
                grid: {
                    top: 100,
                    containLabel: true,
                    left: 30,
                    right: '110'
                },
                xAxis: {
                    type: 'log',
                    name: '人均收入',
                    max: 100000,
                    min: 300,
                    nameGap: 25,
                    nameLocation: 'middle',
                    nameTextStyle: {
                        fontSize: 18
                    },
                    splitLine: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#ccc'
                        }
                    },
                    axisLabel: {
                        formatter: '{value} $'
                    }
                },
                yAxis: {
                    type: 'value',
                    name: '平均寿命',
                    max: 100,
                    nameTextStyle: {
                        color: '#ccc',
                        fontSize: 18
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#ccc'
                        }
                    },
                    splitLine: {
                        show: false
                    },
                    axisLabel: {
                        formatter: '{value} 岁'
                    }
                },
                visualMap: [
                    {
                        show: false,
                        dimension: 3,
                        categories: data.counties,
                        calculable: true,
                        precision: 0.1,
                        textGap: 30,
                        textStyle: {
                            color: '#ccc'
                        },
                        inRange: {
                            color: (function () {
                                var colors = ['#bcd3bb', '#e88f70', '#edc1a5', '#9dc5c8', '#e1e8c8', '#7b7c68', '#e5b5b5', '#f0b489', '#928ea8', '#bda29a'];
                                return colors.concat(colors);
                            })()
                        }
                    }
                ],
                series: [
                    {
                        type: 'scatter',
                        itemStyle: itemStyle,
                        data: data.series[0],
                        symbolSize: function(val) {
                            return sizeFunction(val[2]);
                        }
                    }
                ],
                animationDurationUpdate: 1000,
                animationEasingUpdate: 'quinticInOut'
            },
            options: []
        };

        for (var n = 0; n < data.timeline.length; n++) {
            option.baseOption.timeline.data.push(data.timeline[n]);
            option.options.push({
                title: {
                    show: true,
                    'text': data.timeline[n] + ''
                },
                series: {
                    name: data.timeline[n],
                    type: 'scatter',
                    itemStyle: itemStyle,
                    data: data.series[n],
                    symbolSize: function(val) {
                        return sizeFunction(val[2]);
                    }
                }
            });
        }

        myChart.setOption(option);

    });

}

function init7(){
    var option = {
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c}%"
    },
    // toolbox: {
    //     feature: {
    //         dataView: {readOnly: false},
    //         restore: {},
    //         saveAsImage: {}
    //     }
    // },
    legend: {
        data: ['展现','点击','访问','咨询','订单']
    },
    calculable: true,
    series: [
        {
            name:'漏斗图',
            type:'funnel',
            left: '10%',
            top: 60,
            //x2: 80,
            bottom: 60,
            width: '80%',
            // height: {totalHeight} - y - y2,
            min: 0,
            max: 100,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
                show: true,
                position: 'inside'
            },
            labelLine: {
                length: 10,
                lineStyle: {
                    width: 1,
                    type: 'solid'
                }
            },
            itemStyle: {
                borderColor: '#fff',
                borderWidth: 1
            },
            emphasis: {
                label: {
                    fontSize: 20
                }
            },
            data: [
                {value: 20, name: '访问'},
                {value: 10, name: '咨询'},
                {value: 5, name: '订单'},
                {value: 80, name: '点击'},
                {value: 100, name: '展现'}
            ]
        }
    ]
};
    var histogramChart1 = echarts.init(document.getElementById('echart7'));
    histogramChart1.setOption(option);
}

function init8(){
    var option = {
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c}%"
    },
    // toolbox: {
    //     feature: {
    //         dataView: {readOnly: false},
    //         restore: {},
    //         saveAsImage: {}
    //     }
    // },
    legend: {
        data: ['展现','点击','访问','咨询','订单']
    },
    calculable: true,
    series: [
        {
            name:'漏斗图',
            type:'funnel',
            left: '10%',
            top: 60,
            //x2: 80,
            bottom: 60,
            width: '80%',
            // height: {totalHeight} - y - y2,
            min: 0,
            max: 100,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
                show: true,
                position: 'inside'
            },
            labelLine: {
                length: 10,
                lineStyle: {
                    width: 1,
                    type: 'solid'
                }
            },
            itemStyle: {
                borderColor: '#fff',
                borderWidth: 1
            },
            emphasis: {
                label: {
                    fontSize: 20
                }
            },
            data: [
                {value: 20, name: '访问'},
                {value: 10, name: '咨询'},
                {value: 5, name: '订单'},
                {value: 80, name: '点击'},
                {value: 100, name: '展现'}
            ]
        }
    ]
};
    var histogramChart1 = echarts.init(document.getElementById('echart8'));
    histogramChart1.setOption(option);
}