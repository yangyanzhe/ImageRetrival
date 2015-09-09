################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../FANN.cpp \
../Feature.cpp \
../Interfaces.cpp \
../RunPictureRetrieve.cpp \
../cvgabor.cpp 

OBJS += \
./FANN.o \
./Feature.o \
./Interfaces.o \
./RunPictureRetrieve.o \
./cvgabor.o 

CPP_DEPS += \
./FANN.d \
./Feature.d \
./Interfaces.d \
./RunPictureRetrieve.d \
./cvgabor.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I/usr/local/include/opencv2 -I/usr/local/include -I/usr/local/include/opencv -I/usr/include/python2.7 -I/usr/include/opencv -I/usr/include -I/usr/include/opencv2 -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


