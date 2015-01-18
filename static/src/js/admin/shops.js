// drawPlan.js

Module('drawPlan', function(){
    this.run = function(){
        $(function() {
			if(!layout || !layout.layout || !layout.layout.canvas) {
				alert('请先构建店铺');
				history.back();
				return false;
			}
			var planInfo = layout.layout;
				planData = layout.shop_data ? {
					shop: layout.shop_data,
					icon: layout.icon_data
				} : {
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
					index: index
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
					var thisData = this.data,
						isSaving = false,
						ajaxType = 'post',
						canClose = false;
					$('#shopForm').on('show.bs.modal', function (e) {
						var shopData = planData.shop[thisData.index];
						if(shopData) {
							$('#shopNameInput').val(shopData.name);
							$('#shopTelInput').val(shopData.tel);
							isCreate = 'put';
						} else {
							$('#shopNameInput').val('');
							$('#shopTelInput').val('');
							isCreate = 'post';
						}
					});
					$('#shopForm').modal();
					$('#shopForm').on('hide.bs.modal', function (e) {
						if(canClose) {
							return true;
						}
						if(isSaving) {
							alert('正在保存数据');
							return false;
						}

						var shopName = $.trim($('#shopNameInput').val()),
							shopTel = $.trim($('#shopTelInput').val()),
							index = thisData.index;
						if(shopName && shopTel) {
							planData.shop[index] = {
								floor_id: floor_id,
								name: shopName,
								phone: shopTel,
								index: index,
								id: planData.shop[index] ? planData.shop[index].id : undefined
							};

							isSaving = true;
							$.ajax({
								url: '/apis/apollo/market/shop.json',
								method: ajaxType,
								contentType: 'application/json',
								data: JSON.stringify(planData.shop[index]),
								success: function(d) {
									canClose = true;
									planData.shop[index].id = d.resultd.result.id;
									$('#shopForm').modal('hide');
								},
								error: function(d) {
									var r = confirm('保存失败,关闭后丢失此次保存的数据~！');
									if(r) {
										canClose = true;
										delete planData.shop[index];
										$('#shopForm').modal('hide');
									} else {
										isSaving = false;
									}
								},
								dataType: 'json'
							});
							return false;
						} else {
							alert('数据不全，不保存');
							delete planData.shop[index];
							// return false;
						}
					});
					$('#shopForm').on('hidden.bs.modal', function (e) {
						$(this).off('show.bs.modal hide.bs.modal hidden.bs.modal');
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

			$('#saveBtn').click(function() {
				
			});


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
