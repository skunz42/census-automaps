// https://api.census.gov/data/2020/dec/ddhca?get=NAME,POPGROUP_LABEL,T01001_001N&POPGROUP=1114&for=county:*

package main

import (
	"fmt"

	"tigertrap.net/census-automaps/scraper"
)

func main() {
	message := scraper.Hello("World")
	fmt.Println(message)
}
