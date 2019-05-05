//记账本 selector 填充
function initSelector($, id, datas, default_value){
    for (var prop in datas) {
        if(default_value == datas[prop]){
            var htmls = '<option selected="selected" value = "' + datas[prop] + '">' +datas[prop] + '</option>';
        }else{
            var htmls = '<option value = "' + datas[prop] + '">' +datas[prop] + '</option>';
        }
        $("#"+id).append(htmls);
    };
}


layui.use(['form', 'jquery', 'laydate', 'layer', 'laypage', 'element'], function() {

    var form = layui.form,
	layer = layui.layer,
	$ = layui.jquery,
	dialog = layui.dialog;

    // 获得用户信息，设置html显示项
    var result = (function () {
        var result;
        $.ajax({
               url:"/api/v1/login/baseinfo",
                type:'GET',
                dataType:'json',
                async:false,
                success:function(json){ // http code 200
                    result = json
                }
            });
            return result;
    })();
    console.log(result)

    $("#user_name_id").attr("value",result.data.user_name)
    $("#password_id").attr("value",result.data.password)
    initSelector($, "calender_server_id", result.data.calendar_servers)

    var server_selected = $("#calender_server_id option:selected").val();
    initSelector($, "calender_name_id", result.data.calendar_names[server_selected], "时间日志")

    form.render('select');

    // form.submit 提交
    form.on("submit(confirm_id)", function(data){
        var result = (function () {
            var result;
            $.ajax({
                   url:"api/v1/login/baseinfo",
                    type:'POST',
                    dataType:'json',
                    data:data.field,
                    async:false,
                    success:function(json){ // http code 200
                        result = json
                    }
                });
                return result;
        })();
        console.log(result)

        window.location.href=result.data;
        return false;
    })





})