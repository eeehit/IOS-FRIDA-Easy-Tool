		var targetModule{{2}} = Process.enumerateModules()[0].name;
		var address{{2}} = ptr({{1}});
		var moduleBase{{2}} = Module.getBaseAddress(targetModule{{2}});
		var targetAddress{{2}} = moduleBase{{2}}.add(address{{2}});

		Interceptor.attach(targetAddress{{2}}, {
			onEnter: function(args) {
				var tmp_x0, tmp_x1, tmp_x2, tmp_x3, tmp_x4, tmp_x5, tmp_x6, tmp_x7, tmp_x8, tmp_x9, tmp_x10, tmp_x11, tmp_x12, tmp_x13, tmp_x14, tmp_x15, tmp_x16, tmp_x17, tmp_x18, tmp_x19, tmp_x20, tmp_x21, tmp_x22, tmp_x23, tmp_x24, tmp_x25, tmp_x26, tmp_x27, tmp_x28, tmp_lr;
				
				send(targetAddress{{2}} + ' ' + this.context.x0 + ' ' +  this.context.x1 + ' ' +  this.context.x2 + ' ' + this.context.x3 + ' ' + this.context.x4 + ' ' + this.context.x5 + ' ' + this.context.x6 + ' ' + this.context.x7 + ' ' + this.context.x8 + ' ' + this.context.x9 + ' ' + this.context.x10 + ' ' + this.context.x11 + ' ' + this.context.x12 + ' ' + this.context.x13 + ' ' + this.context.x14 + ' ' + this.context.x15 + ' ' + this.context.x16 + ' ' + this.context.x17 + ' ' + this.context.x18 + ' ' + this.context.x19 + ' ' + this.context.x20 + ' ' + this.context.x21 + ' ' + this.context.x22 + ' ' + this.context.x23 + ' ' + this.context.x24 + ' ' + this.context.x25 + ' ' + this.context.x26 + ' ' + this.context.x27 + ' ' + this.context.x28 + ' ' + this.context.lr + ' ' + moduleBase{{2}});
				

				recv(function(result_json_data) {
					tmp_x0 = result_json_data.x0;
					tmp_x1 = result_json_data.x1;
					tmp_x2 = result_json_data.x2;
					tmp_x3 = result_json_data.x3;
					tmp_x4 = result_json_data.x4;
					tmp_x5 = result_json_data.x5;
					tmp_x6 = result_json_data.x6;
					tmp_x7 = result_json_data.x7;
					tmp_x8 = result_json_data.x8;
					tmp_x9 = result_json_data.x9;
					tmp_x10 = result_json_data.x10;
					tmp_x11 = result_json_data.x11;
					tmp_x12 = result_json_data.x12;
					tmp_x13 = result_json_data.x13;
					tmp_x14 = result_json_data.x14;
					tmp_x15 = result_json_data.x15;
					tmp_x16 = result_json_data.x16;
					tmp_x17 = result_json_data.x17;
					tmp_x18 = result_json_data.x18;
					tmp_x19 = result_json_data.x19;
					tmp_x20 = result_json_data.x20;
					tmp_x21 = result_json_data.x21;
					tmp_x22 = result_json_data.x22;
					tmp_x23 = result_json_data.x23;
					tmp_x24 = result_json_data.x24;
					tmp_x25 = result_json_data.x25;
					tmp_x26 = result_json_data.x26;
					tmp_x27 = result_json_data.x27;
					tmp_x28 = result_json_data.x28;
					tmp_lr = result_json_data.lr;
				}).wait();

				this.context.x0 = tmp_x0 * 1;
				this.context.x1 = tmp_x1 * 1;
				this.context.x2 = tmp_x2 * 1;
				this.context.x3 = tmp_x3 * 1;
				this.context.x4 = tmp_x4 * 1;
				this.context.x5 = tmp_x5 * 1;
				this.context.x6 = tmp_x6 * 1;
				this.context.x7 = tmp_x7 * 1;
				this.context.x8 = tmp_x8 * 1;
				this.context.x9 = tmp_x9 * 1;
				this.context.x10 = tmp_x10 * 1;
				this.context.x11 = tmp_x11 * 1;
				this.context.x12 = tmp_x12 * 1;
				this.context.x13 = tmp_x13 * 1;
				this.context.x14 = tmp_x14 * 1;
				this.context.x15 = tmp_x15 * 1;
				this.context.x16 = tmp_x16 * 1;
				this.context.x17 = tmp_x17 * 1;
				this.context.x18 = tmp_x18 * 1;
				this.context.x19 = tmp_x19 * 1;
				this.context.x20 = tmp_x20 * 1;
				this.context.x21 = tmp_x21 * 1;
				this.context.x22 = tmp_x22 * 1;
				this.context.x23 = tmp_x23 * 1;
				this.context.x24 = tmp_x24 * 1;
				this.context.x25 = tmp_x25 * 1;
				this.context.x26 = tmp_x26 * 1;
				this.context.x27 = tmp_x27 * 1;
				this.context.x28 = tmp_x28 * 1;
				this.context.lr = tmp_lr * 1;
			},
		});