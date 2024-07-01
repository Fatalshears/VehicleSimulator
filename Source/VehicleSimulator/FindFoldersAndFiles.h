// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "FindFoldersAndFiles.generated.h"

/**
 * 
 */
UCLASS()
class VEHICLESIMULATOR_API UFindFoldersAndFiles : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "File")
    static TArray<FString> GetAllFoldersInDirectory(const FString& Directory);

    UFUNCTION(BlueprintCallable, Category = "File")
    static TArray<FString> GetAllFilesInDirectory(const FString& Directory);
	
};
