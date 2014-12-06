// drawPlan.js

Module('drawPlan', function(){
    this.run = function(){
        $(function() {
            (function(bodyStyle) {
				var _w = $('#contentContainer').width(),
					_h,
					imgBg = new Image(),
					imgW, imgH;

				imgBg.src = 'http://3.im.guokr.com/ubm_3Qr4e8OTd_dIw1ihmaSvUNRLPRcKxDnkPVX2DRqvAwAAZgIAAEpQ.jpg';

				imgBg.addEventListener('load', function() {
					var canvas = document.getElementById('canvas'),
						ctx = canvas.getContext('2d'),
						colorList = ['red', 'green', 'blue', 'gray', 'black', 'yellow', 'orange'],
						offsetX = canvas.offsetLeft,
						offsetY = canvas.offsetTop,
						tmpCanvasSurface,
						svgStr = '',
						svgDataList = [];

					// 创建一个和图片一样大小比例的canvas,初始化canvas
					imgW = imgBg.width;
					imgH = imgBg.height;
					canvas.style.backgroundImage = 'url(' + imgBg.src + ')';
					canvas.style.backgroundSize = '100% auto';
					canvas.width = _w;
					canvas.height = imgH / imgW * _w;
					ctx.fillStyle = colorList[Math.floor(Math.random() * colorList.length)];
					tmpCanvasSurface = ctx.getImageData(0, 0, canvas.width, canvas.height);

					// 画线
					// 规则：
					//	1.第一个元素为'rect'
					//	2.每一个点用线连接，然后填充
					function drawLines(coordinateList) {
						ctx.beginPath();
						for(var i in coordinateList) {
							if(i == 0) {
								ctx.moveTo(coordinateList[i].x, coordinateList[i].y);
							} else {
								ctx.lineTo(coordinateList[i].x, coordinateList[i].y);
							}
							ctx.stroke();
						}
						ctx.lineTo(coordinateList[0].x, coordinateList[0].y);
						ctx.closePath();
						ctx.stroke();
						ctx.fill();
					}

					// 获取确定的坐标链表
					function getList() {
						var $planCoordinate = document.getElementById('planCoordinate'),
							coordinateStr = $planCoordinate.value,
							coordinateList,
							tmpStr;

						if(coordinateStr.length) {
							coordinateList = coordinateStr.split(' ');
						} else {
							coordinateList = [];
							return coordinateList;
						}

						for(var i in coordinateList) {
							tmpStr = coordinateList[i];

							coordinateList[i] = {
								x: tmpStr.split(',')[0],
								y: tmpStr.split(',')[1]
							}
						}

						return coordinateList;
					}
					// 删除正在上一条记录
					function delData() {
						var $planCoordinate = document.getElementById('planCoordinate'),
							coordinateStr = $planCoordinate.value,
							coordinateList,
							tmpStr;

						if(coordinateStr.length) {
							coordinateList = coordinateStr.split(' ');
						} else {
							coordinateList = [];
						}

						if(coordinateList.length == 1) {
							$planCoordinate.value = '';
						} else {
							for(var i in coordinateList) {
								tmpStr = coordinateList[i];

								if(i == 0) {
									$planCoordinate.value = tmpStr;
								} else if(i == coordinateList.length - 1) {
									return;
								} else {
									$planCoordinate.value += ' ' + tmpStr;
								}
							}
						}
					}

					// 获取当前点的坐标，e为事件event对象
					function getPoint(e) {
						var x = e.offsetX,
							y = e.offsetY;
						return {
							x: x,
							y: y
						}
					}

					// 转换为SVG格式
					function toSVG(coordinateList) {
						for(var i in coordinateList) {
							if(i == 0) {
								svgStr = 'M' + coordinateList[i].x + ',' + coordinateList[i].y;
							} else {
								svgStr += 'L' + coordinateList[i].x + ',' + coordinateList[i].y;
							}
						}

						svgStr += 'z';
						return svgStr;
					}

					// 画平面图
					function drawPlan(coordinateList) {
						if(coordinateList.length) {
							drawLines(coordinateList);
						}
					}

					// 获取辅助线的列表，并画辅助线
					function drawTmpPlan(coordinateList) {
						if(coordinateList.length) {
							if(coordinateList.length > 2) {
								drawLines(coordinateList);
							}
						}
					}


					document.getElementById('drawBtn').onclick = function() {
						ctx.putImageData(tmpCanvasSurface, 0, 0);

						var list = getList();
						drawPlan(list);
						document.getElementById('planCoordinate').value = '';

						ctx.fillStyle = colorList[Math.floor(Math.random() * colorList.length)];
						tmpCanvasSurface = ctx.getImageData(0, 0, canvas.width, canvas.height);

						// 存储svg信息
						svgDataList.push(toSVG(list));
						document.getElementById('svgList').childNodes[0].nodeValue = svgDataList;
	console.log(toSVG(list));
					};
					document.getElementById('delBtn').onclick = delData;
					canvas.onclick = function(e) {
						var curPos = getPoint(e),
							planValue = document.getElementById('planCoordinate').value;

						if(planValue.length) {
							document.getElementById('planCoordinate').value += ' ' + curPos.x + ',' + curPos.y;
						} else {
							document.getElementById('planCoordinate').value = curPos.x + ',' + curPos.y;
						}
					};
					canvas.addEventListener('mousemove', function(e) {
						ctx.putImageData(tmpCanvasSurface, 0, 0);

						var list = getList(),
							tmpObg = getPoint(e);

						list.push(tmpObg);
						drawTmpPlan(list);
					});
				});
			})(document.body.style);
        });
    }
})
