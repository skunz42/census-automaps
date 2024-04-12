package scraper

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func GetPopGroupCode(popGroup string, lookupPath string) string {
	// Return the population group code for a given group name

	// Get json contents
	jsonContents, err := os.ReadFile(lookupPath)
	if err != nil {
		panic(err)
	}

	// Unmarshall data into generic map
	var groupMapping map[string]interface{}
	if err := json.Unmarshal(jsonContents, &groupMapping); err != nil {
		panic(err)
	}

	// get code and assert as string
	groupCode := groupMapping[popGroup].(string)

	return groupCode
}

func FetchCensusJson(groupCode string, key string) [][]string {
	// Returns the json results from a Census API REST request

	// Create url
	url := fmt.Sprintf("https://api.census.gov/data/2020/dec/ddhca?get=NAME,POPGROUP_LABEL,T01001_001N&POPGROUP=%s&for=county:*&key=%s", groupCode, key)
	fmt.Println(url)

	// Make GET request
	resp, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// Check for bad status
	if resp.StatusCode != 200 {
		panic("Response status code: " + fmt.Sprint(resp.StatusCode))
	}

	// Get response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}

	// Unmarshal results to variable
	var jsonResponse [][]string
	if err := json.Unmarshal(body, &jsonResponse); err != nil {
		panic(err)
	}

	fmt.Println(len(jsonResponse))

	return jsonResponse
}
