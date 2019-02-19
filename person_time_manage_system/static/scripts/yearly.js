// var symptomName = last_month_day();

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
        format:'yyyy-mm-dd',
        onSelect: function(dateText) {
            var dd = new Date(dateText).Format("yyyy-MM-dd");
            date_now = dd
            n = new Date(dateText).getDay()

            m_start_date = addDate(dd, -n)
            m_end_date = addDate(dd, 6-n)

             //设置开始时间、结束时间
            var tlabel =document.getElementById("id_start_date");
            tlabel.innerHTML=m_start_date
            var tlabel =document.getElementById("id_end_date");
            tlabel.innerHTML=m_end_date

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

    // 运动、娱乐次数
    var tlabel =document.getElementById("exercise_nums");
    tlabel.innerHTML="0"
    var tlabel =document.getElementById("fun_nums");
    tlabel.innerHTML="0"

    var echart1 = echarts.init(document.getElementById("Chart1"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("Chart2"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("Chart3"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("Chart4"));
    echart1.clear()

     var ba =    document.getElementById("Chart5")
     ba.innerHTML=""

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
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate;    
    return currentdate;
}

function main(){
    $.get("/api/v1/statistics/yearly/all/"+date_now).done(function (data){
        init0(data)
        init1("Chart1", data.word_cloud)
        init2("Chart2", data.every_week_category_details)
        init3("Chart3", data.category_rectangle)
    })
}

$(function(){
    initDate()
    main()

})

function init0(data){
    //设置开始时间、结束时间
    var tlabel =document.getElementById("id_start_date");
    tlabel.innerHTML=data.year
    var tlabel =document.getElementById("id_end_date");
    tlabel.innerHTML=data.end_date

    // 工作、学习番茄时钟数
    var tlabel =document.getElementById("id_work_tomato_nums");
    tlabel.innerHTML=data.working_tomato_nums
    var tlabel =document.getElementById("id_study_tomato_nums");
    tlabel.innerHTML=data.study_tomato_nums

    // 运动、娱乐次数
    var tlabel =document.getElementById("workout_nums");
    tlabel.innerHTML=data.workout_nums
    var tlabel =document.getElementById("workout_hours");
    tlabel.innerHTML=data.workout_hours
}

function init1(id_str, data1){
    var data=data1

    var option = {
           series: [
                {width: '90%',
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

function init2(id_str, data){
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

function init3(id_str, data1){
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
