# CMake generated Testfile for 
# Source directory: /home/jakob/Documents/Hackathon/lent21/opencv-master/modules/flann
# Build directory: /home/jakob/Documents/Hackathon/lent21/build/modules/flann
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_flann "/home/jakob/Documents/Hackathon/lent21/build/bin/opencv_test_flann" "--gtest_output=xml:opencv_test_flann.xml")
set_tests_properties(opencv_test_flann PROPERTIES  LABELS "Main;opencv_flann;Accuracy" WORKING_DIRECTORY "/home/jakob/Documents/Hackathon/lent21/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/jakob/Documents/Hackathon/lent21/opencv-master/cmake/OpenCVUtils.cmake;1707;add_test;/home/jakob/Documents/Hackathon/lent21/opencv-master/cmake/OpenCVModule.cmake;1311;ocv_add_test_from_target;/home/jakob/Documents/Hackathon/lent21/opencv-master/cmake/OpenCVModule.cmake;1075;ocv_add_accuracy_tests;/home/jakob/Documents/Hackathon/lent21/opencv-master/modules/flann/CMakeLists.txt;2;ocv_define_module;/home/jakob/Documents/Hackathon/lent21/opencv-master/modules/flann/CMakeLists.txt;0;")
