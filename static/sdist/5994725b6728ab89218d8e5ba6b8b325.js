
$(window).on("load",function(){$(".se-pre-con").fadeOut("slow");});
if(root.Bokeh!==undefined){embed_document(root);}else{var attempts=0;var timer=setInterval(function(root){if(root.Bokeh!==undefined){embed_document(root);clearInterval(timer);}
attempts++;if(attempts>100){console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");clearInterval(timer);}},10,root)}})(window);});};if(document.readyState!="loading")fn();else document.addEventListener("DOMContentLoaded",fn);})();