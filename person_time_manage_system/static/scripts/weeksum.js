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

function call_back(data){
    // 数据不为空才设置
    if (typeof(data) === "undefined"){
        return
    } else if (JSON.stringify(data) === "{}"){
        return
    }

    init0(data)
    dashboard_init("Chart1", data.working_and_study_tomato_nums_of_each_day)
    bar_init("Chart2", data.sleep_hours)
    select_bar_init("Chart3", data.every_day_category_details)
    pie_init("Chart4", data.each_category_time_sum)
    init5("Chart5", data.missing_info)
}

function main(){
    $.get("/api/v1/statistics/weekly/all/"+date_now).done(call_back)
}

$(function(){
    initDate()
    $.get("/api/v1/statistics/weekly/all/"+date_now).done(call_back)
    //每隔10秒查询一次
    setInterval(main, 10*1000);

    // // socket和后台通讯
    // var websocket_url =  document.domain + ':' + location.port + '/update';
    // var socket = io.connect(websocket_url);
    // //发送消息
    // socket.emit('weeksum', {"date_str":date_now});
    // //监听回复的消息
    // // socket.on('weeksum',call_back);
    // socket.on('weeksum',function (data) {
    //      console.log("weeksum")
    //     console.log(data)
    //     call_back(data.data)
    //  });
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

function init5(id_str, data){
    console.log(data);
        var tbody =document.getElementById(id_str);
        $("#"+id_str).html("");
        var info = data;
        if (JSON.stringify(info) === '{}' | (typeof info === 'undefined') ){
            return info
        }
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

