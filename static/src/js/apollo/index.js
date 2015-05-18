

// function windowResize(){
// 	var _h = $(window).height();
// 	$('.main, .box').height(_h);
// }
// windowResize();
// $(window).resize(function(){
// 	windowResize();
// });

// drawPlan.js

Module('index', function(){
    this.run = function(){
        $(function() {
			if(!floorData || !floorData.length) {
				console.log('还没构建商店');
				return false;
			}
			var thisFloorData = floorData[0].layout.data,
				planInfo = thisFloorData.layout,
				shopData = thisFloorData.shop_data ? thisFloorData.shop_data : {},
				iconData = thisFloorData.facility_data ? thisFloorData.facility_data : {},
				planData = {
					shop: shopData,
					icon: iconData
				};

			// 初始化列表
			var shopId = 0,
				shopName = '',
				shopTmpl = '<li data-index="{shopId}"><span>{shopName}</span></li>',
				shopHtml,
				$shopList = $('.shopList');
			for(var index in shopData) {
				shopId = index;
				shopName = shopData[index].name;
				shopHtml = shopTmpl.replace('{shopId}', shopId)
									.replace('{shopName}', shopName);
				if(index < 10) {
					$($shopList[0]).append(shopHtml);
				} else {
					$($shopList[1]).append(shopHtml);
				}
			}

			var	canvasInfo = planInfo.canvas,
				wWidth = $('#canvasContainer').width(),
				scale = wWidth / canvasInfo.realWidth,
				_w = wWidth,
				// _w = canvasInfo.height,
				_h = scale * canvasInfo.realHeight,
				startPoint = canvasInfo.startPoint;

			var stage = new Kinetic.Stage({
				container: 'canvasContainer',
				width: _w,
				height: _h
			});

			var staticLayer = new Kinetic.Layer({});

			var shopLayer = new Kinetic.Layer({
				// y: 20,
				// scale: 0.6
			});

			var topLayer = new Kinetic.Layer({
				// y: 20,
				// scale: 0.6
			});

			var tmpInfoList = planInfo.bg,
				tmpSvgStr = '',
				path;

			// bg
			for(var index in tmpInfoList) {
				tmpSvgStr = toSvgPath(tmpInfoList[index]);

				path = new Kinetic.Path({
					data: tmpSvgStr,
					fill: '#e6f9e7',
					stroke: '#fff',
					strokeWidth: 2
				});

				staticLayer.add(path);
			}

			// white
			tmpInfoList = planInfo.white;
			for(var index in tmpInfoList) {
				tmpSvgStr = toSvgPath(tmpInfoList[index]);

				path = new Kinetic.Path({
					data        : tmpSvgStr,
					fill        : '#fff',
					stroke      : '#fff',
					strokeWidth : 2
				});

				staticLayer.add(path);
			}

			// shop
			var shopColor = {
					'default'      : '#c2c1c1',
					'defaultHover' : '#fad1a1',
					'finish'       : '#7FFF00',
					'finishHover'  : '#fad1a1'
				},
				shopPathObj = {},
				lastPath;

			tmpInfoList = planInfo.shop;
			for(var index in tmpInfoList) {
				tmpSvgStr = toSvgPath(tmpInfoList[index]);

				path = new Kinetic.Path({
					data: tmpSvgStr,
					fill: shopColor.default,
					stroke: '#fff',
					strokeWidth: 2
				});

				// 作为标示当前点击元素
				path.data = {
					type: 'shop',
					index: index,
					color: shopColor.default,
					colorHover: shopColor.defaultHover
				};

				shopPathObj[index] = path;

				if(planData.shop[index]) {
					changeColor(path, shopColor.finish, shopColor.finishHover);
				}

				$shopList.find('li[data-index=' + index + ']').hover(function(e) {
					var index = $(this).data('index'),
						thisPath = shopPathObj[index];

					$shopList.find('li[data-index]').removeClass('focus');
					$(this).addClass('focus');
					showShopData(index);

					thisPath.setFill(thisPath.data.colorHover);
					thisPath.setStroke(thisPath.data.colorHover);
					thisPath.moveTo(topLayer);
					topLayer.drawScene();
				}, function(e) {
					var index = $(this).data('index'),
						thisPath = shopPathObj[index];

					thisPath.moveTo(shopLayer);
					topLayer.draw();
				});

				path.on('mouseover', function() {
					if(lastPath) {
						lastPath.moveTo(shopLayer);
						topLayer.draw();
					}

					this.setFill(this.data.colorHover);
					this.setStroke(this.data.colorHover);
					this.moveTo(topLayer);
					topLayer.drawScene();

					showShopData(this.data.index);

					$shopList.find('li[data-index]').removeClass('focus');
					$shopList.find('li[data-index=' + this.data.index + ']').addClass('focus');
				});

				path.on('mouseout', function() {
					lastPath = this;
				});

				path.on('click', function() {
					console.log(shopData[this.data.index]);
					alert(shopData[this.data.index].name);
				});

				shopLayer.add(path);

				function showShopData(index) {
					$('#phone').text(shopData[index].phone);
				}
			}

			// icon
			var iconImgObj = {
				'counter'    : '',
				'restaurant' : '',
				'wc'         : 'http://2.im.guokr.com/zMzEh7Yd8yf4bkDyDZhX-CCQqlyGKo6sinZmtzVZ_3QeAAAAHgAAAFBO.png',
				'escalator'  : '',
				'lift'       : '',
				'stair'      : '',
				'exit'       : '',
				'hydrant'    : '',
				'garbage'    : '',
				'phone'      : '',
				'default'    : 'http://2.im.guokr.com/zMzEh7Yd8yf4bkDyDZhX-CCQqlyGKo6sinZmtzVZ_3QeAAAAHgAAAFBO.png'
			},
			img = new Image(),
			imgLoadedLength = 0,
			tmpPoint;

			img.onload = function() {
				tmpInfoList = planInfo.icon;
				for(var index in tmpInfoList) {
					if(index === 'length') {
						continue;
					}
					tmpPoint = toCurPoint(tmpInfoList[index]);

					circle = new Kinetic.Circle({
						x                 : tmpPoint.x,
						y                 : tmpPoint.y,
						radius            : 15,
						fillPatternImage  : img,
						fillPatternOffset : {
							x : 15,
							y : 15
						},
						stroke            : '#fff',
						strokeWidth       : 2
					});

					// 作为标示当前点击元素
					circle.data = {
						type: 'icon',
						index: index,
						color: shopColor.default,
						colorHover: shopColor.defaultHover
					};

					if(planData.icon[index]) {
						changeIcon(circle, iconImgObj[iconData[index].facility_type], '');
					}

					circle.on('mouseover', function() {
						this.setStroke(this.colorHover);
						this.moveTo(topLayer);
						topLayer.drawScene();
					});

					circle.on('mouseout', function() {
						this.moveTo(shopLayer);
						topLayer.draw();
					});

					circle.on('click', function() {
						console.log(iconData[this.data.index]);
						alert(iconData[this.data.index].facility_type);
					});

					shopLayer.add(circle);
				}
			}
			img.src = iconImgObj.default;

			stage.add(staticLayer);
			stage.add(shopLayer);
			stage.add(topLayer);

			function changeColor(path, color, hoverColor) {
				path.data.color = color;
				path.data.colorHover = hoverColor;
				path.moveTo(shopLayer);
				path.setFill(color);
				path.setStroke('#fff');

				shopLayer.draw();
				// path.moveTo(topLayer);
			}

			function changeIcon(circle, iconImg, colorHover) {
				var tmpIconImg = new Image();
				tmpIconImg.onload = function() {
					circle.data.iconImg = tmpIconImg;
					circle.data.colorHover = colorHover;
					circle.moveTo(shopLayer);
					circle.fillPatternImage(tmpIconImg);
					circle.setStroke('#fff');

					shopLayer.draw();
				}
				tmpIconImg.src = iconImg;
			}

			function toSvgPath(pointList) {
				var svgStr = '',
					curPoint = {
						x: 0,
						y: 0
					};
				for(var i in pointList) {
					curPoint.x = pointList[i].x - startPoint.x;
					curPoint.y = pointList[i].y - startPoint.y;
					curPoint.x *= scale;
					curPoint.y *= scale;
					if(i == 0) {
						svgStr = 'M' + curPoint.x + ',' + curPoint.y;
					} else {
						svgStr += 'L' + curPoint.x + ',' + curPoint.y;
					}
				}

				svgStr += 'z';
				return svgStr;
			}

			function toCurPoint(point) {
				var startPointX = endPointX = point.x - startPoint.x,
					startPointY = point.y - startPoint.y;
				startPointX *= scale;
				startPointY *= scale;

				return {
					x: startPointX,
					y: startPointY
				}
			}
        });
    }
})






