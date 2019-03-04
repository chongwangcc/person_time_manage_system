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


    $("#img_datepicker").on("click", function(e) {
         $('#datepicker').datepicker('show');
    });
    $('#datepicker').datepicker({
        format:'yyyy',
        changeMonth: false,
        changeYear: true,
        showButtonPanel: true,


        onClose: function(dateText, inst) {
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
             //设置开始时间、结束时间
             //设置开始时间、结束时间
            var tlabel =document.getElementById("id_start_date");
            tlabel.innerHTML=year
            var tlabel =document.getElementById("id_end_date");
            tlabel.innerHTML="12-31"

            date_now=year

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
    var tlabel =document.getElementById("workout_nums");
    tlabel.innerHTML="0"
    var tlabel =document.getElementById("workout_hours");
    tlabel.innerHTML="0"

    var echart1 = echarts.init(document.getElementById("Chart1"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("Chart2"));
    echart1.clear()
    var echart1 = echarts.init(document.getElementById("Chart3"));
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
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate;    
    return currentdate;
}

function main(){
    $.get("/api/v1/statistics/yearly/all/"+date_now).done(function (data){
        // 数据不为空才设置
        if (typeof(data) === "undefined"){
            return
        } else if (JSON.stringify(data) === "{}"){
            return
        }

        init0(data)
        word_cloud_init("Chart1", data.word_cloud)
        select_bar_init("Chart2", data.every_week_category_details)
        rect_init("Chart3", data.category_rectangle)
    })
}

$(function(){
    initDate()
    main()
    //每隔10秒查询一次
    setInterval(main, 10000);
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

