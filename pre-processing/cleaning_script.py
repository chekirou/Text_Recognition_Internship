from cleaning import Cleaner
from Scrapper import Scrapper
import pandas as pd
if __name__ == "__main__":
	cleaner = Cleaner("../cache")
	print("Enter 1800<year<1900")
	
	year = int(input())
	if year >= 1800 and year <= 1900:
		print("=======> " + str(year))
		arks = Scrapper.get_arks(year)
		for ark in arks:
			print("=======>"  + ark)
			print(" download")
			file = Scrapper.get_document(ark)
			print(" extraction ")
			df = cleaner.extract(file)
			print("post processing")
			df = cleaner.postProcess(df)
			print(" saving ")
			cleaner.save(df, ark)
			print(" finnished " + ark)
			print("\n\n\n")
			del file
			del df
