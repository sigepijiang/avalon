// drawPlan.js

Module('drawPlan', function(){
    this.run = function(){
        $(function() {
			if(!layout || !layout.layout || layout.layout.canvas) {
				alert('请先构建店铺');
				history.back();
				return false;
			}
			var planInfo = layout.layout,
				planData = {
					shop: {

					},
					icon: {

					}
				};
			var	canvasInfo = planInfo.canvas,
				_w = canvasInfo.width,
				_h = canvasInfo.height;

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
			tmpInfoList = planInfo.shop;
			for(var index in tmpInfoList) {
				tmpSvgStr = toSvgPath(tmpInfoList[index]);

				path = new Kinetic.Path({
					data: tmpSvgStr,
					fill: '#edd0ad',
					stroke: '#fff',
					strokeWidth: 2
				});

				// 作为标示当前点击元素
				path.data = {
					type: 'shop',
					key: index
				};

				path.on('mouseover', function() {
					this.setFill('#fad1a1');
					this.setStroke('#fad1a1');
					this.moveTo(topLayer);
					topLayer.drawScene();
				});

				path.on('mouseout', function() {
					this.setFill('#edd0ad');
					this.moveTo(shopLayer);
					topLayer.draw();
				});

				path.on('click', function() {
					var thisData = this.data;
					$('#shopForm').on('show.bs.modal', function (e) {
						var shopData = planData.shop[thisData.key];
						if(shopData) {
							$('#shopNameInput').val(shopData.name);
							$('#shopTelInput').val(shopData.tel);
						} else {
							$('#shopNameInput').val('');
							$('#shopTelInput').val('');
						}
					});
					$('#shopForm').modal();
					$('#shopForm').on('hidden.bs.modal', function (e) {
						var shopName = $.trim($('#shopNameInput').val()),
							shopTel = $.trim($('#shopTelInput').val()),
							key = thisData.key;
						if(shopName && shopTel) {
							planData.shop[key] = {
								name: shopName,
								tel: shopTel
							}
						} else {
							delete planData.shop[key];
							return false;
						}

						$(this).off('show.bs.modal hidden.bs.modal');
					});
				});

				shopLayer.add(path);
			}
			$('#shopForm').on('shown.bs.modal', function (e) {
				$('#shopNameInput').focus();
			});

			// icon
			tmpInfoList = planInfo.icon;
			for(var index in tmpInfoList) {
				tmpSvgStr = toSvgAce(tmpInfoList[index]);

				path = new Kinetic.Path({
					data: tmpSvgStr,
					fill: '#edd0ad',
					stroke: '#fff',
					strokeWidth: 2
				});

				// 作为标示当前点击元素
				path.data = {
					type: 'icon',
					key: index
				};

				path.on('mouseover', function() {
					this.setFill('#fad1a1');
					this.setStroke('#fad1a1');
					this.moveTo(topLayer);
					topLayer.drawScene();
				});

				path.on('mouseout', function() {
					this.setFill('#edd0ad');
					this.moveTo(shopLayer);
					topLayer.draw();
				});

				path.on('click', function() {
					var thisData = this.data;
					$('#iconForm').on('show.bs.modal', function (e) {
						var iconData = planData.icon[thisData.key];
						if(iconData) {
							$('#iconType').val(iconData.value);
						} else {
							$('#iconType').val('');
						}

					});
					$('#iconForm').modal();
					$('#iconForm').on('hidden.bs.modal', function (e) {
						var iconSelect = $('#iconType').val(),
							key = thisData.key;
						if(iconSelect) {
							planData.icon[key] = {
								value: iconSelect
							}
						} else {
							delete planData.icon[key];
							return false;
						}

						console.log(planData);
						$(this).off('show.bs.modal hidden.bs.modal');
					});
				});

				shopLayer.add(path);
			}

			$('#iconForm').on('shown.bs.modal', function (e) {
				$('#iconType').focus();
			});

			stage.add(staticLayer);
			stage.add(shopLayer);
			stage.add(topLayer);


			function toSvgPath(pointList) {
				var svgStr = '';
				for(var i in pointList) {
					if(i == 0) {
						svgStr = 'M' + pointList[i].x + ',' + pointList[i].y;
					} else {
						svgStr += 'L' + pointList[i].x + ',' + pointList[i].y;
					}
				}

				svgStr += 'z';
				return svgStr;
			}

			function toSvgAce(point) {
				var startPointX = endPointX = point.x,
					startPointY = point.y -15,
					endPointY = point.y - 14.9999,
					svgStr = 'M' + startPointX + ',' + startPointY + 'A15,15,0,1,1,' + endPointX + ',' + endPointY + 'Z';

				return svgStr;
			}
        });
    }
})
