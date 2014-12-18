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
			// 			ctx = canvas.getContext('2d'),
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
			// 		ctx.fillStyle = colorList[Math.floor(Math.random() * colorList.length)];
			// 		tmpCanvasSurface = ctx.getImageData(0, 0, canvas.width, canvas.height);

			// 		// 画线
			// 		// 规则：
			// 		//	每一个点用线连接，然后填充
			// 		function drawLines(coordinateList) {
			// 			ctx.beginPath();
			// 			for(var i in coordinateList) {
			// 				if(i == 0) {
			// 					ctx.moveTo(coordinateList[i].x, coordinateList[i].y);
			// 				} else {
			// 					ctx.lineTo(coordinateList[i].x, coordinateList[i].y);
			// 				}
			// 				ctx.stroke();
			// 			}
			// 			ctx.lineTo(coordinateList[0].x, coordinateList[0].y);
			// 			ctx.closePath();
			// 			ctx.stroke();
			// 			ctx.fill();
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
				ctx: null,
				canvasBg: new Image(),
				offsetX: 0, // canvas 的offset
				offsetY: 0,
				colorList: ['red', 'green', 'blue', 'gray', 'black', 'yellow', 'orange'],
				canvasSurface: null, // 取每一个pointList之前保存的canvas画布
				pointList: [],

				// para: 
				//		canvasContainer: canvas的容器，DOM对象
				init: function(canvasContainer, canvasEle, canvasBg, cb) {
					// init var
					var that = this;
					this.canvas = canvasEle;
					this.ctx = this.canvas.getContext('2d');
					this._w = $(canvasContainer).width()
					this.offsetX = this.canvas.offsetLeft;
					this.offsetY = this.canvas.offsetTop;

					// init canvas
					var imgBg = new Image();

					imgBg.addEventListener('load', function() {
						var imgW, imgH;

						imgW = imgBg.width;
						imgH = imgBg.height;
						that.canvas.style.backgroundImage = 'url(' + imgBg.src + ')';
						that.canvas.style.backgroundSize = '100% auto';
						that.canvas.width = that._w;
						that.canvas.height = that._h = imgH / imgW * that._w;
						that.ctx.fillStyle = that.colorList[Math.floor(Math.random() * that.colorList.length)];
						that.canvasSurface = that.ctx.getImageData(0, 0, that._w, that._h);

						initComplete = true;

						if(cb) {
							cb();
						}
					});

					imgBg.src = canvasBg
				},
				getPoint: function (e) { // 获取当前点的坐标，e为事件event对象
					var x = e.offsetX,
						y = e.offsetY;
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
				getPointList: function() {
					return this.pointList;
				},
				clearPointList: function() {
					this.pointList = [];
				},
				drawLines: function() {
					var ctx = this.ctx,
						pointList = this.pointList;

					if(pointList.length < 2) {
						return false;
					}

					ctx.beginPath();
					for(var i in pointList) {
						if(i == 0) {
							ctx.moveTo(pointList[i].x, pointList[i].y);
						} else {
							ctx.lineTo(pointList[i].x, pointList[i].y);
						}
						ctx.stroke();
					}
					ctx.lineTo(pointList[0].x, pointList[0].y);
					ctx.closePath();
					ctx.stroke();
					ctx.fill();
				},
				drawPlan: function() {
					this.ctx.putImageData(this.canvasSurface, 0, 0);

					this.drawLines();
					this.canvasSurface = this.ctx.getImageData(0, 0, this._w, this._h);
				},
				drawTmpPlan: function(e) {
					this.addPoint(e);
					this.ctx.putImageData(this.canvasSurface, 0, 0);

					this.drawLines();
					this.delPoint();
				},
				resetCanvas: function(cb) {
					this.ctx.clearRect(0, 0, this._w, this._h);
					this.canvasSurface = this.ctx.getImageData(0, 0, this._w, this._h);
					this.pointList = [];

					if(cb) {
						cb();
					}
				}


			};

			var canvasContainer = document.getElementById('contentContainer'),
				canvas = document.getElementById('canvas'),
				canvasBg = 'http://3.im.guokr.com/ubm_3Qr4e8OTd_dIw1ihmaSvUNRLPRcKxDnkPVX2DRqvAwAAZgIAAEpQ.jpg',
				planInfo = {};

			buildingInit();
			$('#nextBtn').click(function() {
				console.log($(this).data('operation'));
				console.log($(this).attr('data-operation'));
				switch($(this).attr('data-operation')) {
					case 'shop':
						shopInit();
						break;
					case 'white':
						whiteInit();
						break;
					case 'icon':
						iconInit();
						break;
				}
			});

			// 取建筑轮廓信息
			function buildingInit() {
				$('#nextBtn').attr('data-operation', 'white');
				planCanvas.init(canvasContainer, canvas, canvasBg, function() {
					// canvas取点处理
					alert('请选取基准零点坐标');
					var isFirstPoint = true;
					canvas.onclick = function(e) {
						if(isFirstPoint) {
							var point = planCanvas.getPoint(e);

							if(!planInfo['canvas']) {
								var r = confirm('确认选择(' + point.x + ',' + point.y + ')点作为基准零点？');

								if(r) {
									planInfo.canvas = {};
									planInfo.canvas.startPoint = {
										x: point.x,
										y: point.y
									};
								} else {
									alert('请重新选择基准点坐标');
								}
								return;
							}
						}

						planCanvas.addPoint(e);
					};
					document.getElementById('drawBtn').onclick = function(e) {
						var pointList = planCanvas.getPointList();
						planCanvas.drawPlan();
						planCanvas.clearPointList();

						if(!planInfo['bg']) {
							planInfo.bg = [];
						}
						planInfo.bg.push(pointList);

						if(!planInfo.canvas.width || !planInfo.canvas.height) {
							planInfo.canvas.width = planCanvas._w;
							planInfo.canvas.height = planCanvas._h;
						}
						console.log(planInfo)
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
					};
				});
			}

			// 取空地信息
			function whiteInit() {
				$('#nextBtn').attr('data-operation', 'shop');
				planCanvas.resetCanvas(function() {
					// canvas取点处理
					canvas.onclick = function(e) {
						planCanvas.addPoint(e);
					};
					document.getElementById('drawBtn').onclick = function(e) {
						var pointList = planCanvas.getPointList();
						planCanvas.drawPlan();
						planCanvas.clearPointList();

						if(!planInfo['white']) {
							planInfo['white'] = [];
						}
						planInfo.white.push(pointList);
						console.log(planInfo)
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
					};
				});
			}

			// 取店铺信息
			function shopInit() {
				$('#nextBtn').attr('data-operation', 'icon');
				planCanvas.resetCanvas(function() {
					// canvas取点处理
					canvas.onclick = function(e) {
						planCanvas.addPoint(e);
					};
					document.getElementById('drawBtn').onclick = function(e) {
						var pointList = planCanvas.getPointList();
						planCanvas.drawPlan();
						planCanvas.clearPointList();

						if(!planInfo['shop']) {
							planInfo['shop'] = [];
						}
						planInfo.shop.push(pointList);
						console.log(planInfo)
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
					};
				});
			}
        });
    }
})
