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
        // 数据不为空才设置
        if (typeof(data) === "undefined"){
            return
        } else if (JSON.stringify(data) === "{}"){
            return
        }
        init0(data.this_month)
        word_cloud_init("echart1", data.this_month.word_cloud)
        radar_init("echart3", data.this_month.ability_redar)
        line_init("echart7", data.this_month.living_time)
        bar_init("echart5", data.this_month)

        word_cloud_init("echart2", data.last_month.word_cloud)
        radar_init("echart4", data.last_month.ability_redar)
        line_init("echart8", data.last_month.living_time)
        bar_init("echart6", data.last_month)
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

