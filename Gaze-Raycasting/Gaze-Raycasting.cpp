#include "Gaze-Raycasting.h"
using namespace std;

int main(void) {

	std::vector<float> gaze_n = normalize(gaze);
	std::vector<float> gaze0_n = normalize(gaze0);

	//TODO: signum ergänzen	
	float yaw = acos(gaze_n[2] / compute_norm(gaze_n)) * 180 / PI * sgn(gaze[0]);

		
	float dot = std::inner_product(gaze_n.begin(), gaze_n.end(), gaze0_n.begin(), 0);
	//TODO: signum ergänzen	
	float pitch = acos(dot / compute_norm(gaze0_n)) * 180 / PI * sgn(gaze[1]);

	cout << dot;
}



