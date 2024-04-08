// https://api.census.gov/data/2020/dec/ddhca?get=NAME,POPGROUP_LABEL,T01001_001N&POPGROUP=1114&for=county:*

package main

import (
	"flag"
	"fmt"

	"tigertrap.net/census-automaps/scraper"
)

func main() {
	ethnicityArg := flag.String("ethnicity", "", "Ethnicity we are searching for")
	lookupPathArg := flag.String("lookuppath", "", "Path where mappings are stored")

	flag.Parse()
	ethnicity := *ethnicityArg
	ethnicityFull := ethnicity + " alone or in any combination"
	lookupPath := *lookupPathArg

	fmt.Println("Getting population group code for ethnicity", ethnicity)
	groupCode := scraper.GetPopGroupCode(ethnicityFull, lookupPath)
	fmt.Println("Population group code:", groupCode)
}
