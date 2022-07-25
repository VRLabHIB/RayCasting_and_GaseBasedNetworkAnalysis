## I.	Enable eye-tracking in the Unreal Engine using the SRanipal SDK 
**Installation and Integration of SRanipal Eye Tracker**

- Setup Steam VR

- Install Steam https://store.steampowered.com/?l=english
- Inside the Steam Client install SteamVR

- Setup SRanipal
- Information for Sranipal Eye-Tracking is given by VIVE
	- https://developer.vive.com/resources/vive-sense/sdk/vive-eye-and-facial-tracking-sdk/

- Download and Install VIVE_SRanipalInstaller_1.3.2.0.msi (version might be different)


**Get started with the Unreal Engine**

- Install the Epic Game Launcher and register
- Go to library and Install Unreal Engine (maybe some troubles occur here, if so see: https://answers.unrealengine.com/questions/1035057/view.html)
- We used the Unreal Engine 4, Version 4.23.1 (individual costumisations are maybe necessary with another version) #Try Other Versions
- Start Unreal Engine and setup a new Project

- Install the SDK for Eye-Tracking
- Download SDK-v1.3.3.0.zip from https://hub.vive.com/en-US/download (version might be different)
- unpack SDK in prefered folder
- under C:\...\SDK\03_Unreal\Document\Eye\ you find a documentation to setup Eye-Tracking in Unreal ('Getting Started with SRanipal in Unreal Eye-v1.3.3.0.pdf')
- Quick steps: 
	- Copy Plugin Folder into your Unreal Project folder. 
	- Restart the editor and enable SRanipal ind Settings->Plugins
	- Under Project Settings -> Plugins -> SRanipal you can enable eye by default or put this Code into the BP 
	

![Pasted image 20220322131247](https://user-images.githubusercontent.com/74495398/177186048-10f7c27c-6b6f-4682-ac30-087cbccaef0d.png)


Unreal Setup needed for VR projects:
https://docs.unrealengine.com/4.27/en-US/SharingAndReleasing/XRDevelopment/VR/VRPlatforms/SteamVR/QuickStart/


![Pasted image 20220516151029 | Width 250](https://user-images.githubusercontent.com/74495398/177186180-2b1d50d0-2413-4b7b-919d-cda08516e7ee.png)

![Unreal_Settings](https://user-images.githubusercontent.com/74495398/180719976-5b61701a-b926-48d0-bc5b-c28e49dd738b.png =100x20)


Create C++ Actor calle EyeTracker. copy paste in the C++ script in EyeTracker.h and EyeTracker.cpp

To be able to get access to the SDK Sranipal Eye Data we need to add something in the Environment build data file.
This file can be found in the Project (lets assume our new VR project is called VRTest): VRtest/Source/VRtest/Vrtest.Build.cs
Open file and add  "SRanipal", "SRanipalEye" to PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "SRanipal", "SRanipalEye" }).

Save and compile the project again. 

## II.	Create an eye-tracking Actor to provide and collect the eye-data: 

- Create a C++ Actor in your project called EyeTracker. Tow C++ files will be created in the Source folder of your Unreal project. 
- Copy the code from the two given files (EyeTracker.h & EyeTracker.cpp) into the respective newly created files.
- Modify the data collection pipeline in the script as you want  
- Go back to Unreal an create an "BP_EyeTracker" Blueprint from the C++ Actors.
- In the Blueprint create the following variables and functions to enable Gaze-Raycasting

## III.	Transform local gaze directions into global gaze directions:

![grafik](https://user-images.githubusercontent.com/74495398/180719126-df7bcee5-2758-4797-924b-001699682a62.png)

