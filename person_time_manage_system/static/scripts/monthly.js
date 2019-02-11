var date_now = getNowFormatDate()

function initDate(){
    Date.prototype.Format = function (fmt) { //author: meizz
        var o = {
                "M+": this.getMonth() + 1, //月份
                "d+": this.getDate(), //日
                "h+": this.getHours(), //小时
                "m+": this.getMinutes(), //分
                "s+": this.getSeconds(), //秒
                "q+": Math.floor((this.getMonth() + 3) / 3), //季度
                "S": this.getMilliseconds() //毫秒
            };
        if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
            if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }

    function addDate(date,days){
       var d=new Date(date);
       d.setDate(d.getDate()+days);
       var m=d.getMonth()+1;
       return d.getFullYear()+'-'+m+'-'+d.getDate();
     }

    $("#img_datepicker").on("click", function(e) {
         $('#datepicker').datepicker('show');
    });
    $('#datepicker').datepicker({
        format:'yyyy-mm',
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        beforeShow: function(dateText, inst){
			 $("#ui-datepicker-div").addClass('month');
		},
        onClose: function(dateText, inst) {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            m_start_date = new Date(year, month, 1);
            m_end_date = new Date(year, month+1, 0);
            console.log(m_start_date)
            console.log(m_end_date)
             //设置开始时间、结束时间
            var tlabel =document.getElementById("id_start_date");
            tlabel.innerHTML=addDate(m_start_date, 0)
            var tlabel =document.getElementById("id_end_date");
            tlabel.innerHTML=addDate(m_end_date, 0)

            date_now=year+"-"+(month+1)

            //调用后台接口
            clearCharts()
            main()
        }
    });
}

function clearCharts(){

    // 工作、学习番茄时钟数
    var tlabel =document.getElementById("id_work_tomato_nums");
    tlabel.innerHTML="0"
    var tlabel =document.getElementById("id_study_tomato_nums");
    tlabel.innerHTML="0"

    // 本月已过、活着时间占比
    var tlabel =document.getElementById("id_month_passed");
    tlabel.innerHTML="0%"
    var tlabel =document.getElementById("id_living_percent");
    tlabel.innerHTML="0%"

    var echart1 = echarts.init(document.getElementById("echart1"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("echart2"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("echart3"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("echart4"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("echart5"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("echart6"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("echart7"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("echart8"));
    echart1.clear()

}

function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var currentdate = date.getFullYear() + seperator1 + month    
    return currentdate;
}

function main(){

    restful_url="/api/v1/statistics/monthly/all/"+date_now

    $.get(restful_url).done(function (data){

        init0(data)
        init1("echart1", data.word_cloud)
        init2("echart2", data.ability_redar)
        init3("echart3", data.compare)
        init4("echart4", data.living_time)
        init5("echart5", data.category_rectangle)
        init6("echart6", data.living_evolution)
        init7("echart7", data.working_hours_transform_rate)
        init8("echart8", data.learning_hours_transform_rate)
    })
}

$(function(){
    initDate()
    main()
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

    // 本月已过
    var tlabel =document.getElementById("id_month_passed");
    tlabel.innerHTML=data.during_percent
    var tlabel =document.getElementById("id_living_percent");
    tlabel.innerHTML=data.living_percent
}

function init1(id_str, data1){

    var data=data1

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
                    data:data
                }
                ]
      };
    var mychart = echarts.init(document.getElementById(id_str));
    mychart.setOption(option);
}

function init2(id_str, data1){

    var data = data1

    var option = {
      legend: {
          x:"left",
          top: 20,
          itemWidth: 12,
          itemHeight: 12,
          data: ['上月', '本月'],
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
              name: '体力值',
              max: 10
          }, {
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

function init3(id_str, data1){
    var data=data1
    option = {
        grid: {
            containLabel: true,
            x:'5%',
            y:'15%',
            x2:'5%',
            y2:'3%'
        },
        legend: {
            data: ['增速','上月',"本月"],
                      textStyle: {
              color: '#fff'
          }
        },
        xAxis: [{
            type: 'category',
            axisTick: {
                alignWithLabel: true
            },
            data: data.type,
            axisLine: {
                lineStyle: {
                    color: '#ccc'
                }
            },
        }],
        yAxis: [{
            type: 'value',
            name: '增速',
            position: 'right',
            axisLabel: {
                formatter: '{value} %'
            },
            axisLine: {
                lineStyle: {
                        color: '#ccc'
                    }
                },
        }, {
            type: 'value',
            name: '时长',
            position: 'left',
            axisLine: {
                lineStyle: {
                        color: '#ccc'
                    }
             },
        }],
        series: [{
            name: '增速',
            type: 'line',
            label: {
                    normal: {
                        show: true,
                        position: 'top',
                    }
                },
            lineStyle: {
                    normal: {
                        width: 3,
                        shadowColor: 'rgba(0,0,0,0.4)',
                        shadowBlur: 10,
                        shadowOffsetY: 10
                    }
                },
            data: data.growth
        }, {
            name: '上月',
            type: 'bar',
            yAxisIndex: 1,
            label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
            data: data.last_month
        }, {
            name: '本月',
            type: 'bar',
            yAxisIndex: 1,
            label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
            data: data.this_month
        }]
    };
    var mychart = echarts.init(document.getElementById(id_str));
    mychart.setOption(option);
}

function init4(id_str, data1){

    var last_month_data = data1.last_month_data
    var this_month_data = data1.this_month_data

    option = {
        legend: {
            data:['上月','本月'],
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
                name:'上月',
                type:'line',
                stack: '总量',
                areaStyle: {},
                data:last_month_data
            },
            {
                name:'本月',
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

function init5(id_str, data1){
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
    var formatUtil = echarts.format;
    var myChart = echarts.init(document.getElementById(id_str));
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

function init6(id_str, data1) {
    // https://gallery.echartsjs.com/editor.html?c=bubble-gradient
    var myChart = echarts.init(document.getElementById(id_str));
    var data = data1
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
        var y = Math.sqrt(x / 5e9) + 0.1;
        return y * 80;
    };
    // Schema:
    var schema = [
        {name: 'Sleep', index: 0, text: '睡眠时间', unit: '小时'},
        {name: 'Za', index: 1, text: '杂项时间', unit: '小时'},
        {name: 'time', index: 2, text: '时间', unit: ''},
        {name: 'category', index: 3, text: '类别', unit: ''}
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
                bottom: 0,
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
            title: [{
                text: data.timeline[0],
                textAlign: 'center',
                left: '63%',
                top: '55%',
                textStyle: {
                    fontSize: 20,
                    color: 'rgba(255, 255, 255, 0.7)'
                }
            }],
            grid: {
                top: "25%",
                bottom: 25,
                containLabel: true,
                left: 25,
                right: 70
            },
            xAxis: {
                type: 'log',
                name: '杂项时间',
                nameGap:"30",
                nameLocation: 'middle',
                nameTextStyle: {
                    fontSize: 15
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
                    formatter: '{value} h'
                }
            },
            yAxis: {
                type: 'value',
                name: '睡眠时间',
                max: 100,
                nameTextStyle: {
                    color: '#ccc',
                    fontSize: 15
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
                    formatter: '{value} h'
                }
            },
            visualMap: [{
                show: true,
                dimension: 3,
                categories: data.counties,
                calculable: true,
                precision: 0.1,
                left:"center",                              //组件离容器左侧的距离,'left', 'center', 'right','20%'
                top:"top",                                   //组件离容器上侧的距离,'top', 'middle', 'bottom','20%'
                right:"auto",                               //组件离容器右侧的距离,'20%'
                bottom:"auto",
                orient:"horizontal",
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
}

function init7(id_str, data1){
    var data=data1
    var option = {
        legend: {
            data: data.legend,
             textStyle: {
              color: '#fff'
          },
             top: 20,
        },

        calculable: true,
        series: [
            {
                type:'funnel',
                left: '10%',
                top: 60,
                //x2: 80,
                bottom: 30,
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
                emphasis: {
                    label: {
                        fontSize: 20
                    }
                },
                data: data.value
            }
        ]
    };
    var mychart = echarts.init(document.getElementById(id_str));
    mychart.setOption(option);
}

function init8(id_str, data1){
    var data=data1
    var option = {
        legend: {
            data: data.legend,
             textStyle: {
              color: '#fff'
          },
             top: 20,
        },
        calculable: true,
        series: [
            {
                type:'funnel',
                left: '10%',
                top: "20%",
                bottom: "10%",
                width: '80%',
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
                emphasis: {
                    label: {
                        fontSize: 20
                    }
                },
                data: data.value
            }
        ]
    };
    var mychart = echarts.init(document.getElementById(id_str));
    mychart.setOption(option);
}