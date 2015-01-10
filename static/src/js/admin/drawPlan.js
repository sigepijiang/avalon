// drawPlan.js

Module('drawPlan', function(){
    this.run = function(){
        $(function() {
			//(function(bodyStyle) {
			// 	var _w = $('#contentContainer').width(),
			// 		_h,
			// 		imgBg = new Image(),
			// 		imgW, imgH;

			// 	imgBg.src = 'http://3.im.guokr.com/ubm_3Qr4e8OTd_dIw1ihmaSvUNRLPRcKxDnkPVX2DRqvAwAAZgIAAEpQ.jpg';

			// 	imgBg.addEventListener('load', function() {
			// 		var canvas = document.getElementById('canvas'),
			// 			cxt = canvas.getContext('2d'),
			// 			colorList = ['red', 'green', 'blue', 'gray', 'black', 'yellow', 'orange'],
			// 			offsetX = canvas.offsetLeft,
			// 			offsetY = canvas.offsetTop,
			// 			tmpCanvasSurface,
			// 			svgStr = '',
			// 			svgDataList = [];

			// 		// 创建一个和图片一样大小比例的canvas,初始化canvas
			// 		imgW = imgBg.width;
			// 		imgH = imgBg.height;
			// 		canvas.style.backgroundImage = 'url(' + imgBg.src + ')';
			// 		canvas.style.backgroundSize = '100% auto';
			// 		canvas.width = _w;
			// 		canvas.height = imgH / imgW * _w;
			// 		cxt.fillStyle = colorList[Math.floor(Math.random() * colorList.length)];
			// 		tmpCanvasSurface = cxt.getImageData(0, 0, canvas.width, canvas.height);

			// 		// 画线
			// 		// 规则：
			// 		//	每一个点用线连接，然后填充
			// 		function drawLines(coordinateList) {
			// 			cxt.beginPath();
			// 			for(var i in coordinateList) {
			// 				if(i == 0) {
			// 					cxt.moveTo(coordinateList[i].x, coordinateList[i].y);
			// 				} else {
			// 					cxt.lineTo(coordinateList[i].x, coordinateList[i].y);
			// 				}
			// 				cxt.stroke();
			// 			}
			// 			cxt.lineTo(coordinateList[0].x, coordinateList[0].y);
			// 			cxt.closePath();
			// 			cxt.stroke();
			// 			cxt.fill();
			// 		}

			// 		// 获取确定的坐标链表
			// 		function getList() {
			// 			var $planCoordinate = document.getElementById('planCoordinate'),
			// 				coordinateStr = $planCoordinate.value,
			// 				coordinateList,
			// 				tmpStr;

			// 			if(coordinateStr.length) {
			// 				coordinateList = coordinateStr.split('\n');
			// 			} else {
			// 				coordinateList = [];
			// 				return coordinateList;
			// 			}

			// 			for(var i in coordinateList) {
			// 				tmpStr = coordinateList[i];

			// 				coordinateList[i] = {
			// 					x: tmpStr.split(',')[0],
			// 					y: tmpStr.split(',')[1]
			// 				}
			// 			}

			// 			return coordinateList;
			// 		}
			// 		// 删除正在上一条记录
			// 		function delData() {
			// 			var $planCoordinate = document.getElementById('planCoordinate'),
			// 				coordinateStr = $planCoordinate.value,
			// 				coordinateList,
			// 				tmpStr;

			// 			if(coordinateStr.length) {
			// 				coordinateList = coordinateStr.split('\n');
			// 			} else {
			// 				coordinateList = [];
			// 			}

			// 			if(coordinateList.length == 1) {
			// 				$planCoordinate.value = '';
			// 			} else {
			// 				for(var i in coordinateList) {
			// 					tmpStr = coordinateList[i];

			// 					if(i == 0) {
			// 						$planCoordinate.value = tmpStr;
			// 					} else if(i == coordinateList.length - 1) {
			// 						return;
			// 					} else {
			// 						$planCoordinate.value += '\n' + tmpStr;
			// 					}
			// 				}
			// 			}
			// 		}

			// 		// 获取当前点的坐标，e为事件event对象
			// 		function getPoint(e) {
			// 			var x = e.offsetX,
			// 				y = e.offsetY;
			// 			return {
			// 				x: x,
			// 				y: y
			// 			}
			// 		}

			// 		// 转换为SVG格式
			// 		function toSVG(coordinateList) {
			// 			for(var i in coordinateList) {
			// 				if(i == 0) {
			// 					svgStr = 'M' + coordinateList[i].x + ',' + coordinateList[i].y;
			// 				} else {
			// 					svgStr += 'L' + coordinateList[i].x + ',' + coordinateList[i].y;
			// 				}
			// 			}

			// 			svgStr += 'z';
			// 			return svgStr;
			// 		}

			// 		// 画平面图
			// 		function drawPlan(coordinateList) {
			// 			if(coordinateList.length) {
			// 				drawLines(coordinateList);
			// 			}
			// 		}

			// 		// 获取辅助线的列表，并画辅助线
			// 		function drawTmpPlan(coordinateList) {
			// 			if(coordinateList.length) {
			// 				if(coordinateList.length > 2) {
			// 					drawLines(coordinateList);
			// 				}
			// 			}
			// 		}


			// 		
			// })(document.body.style);

			var planCanvas = {
				initComplete: false,
				_w: 0, // canvas width
				_h: 0, // canvas height
				canvas: null,
				cxt: null,
				canvasBg: new Image(),
				offsetX: 0, // canvas 的offset
				offsetY: 0,
				colorList: ['red', 'green', 'blue', 'gray', 'black', 'yellow', 'orange'],
				canvasSurface: null, // 取每一个pointList之前保存的canvas画布
				pointList: [],

				// para:
				//		canvasContainer: canvas的容器，DOM对象
				//		canvasH没有用，图片还是会等比大小的
				init: function(canvasContainer, canvasEle, canvasBg, canvasW, canvasH, cb) {
					// init var
					var that = this;
					this.canvas = canvasEle;
					this.cxt = this.canvas.getContext('2d');
					this._w = canvasW !== 0 ? canvasW : $(canvasContainer).width();

					// init canvas
					var imgBg = new Image();

					imgBg.addEventListener('load', function() {
						that.offsetX = that.canvas.offsetLeft;
						that.offsetY = that.canvas.offsetTop;

						var imgW, imgH;

						imgW = imgBg.width;
						imgH = imgBg.height;
						that.canvas.style.backgroundImage = 'url(' + imgBg.src + ')';
						that.canvas.style.backgroundSize = '100% auto';
						that.canvas.width = that._w;
						that.canvas.height = that._h = imgH / imgW * that._w;
						that.cxt.fillStyle = that.colorList[Math.floor(Math.random() * that.colorList.length)];
						that.cxt.font = "32pt Arial";
						that.canvasSurface = that.cxt.getImageData(0, 0, that._w, that._h);

						initComplete = true;

						if(cb) {
							cb();
						}
					});

					$(window).resize(function() {
						that.offsetX = that.canvas.offsetLeft;
						that.offsetY = that.canvas.offsetTop;
					});

					imgBg.src = canvasBg
				},
				getPoint: function (e) { // 获取当前点的坐标，e为事件event对象
					var x = (e.clientX + document.body.scrollLeft || e.pageX) - this.offsetX || 0,
						y = (e.clientY + document.body.scrollTop || e.pageY) - this.offsetY || 0;
					return {
						x: x,
						y: y
					}
				},
				delPoint: function() { // 删除上一个点
					if(this.pointList.length) {
						this.pointList.pop();
					}
				},
				addPoint: function(e) {
					var curPos = this.getPoint(e);

					this.pointList.push(curPos);
				},
				addPointToPointList: function(x, y) {
					this.pointList.push({
						x: x,
						y: y
					})
				},
				getPointList: function() {
					return this.pointList;
				},
				clearPointList: function() {
					this.pointList = [];
				},
				drawPoints: function() { // 用于画icon
					var cxt = this.cxt,
						pointList = this.pointList;

					// cxt.putImageData(this.canvasSurface, 0, 0);
					for(var i in pointList) {
						cxt.beginPath();
						cxt.arc(pointList[i].x , pointList[i].y, 15, 0, Math.PI*2, true);
						cxt.fill();

						this.drawIndex(pointList[i].x , pointList[i].y, i);
					}
				},
				drawLines: function() {
					var cxt = this.cxt,
						pointList = this.pointList;

					if(pointList.length < 2) {
						return false;
					}

					cxt.beginPath();
					for(var i in pointList) {
						if(i == 0) {
							cxt.moveTo(pointList[i].x, pointList[i].y);
						} else {
							cxt.lineTo(pointList[i].x, pointList[i].y);
						}
						cxt.stroke();
					}
					cxt.lineTo(pointList[0].x, pointList[0].y);
					cxt.closePath();
					cxt.stroke();
					cxt.fill();
				},
				drawIndex: function(x, y, index) {
					var cxt = this.cxt;

					cxt.beginPath();
					cxt.save();
					cxt.fillStyle = 'white';
					cxt.fillText(index, x, y + 32);
					cxt.fill();
					cxt.stroke();
					cxt.restore();

					this.canvasSurface = this.cxt.getImageData(0, 0, this._w, this._h);
				},
				drawPlan: function() {
					this.cxt.putImageData(this.canvasSurface, 0, 0);

					this.drawLines();
					this.clearPointList();
					this.canvasSurface = this.cxt.getImageData(0, 0, this._w, this._h);
				},
				drawTmpPlan: function(e) {
					this.addPoint(e);
					this.cxt.putImageData(this.canvasSurface, 0, 0);

					this.drawLines();
					this.delPoint();
				},
				resetCanvas: function(cb) {
					this.cxt.clearRect(0, 0, this._w, this._h);
					this.canvasSurface = this.cxt.getImageData(0, 0, this._w, this._h);
					this.clearPointList();

					if(cb) {
						cb();
					}
				}


			};

			var utils = {
				/*
				* 检测对象是否是空对象(不包含任何可读属性)。
				* 方法只既检测对象本身的属性，不检测从原型继承的属性。
				*/
				isOwnEmpty: function(obj)
				{
					for(var name in obj)
					{
						if(obj.hasOwnProperty(name))
						{
							return false;
						}
					}
					return true;
				}
			}

			var canvasContainer = document.getElementById('contentContainer'),
				canvas = document.getElementById('canvas'),
				canvasBg = 'http://3.im.guokr.com/ubm_3Qr4e8OTd_dIw1ihmaSvUNRLPRcKxDnkPVX2DRqvAwAAZgIAAEpQ.jpg',
				planInfo = !utils.isOwnEmpty(layout) && layout.layout ? layout.layout : {},
				isInit = true;
console.log(planInfo)
			buildingInit();
			$('a[data-operation]').click(function() {
				switch($(this).attr('data-operation')) {
					case 'bg':
						buildingInit();
						break;
					case 'shop':
						shopInit();
						break;
					case 'white':
						whiteInit();
						break;
					case 'icon':
						iconInit();
						break;
					default:
						iconInit();
				}
			});

			$('#saveBtn').click(function() {
				$.ajax({
					url: '/apis/apollo/market/floor.json',
					method: 'post',
					contentType: 'application/json',
					data: JSON.stringify({
						floor_id: floor_id,
						layout: planInfo
					}),
					success: function(d) {

					},
					error: function(d) {

					},
					dataType: 'json'
				})
			});

			function buildPointList(list) {
				$('#pointList').html('');
				for(var index in list) {
					$('#pointList').prepend('<li>' + list[index].x + ',' + list[index].y + '</li>');
				}
			}

			// 重画该层图形
			// 用于重画building，white，shop；
			// icon单独有重画的方法
			function redraw(list) {
				planCanvas.resetCanvas();
				var point;
				for(var i in list) {
					planCanvas.clearPointList();
					for(var j in list[i]) {
						point = list[i][j];
						planCanvas.addPointToPointList(point.x, point.y);
					}
					planCanvas.drawPlan();
					planCanvas.drawIndex(list[i][0].x, list[i][0].y, i);
				}
				updateDelOption(list.length);
			}

			// 把画icon的index的方法放在了drawPoints里边
			// icon比较特殊，一个点就代表一个block
			function redrawIcon(list) {
				planCanvas.resetCanvas();
				var point;
				for(var i in list) {
					point = list[i];
					planCanvas.addPointToPointList(point.x, point.y);
				}

				planCanvas.drawPoints();
				updateDelOption(list.length);
			}

			// 更新删除的下来菜单
			function updateDelOption(length) {
				var optionHtml = '';

				for(var i = 0; i < length; i++) {
					optionHtml += '<option value="' + i + '">' + i + '</option>';
				}
				$('#delOption').html(optionHtml);
			}

			// 取建筑轮廓信息
			function buildingInit() {
				var canvasW = planInfo.canvas && planInfo.canvas.width ? planInfo.canvas.width : 0,
					canvasH = planInfo.canvas && planInfo.canvas.height ? planInfo.canvas.height : 0;

				$('#nextBtn').attr('data-operation', 'white');
				$('a[data-operation="bg"]').addClass('active').siblings().removeClass('active');
				if(isInit) {
					planCanvas.init(canvasContainer, canvas, canvasBg, canvasW, canvasH, buildingCb);
					isInit = false;
				} else {
					planCanvas.resetCanvas(buildingCb);
				}

				function buildingCb() {
					// canvas取点处理
					if(!planInfo.canvas || !planInfo.canvas.startPoint) {
						alert('请选取基准零点坐标');
					}
					canvas.onclick = function(e) {
						if(!planInfo['canvas']) {
							planInfo.canvas = {};

							var point = planCanvas.getPoint(e);
							var r = confirm('确认选择(' + point.x + ',' + point.y + ')点作为基准零点？');

							if(r) {
								planInfo.canvas.startPoint = {
									x: point.x,
									y: point.y
								};

								if(!planInfo.canvas.width || !planInfo.canvas.height) {
									planInfo.canvas.width = planCanvas._w;
									planInfo.canvas.height = planCanvas._h;
								}
							} else {
								alert('请重新选择基准点坐标');
							}
							return;
						}

						planCanvas.addPoint(e);
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('drawBtn').onclick = function(e) {
						var pointList = planCanvas.getPointList();
						planCanvas.drawPlan();

						if(!planInfo['bg']) {
							planInfo.bg = [];
						}
						planInfo.bg.push(pointList);
						planCanvas.drawIndex(pointList[0].x, pointList[0].y, planInfo.bg.length - 1);
						updateDelOption(planInfo.bg.length);
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('delBlockBtn').onclick = function(e) {
						var index = $('#delOption').val();

						if(index) {
							var r = confirm('确定要删除模块' + index + '?');
							if(r) {
								planInfo.bg.splice(index, 1);
								redraw(planInfo.bg);
								updateDelOption(planInfo.bg.length);
							}
						}
					}

					// 初始化已有数据
					if(planInfo.bg && planInfo.bg.length) {
						redraw(planInfo.bg);
					}
				}
			}

			// 取空地信息
			function whiteInit() {
				$('#nextBtn').attr('data-operation', 'shop');
				$('a[data-operation="white"]').addClass('active').siblings().removeClass('active');
				planCanvas.resetCanvas(function() {
					// canvas取点处理
					canvas.onclick = function(e) {
						planCanvas.addPoint(e);
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('drawBtn').onclick = function(e) {
						var pointList = planCanvas.getPointList();
						planCanvas.drawPlan();

						if(!planInfo['white']) {
							planInfo['white'] = [];
						}
						planInfo.white.push(pointList);
						planCanvas.drawIndex(pointList[0].x, pointList[0].y, planInfo.white.length - 1);
						updateDelOption(planInfo.white.length);
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('delBlockBtn').onclick = function(e) {
						var index = $('#delOption').val();

						if(index) {
							var r = confirm('确定要删除模块' + index + '?');
							if(r) {
								planInfo.white.splice(index, 1);
								redraw(planInfo.white);
								updateDelOption(planInfo.white.length);
							}
						}
					}
				});

				// 初始化已有数据
				if(planInfo.white && planInfo.white.length) {
					redraw(planInfo.white);
				}
			}

			// 取店铺信息
			function shopInit() {
				$('#nextBtn').attr('data-operation', 'icon');
				$('a[data-operation="shop"]').addClass('active').siblings().removeClass('active');
				planCanvas.resetCanvas(function() {
					// canvas取点处理
					canvas.onclick = function(e) {
						planCanvas.addPoint(e);
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('drawBtn').onclick = function(e) {
						var pointList = planCanvas.getPointList();
						planCanvas.drawPlan();

						if(!planInfo['shop']) {
							planInfo['shop'] = [];
						}
						planInfo.shop.push(pointList);
						planCanvas.drawIndex(pointList[0].x, pointList[0].y, planInfo.shop.length - 1);
						updateDelOption(planInfo.shop.length);
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('delBlockBtn').onclick = function(e) {
						var index = $('#delOption').val();

						if(index) {
							var r = confirm('确定要删除模块' + index + '?');
							if(r) {
								planInfo.shop.splice(index, 1);
								redraw(planInfo.shop);
								updateDelOption(planInfo.shop.length);
							}
						}
					}
				});

				// 初始化已有数据
				if(planInfo.shop && planInfo.shop.length) {
					redraw(planInfo.shop);
				}
			}

			// 取Icon信息
			function iconInit() {
				$('#nextBtn').attr('data-operation', 'over');
				$('a[data-operation="icon"]').addClass('active').siblings().removeClass('active');
				planCanvas.resetCanvas(function() {
					// canvas取点处理
					canvas.onclick = function(e) {
						planCanvas.addPoint(e);
						buildPointList(planCanvas.getPointList());
						planCanvas.drawPoints();
					};
					document.getElementById('drawBtn').onclick = function(e) {
						var pointList = planCanvas.getPointList();

						if(!planInfo['icon']) {
							planInfo['icon'] = [];
						}
						planInfo.icon = pointList;
						planCanvas.drawIndex(pointList[0].x, pointList[0].y, planInfo.icon.length - 1);
						updateDelOption(planInfo.icon.length);
					};
					canvas.onmousemove = function(e) {
						planCanvas.addPoint(e);
						planCanvas.drawPoints();
						planCanvas.delPoint();
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('delBlockBtn').onclick = function(e) {
						var index = $('#delOption').val();

						if(index) {
							var r = confirm('确定要删除模块' + index + '?');
							if(r) {
								planInfo.icon.splice(index, 1);
								redrawIcon(planInfo.icon);
								updateDelOption(planInfo.icon.length);
							}
						}
					}
				});
				// 初始化已有数据
				if(planInfo.icon && planInfo.icon.length) {
					redrawIcon(planInfo.icon);
				}
			}
        });
    }
})
