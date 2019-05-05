layui.define(['jquery'], function (exports) {
  "use strict";
  var $ = layui.$;
  $.fn.step = function(options) {
    var opts = $.extend({}, $.fn.step.defaults, options);
    var size=this.find(".step-header li").length;
    var barWidth=opts.initStep<size?100/(1*size)+100*(opts.initStep-1)/size : 100;
    var curPage=opts.initStep;
    var steps = this;
    var bar_w = (100 - (100/size)) + '%';
    this.find(".step-header").prepend("<div class=\"step-bar\" style='width:"+bar_w+"'><div class=\"step-bar-active\"></div></div>");
    this.find(".step-list").eq(opts.initStep).show();
    if (size<opts.initStep) {
      opts.initStep=size;
    }
    if (opts.animate==false) {
      opts.speed=0;
    }
    this.find(".step-header li").each(function (i, li) {
      if(i == 0){
        $(li).addClass("step-current")
            .append('<a href="javascript:;" class="jump-steps" data-step="'+(i+1)+'">'+(i+1)+'</a>');
      } else if (i<opts.initStep){
        $(li).addClass("step-active")
            .append('<a href="javascript:;" class="jump-steps" data-step="'+(i+1)+'"></a>');
      }else{
        $(li).append('<a href="javascript:;" class="jump-steps" data-step="'+(i+1)+'">'+(i+1)+'</a>');
      }
    });
    this.find(".step-header li").css({
      "width": 100/size+"%"
    });
    this.find(".step-header").show();
    this.find(".step-bar-active").animate({
          "width": barWidth+"%"},
        opts.speed, function() {

        });

    this.find(".jump-steps").on('click',function () {
      var step_id = $(this).attr("data-step");
      steps.goStep(step_id);
    });

    this.nextStep=function() {
      if (curPage>=size) {
        return false;
      }
      var next_step_num = curPage == 0? 2:  curPage+1;
      return this.goStep(next_step_num);
    };

    this.preStep=function() {
      if (curPage<=1) {
        return false;
      }
      var pre_step_num = curPage == 1? 1: curPage-1;
      return this.goStep(pre_step_num);
    };

    this.goStep=function(page) {
      if (page ==undefined || isNaN(page) || page<0) {
        if(window.console&&window.console.error){
          console.error('the method goStep has a error,page:'+page);
        }
        return false;
      }
      curPage=parseInt(page);
      this.find(".step-list").hide();
      this.find(".step-list").eq(curPage-1).show();
      this.find(".step-header li").each(function (i, li) {
        var $li=$(li);
        $li.removeClass('step-current')
            .removeClass('step-active');
        $li.find("a").html(i+1);
        if ((i+1)<page){
          $li.addClass('step-active');
          $li.find("a").empty();
          if(opts.scrollTop){
            $('html,body').animate({scrollTop:0}, 'slow');
          }
        }else if((i+1) == page){
          $li.addClass('step-current');
        }
      });
      var bar_rate = 100/(100-(100/size));

      barWidth= page<size? (100/(2*size)+100*(page-1)/size)*bar_rate : 100;
      this.find(".step-bar-active").animate({
            "width": barWidth+"%"},
          opts.speed, function() {

          });
      return true;
    };
    return this;
  };
  $.fn.step.defaults = {
    animate:true,
    speed:200,
    initStep:0,
    scrollTop:true
  };

  exports('steps', $);
});