// Fill out your copyright notice in the Description page of Project Settings.


#include "FindFoldersAndFiles.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "HAL/PlatformFilemanager.h"

TArray<FString> UFindFoldersAndFiles::GetAllFoldersInDirectory(const FString& Directory)
{
    TArray<FString> Folders;
    IFileManager& FileManager = IFileManager::Get();

    // Get the project content directory
    FString ContentDir = FPaths::ProjectContentDir();

    FString RelativeDirectory = FPaths::Combine(ContentDir, Directory);

    FileManager.FindFiles(Folders, *RelativeDirectory, false, true);

    return Folders;
}

TArray<FString> UFindFoldersAndFiles::GetAllFilesInDirectory(const FString& Directory)
{
    TArray<FString> Files;
    IFileManager& FileManager = IFileManager::Get();
    // Array to hold processed file names
    TArray<FString> ProcessedFiles;

    // Get the project content directory
    FString ContentDir = FPaths::ProjectContentDir();

    FString RelativeDirectory = FPaths::Combine(ContentDir, Directory);

    FileManager.FindFiles(Files, *RelativeDirectory, true, false);

    // Iterate through each file
    for (FString& File : Files)
    {
        // Get the base file name (file name without extension)
        FString BaseFileName = FPaths::GetBaseFilename(File);
        // Remove the .uasset extension
        File.RemoveFromEnd(TEXT(".uasset"));
        BaseFileName.Append(".");
        BaseFileName.Append(File);
        if (!File.EndsWith(TEXT(".uexp")))
        {
            ProcessedFiles.Add(BaseFileName);
        }

    }

    return ProcessedFiles;
}

