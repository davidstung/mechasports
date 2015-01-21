translate([-500,-1500,0]){
	translate([50,2750,25]) color([1,1,1],1){cube([700,100,25]);};
	translate([450,2870,25]) color([0,0,1],1){cube([100,100,25]);};
	for (i = [100:200:900]){
		translate([i-50,2600,25]) color([1-i/900.0,i/900.0,0],1){cube([100,100,25]);};
		for (z = [150:150:i*2.7]){
			translate([i-25,z,25])color("goldenrod",1){cube([50,50,25]);};
			};
	}
	color("black",1){cube([1000,3000,49]);};
};