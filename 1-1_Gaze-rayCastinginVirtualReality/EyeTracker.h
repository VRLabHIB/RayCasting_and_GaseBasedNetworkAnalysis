// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <Engine.h>
#include "Engine.h"
#include <Runtime/Engine/Classes/Kismet/KismetMathLibrary.h>
#include <Runtime/Engine/Classes/Kismet/KismetMathLibrary.inl>
#include "Misc/DateTime.h"
#include "EyeTracker.generated.h"

//Important to make the script running!
//open your build file (e.g. TestEnv.Build.cs) 
//Add packages into PublicDependencyModuleNames.AddRange(new string[]{ "Core", "CoreUObject", "Engine", "InputCore","SRanipal","SRanipalEye" });
//The folowwing packages are needed: "SRanipal", "SRanipalEye"

using namespace std;

UCLASS()
class CLASSROOM_API AEyeTracker : public AActor
{
	GENERATED_BODY()

public:
	// Sets default values for this actor's properties
	AEyeTracker();

	/* 
	#### Getter Variable of Gaze Dircetion for Gaze Raycasting #####
	We use the UE class FVector as object type to be able to access
	the Gaze Vector in the UE Blueprint.
	*/
	
	//Gaze Direction
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Gaze;
	
	/*
	#### Getter Variable of Gaze Dircetion for Gaze Raycasting #####
	We use the UE class FVector as object type to be able to access
	the Gaze Vector in the UE Blueprint.
	*/

	// Settings Variables
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Filename;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Save_Path;




	//BP Variables
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Dimension;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString State;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SubState;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ControllerLeftClick;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ControllerRightClick;

	//Specific for EyeStan (for Station 2 and 3)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ColoredCube;

	//Specific for MR BR
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Stimulus;


	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString D2_X;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString D2_Y;


	//HMD Location and Rotation
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector PlayerLocation;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FRotator PlayerRotation;

	//Raycasting Variables
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString RayDistance;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector RayLocation;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector RayImpactPoint;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		AActor* RayHitActor;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString RayHitComponent;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D RayScreenLocation;


	//Define filename and save path
	std::string filename;
	std::string save_path; 

	//Create CSV file as an empty string
	std::string csv_file = "";


protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:
	// Called every frame
	virtual void Tick(float DeltaTime) override;

};
