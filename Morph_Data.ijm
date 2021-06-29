requires("1.52t");

/******
Variables and User Input
*******/

//Enable this to have more info (but it will slow down the plugin)
LOG = false

//Let's assume you won't have more than 10 slices neither images
//If you do, add them here!
slices = newArray("Slice 1", "Slice 2", "Slice 3", "Slice 4", "Slice 5", "Slice 6", "Slice 7", "Slice 8", "Slice 9", "Slice 10");
images = newArray("Image 1", "Image 2", "Image 3", "Image 4", "Image 5", "Image 6", "Image 7", "Image 8", "Image 9", "Image 10");

/******
Plugin Execution
*******/

//Get the animals' folder
sourceDir = getDirectory("Where is the folder containing the animals?");
if(sourceDir == ""){
	exit("Wrong directory. Closing plugin.");
} else{ 
	//Prevents image windows from opening while the script is running (uncomment the next line if you want the plugin to be even faster)
	//setBatchMode(true);
	animals = getAnimalsNames(sourceDir);
	//where to save outline and shaped images
	saveDir = createResultsDir(sourceDir);
	//get data
	nrOfCells = getAndSaveData(sourceDir, animals, saveDir);
	//finishing
	if(nrOfCells == 0){
		exit("0 cells were analyzed! Maybe you provided the wrong dir?");
	} else {
		exit("Plugin finished! " + nrOfCells + " cells analyzed!");
	}
}

//Get the name of the animals
function getAnimalsNames(dir) {
	animals = newArray();
	list = getFileList(sourceDir);
	if(LOG){
		for(i=0; i<list.length; i++) {
			print("Animal: " + list[i]);
		}
	}
	return list;
}

//Get results dir for FracLac data
function createResultsDir(sourceDir) {
	saveDir = sourceDir+File.separator+"FracLac Results"+File.separator;
	//Create results dir
	if (!File.exists(saveDir)){ //if it does not exist yet try to create
		File.makeDirectory(saveDir);
		if (!File.exists(saveDir)){ //still does not exist - could not create
    		exit("Unable to create RESULTS directory at: " + saveDir ". Create it manually.");
    	} else{
    		File.makeDirectory(saveDir+"Area"+File.separator);
    		File.makeDirectory(saveDir+"Perimeter"+File.separator);
    	}
    }	
    return saveDir;
}

//Get Skeleton and Frac Lac Data
function getAndSaveData(sourceDir, animals, saveDir) {
	//total number of cells
	nrOfCells = 0;
	//for each ANIMAL
	for (i=0; i<animals.length; i++){
		//for each SLICE
		for (j=0; j<slices.length; j++){
			//for each IMAGE
			for (k=0; k<images.length; k++){	
				images_dir = sourceDir+animals[i]+slices[j]+File.separator+images[k]+File.separator;
				//if the specified directory EXISTS
				if (File.exists(images_dir)){
					//get cells inside folder
					images_list = getFileList(images_dir);
					for (l=0; l<images_list.length; l++){
						//if not the results folder
						if(!endsWith(images_list[l], "/")){
							//Get Skeleton Data
		      				applySkeletonPlugin(images_list[l], animals[i], slices[j], images[k], images_dir);
							//Get FracLac Data
		      				applyFracLacPlugin(images_list[l], animals[i], slices[j], images[k], images_dir, saveDir);
		      				//increment nr of cells analyzed
		      				nrOfCells = nrOfCells+1;
						}
					}
				}
			}
		}
	}
	return nrOfCells;
}

//Apply skeleton
function applySkeletonPlugin(microglia, animal, slice, image, images_dir) {
	//handle vars
	animal = substring(animal, 0, animal.length-1);
	//open Microglia image
	open(images_dir+microglia);		
	//Process > Binary > Skeletonize	
	setOption("BlackBackground", true);
	run("Skeletonize");
	//Skeleton > Analuze Skeleton (Show Detailed Info - YES)	
	run("Analyze Skeleton (2D/3D)", "prune=none show");
	//Create results dir
	resultsDir = images_dir+"results"+File.separator;
	if (!File.exists(resultsDir)){ //if it does not exist yet try to create
		File.makeDirectory(resultsDir);
		if (!File.exists(resultsDir)){ //still does not exist - could not create
    		exit("Unable to create RESULTS directory at: " + resultsDir);
    	}
    }
	//Select and obtain results data
	auxFileName = animal+"_"+replace(slice+"_"+image," ", "_")+"_"+replace(microglia, ".tif", "");
	resultsFileName = resultsDir+animal+"__"+replace(slice+"_"+image," ", "_")+"_"+replace(microglia, ".tif", "");
	selectWindow("Results");
	setResult("animal", 0, animal);
	setResult("microglia", 0, auxFileName);
	saveAs("Results", resultsFileName+"_Skeleton_Results.csv");
	//Select and obtain branch information data
	selectWindow("Branch information");
	saveAs("Results", resultsFileName+"_Branch_Information.csv");
	run("Close");
	cleanUp();
}

//Apply FracLac
function applyFracLacPlugin(microglia, animal, slice, image, images_dir, saveDir) {
	//handle vars
	animal = substring(animal, 0, animal.length-1);
	auxFileName = animal+"__"+replace(slice+"_"+image," ", "_")+"_"+replace(microglia, ".tif", "");
	areaFileName = saveDir+"Area"+File.separator+auxFileName;
	perimeterFileName = saveDir+"Perimeter"+File.separator+auxFileName;
	//open Microglia image
	open(images_dir+microglia);	
	saveAs("tiff", areaFileName+"_AREA");	
	//Process > Binary > Outline	
	run("Outline");
	saveAs("tiff", perimeterFileName+"_PERIMETER");
	//close image
	run("Close");
}

//Closes the "Results" and "Log" windows and all image windows
function cleanUp() {
	if (isOpen("Results")) {
		selectWindow("Results"); 
		run("Close");
    }
    if (isOpen("Log")) {
		selectWindow("Log");
		run("Close");
    }
    while (nImages()>0) {
		selectImage(nImages());  
		run("Close");
    }
}
