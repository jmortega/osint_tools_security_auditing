function attachEvent(element,name,f){
 f=Function.closure(element,f);if(element.addEventListener){
 element.addEventListener(name,f,false);}else if(element.attachEvent){
 element.attachEvent("on"+name,f);}else{
 element["on"+name]=f;}
 element[name]=f;}
Function.closure=function(parent,f){
 return function(){ return f.apply(parent,arguments);};};
Object.keys=function(object){
 var a=[];for(var k in object)a.push(k);return a;};
Object.values=function(object){
 var a=[];for(var k in object)a.push(object[k]);return a;};
Array.sum=function(array){
 for(var i=0,sum=0;i < array.length;sum+=array[i++]){};return sum;};
Array.index=function(array,v){
 for(var i=0;i < array.length;i++){ if(array[i]===v)return i;}
 return-1;};
Array.choice=function(array){
 return array[Math.round(Math.random()*(array.length-1))];};
Array.unique=function(array){
 var a=array.slice();for(var i=a.length-1;i > 0;--i){
 var v=a[i];for(var j=i-1;j >=0;--j){
 if(a[j]===v)a.splice(j,1);i--;}
 }
 return a;};
var choice=Array.choice;
Math.degrees=function(radians){
 return radians*180/Math.PI;};
Math.radians=function(degrees){
 return degrees/180*Math.PI;};
Math.coordinates=function(x,y,distance,angle){
 return[x+distance*Math.cos(Math.radians(angle)),
 y+distance*Math.sin(Math.radians(angle))];};
var __MOUSE__={
 x: 0,
 y: 0,
 _x0: 0,
 _y0: 0,
 dx: 0,
 dy: 0,
 pressed: false,
 dragged: false,
 relative: function(element){
 var dx=0;var dy=0;if(element.offsetParent){
 do{
 dx+=element.offsetLeft;dy+=element.offsetTop;}while(element=element.offsetParent);}
 return{
 x: __MOUSE__.x-dx,
 y: __MOUSE__.y-dy
 }
 }
};
attachEvent(document,"mousemove",function(e){
 __MOUSE__.x=e.pageX ||(e.clientX+(document.documentElement.scrollLeft || document.body.scrollLeft));__MOUSE__.y=e.pageY ||(e.clientY+(document.documentElement.scrollTop || document.body.scrollTop));if(__MOUSE__.pressed){
 __MOUSE__.dragged=true;__MOUSE__.dx=__MOUSE__.x-__MOUSE__._x0;__MOUSE__.dy=__MOUSE__.y-__MOUSE__._y0;}
});
attachEvent(document,"mousedown",function(e){
 __MOUSE__.pressed=true;__MOUSE__._x0=__MOUSE__.x;__MOUSE__._y0=__MOUSE__.y;});
attachEvent(document,"mouseup",function(e){
 __MOUSE__.pressed=false;__MOUSE__.dragged=false;__MOUSE__.dx=0;__MOUSE__.dy=0;});
function _unselectable(element){
 if(element){
 element.onselectstart=function(){ return false;};element.unselectable="on";element.style.MozUserSelect="none";element.style.cursor="default";}
}
(function(){
 var initialized=false;var has_super=/xyz/.test(function(){ xyz;})?/\b_super\b/:/.*/;this.Class=function(){};Class.extend=function(properties){
 var _super=this.prototype;initialized=true;var p=new this();
 initialized=false;
 for(var k in properties){
 p[k]=typeof properties[k]=="function"
 && typeof _super[k]=="function"
 && has_super.test(properties[k])?(function(k,f){ return function(){
 var s,r;s=this._super;
 this._super=_super[k];r=f.apply(this,arguments);
 this._super=s;return r;};
 })(k,properties[k]): properties[k];}
 function Class(){
 if(!initialized && this.init){
 this.init.apply(this,arguments);}
 }
 Class.constructor=Class;Class.prototype=p;
 Class.extend=arguments.callee;return Class;};})();
function _parseRGBA(clr){
 if(clr && clr.rgba && clr._get){
 return clr._get();}
 if(clr instanceof Array){
 var r=Math.round(clr[0]*255);var g=Math.round(clr[1]*255);var b=Math.round(clr[2]*255);return "rgba("+r+","+g+","+b+","+clr[3]+")";
 }
 if(clr===null){
 return "rgba(0,0,0,0)";}
 return clr;}
var _GRAPH_FILL1=null;var _GRAPH_FILL2=null;function _ctx_graph_fillStyle(clr,ctx){
 clr=_parseRGBA(clr);if(clr===undefined){
 if(_ctx && _ctx.state && _ctx.state.fill !==undefined){
 clr=_parseRGBA(_ctx.state.fill);}else{
 clr="rgba(0,0,0,0)";}
 }
 if(_GRAPH_FILL1 !=clr || _GRAPH_FILL2 !=ctx.fillStyle){
 _GRAPH_FILL1=ctx.fillStyle=clr;_GRAPH_FILL2=ctx.fillStyle;}
}
var _GRAPH_STROKE1=null;var _GRAPH_STROKE2=null;function _ctx_graph_strokeStyle(clr,ctx){
 clr=_parseRGBA(clr);if(clr===undefined){
 if(_ctx && _ctx.state && _ctx.state.stroke !==undefined){
 clr=_parseRGBA(_ctx.state.stroke);}else{
 clr="rgba(0,0,0,1)";}
 }
 if(_GRAPH_STROKE1 !=clr || _GRAPH_STROKE2 !=ctx.strokeStyle){
 _GRAPH_STROKE1=ctx.strokeStyle=clr;_GRAPH_STROKE2=ctx.strokeStyle;}
}
function _ctx_graph_lineWidth(w1,w2,ctx){
 if(w1===undefined){
 w1=_ctx && _ctx.state && _ctx.state.strokewidth || 1.0;}
 ctx.lineWidth=w1+w2 || 0;}
var Node=Class.extend({
 init: function(id,a){
 if(a===undefined)a={};if(a.x===undefined)a.x=0;if(a.y===undefined)a.y=0;if(a.radius===undefined)a.radius=5;if(a.fixed===undefined)a.fixed=false;
 this.graph=null;this.links=new NodeLinks();this.id=id;this.x=0;
 this.y=0;
 this._x=a.x;this._y=a.y;this._vx=0;this._vy=0;this.radius=a.radius;this.fixed=a.fixed;this.fill=a.fill;this.stroke=a.stroke;this.strokewidth=a.strokewidth;this.weight=a.weight || 0;this.centrality=a.centrality || 0;this.degree=a.degree || 0;this.text=null;if(a.text !=false){
 var div=document.createElement('div');var txt=((a.label || id)+"").replace("\\\"","\"");txt=txt.replace("<","&lt;");txt=txt.replace(">","&gt;");div.innerHTML=(a.href)? '<a href="'+a.href+'">'+txt+"</a>" : txt;div.className=(a.css)?("node-label "+a.css): "node-label";div.style.fontFamily=(a.font)? a.font : "";div.style.fontSize=(a.fontsize)? a.fontsize+"px" : "";div.style.fontWeight=(a.fontweight)? a.fontweight : "";
 div.style.color=(typeof(a.text)=="string")? a.text : "";this.text=div;_unselectable(div);}
 },
 edges: function(){
 var a=[];for(var i=0;i < this.graph.edges.length;i++){
 var e=this.graph.edges[i];if(e.node1==this || e.node2==this){
 a.push(e);}
 }
 return a;},
 flatten: function(depth,traversable,_visited){
 if(depth===undefined)depth=1;if(traversable===undefined)traversable=function(node,edge){ return true;};_visited=_visited ||{};_visited[this.id]=[this,depth];if(depth >=1){
 for(var i=0;i < this.links.length;i++){
 var n=this.links[i];if(!_visited[n.id]|| _visited[n.id][1]< depth-1){
 if(traversable(this,this.links.edges[n.id])){
 n.flatten(depth-1,traversable,_visited);}
 }
 }
 }
 var a=Object.values(_visited);
 for(var i=0;i < a.length;i++){
 a[i]=a[i][0];}
 return a;},
 draw: function(weighted){
 var ctx=this.graph._ctx;
 if(weighted && weighted !=false && this.centrality >((weighted==true)?-1:weighted)){
 var w=this.centrality*35;_ctx_graph_fillStyle("rgba(0,0,0,0.075)",ctx);ctx.beginPath();ctx.arc(this.x,this.y,this.radius+w,0,Math.PI*2,true);ctx.closePath();ctx.fill();}
 _ctx_graph_lineWidth(this.strokewidth,0,ctx);_ctx_graph_strokeStyle(this.stroke,ctx);_ctx_graph_fillStyle(this.fill,ctx);ctx.beginPath();ctx.arc(this.x,this.y,this.radius,0,Math.PI*2,true);ctx.closePath();ctx.fill();ctx.stroke();
 if(this.text){
 this.text.style.display="inline";this.text.style.position="absolute";this.text.style.left=Math.round(this.x+this.radius/2+this.graph.canvas.width/2)+"px";this.text.style.top=Math.round(this.y+this.radius/2+this.graph.canvas.height/2)+"px";}
 },
 contains: function(x,y){
 return Math.abs(this.x-x)< this.radius*2 &&
 Math.abs(this.y-y)< this.radius*2
 }
});
var NodeLinks=Class.extend({
 init: function(){
 this.edges={};this.length=0;},
 append: function(node,edge){
 if(!this.edges[node.id]){
 this[this.length]=node;
 this.length+=1;}
 this.edges[node.id]=edge;},
 remove: function(node){
 var i=Array.index(this,node);if(i >=0){
 for(var j=i;j < this.length;j++)this[j]=this[j+1];this.length-=1;delete this.edges[node.id];}
 },
 edge: function(node){
 return this.edges[(node instanceof Node)? node.id : node]|| null;}
});
var Edge=Class.extend({
 init: function(node1,node2,a){
 if(a===undefined)a={};if(a.weight===undefined)a.weight=0.0;if(a.length===undefined)a.length=1.0;if(a.type===undefined)a.type=null;
 this.node1=node1;this.node2=node2;this.weight=a.weight;this.length=a.length;this.type=a.type;this.stroke=a.stroke;this.strokewidth=a.strokewidth;},
 draw: function(weighted,directed){
 var w=weighted && this.weight || 0;var ctx=this.node1.graph._ctx;_ctx_graph_lineWidth(this.strokewidth,w,ctx);_ctx_graph_strokeStyle(this.stroke,ctx);ctx.beginPath();ctx.moveTo(this.node1.x,this.node1.y);ctx.lineTo(this.node2.x,this.node2.y);ctx.stroke();if(directed){
 this.drawArrow(this.strokewidth);}
 },
 drawArrow: function(strokewidth){
 var s=(strokewidth !==undefined)? strokewidth : _ctx && _ctx.state && _ctx.state.strokewidth || 1;var x0=this.node1.x;var y0=this.node1.y;var x1=this.node2.x;var y1=this.node2.y;
 var a=Math.degrees(Math.atan2(y1-y0,x1-x0));
 var d=Math.sqrt(Math.pow(x1-x0,2)+Math.pow(y1-y0,2));var r=Math.max(s*4,8);var p1=Math.coordinates(x0,y0,d-this.node2.radius-1,a);var p2=Math.coordinates(p1[0],p1[1],-r,a-20);var p3=Math.coordinates(p1[0],p1[1],-r,a+20);var ctx=this.node1.graph._ctx;_ctx_graph_fillStyle(ctx.strokeStyle,ctx);ctx.beginPath();ctx.moveTo(p1[0],p1[1]);ctx.lineTo(p2[0],p2[1]);ctx.lineTo(p3[0],p3[1]);ctx.fill();}
});
var SHADOW=0.0;
var SPRING="spring";
var EIGENVECTOR="eigenvector";var BETWEENNESS="betweenness";
var WEIGHT="weight"
var CENTRALITY="centrality"
var Graph=Class.extend({
 init: function(canvas,distance,layout){
 if(distance===undefined)distance=10;if(layout===undefined)layout=SPRING;this.canvas=canvas;_unselectable(canvas);this._ctx=this.canvas? this.canvas.getContext("2d"): null;this.nodeset={};this.nodes=[];this.edges=[];this.root=null;this.mouse=__MOUSE__;this.distance=distance;this.layout=(layout==SPRING)? new GraphSpringLayout(this):
 new GraphLayout(this);},
 $: function(id){
 return this.nodeset[id];},
 append: function(base,a){
 if(base==Node)
 return this.add_node(a.id,a);if(base==Edge)
 return this.add_edge(a.id1,a.id2,a);},
 addNode: function(id,a){
 var n=a && a._super || Node;n=(id instanceof Node)? id :(this.nodeset[id])? this.nodeset[id]: new n(id,a);if(a && a.root)this.root=n;if(!this.nodeset[n.id]){
 this.nodes.push(n);this.nodeset[n.id]=n;n.graph=this;if(n.text && this.canvas && this.canvas.parentNode){
 this.canvas.parentNode.appendChild(n.text);}
 }
 return n;},
 addEdge: function(id1,id2,a){
 var n1=this.addNode(id1);var n2=this.addNode(id2);
 var e1=n1.links.edge(n2)
 if(e1 && e1.node1==n1 && e1.node2==n2){
 return e1;
 }
 e2=a && a._super || Edge;e2=new e2(n1,n2,a);this.edges.push(e2);
 n1.links.append(n2,edge=e2)
 n2.links.append(n1,edge=e1||e2)
 return e2;},
 remove: function(x){
 if(x instanceof Node && this.nodeset[x.id]){
 delete this.nodeset[x.id];this.nodes.splice(Array.index(this.nodes,x),1);x.graph=null;
 var a=[];for(var i=0;i < this.edges.length;i++){
 var e=this.edges[i];if(x==e.node1 || x==e.node2){
 if(x==e.node2)e.node1.links.remove(x);if(x==e.node1)e.node2.links.remove(x);}else{
 a.push(e);}
 }
 this.edges=a;
 if(x.text)x.text.parentNode.removeChild(x.text);}
 if(x instanceof Edge){
 this.edges.splice(Array.index(this.edges,x),1);}
 },
 node: function(id){
 if(id instanceof Node && id.graph==this)return id;return this.nodeset[id]|| null;},
 edge: function(id1,id2){
 if(id1 instanceof Node && id1.graph==this)id1=id1.id;if(id2 instanceof Node && id2.graph==this)id2=id2.id;return(this.nodeset[id1]&& this.nodeset[id2])? this.nodeset[id1].links.edge(id2): null;},
 paths: function(node1,node2,length,path){
 if(length===undefined)length=4;if(path===undefined)path=[];if(!(node1 instanceof Node))node1=this.nodeset(node1);if(!(node2 instanceof Node))node2=this.nodeset(node2);var p=[];var P=Graph.paths(this,node1.id,node2.id,length,path,true);for(var i=0;i < P.length;i++){
 var n=[];for(var j=0;j < P[i].length;j++){
 n.push(this.nodeset[P[i][j]]);}
 p.push(n);}
 return p;},
 shortestPath: function(node1,node2,a){
 if(!(node1 instanceof Node))node1=this.nodeset[node1];if(!(node2 instanceof Node))node2=this.nodeset[node2];try{
 var p=Graph.dijkstraShortestPath(this,node1.id,node2.id,a);var n=[];for(var i=0;i < p.length;i++){
 n.push(this.nodeset[p[i]]);}
 return n;}catch(e){
 return null;}
 },
 shortestPaths: function(node,a){
 if(!(node instanceof Node))node=this.nodeset[node];var p={};var P=Graph.dijkstraShortestPaths(this,node.id,a);for(var id in P){
 if(P[id]){
 var n=[];for(var i=0;i < P[id].length;i++){
 n.push(this.nodeset[P[id][i]]);}
 p[this.nodeset[id]]=n;}else{
 p[this.nodeset[id]]=null;}
 }
 },
 eigenvectorCentrality: function(graph,a){
 var ec=Graph.eigenvectorCentrality(this,a);var r={};for(var id in ec){
 var n=this.nodeset[id];n.weight=ec[id];r[n]=n.weight;}
 return r;},
 betweennessCentrality: function(graph,a){
 var bc=Graph.brandesBetweennessCentrality(this,a);var r={};for(var id in bc){
 var n=this.nodeset[id];n.centrality=bc[id];r[n]=n.centrality;}
 return r;},
 degreeCentrality: function(graph){
 var r={};for(var i=0;i < this.nodes.length;i++){
 var n=this.nodes[i];n.degree=n.links.length/this.nodes.length;r[n]=n.degree;}
 return r;},
 sorted: function(order,threshold){
 if(order===undefined)order=WEIGHT;if(threshold===undefined)threshold=0.0;var a=[];for(var i=0;i < this.nodes.length;i++){
 if(this.nodes[i][order]>=threshold){
 a.push([this.nodes[i][order],this.nodes[i]]);}
 }
 a=a.sort();a=a.reverse();for(var i=0;i < a.length;i++){
 a[i]=a[i][1];}
 return a;},
 prune: function(depth){
 if(depth===undefined)depth=0;var m={};for(i=0;i<this.nodes.length;i++){
 m[this.nodes[i].id]=0;}
 for(i=0;i<this.edges.length;i++){
 m[this.edges[i].node1.id]+=1;m[this.edges[i].node2.id]+=1;}
 for(id in m){
 if(m[id]<=depth){
 this.remove(this.nodeset[id]);}
 }
 },
 fringe: function(depth){
 if(depth===undefined)depth=0;var u=[];for(var i=0;i < this.nodes.length;i++){
 if(this.nodes[i].links.length==1){
 u.push.apply(u,this.nodes[i].flatten(depth));}
 }
 return Array.unique(u);},
 density: function(){
 return 2.0*this.edges.length/(this.nodes.length*(this.nodes.length-1));},
 split: function(){
 return Graph.partition(this);},
 update: function(iterations,weight,limit){
 if(iterations===undefined)iterations=2;for(var i=0;i < iterations;i++){
 this.layout.update(weight,limit);}
 },
 draw: function(weighted,directed){
 this._ctx.save();this._ctx.translate(this.canvas.width/2,this.canvas.height/2);for(var i=0;i < this.edges.length;i++){
 this.edges[i].draw(weighted,directed);}
 for(var i=0;i < this.nodes.length;i++){
 this.nodes[i].draw(weighted);}
 this._ctx.restore();},
 drag: function(mouse){
 var pt=null;if(mouse.pressed){
 pt=mouse.relative && mouse.relative(this.canvas)||{x: mouse.x,y: mouse.y};pt.x-=this.canvas.width/2;
 pt.y-=this.canvas.height/2;}
 if(mouse.pressed && !mouse.dragged){
 this.dragged=this.nodeAt(pt.x,pt.y);}
 if(!mouse.pressed){
 this.dragged=null;}
 if(this.dragged){
 this.dragged._x=pt.x/this.distance;this.dragged._y=pt.y/this.distance;this.layout.iterations=0;this._i=0;}
 },
 loop: function(a){
 if(a===undefined)a={};if(a.frames===undefined)a.frames=500;if(a.fps===undefined)a.fps=30;if(a.ipf===undefined)a.ipf=2;this._i=0;this._frames=a.frames;this._animation=setInterval(function(g){
 if(g._i < g._frames){
 g._ctx.clearRect(0,0,g.canvas.width,g.canvas.height);if(SHADOW){
 g._ctx.shadowColor="rgba(0,0,0,"+SHADOW+")";g._ctx.shadowBlur=8;g._ctx.shadowOffsetX=6;g._ctx.shadowOffsetY=6;}
 g.update(a.ipf);g.draw(a.weighted,a.directed);g._i+=1;}
 g.drag(g.mouse);},1000/a.fps,this);},
 stop: function(){
 clearInterval(this._animation);this._animation=null;},
 nodeAt: function(x,y){
 for(var i=0;i < this.nodes.length;i++){
 var n=this.nodes[i];if(n.contains(x,y)){
 return n;}
 }
 },
 _addNodeCopy: function(n,a){
 var args={
 radius: n.radius,
 fill: n.fill,
 stroke: n.stroke,
 strokewidth: n.strokewidth,
 text: n.text? n.text.style.color || true : false,
 font: n.text? n.text.style.fontFamily || null : null,
 fontsize: n.text? parseInt(n.text.style.fontSize)|| null : null,
 fontweight: n.text? n.text.style.fontWeight || null : null,
 css: n.text? n.text.className || null : null,
 root: a && a.root || false
 };var a=n.text? n.text.getElementsByTagName("a"): null;if(a && a.length > 0)args.href=a[0].href || null;this.addNode(n.id,args);},
 _addEdgeCopy: function(e,a){
 if(!((a && a["node1"]|| e.node1).id in this.nodeset)||
 !((a && a["node2"]|| e.node2).id in this.nodeset)){
 return;}
 this.addEdge(
 a && a["node1"]|| this.nodeset[e.node1.id],
 a && a["node2"]|| this.nodeset[e.node2.id],{
 weight: e.weight,
 length: e.length,
 type: e.type,
 stroke: e.stroke,
 strokewidth: e.strokewidth
 }
 );},
 copy: function(canvas,nodes){
 if(nodes===undefined)nodes=this.nodes;var g=new Graph(canvas,this.distance,null);g.layout=this.layout.copy(g);for(var i=0;i < nodes.length;i++){
 var n=nodes[i];if(!(n instanceof Node))n=this.nodeset[n];g._addNodeCopy(n,{root:this.root==n});}
 for(var i=0;i < this.edges.length;i++){
 var e=this.edges[i];g._addEdgeCopy(e);}
 return g;},
 clear: function(){
 if(this.canvas && this._ctx){
 this._ctx.clearRect(0,0,this.canvas.width,this.canvas.height);}
 for(var i=0;i < this.nodes.length;i++){
 var n=this.nodes[i];if(n.text && n.text.parentNode){
 n.text.parentNode.removeChild(n.text);n.text=null;}
 }
 this.nodeset={};this.nodes=[];this.edges=[];this.root=null;this.layout=null;this.canvas=null;}
});
GraphLayout=Class.extend({
 init: function(graph){
 this.graph=graph;this.iterations=0;},
 update: function(){
 this.iterations+=1;},
 reset: function(){
 this.iterations=0;for(var i=0;i < this.graph.nodes.length;i++){
 var n=this.graph.nodes[i];n._x=0;n._y=0;n._vx=0;n._vy=0;}
 },
 bounds: function(){
 var min={'x':+Infinity,'y':+Infinity}
 var max={'x':-Infinity,'y':-Infinity}
 for(var i=0;i < this.graph.nodes.length;i++){
 var n=this.graph.nodes[i];if(n._x < min.x)min.x=n._x;if(n._y < min.y)min.y=n._y;if(n._x > max.x)max.x=n._x;if(n._y > max.y)max.y=n._y;}
 return[min.x,min.y,max.x-min.x,max.y-min.y];},
 copy: function(graph){
 return new GraphLayout(graph);}
});
GraphSpringLayout=GraphLayout.extend({
 init: function(graph){
 this._super(graph);this.k=4.0;
 this.force=0.01;
 this.repulsion=50;
 },
 _distance: function(node1,node2){
 var dx=node2._x-node1._x;var dy=node2._y-node1._y;var d2=dx*dx+dy*dy;if(d2 < 0.01){
 dx=Math.random()*0.1+0.1;dy=Math.random()*0.1+0.1;d2=dx*dx+dy*dy;}
 return[dx,dy,Math.sqrt(d2),d2];},
 _repulse: function(node1,node2){
 var a=this._distance(node1,node2);dx=a[0];dy=a[1];d=a[2];d2=a[3];if(d < this.repulsion){
 var f=Math.pow(this.k,2)/d2;node2._vx+=f*dx;node2._vy+=f*dy;node1._vx-=f*dx;node1._vy-=f*dy;}
 },
 _attract: function(node1,node2,weight,length){
 var a=this._distance(node1,node2);dx=a[0];dy=a[1];d=a[2];d2=a[3];var d=Math.min(d,this.repulsion);var f=(d2-Math.pow(this.k,2))/this.k*length;f*=weight*0.5+1;f/=d;node2._vx-=f*dx;node2._vy-=f*dy;node1._vx+=f*dx;node1._vy+=f*dy;},
 update: function(weight,limit){
 if(weight===undefined)weight=10.0;if(limit===undefined)limit=0.5;
 this._super();
 for(var i=0;i < this.graph.nodes.length;i++){
 var n1=this.graph.nodes[i];for(var j=i+1;j < this.graph.nodes.length;j++){
 var n2=this.graph.nodes[j];this._repulse(n1,n2);}
 }
 for(var i=0;i < this.graph.edges.length;i++){
 var e=this.graph.edges[i];this._attract(e.node1,e.node2,weight*e.weight,1.0/(e.length||0.01));}
 for(var i=0;i < this.graph.nodes.length;i++){
 var n=this.graph.nodes[i];if(!n.fixed){
 n._x+=Math.max(-limit,Math.min(this.force*n._vx,limit));n._y+=Math.max(-limit,Math.min(this.force*n._vy,limit));n.x=n._x*n.graph.distance;n.y=n._y*n.graph.distance;}
 n._vx=0;n._vy=0;}
 },
 copy: function(graph){
 var g=new GraphSpringLayout(graph);g.k=this.k;g.force=this.force;g.repulsion=this.repulsion;return g;}
});
Graph.depthFirstSearch=function(node,a){
 if(a===undefined)a={};if(a.visit===undefined)a.visit=function(node){ return false;};if(a.traversable===undefined)a.traversable=function(node,edge){ return true;};var stop=visit(node);a._visited=a._visited ||{};a._visited[node.id]=true;for(var i=0;i < node.links.length;i++){
 var n=node.links[i];if(stop)return true;if(a.traversable(node,node.links.edge(n)==false))continue;if(!a._visited[n.id]){
 stop=Graph.depthFirstSearch(n,a);}
 }
 return stop;};
dfs=Graph.depthFirstSearch;
Graph.breadthFirstSearch=function(node,a){
 if(a===undefined)a={};if(a.visit===undefined)a.visit=function(node){ return false;};if(a.traversable===undefined)a.traversable=function(node,edge){ return true;};
 var q=[node];var _visited={};while(q.length > 0){
 node=q.splice(0,1)[0];if(!_visited[node.id]){
 if(a.visit(node))
 return true;for(var i=0;i < node.links.length;i++){
 var n=node.links[i];if(a.traversable(node,node.links.edge(n))!=false)q.push(n);}
 _visited[node.id]=true;}
 }
 return false;};
bfs=Graph.breadthFirstSearch;
Graph.paths=function(graph,id1,id2,length,path,_root){
 if(path.length >=length){
 return[];}
 if(!(id1 in graph.nodeset)){
 return[];}
 if(id1==id2){
 path=path.slice();path.push(id1);return[path];}
 path=path.slice();path.push(id1);var p=[];var n=graph.nodeset[id1].links;for(var i=0;i < n.length;i++){
 if(Array.index(path,n[i].id)< 0){
 p=p.push.apply(Graph.paths(graph,n[i].id,id2,length,path,false));}
 }
 if(_root !=false)p.sort(function(a,b){ return a.length-b.length;});return p;};
function edges(path){
 if(path && path.length > 1){
 var e=[];for(var i=0;i < path.length-1;i++){
 e.push(path[i].links.edge(path[i+1]));}
 return e;}
 return[];};
var Heap=Class.extend({
 init: function(){
 this.k=[];this.w=[];this.length=0;},
 push: function(key,weight){
 var i=0;while(i <=this.w.length && weight <(this.w[i]||Infinity))i++;this.k.splice(i,0,key);this.w.splice(i,0,weight);this.length+=1;return true;
 },
 pop: function(){
 this.length-=1;this.w.pop();return this.k.pop();}
});
Graph.adjacency=function(graph,a){
 if(a===undefined)a={};if(a.directed===undefined)a.directed=false;if(a.reversed===undefined)a.reversed=false;if(a.stochastic===undefined)a.stochastic=false;var map={};for(var i=0;i < graph.nodes.length;i++){
 map[graph.nodes[i].id]={};}
 for(var i=0;i < graph.edges.length;i++){
 var e=graph.edges[i];var id1=e[(a.reversed)?"node2":"node1"].id;var id2=e[(a.reversed)?"node1":"node2"].id;map[id1][id2]=1.0-e.weight*0.5;if(a.heuristic){
 map[id1][id2]+=a.heuristic(id1,id2);}
 if(!a.directed){
 map[id2][id1]=map[id1][id2];}
 }
 if(a.stochastic){
 for(var id1 in map){
 var n=Array.sum(Object.values(map[id1]));for(var id2 in map[id1]){
 map[id1][id2]/=n;}
 }
 }
 return map;};
Graph.dijkstraShortestPath=function(graph,id1,id2,a){
 function flatten(array){
 var a=[];for(var i=0;i < array.length;i++){
(array[i]instanceof Array)? a=a.concat(flatten(array[i])): a.push(array[i]);}
 return a;}
 var G=Graph.adjacency(graph,a);var q=new Heap();q.push([0,id1,[]],0);var visited={};for(;;){
 var x=q.pop();cost=x[0];n1=x[1];path=x[2];visited[n1]=true;if(n1==id2){
 var r=flatten(path);r.reverse();
 r.push(n1);return r;}
 var path=[n1,path];for(var n2 in G[n1]){
 if(!visited[n2]){
 q.push([cost+G[n1][n2],n2,path],cost+G[n1][n2]);}
 }
 }
};
Graph.dijkstraShortestPaths=function(graph,id,a){
 var W=Graph.adjacency(graph,a);var Q=new Heap();
 var D={};
 var P={};
 P[id]=[id];var seen={id: 0};Q.push([0,id],0);while(Q.length){
 var q=Q.pop();dist=q[0];v=q[1];if(v in D)continue;D[v]=dist;for(var w in W[v]){
 var vw_dist=D[v]+W[v][w];if(!(w in D)&&(!(w in seen)|| vw_dist < seen[w])){
 seen[w]=vw_dist;Q.push([vw_dist,w],vw_dist);P[w]=P[v].slice();P[w].push(w);}
 }
 }
 for(var n in graph.nodeset){
 if(!(n in P))P[n]=null;}
 return P;};
Graph.brandesBetweennessCentrality=function(graph,a){
 if(a===undefined)a={};if(a.normalized===undefined)a.normalized=true;if(a.directed===undefined)a.directed=false;var W=Graph.adjacency(graph,a);var b={};for(var n in graph.nodeset)b[n]=0.0;for(var id in graph.nodeset){
 var Q=new Heap();
 var D={};
 var P={};
 for(var n in graph.nodeset)P[n]=[];var seen={id: 0};Q.push([0,id,id],0);var S=[];var E={};for(var n in graph.nodeset)E[n]=0;
 E[id]=1.0;while(Q.length){
 var q=Q.pop();dist=q[0];pred=q[1];v=q[2];if(v in D)continue;D[v]=dist;S.push(v);E[v]+=E[pred];for(var w in W[v]){
 var vw_dist=D[v]+W[v][w];if(!(w in D)&&(!(w in seen)|| vw_dist < seen[w])){
 seen[w]=vw_dist;Q.push([vw_dist,v,w],vw_dist);P[w]=[v];E[w]=0.0;}else if(vw_dist==seen[w]){
 P[w].push(v);E[w]=E[w]+E[v];}
 }
 }
 var d={};for(var v in graph.nodeset)d[v]=0;while(S.length){
 var w=S.pop();for(var i=0;i < P[w].length;i++){
 v=P[w][i];d[v]+=(1+d[w])*E[v]/E[w];}
 if(w !=id){
 b[w]+=d[w];}
 }
 }
 var m=a.normalized? Math.max.apply(Math,Object.values(b))|| 1 : 1;for(var id in b)b[id]=b[id]/m;return b;};
Graph.eigenvectorCentrality=function(graph,a){
 if(a===undefined)a={};if(a.normalized===undefined)a.normalized=true;if(a.reversed===undefined)a.reversed=true;if(a.rating===undefined)a.rating={};if(a.iterations===undefined)a.iterations=100;if(a.tolerance===undefined)a.tolerance=0.0001;function normalize(vector){
 var w=1.0/(Array.sum(Object.values(vector))|| 1);for(var node in vector){
 vector[node]*=w;}
 }
 var G=Graph.adjacency(graph,a);var v={};for(var n in graph.nodeset)v[n]=Math.random();normalize(v);
 for(var i=0;i < a.iterations;i++){
 var v0=v
 var v={};for(var k in v0)v[k]=0;for(var n1 in v){
 for(var n2 in G[n1]){
 v[n1]+=0.01+v0[n2]*G[n1][n2]*(a.rating[n]? a.rating[n]: 1);}
 }
 normalize(v);var e=0;for(var n in v)e+=Math.abs(v[n]-v0[n]);
 if(e < graph.nodes.length*a.tolerance){
 var m=a.normalized? Math.max.apply(Math,Object.values(v))|| 1 : 1;for(var id in v)v[id]/=m;return v;}
 }
 if(window.console){
 console.warn("node weight is 0 because Graph.eigenvectorCentrality()did not converge.");}
 var x={};for(var n in graph.nodeset)x[n]=0;return x;};
Array.union=function(a,b){
 return Array.unique(a.concat(b));};
Array.intersection=function(a,b){
 var r=[],m={},i;for(i=0;i < b.length;i++)m[b[i]]=true;for(i=0;i < a.length;i++){
 if(a[i]in m)r.push(a[i]);
 }
 return r;};
Array.difference=function(a,b){
 var r=[],m={},i;for(i=0;i < b.length;i++)m[b[i]]=true;for(i=0;i < a.length;i++){
 if(!(a[i]in m))r.push(a[i]);}
 return r;};
Graph.partition=function(graph){
 var g=[];for(var i=0;i < graph.nodes.length;i++){
 var n=graph.nodes[i];n=n.flatten();var d={};for(var j=0;j < n.length;j++)d[n[j].id]=true;g.push(Object.keys(d));}
 for(var i=g.length-1;i >=0;i--){
 for(var j=g.length-1;j >=i+1;j--){
 if(g[i].length > 0 && g[j].length > 0 && Array.intersection(g[i],g[j]).length > 0){
 g[i]=Array.union(g[i],g[j]);g[j]=[];}
 }
 }
 for(var i=g.length-1;i >=0;i--){
 if(g[i].length==0)g.splice(i,1);}
 for(var i=0;i < g.length;i++){
 var n=[];for(var j=0;j < g[i].length;j++)n[j]=graph.nodeset[g[i][j]];g[i]=graph.copy(graph.canvas,nodes=n);}
 g.sort(function(a,b){ return b.length-a.length;});return g;};
Graph.isClique=function(graph){
 return(graph.density()==1.0);};
Graph.clique=function(graph,id){
 if(id instanceof Node){
 id=id.id;}
 var a=[id];for(var i=0;i < graph.nodes.length;i++){
 var n=graph.nodes[i];var b=true;for(var j=0;j < a.length;j++){
 if(n.id !=a[i].id && graph.edge(n.id,a[i].id)==null){
 b=false;break;}
 }
 if(b && n.id !=a[i].id){
 a.push(n.id);}
 return a;}
};
Graph.cliques=function(graph,threshold){
 if(threshold===undefined)threshold=3;var a=[];for(var i=0;i < graph.nodes.length;i++){
 var n=graph.nodes[i];var c=Graph.clique(graph,n.id);if(c.length >=threshold){
 c.sort();if(Array.index(a,c)< 0){
 a.push(c);}
 }
 }
};
Graph.unlink=function(graph,node1,node2){
 if(!(node1 instanceof Node))node1=graph.nodeset[node1];if(!(node2 instanceof Node))node2=graph.nodeset[node2];var e=graph.edges.slice();for(var i=0;i < e.length;i++){
 if((node1==e[i].node1 || node1==e[i].node2)&&
(node2==e[i].node1 || node2==e[i].node2 || node2===undefined)){
 graph.edges.splice(Array.index(graph.edges,e[i]),1);}
 try{
 node1.links.remove(Array.index(node1.links,node2),1);node2.links.remove(Array.index(node2.links,node1),1);}catch(x){
 }
 }
};
Graph.redirect=function(graph,node1,node2){
 if(!(node1 instanceof Node))node1=graph.nodeset[node1];if(!(node2 instanceof Node))node2=graph.nodeset[node2];for(var i=0;i < graph.edges.length;i++){
 var e=graph.edges[i];if(node1==e.node1 || node1==e.node2){
 if(e.node1==node1 && e.node2 !=node2){
 graph._addEdgeCopy(e,node2,e.node2);}
 if(e.node2==node1 && e.node1 !=node2){
 graph._addEdgeCopy(e,e.node1,node2);}
 }
 }
 Graph.unlink(graph,node1);};
Graph.cut=function(graph,node){
 if(!(node instanceof Node))node=graph.nodeset[node];for(var i=0;i < graph.edges.length;i++){
 var e=graph.edges[i];if(node==e.node1 || node==e.node2){
 for(var j=0;j < node.links.length;j++){
 var n=node.links[j];if(e.node1==node && e.node2 !=n){
 graph._addEdgeCopy(e,n,e.node2);}
 if(e.node2==node && e.node1 !=n){
 graph._addEdgeCopy(e,e.node1,n);}
 }
 }
 }
 Graph.unlink(graph,node);};
Graph.insert=function(graph,node,a,b){
 if(!(node instanceof Node))node=graph.nodeset[node];if(!(a instanceof Node))a=graph.nodeset[a];if(!(b instanceof Node))b=graph.nodeset[b];for(var i=0;i < graph.edges.length;i++){
 var e=graph.edges[i];if(e.node1==a && e.node2==b){
 graph._addEdgeCopy(e,a,node);graph._addEdgeCopy(e,node,b);}
 if(e.node1==b && e.node2==a){
 grapg._addEdgeCopy(e,b,node);graph._addEdgeCopy(e,node,a);}
 }
 Graph.unlink(graph,a,b);};