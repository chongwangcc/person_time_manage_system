// var symptomName = last_month_day();

$(function(){
    init3()
    init4()
    init5()
    init6()
  // init();
  // init2();
})


function init(){
  //地图
  var mapChart = echarts.init(document.getElementById('mapChart'));
  mapChart.setOption({
      bmap: {
          center: [118.096435,24.485408],
          zoom: 12,
          roam: true,

      },
      tooltip : {
          trigger: 'item',
          formatter:function(params, ticket, callback){
              return params.value[2]
          }
      },
      series: [{
          type: 'scatter',
          coordinateSystem: 'bmap',
          data: [
            [118.096435, 24.485408, '厦门市'] ,
            [118.094564, 24.457358, '厦门第一医院'] ,
            [118.104103, 24.477761, '厦门中山医院'],
            [118.14748, 24.506295, '厦门中医院'],
            [118.254841, 24.665349, '厦门第五医院'],
           ]
      }]
  });
  mapChart.on('click', function (params) {
      $("#el-dialog").removeClass('hide');
      $("#reportTitle").html(params.value[2]);
  });

  var bmap = mapChart.getModel().getComponent('bmap').getBMap()
  bmap.addControl(new BMap.MapTypeControl({mapTypes: [BMAP_NORMAL_MAP,BMAP_SATELLITE_MAP ]}));
  bmap.setMapStyle({style:'midnight'})


  var pieChart1 = echarts.init(document.getElementById('pieChart1'));
  pieChart1.setOption({

    color:["#87cefa","#ff7f50","#32cd32","#da70d6",],

    legend: {
        y : '260',
        x : 'center',
        textStyle : {
            color : '#ffffff',

        },
         data : ['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a}<br/>{b}<br/>{c}G ({d}%)"
    },
    calculable : false,
    series : [
        {
            name:'采集数据量',
            type:'pie',
            radius : ['40%', '70%'],
            center : ['50%', '45%'],
            itemStyle : {
                normal : {
                    label : {
                        show : false
                    },
                    labelLine : {
                        show : false
                    }
                },
                emphasis : {
                    label : {
                        show : true,
                        position : 'center',
                        textStyle : {
                            fontSize : '20',
                            fontWeight : 'bold'
                        }
                    }
                }
            },
            data:[
                {value:335, name:'厦门第一医院'},
                {value:310, name:'厦门中山医院'},
                {value:234, name:'厦门中医院'},
                {value:135, name:'厦门第五医院'}

            ]
        }
    ]
    });


    var lineChart = echarts.init(document.getElementById('lineChart'));
    lineChart.setOption({

      color:["#87cefa","#ff7f50","#32cd32","#da70d6",],
      legend: {
          y : '260',
          x : 'center',
          textStyle : {
              color : '#ffffff',

          },
           data : ['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
      },
      calculable : false,
      tooltip : {
          trigger: 'item',
          formatter: "{a}<br/>{b}<br/>{c}条"
      },
      yAxis: [
            {
                type: 'value',
                axisLine : {onZero: false},
                axisLine:{
                    lineStyle:{
                        color: '#034c6a'
                    },
                },

                axisLabel: {
                    textStyle: {
                        color: '#fff'
                    },
                    formatter: function (value) {
                        return value + "k条"
                    },
                },
                splitLine:{
                    lineStyle:{
                        width:0,
                        type:'solid'
                    }
                }
            }
        ],
        xAxis: [
            {
                type: 'category',
                data : ['8:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00'],
                axisLine:{
                    lineStyle:{
                        color: '#034c6a'
                    },
                },
                splitLine: {
                    "show": false
                },
                axisLabel: {
                    textStyle: {
                        color: '#fff'
                    },
                    formatter: function (value) {
                        return value + ""
                    },
                },
                splitLine:{
                    lineStyle:{
                        width:0,
                        type:'solid'
                    }
                },
            }
        ],
        grid:{
                left: '5%',
                right: '5%',
                bottom: '20%',
                containLabel: true
        },
        series : [
          {
              name:'厦门第一医院',
              type:'line',
              smooth:true,
              itemStyle: {
                  normal: {
                      lineStyle: {
                          shadowColor : 'rgba(0,0,0,0.4)'
                      }
                  }
              },
              data:[15, 0, 20, 45, 22.1, 25, 70, 55, 76]
          },
          {
              name:'厦门中山医院',
              type:'line',
              smooth:true,
              itemStyle: {
                  normal: {
                      lineStyle: {
                          shadowColor : 'rgba(0,0,0,0.4)'
                      }
                  }
              },
              data:[25, 10, 30, 55, 32.1, 35, 80, 65, 76]
          },
          {
              name:'厦门中医院',
              type:'line',
              smooth:true,
              itemStyle: {
                  normal: {
                      lineStyle: {
                          shadowColor : 'rgba(0,0,0,0.4)'
                      }
                  }
              },
              data:[35, 20, 40, 65, 42.1, 45, 90, 75, 96]
          },
          {
              name:'厦门第五医院',
              type:'line',
              smooth:true,
              itemStyle: {
                  normal: {
                      lineStyle: {
                          shadowColor : 'rgba(0,0,0,0.4)'
                      }
                  }
              },
              data:[45, 30, 50, 75, 52.1, 55, 100, 85, 106]
          }
      ]
    });

    var histogramChart = echarts.init(document.getElementById('histogramChart'));
    histogramChart.setOption({

      color:["#87cefa","#ff7f50","#32cd32","#da70d6",],
      legend: {
          y : '250',
          x : 'center',
          data:['厦门第一医院', '厦门中山医院','厦门中医院','厦门第五医院'],
          textStyle : {
              color : '#ffffff',

          }
      },

      calculable :false,


      grid:{
              left: '5%',
              right: '5%',
              bottom: '20%',
              containLabel: true
      },

      tooltip : {
          trigger: 'axis',
          axisPointer : {
              type : 'shadow'
          }
      },

      xAxis : [
          {
              type : 'value',
              axisLabel: {
                  show: true,
                  textStyle: {
                      color: '#fff'
                  }
              },
              splitLine:{
                  lineStyle:{
                      color:['#f2f2f2'],
                      width:0,
                      type:'solid'
                  }
              }

          }
      ],

      yAxis : [
          {
              type : 'category',
              data:['门诊人数(人)', '住院人次(人)','人均费用(元)'],
              axisLabel: {
                  show: true,
                  textStyle: {
                      color: '#fff'
                  }
              },
              splitLine:{
                  lineStyle:{
                      width:0,
                      type:'solid'
                  }
              }
          }
      ],

      series : [
          {
              name:'厦门第一医院',
              type:'bar',
              stack: '总量',
              itemStyle : { normal: {label : {show: true, position: 'insideRight'}}},
              data:[320, 302, 301]
          },
          {
              name:'厦门中山医院',
              type:'bar',
              stack: '总量',
              itemStyle : { normal: {label : {show: true, position: 'insideRight'}}},
              data:[120, 132, 101]
          },
          {
              name:'厦门中医院',
              type:'bar',
              stack: '总量',
              itemStyle : { normal: {label : {show: true, position: 'insideRight'}}},
              data:[220, 182, 191]
          },
          {
              name:'厦门第五医院',
              type:'bar',
              stack: '总量',
              itemStyle : { normal: {label : {show: true, position: 'insideRight'}}},
              data:[150, 212, 201]
          }

      ]
   });

   var lineChart2 = echarts.init(document.getElementById('lineChart2'));
   lineChart2.setOption({

     color:["#87cefa","#ff7f50","#32cd32","#da70d6",],
     legend: {
         y : '260',
         x : 'center',
         textStyle : {
             color : '#ffffff',

         },
          data : ['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
     },
     calculable : false,
     tooltip : {
         trigger: 'item',
         formatter: "{a}<br/>{b}<br/>{c}条"
     },
     yAxis: [
           {
               type: 'value',
               axisLine : {onZero: false},
               axisLine:{
                   lineStyle:{
                       color: '#034c6a'
                   },
               },

               axisLabel: {
                   textStyle: {
                       color: '#fff'
                   },
                   formatter: function (value) {
                       return value + "k条"
                   },
               },
               splitLine:{
                   lineStyle:{
                       width:0,
                       type:'solid'
                   }
               }
           }
       ],
       xAxis: [
           {
               type: 'category',
               data : ['8:00','10:00','12:00','14:00','16:00','18:00'],
               axisLine:{
                   lineStyle:{
                       color: '#034c6a'
                   },
               },
               splitLine: {
                   "show": false
               },
               axisLabel: {
                   textStyle: {
                       color: '#fff'
                   },
                   formatter: function (value) {
                       return value + ""
                   },
               },
               splitLine:{
                   lineStyle:{
                       width:0,
                       type:'solid'
                   }
               },
           }
       ],
       grid:{
               left: '5%',
               right: '5%',
               bottom: '20%',
               containLabel: true
       },
       series : [
         {
             name:'厦门第一医院',
             type:'line',
             smooth:true,
             itemStyle: {
                 normal: {
                     lineStyle: {
                         shadowColor : 'rgba(0,0,0,0.4)'
                     }
                 }
             },
             data:[15, 0, 20, 45, 22.1, 25,].reverse()
         },
         {
             name:'厦门中山医院',
             type:'line',
             smooth:true,
             itemStyle: {
                 normal: {
                     lineStyle: {
                         shadowColor : 'rgba(0,0,0,0.4)'
                     }
                 }
             },
             data:[25, 10, 30, 55, 32.1, 35, ].reverse()
         },
         {
             name:'厦门中医院',
             type:'line',
             smooth:true,
             itemStyle: {
                 normal: {
                     lineStyle: {
                         shadowColor : 'rgba(0,0,0,0.4)'
                     }
                 }
             },
             data:[35, 20, 40, 65, 42.1, 45, ].reverse()
         },
         {
             name:'厦门第五医院',
             type:'line',
             smooth:true,
             itemStyle: {
                 normal: {
                     lineStyle: {
                         shadowColor : 'rgba(0,0,0,0.4)'
                     }
                 }
             },
             data:[45, 30, 50, 75, 52.1, 55, 6].reverse()
         }
     ]
   });



}

function init2(){
  var lineChart3 = echarts.init(document.getElementById('lineChart3'));
  lineChart3.setOption({

    color:["#87cefa","#ff7f50",],
    legend: {
        y : 'top',
        x : 'center',
        textStyle : {
            color : '#ffffff',

        },
         data : ['门诊人次','住院人次'],
    },
    calculable : false,
    tooltip : {
        trigger: 'item',
        formatter: "{a}<br/>{b}<br/>{c}人"
    },
    dataZoom: {
         show: true,
         realtime : true,
         start: 0,
         end: 18,
         height: 20,
         backgroundColor: '#f8f8f8',
         dataBackgroundColor: '#e4e4e4',
         fillerColor: '#87cefa',
         handleColor: '#87cefa',
     },
    yAxis: [
          {
              type: 'value',
              axisLine : {onZero: false},
              axisLine:{
                  lineStyle:{
                      color: '#034c6a'
                  },
              },

              axisLabel: {
                  textStyle: {
                      color: '#fff'
                  },
                  formatter: function (value) {
                      return value + "人"
                  },
              },
              splitLine:{
                  lineStyle:{
                      width:0,
                      type:'solid'
                  }
              }
          }
      ],
      xAxis: [
          {
              type: 'category',
              data : symptomName,
              boundaryGap : false,
              axisLine:{
                  lineStyle:{
                      color: '#034c6a'
                  },
              },
              splitLine: {
                  "show": false
              },
              axisLabel: {
                  textStyle: {
                      color: '#fff'
                  },
                  formatter: function (value) {
                      return value + ""
                  },
              },
              splitLine:{
                  lineStyle:{
                      width:0,
                      type:'solid'
                  }
              },
          }
      ],
      grid:{
              left: '5%',
              right: '5%',
              bottom: '20%',
              containLabel: true
      },
      series : [
        {
            name:'门诊费用',
            type:'line',
            smooth:true,
            itemStyle: {
                normal: {
                    lineStyle: {
                        shadowColor : 'rgba(0,0,0,0.4)'
                    }
                }
            },
            data:[1150, 180, 2100, 2415, 1212.1, 3125,1510, 810, 2100, 2415, 1122.1, 3215,1510, 801, 2001, 2245, 1232.1, 3245,1520, 830, 2200, 2145, 1223.1, 3225,150, 80, 200, 245, 122.1, 325]
        },
        {
            name:'住院费用',
            type:'line',
            smooth:true,
            itemStyle: {
                normal: {
                    lineStyle: {
                        shadowColor : 'rgba(0,0,0,0.4)'
                    }
                }
            },
            data:[2500, 1000, 3000, 5005, 3200.1, 3005, 2500, 1000, 3000, 5005, 3200.1, 3005,2500, 1000, 3000, 5005, 3200.1, 3005,2500, 1000, 3000, 5005, 3200.1, 3005, 2500, 1000, 3000, 5005, 3200.1, 3005,2500, 1000, 3000, 5005, 3200.1, 3005,]
        },
    ]
  });


  var lineChart4 = echarts.init(document.getElementById('lineChart4'));
  lineChart4.setOption({

    color:["#87cefa","#ff7f50",],
    calculable : false,
    tooltip : {
        trigger: 'item',
        formatter: "{a}<br/>{b}<br/>{c}元"
    },
    dataZoom: {
         show: true,
         realtime : true,
         start: 0,
         end: 18,
         height: 20,
         backgroundColor: '#f8f8f8',
         dataBackgroundColor: '#e4e4e4',
         fillerColor: '#87cefa',
         handleColor: '#87cefa',
     },
    yAxis: [
          {
              type: 'value',
              axisLine : {onZero: false},
              axisLine:{
                  lineStyle:{
                      color: '#034c6a'
                  },
              },

              axisLabel: {
                  textStyle: {
                      color: '#fff'
                  },
                  formatter: function (value) {
                      return value + "元"
                  },
              },
              splitLine:{
                  lineStyle:{
                      width:0,
                      type:'solid'
                  }
              }
          }
      ],
      xAxis: [
          {
              type: 'category',
              data : symptomName,
              boundaryGap : false,
              axisLine:{
                  lineStyle:{
                      color: '#034c6a'
                  },
              },
              splitLine: {
                  "show": false
              },
              axisLabel: {
                  textStyle: {
                      color: '#fff'
                  },
                  formatter: function (value) {
                      return value + ""
                  },
              },
              splitLine:{
                  lineStyle:{
                      width:0,
                      type:'solid'
                  }
              },
          }
      ],
      grid:{
              left: '5%',
              right: '5%',
              bottom: '20%',
              containLabel: true
      },
      series : [
        {
            name:'医疗费用',
            type:'line',
            smooth:true,
            itemStyle: {
                normal: {
                    lineStyle: {
                        shadowColor : 'rgba(0,0,0,0.4)'
                    }
                }
            },
            data:[1500, 800, 1200, 2450, 1122.1, 1325,1150, 180, 1200, 1245, 1122.1, 1325,150, 180, 1200, 2145, 1212.1, 3215,1510, 180, 2100, 2415, 122.1, 325,150, 80, 200, 245, 122.1, 325].reverse()
        },
    ]
  });

  //年龄分布
  var pieChart2 = echarts.init(document.getElementById('pieChart2'));
  pieChart2.setOption({
    color:["#32cd32","#ff7f50","#87cefa","#FD6C88","#4b5cc4","#faff72"],
    tooltip : {
     trigger: 'item',
     formatter: "{a}<br/>{b}<br/>{c}人"
    },
    calculable : true,
    series : [
        {
            name:'发病人数',
            type:'pie',
            radius : [30, 110],
            center : ['50%', '50%'],
            roseType : 'area',
            x: '50%',



            sort : 'ascending',
            data:[
                {value:10, name:'婴儿(1-3岁)'},
                {value:5, name:'少儿(4-10岁)'},
                {value:15, name:'少年(10-18岁)'},
                {value:25, name:'青年(18-45岁)'},
                {value:125, name:'中年(45-60岁)'},
                {value:175, name:'老年(60岁以上)'},
            ]
        }
    ]
  })

  //医疗费用组成
  var pieChart3 = echarts.init(document.getElementById('pieChart3'));
  pieChart3.setOption({
    color:["#32cd32","#ff7f50","#87cefa","#FD6C88","#4b5cc4","#faff72"],
    tooltip : {
     trigger: 'item',
     formatter: "{a}<br/>{b}<br/>{c}元"
    },
    calculable : true,
    series : [
        {
            name:'发病人数',
            type:'pie',
            radius : [30, 110],
            center : ['50%', '50%'],
            roseType : 'area',
            x: '50%',



            sort : 'ascending',
            data:[
                {value:10, name:'诊察费用'},
                {value:500, name:'检查费用'},
                {value:150, name:'检验费用'},
                {value:250, name:'西药费用'},
                {value:125, name:'中药费用'},
                {value:1750, name:'手术费用'},
            ]
        }
    ]
  })
}

function init3(){
    // 番茄始终达标率
    //调用后台接口，获得番茄数
    var date_now = "2019.1.16"
    $.get("/fanqie_shu/"+date_now).done(function (data) {
        var nums = data.study_tomato_nums
        //设置番茄始终达标数
        var pieChart1 = echarts.init(document.getElementById('pieChart1'));
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
    })


}

function init4(){
    var date_now = "2019.1.16"
    $.get("/sleep_hours/"+date_now).done(function (data) {
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

        var histogramChart = echarts.init(document.getElementById('histogramChart'));
        histogramChart.setOption(option2)
    });
}

function init5(){
     var date_now = "2019.1.16"
     $.get("/each_category_hours/"+date_now).done(function (data) {

         var scaleData = data;
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

         var lineChart = echarts.init(document.getElementById('lineChart'));
         lineChart.setOption(option)
     });

}

function init6(){
    var corlor_list = ["rgba(255,144,128,1)", "rgba(0,191,183,1)", ]
    var xData = [" 星期1"," 星期2"," 星期3"," 星期4"," 星期5"," 星期6"," 星期7"]
    var legendData =  ['睡觉', '学习', '吃饭']
    var all_data_list = [
         [
                    709,
                    1917,
                    2455,
                    2610,
                    1719,
                    1433,
                    1544,
                    3285,
                    5208,
                    3372,
                    2484,
                    4078
                ],[
                    327,
                    1776,
                    507,
                    1200,
                    800,
                    482,
                    204,
                    1390,
                    1001,
                    951,
                    381,
                    220
                ]
    ]

    var total_data = [
                    1036,
                    3693,
                    2962,
                    3810,
                    2519,
                    1915,
                    1748,
                    4675,
                    6209,
                    4323,
                    2865,
                    4298
                ]
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
    for(var i=0;i<corlor_list.length;i++){
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
            start: 10,
            end: 80,
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

    var mapChart = echarts.init(document.getElementById('mapChart'));
    mapChart.setOption(option)
}