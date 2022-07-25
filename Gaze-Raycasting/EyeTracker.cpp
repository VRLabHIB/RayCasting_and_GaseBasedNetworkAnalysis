// Fill out your copyright notice in the Description page of Project Settings.

#include "EyeTracker.h"
#include <string>
#include "Misc/DateTime.h"
#include "SRanipalEye_FunctionLibrary.h"
#include <SRanipal_API_Eye.h>
#include <Engine.h>
#include "Engine.h"
#include <Runtime/Engine/Classes/Kismet/KismetMathLibrary.h>
#include <Runtime/Engine/Classes/Kismet/KismetMathLibrary.inl>


using namespace std;


AEyeTracker::AEyeTracker()
{
	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

}

// Called when the game starts or when spawned
void AEyeTracker::BeginPlay()
{
	//Create csv file Header at the beginning of the run
	Super::BeginPlay();
	csv_file += "date, time, dimension, state, substate, controllerleftclick, controllerrightclick, coloredcube, stimulus, 2d_x, 2d_y,";
	csv_file += "playerlocationX,playerlocationY,playerlocationZ,";
	csv_file += "playerrotationRoll,playerrotationPitch,playerrotationYaw,";
	csv_file += "raydistance,raylocationX,raylocationY,raylocationZ,";
	csv_file += "rayimpactpointX,rayimpactpointY,rayimpactpointZ,";
	csv_file += "rayhitcomponent,rayscreenlocationX,rayscreenlocationX,";
	csv_file += "combined.convergence_distance_mm,combined.convergence_distance_validity,";
	csv_file += "combined.eye_data.eye_openness,";
	csv_file += "combined.gaze_direction_normalized.X,combined.gaze_direction_normalized.Y,combined.gaze_direction_normalized.Z,";
	csv_file += "combined.gaze_origin_mm.X,combined.gaze_origin_mm.Y,combined.gaze_origin_mm.Z,";
	csv_file += "combined.pupil_diameter_mm,combined.pupil_position_in_sensor_area.X,combined.pupil_position_in_sensor_area.Y,";
	csv_file += "left.eye_openness,";
	csv_file += "left.gaze_direction_normalized.X,left.gaze_direction_normalized.Y,left.gaze_direction_normalized.Z,";
	csv_file += "left.gaze_origin_mm.X, left.gaze_origin_mm.Y, left.gaze_origin_mm.Z,";
	csv_file += "left.pupil_diameter_mm,left.pupil_position_in_sensor_area.X,left.pupil_position_in_sensor_area.Y,";
	csv_file += "right.eye_openness,";
	csv_file += "right.gaze_direction_normalized.X,right.gaze_direction_normalized.Y,right.gaze_direction_normalized.Z,";
	csv_file += "right.gaze_origin_mm.X,right.gaze_origin_mm.Y,right.gaze_origin_mm.Z,";
	csv_file += "right.pupil_diameter_mm,right.pupil_position_in_sensor_area.X,right.pupil_position_in_sensor_area.Y,";
	csv_file += "left.eye_wide,right.eye_wide \n";

}

// Called every frame
void AEyeTracker::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	//Access eye and gaze information via SDK SRanipal
	ViveSR::anipal::Eye::EyeData_v2 data;
	ViveSR::anipal::Eye::GetEyeData_v2(&data);

	/*
	##### Access gaze direction from SRanipal VIVE Eye and Facial Tracking SDK #####
	*/

	//The normalized, combined gaze direction of the cyclopean eye (calculated by the integrated Software)
	float gazeX = data.verbose_data.combined.eye_data.gaze_direction_normalized.X;
	float gazeY = data.verbose_data.combined.eye_data.gaze_direction_normalized.Y;
	float gazeZ = data.verbose_data.combined.eye_data.gaze_direction_normalized.Z;

	//Set UE Vector to local gaze directions to further process in the UE Blueprint
	Gaze = FVector(gazeX, gazeY, gazeZ);
	/*
	##### Access other variables from SRanipal VIVE Eye and Facial Tracking SDK #####
	Here we can collect all other vriables provided by the SDK and also store them in our final dataframe
	*/
	//PlayerLocation and Rotation
	float playerlocationX = PlayerLocation.X;
	float playerlocationY = PlayerLocation.Y;
	float playerlocationZ = PlayerLocation.Z;

	float playerrotationRoll = PlayerRotation.Roll;
	float playerrotationPitch = PlayerRotation.Pitch;
	float playerrotationYaw = PlayerRotation.Yaw;

	//Rayast Variables
	float raylocationX = RayLocation.X;
	float raylocationY = RayLocation.Y;
	float raylocationZ = RayLocation.Z;

	float rayimpactpointX = RayImpactPoint.X;
	float rayimpactpointY = RayImpactPoint.Y;
	float rayimpactpointZ = RayImpactPoint.Z;

	float rayscreenlocationX = RayScreenLocation.X;
	float rayscreenlocationY = RayScreenLocation.Y;

	//##### Creating one line of data for one tick or time frame and append it to the existing file
	//Time
	FDateTime Now = FDateTime::Now();
	csv_file += std::to_string(Now.GetYear()) + '.' + std::to_string(Now.GetMonth()) + '.' + std::to_string(Now.GetDay()) + ",";
	csv_file += std::to_string(Now.GetHour()) + '.' + std::to_string(Now.GetMinute()) + '.' + std::to_string(Now.GetSecond()) + "." + std::to_string(Now.GetMillisecond()) + ",";

	//EnvInformation
	std::string dimension(TCHAR_TO_UTF8(*Dimension));
	csv_file += dimension + ",";
	std::string state(TCHAR_TO_UTF8(*State));
	csv_file += state + ",";
	std::string substate(TCHAR_TO_UTF8(*SubState));
	csv_file += substate + ",";
	std::string controllerleftclick(TCHAR_TO_UTF8(*ControllerLeftClick));
	csv_file += controllerleftclick + ",";
	std::string controllerrightclick(TCHAR_TO_UTF8(*ControllerRightClick));
	csv_file += controllerrightclick + ",";

	std::string coloredcube(TCHAR_TO_UTF8(*ColoredCube));
	csv_file += coloredcube + ",";

	std::string stimulus(TCHAR_TO_UTF8(*Stimulus));
	csv_file += stimulus + ",";


	std::string d2_x(TCHAR_TO_UTF8(*D2_X));
	csv_file += d2_x + ",";
	std::string d2_y(TCHAR_TO_UTF8(*D2_Y));
	csv_file += d2_y + ",";

	//Player Location and Rotation
	csv_file += std::to_string(playerlocationX) + ",";
	csv_file += std::to_string(playerlocationY) + ",";
	csv_file += std::to_string(playerlocationZ) + ",";
	csv_file += std::to_string(playerrotationRoll) + ",";
	csv_file += std::to_string(playerrotationPitch) + ",";
	csv_file += std::to_string(playerrotationYaw) + ",";

	//Raycast Variables
	std::string raydistance(TCHAR_TO_UTF8(*RayDistance));
	csv_file += raydistance + ",";

	csv_file += std::to_string(raylocationX) + ",";
	csv_file += std::to_string(raylocationY) + ",";
	csv_file += std::to_string(raylocationZ) + ",";

	csv_file += std::to_string(rayimpactpointX) + ",";
	csv_file += std::to_string(rayimpactpointY) + ",";
	csv_file += std::to_string(rayimpactpointZ) + ",";

	std::string rayhitcomponent(TCHAR_TO_UTF8(*RayHitComponent));
	csv_file += rayhitcomponent + ",";

	csv_file += std::to_string(rayscreenlocationX) + ",";
	csv_file += std::to_string(rayscreenlocationX) + ",";

	//Gaze Data from Eye-Tracker
	//Combined Cyclopean Eye
	csv_file += std::to_string(data.verbose_data.combined.convergence_distance_mm) + ",";
	csv_file += std::to_string(data.verbose_data.combined.convergence_distance_validity) + ",";

	csv_file += std::to_string(data.verbose_data.combined.eye_data.eye_openness) + ",";

	csv_file += std::to_string(gazeX) + ","; //combined gaze direction normalized
	csv_file += std::to_string(gazeY) + ",";
	csv_file += std::to_string(gazeZ) + ",";

	csv_file += std::to_string(data.verbose_data.combined.eye_data.gaze_origin_mm.X) + ",";
	csv_file += std::to_string(data.verbose_data.combined.eye_data.gaze_origin_mm.Y) + ",";
	csv_file += std::to_string(data.verbose_data.combined.eye_data.gaze_origin_mm.Z) + ",";

	csv_file += std::to_string(data.verbose_data.combined.eye_data.pupil_diameter_mm) + ",";

	csv_file += std::to_string(data.verbose_data.combined.eye_data.pupil_position_in_sensor_area.X) + ",";
	csv_file += std::to_string(data.verbose_data.combined.eye_data.pupil_position_in_sensor_area.Y) + ",";

	//Left Eye
	csv_file += std::to_string(data.verbose_data.left.eye_openness) + ",";

	csv_file += std::to_string(data.verbose_data.left.gaze_direction_normalized.X) + ",";
	csv_file += std::to_string(data.verbose_data.left.gaze_direction_normalized.Y) + ",";
	csv_file += std::to_string(data.verbose_data.left.gaze_direction_normalized.Z) + ",";

	csv_file += std::to_string(data.verbose_data.left.gaze_origin_mm.X) + ",";
	csv_file += std::to_string(data.verbose_data.left.gaze_origin_mm.Y) + ",";
	csv_file += std::to_string(data.verbose_data.left.gaze_origin_mm.Z) + ",";

	csv_file += std::to_string(data.verbose_data.left.pupil_diameter_mm) + ",";

	csv_file += std::to_string(data.verbose_data.left.pupil_position_in_sensor_area.X) + ",";
	csv_file += std::to_string(data.verbose_data.left.pupil_position_in_sensor_area.Y) + ",";

	//Right Eye
	csv_file += std::to_string(data.verbose_data.right.eye_openness) + ",";

	csv_file += std::to_string(data.verbose_data.right.gaze_direction_normalized.X) + ",";
	csv_file += std::to_string(data.verbose_data.right.gaze_direction_normalized.Y) + ",";
	csv_file += std::to_string(data.verbose_data.right.gaze_direction_normalized.Z) + ",";

	csv_file += std::to_string(data.verbose_data.right.gaze_origin_mm.X) + ",";
	csv_file += std::to_string(data.verbose_data.right.gaze_origin_mm.Y) + ",";
	csv_file += std::to_string(data.verbose_data.right.gaze_origin_mm.Z) + ",";

	csv_file += std::to_string(data.verbose_data.right.pupil_diameter_mm) + ",";

	csv_file += std::to_string(data.verbose_data.right.pupil_position_in_sensor_area.X) + ",";
	csv_file += std::to_string(data.verbose_data.right.pupil_position_in_sensor_area.Y) + ",";

	//EyeData
	csv_file += std::to_string(data.expression_data.left.eye_wide) + ",";
	csv_file += std::to_string(data.expression_data.right.eye_wide) + ",";

	csv_file += "\n";

	//Set filename and saving path
	filename = TCHAR_TO_ANSI(*Filename);
	save_path = TCHAR_TO_ANSI(*Save_Path);

	//Save CSV file in every tick (this avoids loosing the dataframe in case of a crash of the session)
	std::ofstream file(save_path + filename + ".csv");
	file << csv_file;

	//Display Functions
	//DrawDebugLine(GetWorld(), PlayerLocation, GazedHitLocation, FColor::Orange, false, 2.0f);
	//FString test = FString::SanitizeFloat(R);
	

}

