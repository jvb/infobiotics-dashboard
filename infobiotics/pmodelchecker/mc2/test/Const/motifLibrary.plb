libraryOfModules transcriptionalMotifs

	NAR({X},{c_1,c_2,c_3},{l}) =
	{
		UnReg({X},{c_1},{l}) from basicLibrary.plb
		NegReg({X,X},{c_2,c_3},{l}) from basicLibrary.plb
	}

	CoopNAR({X},{c_1,c_2,c_3,c_4,c_5,c_6,c_7},{l}) =
	{
		UnReg({X},{c_1},{l}) from basicLibrary.plb
		CoopNegReg({X,X},{c_2,c_3,c_4,c_5,c_6,c_7},{l}) from basicLibrary.plb 
	}

	PAR({X},{c_1,c_2,c_3,c_4},{l}) =
	{
		UnReg({X},{c_1},{l}) from basicLibrary.plb
		PosReg({X,Y},{c_2,c_3,c_4},{l}) from basicLibrary.plb
	}


endLibraryOfModules
