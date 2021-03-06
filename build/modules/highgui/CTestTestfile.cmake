# CMake generated Testfile for 
# Source directory: /home/jakob/Documents/Hackathon/lent21/opencv-master/modules/highgui
# Build directory: /home/jakob/Documents/Hackathon/lent21/build/modules/highgui
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_highgui "/home/jakob/Documents/Hackathon/lent21/build/bin/opencv_test_highgui" "--gtest_output=xml:opencv_test_highgui.xml")
set_tests_properties(opencv_test_highgui PROPERTIES  LABELS "Main;opencv_highgui;Accuracy" WORKING_DIRECTORY "/home/jakob/Documents/Hackathon/lent21/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/jakob/Documents/Hackathon/lent21/opencv-master/cmake/OpenCVUtils.cmake;1707;add_test;/home/jakob/Documents/Hackathon/lent21/opencv-master/cmake/OpenCVModule.cmake;1311;ocv_add_test_from_target;/home/jakob/Documents/Hackathon/lent21/opencv-master/modules/highgui/CMakeLists.txt;165;ocv_add_accuracy_tests;/home/jakob/Documents/Hackathon/lent21/opencv-master/modules/highgui/CMakeLists.txt;0;")
