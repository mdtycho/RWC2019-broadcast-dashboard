
$(window).on("load",function(){$(".se-pre-con").fadeOut("slow");});
(function(){var fn=function(){Bokeh.safely(function(){(function(root){function embed_document(root){var docs_json='{"1ded7716-5ad6-46ac-9297-e47d441ca1e6":{"roots":{"references":[{"attributes":{"below":[{"id":"1096","type":"LinearAxis"}],"center":[{"id":"1100","type":"Grid"},{"id":"1105","type":"Grid"}],"left":[{"id":"1101","type":"LinearAxis"}],"plot_height":400,"plot_width":400,"renderers":[{"id":"1122","type":"GlyphRenderer"}],"title":{"id":"1133","type":"Title"},"toolbar":{"id":"1112","type":"Toolbar"},"x_range":{"id":"1088","type":"DataRange1d"},"x_scale":{"id":"1092","type":"LinearScale"},"y_range":{"id":"1090","type":"DataRange1d"},"y_scale":{"id":"1094","type":"LinearScale"}},"id":"1087","subtype":"Figure","type":"Plot"},{"attributes":{},"id":"1110","type":"ResetTool"},{"attributes":{"callback":null},"id":"1088","type":"DataRange1d"},{"attributes":{},"id":"1111","type":"HelpTool"},{"attributes":{"line_alpha":0.1,"line_color":"#1f77b4","line_width":2,"x":{"field":"x"},"y":{"field":"y"}},"id":"1121","type":"Line"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"1106","type":"PanTool"},{"id":"1107","type":"WheelZoomTool"},{"id":"1108","type":"BoxZoomTool"},{"id":"1109","type":"SaveTool"},{"id":"1110","type":"ResetTool"},{"id":"1111","type":"HelpTool"}]},"id":"1112","type":"Toolbar"},{"attributes":{"callback":null},"id":"1090","type":"DataRange1d"},{"attributes":{"source":{"id":"1119","type":"ColumnDataSource"}},"id":"1123","type":"CDSView"},{"attributes":{},"id":"1092","type":"LinearScale"},{"attributes":{},"id":"1094","type":"LinearScale"},{"attributes":{"formatter":{"id":"1138","type":"BasicTickFormatter"},"ticker":{"id":"1097","type":"BasicTicker"}},"id":"1096","type":"LinearAxis"},{"attributes":{},"id":"1097","type":"BasicTicker"},{"attributes":{},"id":"1140","type":"UnionRenderers"},{"attributes":{"ticker":{"id":"1097","type":"BasicTicker"}},"id":"1100","type":"Grid"},{"attributes":{"formatter":{"id":"1136","type":"BasicTickFormatter"},"ticker":{"id":"1102","type":"BasicTicker"}},"id":"1101","type":"LinearAxis"},{"attributes":{},"id":"1102","type":"BasicTicker"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"1141","type":"BoxAnnotation"},{"attributes":{"dimension":1,"ticker":{"id":"1102","type":"BasicTicker"}},"id":"1105","type":"Grid"},{"attributes":{},"id":"1138","type":"BasicTickFormatter"},{"attributes":{},"id":"1139","type":"Selection"},{"attributes":{"line_color":"#1f77b4","line_width":2,"x":{"field":"x"},"y":{"field":"y"}},"id":"1120","type":"Line"},{"attributes":{"callback":null,"data":{"x":[1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016],"y":[53,67,71,75,56,56,56,56,48,50,49,51,50,50,50,50,50,50,51,49,49,49,51,51]},"selected":{"id":"1139","type":"Selection"},"selection_policy":{"id":"1140","type":"UnionRenderers"}},"id":"1119","type":"ColumnDataSource"},{"attributes":{"data_source":{"id":"1119","type":"ColumnDataSource"},"glyph":{"id":"1120","type":"Line"},"hover_glyph":null,"muted_glyph":null,"nonselection_glyph":{"id":"1121","type":"Line"},"selection_glyph":null,"view":{"id":"1123","type":"CDSView"}},"id":"1122","type":"GlyphRenderer"},{"attributes":{"text":""},"id":"1133","type":"Title"},{"attributes":{},"id":"1106","type":"PanTool"},{"attributes":{},"id":"1136","type":"BasicTickFormatter"},{"attributes":{},"id":"1107","type":"WheelZoomTool"},{"attributes":{"overlay":{"id":"1141","type":"BoxAnnotation"}},"id":"1108","type":"BoxZoomTool"},{"attributes":{},"id":"1109","type":"SaveTool"}],"root_ids":["1087"]},"title":"Bokeh Application","version":"1.3.4"}}';var render_items=[{"docid":"1ded7716-5ad6-46ac-9297-e47d441ca1e6","roots":{"1087":"d1dba8d2-feb1-4527-bd91-90612a9400cc"}}];root.Bokeh.embed.embed_items(docs_json,render_items);}
if(root.Bokeh!==undefined){embed_document(root);}else{var attempts=0;var timer=setInterval(function(root){if(root.Bokeh!==undefined){embed_document(root);clearInterval(timer);}
attempts++;if(attempts>100){console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");clearInterval(timer);}},10,root)}})(window);});};if(document.readyState!="loading")fn();else document.addEventListener("DOMContentLoaded",fn);})();