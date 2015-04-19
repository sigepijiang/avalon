

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
					data: tmpSvgStr,
					fill: '#fff',
					stroke: '#fff',
					strokeWidth: 2
				});

				staticLayer.add(path);
			}

			// shop
			var shopColor = {
					'default': '#edd0ad',
					'defaultHover': '#fad1a1',
					'finish': '#7FFF00',
					'finishHover': '#fad1a1'
				};

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

				if(planData.shop[index]) {
					changeColor(path, shopColor.finish, shopColor.defaultHover);
				}

				path.on('mouseover', function() {
					this.setFill(this.data.colorHover);
					this.setStroke(this.data.colorHover);
					this.moveTo(topLayer);
					topLayer.drawScene();
				});

				path.on('mouseout', function() {
					this.moveTo(shopLayer);
					topLayer.draw();
				});

				path.on('click', function() {
					console.log(shopData[this.data.index]);
					alert(shopData[this.data.index].name);
				});

				shopLayer.add(path);
			}

			// icon
			tmpInfoList = planInfo.icon;
			for(var index in tmpInfoList) {
				tmpSvgStr = toSvgAce(tmpInfoList[index]);

				path = new Kinetic.Path({
					data: tmpSvgStr,
					fill: shopColor.default,
					stroke: '#fff',
					strokeWidth: 2
				});

				// 作为标示当前点击元素
				path.data = {
					type: 'icon',
					index: index,
					color: shopColor.default,
					colorHover: shopColor.defaultHover
				};

				if(planData.icon[index]) {
					changeColor(path, shopColor.finish, shopColor.defaultHover);
				}

				path.on('mouseover', function() {
					this.setFill(shopColor.defaultHover);
					this.setStroke(shopColor.defaultHover);
					this.moveTo(topLayer);
					topLayer.drawScene();
				});

				path.on('mouseout', function() {
					this.moveTo(shopLayer);
					topLayer.draw();
				});

				path.on('click', function() {
					console.log(iconData[this.data.index]);
					alert(iconData[this.data.index].facility_type);
				});

				shopLayer.add(path);
			}

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

			function toSvgAce(point) {
				var startPointX = endPointX = point.x - startPoint.x,
					startPointY = point.y - startPoint.y - 15,
					endPointY = point.y - startPoint.y - 14.9999,
					svgStr;
				startPointX *= scale;
				startPointY *= scale;
				endPointX *= scale;
				endPointY *= scale;
				svgStr = 'M' + startPointX + ',' + startPointY + 'A15,15,0,1,1,' + endPointX + ',' + endPointY + 'Z';

				return svgStr;
			}
        });
    }
})






