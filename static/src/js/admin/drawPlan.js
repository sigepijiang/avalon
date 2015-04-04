// drawPlan.js

Module('drawPlan', function(){
    this.run = function(){
        $(function() {
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
					this._w = canvasW ? canvasW : $(canvasContainer).width();

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

					imgBg.src = canvasBg;
				},
				getPoint: function (e) { // 获取当前点的坐标，e为事件event对象
					var x = (e.clientX + document.body.scrollLeft || e.pageX) - this.offsetX || 0,
						y = (e.clientY + document.body.scrollTop || e.pageY) - this.offsetY || 0;
					return {
						x: x,
						y: y
					};
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
					});
				},
				getPointList: function() {
					return this.pointList;
				},
				clearPointList: function() {
					this.pointList = [];
				},
				drawPoints: function(pointObj) { // 用于画icon
					var cxt = this.cxt;

					// 清空canvas
					this.cxt.clearRect(0, 0, this._w, this._h);
					// cxt.putImageData(this.canvasSurface, 0, 0);
					for(var i in pointObj) {
						if(i === 'length') {
							continue;
						}
						cxt.beginPath();
						cxt.arc(pointObj[i].x , pointObj[i].y, 15, 0, Math.PI*2, true);
						cxt.fill();

						this.drawIndex(pointObj[i].x , pointObj[i].y, i);
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
			};

			var canvasContainer = document.getElementById('contentContainer'),
				canvas = document.getElementById('canvas'),
				canvasBg = '',
				// planInfo = !utils.isOwnEmpty(layout) && layout.layout ? layout.layout : {},
				isInit = true;

			window.planInfo = !utils.isOwnEmpty(layout) && layout.layout ? layout.layout : {};
			if(!utils.isOwnEmpty(planInfo) && planInfo.bgImg) {
				canvasBg = planInfo.bgImg;
				buildingInit();
			} else {
				$('#canvasBgModal').modal();
			}
			$('#bgInput').change(function(){
				avalon.ajaxupload.upload(
					'/apis/aphrodite/image.json',
					$(this),
					{
						success: function(d) {
							var data = $.parseJSON(d);
							if(data.ok && data.result) {
								$('#bgTmpImg').attr('src', data.result.url);
							} else {
								console.error(data);
								alert('出错了');
							}
						}
					}
				);
			});
			$('#canvasBgModal').on('hide.bs.modal', function (e) {
				canvasBg = $('#bgTmpImg').attr('src');
				if(!canvasBg) {
					alert('选择背景');
					return false;
				}
				if(planInfo.bgImg) {
					planCanvas.init(canvasContainer, canvas, canvasBg, null, null, buildingInit);
					// planCanvas.canvas.style.backgroundImage = 'url(' + canvasBg + ')';
				} else {
					buildingInit();
				}
				planInfo.bgImg = canvasBg;
			});
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
						if(d.ok) {
							location.href = url_parent;
						}
					},
					error: function(d) {

					},
					dataType: 'json'
				});
			});

			$('#bgBtn').click(function() {
				$('#canvasBgModal').modal();
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
			function redraw(planDetailObj) {
				planCanvas.resetCanvas();
				var point;
				for(var key in planDetailObj) {
					if(key === 'length') {
						continue;
					}
					planCanvas.clearPointList();
					for(var j in planDetailObj[key]) {
						point = planDetailObj[key][j];
						planCanvas.addPointToPointList(point.x, point.y);
					}
					planCanvas.drawPlan();
					planCanvas.drawIndex(planDetailObj[key][0].x, planDetailObj[key][0].y, key);
				}
				updateDelOption(planDetailObj);
			}

			// 把画icon的index的方法放在了drawPoints里边
			// icon比较特殊，一个点就代表一个block
			function redrawIcon(planDetailObj) {
				planCanvas.resetCanvas();
				var point;
				for(var i in planDetailObj) {
					point = planDetailObj[i];
					planCanvas.addPointToPointList(point.x, point.y);
				}

				planCanvas.drawPoints(planDetailObj);
				updateDelOption(planDetailObj);
			}

			// 更新删除的下来菜单
			function updateDelOption(planDetailObj) {
				var optionHtml = '';

				for(var key in planDetailObj) {
					if(key === 'length') {
						continue;
					}
					optionHtml += '<option value="' + key + '">' + key + '</option>';
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
						if(!planInfo['canvas'] || !planInfo.canvas.startPoint) {
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
						var pointList = planCanvas.getPointList(),
							planKey;
						planCanvas.drawPlan();

						if(!planInfo['bg']) {
							planInfo.bg = {
								length: 0
							};
						}
						planKey = planInfo.bg.length++;
						planInfo.bg[planKey] = pointList;
						planCanvas.drawIndex(pointList[0].x, pointList[0].y, planKey);
						updateDelOption(planInfo.bg);
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('delBlockBtn').onclick = function(e) {
						var key = $('#delOption').val();

						if(key) {
							var r = confirm('确定要删除模块' + key + '?');
							if(r) {
								delete planInfo.bg[key];
								redraw(planInfo.bg);
								updateDelOption(planInfo.bg);
							}
						}
					};

					// 初始化已有数据
					if(planInfo.bg && planInfo.bg.length) {
						redraw(planInfo.bg);
					} else {
						redraw([]);
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
						var pointList = planCanvas.getPointList(),
							planKey;
						planCanvas.drawPlan();

						if(!planInfo['white']) {
							planInfo.white = {
								length: 0
							};
						}
						planKey = planInfo.white.length++;
						planInfo.white[planKey] = pointList;
						planCanvas.drawIndex(pointList[0].x, pointList[0].y, planKey);
						updateDelOption(planInfo.white);
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('delBlockBtn').onclick = function(e) {
						var key = $('#delOption').val();

						if(key) {
							var r = confirm('确定要删除模块' + key + '?');
							if(r) {
								delete planInfo.white[key];
								redraw(planInfo.white);
								updateDelOption(planInfo.white
									);
							}
						}
					};
				});

				// 初始化已有数据
				if(planInfo.white && planInfo.white.length) {
					redraw(planInfo.white);
				} else {
					redraw([]);
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
						var pointList = planCanvas.getPointList(),
							planKey;
						planCanvas.drawPlan();

						if(!planInfo['shop']) {
							planInfo.shop = {
								length: 0
							};
						}
						planKey = planInfo.shop.length++;
						planInfo.shop[planKey] = pointList;
						planCanvas.drawIndex(pointList[0].x, pointList[0].y, planKey);
						updateDelOption(planInfo.shop);
					};
					canvas.onmousemove = function(e) {
						planCanvas.drawTmpPlan(e);
					};
					document.getElementById('delBtn').onclick = function(e) {
						planCanvas.delPoint();
						buildPointList(planCanvas.getPointList());
					};
					document.getElementById('delBlockBtn').onclick = function(e) {
						var key = $('#delOption').val();

						if(key) {
							var r = confirm('确定要删除模块' + key + '?');
							if(r) {
								delete planInfo.shop[key];
								redraw(planInfo.shop);
								updateDelOption(planInfo.shop);
							}
						}
					};
				});

				// 初始化已有数据
				if(planInfo.shop && planInfo.shop.length) {
					redraw(planInfo.shop);
				} else {
					redraw([]);
				}
			}

			// 取Icon信息
			function iconInit() {
				$('#nextBtn').attr('data-operation', 'over');
				$('a[data-operation="icon"]').addClass('active').siblings().removeClass('active');
				planCanvas.resetCanvas(function() {
					// canvas取点处理
					canvas.onclick = function(e) {
						var curPos = planCanvas.getPoint(e);

						planKey = planInfo.icon.length++;
						planInfo.icon[planKey] = curPos;
						planCanvas.drawPoints(planInfo.icon);
						updateDelOption(planInfo.icon);
					};
					document.getElementById('drawBtn').onclick = function(e) {
						// do nothing
					};
					canvas.onmousemove = function(e) {
						var curPos = planCanvas.getPoint(e);

						if(!planInfo['icon']) {
							planInfo['icon'] = {
								length: 0
							};
						}
						planKey = planInfo.icon.length++;
						planInfo.icon[planKey] = curPos;
						planCanvas.drawPoints(planInfo.icon);
						delete planInfo.icon[--planInfo.icon.length];
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
								delete planInfo.icon[index];
								redrawIcon(planInfo.icon);
								updateDelOption(planInfo.icon);
							}
						}
					};
				});
				// 初始化已有数据
				if(planInfo.icon && planInfo.icon.length) {
					redrawIcon(planInfo.icon);
				} else {
					redrawIcon([]);
				}
			}
        });
    };
});
