// sets imu to 350 degrees
rst 350;
// turn to 180 degrees
turn 180;
// drive 20mm 
drive 20;
// call a with b, c, d -> a(b,c,d), the function is a C function
// i won't add anything to define functions in here
call a : b,c,d;
// waits for 500 ms
slp 500;
// sets the drive velocity to 50 percent;
drive_vel 50;
// sets the turn velocity to 50 percent;
turn_vel 50;
