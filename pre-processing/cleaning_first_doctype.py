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
			print(f"- download {ark}")
			file = Scrapper.get_document(ark)
			print("- Extraction {ark}")
			df = cleaner.extract(file)
			print(f"{df.shape[0]} rows detected")
			print(f"- Post processing {ark}")
			df = cleaner.postProcess(df)
			print("- Spell checking")
			df = cleaner.spell_check(df)
			print("- saving ")
			cleaner.save(df, ark)
			print(" finnished " + ark)
			print("\n")
			del file
			del df
