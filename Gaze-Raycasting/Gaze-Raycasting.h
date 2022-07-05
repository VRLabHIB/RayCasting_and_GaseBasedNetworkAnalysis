#pragma once
#include <iostream>
#include <vector>
#include <math.h>
#include <numeric>

//Plugin gaze, head and rotation input from Unreal later
std::vector<float> gaze = { 0,1,0 };
std::vector<float> gaze0 = { gaze[0],0,gaze[2]};

std::vector<float> fw = { 0,0,1 };

std::vector<float> location = { 3,2,1 };
std::vector<float> rotation = { 40,10,20 };

float  pitch;
#define PI 3.14159265

float compute_norm(std::vector<float> vec) {
	//computes the L2 norm of a 3D vector
	float norm = sqrt(pow(vec[0], 2) + pow(vec[1], 2) + pow(vec[2], 2));
	if (norm <= 0.000001) {
		norm = 0;
	};

	return norm;
}

std::vector<float> normalize(std::vector<float> vec) {
	// input a 3D euclidian vector; returns a L2 normalized one
	
	float norm = compute_norm(vec);

	std::vector<float> vec_n = { vec[0] / norm,vec[1] / norm,vec[2] / norm };

	return vec_n;
}

template <typename T> int sgn(T val) {
	return (T(0) < val) - (val < T(0));
};

