

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
			if(!layout || !layout.layout || !layout.layout.canvas) {
				alert('请先构建店铺');
				history.back();
				return false;
			}
			var planInfo = layout.layout,
				shopData = layout.shop_data ? layout.shop_data : {},
				iconData = layout.facility_data ? layout.facility_data : {},
				planData = {
					shop: shopData,
					icon: iconData
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
					var thisData = this.data,
						isSaving = false,
						ajaxType = 'post',
						canClose = false,
						thisPath = this;
					$('#shopForm').on('show.bs.modal', function (e) {
						var shopData = planData.shop[thisData.index];
						if(shopData) {
							$('#shopNameInput').val(shopData.name);
							$('#shopTelInput').val(shopData.phone);
							ajaxType = 'put';
						} else {
							$('#shopNameInput').val('');
							$('#shopTelInput').val('');
							ajaxType = 'post';
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
									planData.shop[index].id = d.result.id;
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
						}
					});
					$('#shopForm').on('hidden.bs.modal', function (e) {
						if(planData.shop[thisPath.data.index]) {
							changeColor(thisPath, shopColor.finish, shopColor.finishHover);
						} else {
							changeColor(thisPath, shopColor.default, shopColor.defaultHover);
						}
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
					var thisData = this.data,
						isSaving = false,
						ajaxType = 'post',
						canClose = false,
						thisPath = this;
					$('#iconForm').on('show.bs.modal', function (e) {
						var iconData = planData.icon[thisData.index];
						if(iconData) {
							$('#iconType').val(iconData.facility_type);
							ajaxType = 'put';
						} else {
							$('#iconType').val('');
							ajaxType = 'post';
						}

					});
					$('#iconForm').modal();
					$('#iconForm').on('hide.bs.modal', function (e) {
						if(canClose) {
							return true;
						}
						if(isSaving) {
							alert('正在保存数据');
							return false;
						}

						var iconSelect = $('#iconType').val(),
							index = thisData.index;
						if(iconSelect) {
							planData.icon[index] = {
								floor_id: floor_id,
								facility_type: iconSelect,
								index: index,
								id: planData.icon[index] ? planData.icon[index].id : undefined
							};

							isSaving = true;
							$.ajax({
								url: '/apis/apollo/market/facility.json',
								method: ajaxType,
								contentType: 'application/json',
								data: JSON.stringify(planData.icon[index]),
								success: function(d) {
									canClose = true;
									planData.icon[index].id = d.result.id;
									$('#iconForm').modal('hide');
								},
								error: function(d) {
									var r = confirm('保存失败,关闭后丢失此次保存的数据~！');
									if(r) {
										canClose = true;
										delete planData.icon[index];
										$('#iconForm').modal('hide');
									} else {
										isSaving = false;
									}
								},
								dataType: 'json'
							});
							return false;
						} else {
							alert('数据不全，不保存');
							delete planData.icon[index];
							// return false;
						}
					});
					$('#iconForm').on('hidden.bs.modal', function (e) {
						if(planData.icon[thisPath.data.index]) {
							changeColor(thisPath, shopColor.finish, shopColor.finishHover);
						} else {
							changeColor(thisPath, shopColor.default, shopColor.defaultHover);
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
				history.back();
			});

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






